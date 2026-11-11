#!/usr/bin/env python3
"""
Skill Ecosystem Evaluation Harness (product-operations unified lifecycle).

Measures whether the agent skill ecosystem under `.agents/skills/` covers the
FULL product-operations lifecycle ("产品运营不分家") and is consistently
published across the three surfaces:

  1. Repo source of truth   : .agents/skills/<id>/SKILL.md
  2. CLI registry           : cli/src/skills-meta.mjs  (SKILLS array)
  3. CLI install bundle     : cli/skills/<id>/SKILL.md

Outputs (all deterministic, file-based, no network):
METRIC ecosystem_score=<float 0.0-100.0>   PRIMARY
METRIC lifecycle_coverage=<float 0.0-1.0>  fraction of 10 lifecycle stages covered
METRIC ops_coverage=<float 0.0-1.0>        quality of operations/growth coverage
METRIC avg_skill_quality=<float 0.0-1.0>   mean per-skill craft score
METRIC cli_sync=<float 0.0-1.0>            three-surface registry consistency
METRIC handoff_coverage=<float 0.0-1.0>    fraction of 12 documented lifecycle handoffs
METRIC trigger_disambiguation=<float 0.0-1.0> fraction of ambiguous skill pairs
                                             with explicit sibling pointers
METRIC ambiguous_pairs=<int>               count of ambiguous description pairs
METRIC docs_quality=<float 0.0-1.0>        dual-track reference-doc quality
                                             (AGENTS.md SOP 3 baseline)
METRIC handoff_documented=<int>             count of documented handoff edges
METRIC skill_count=<int>                   skills on disk
METRIC registered_count=<int>               skills in CLI meta
METRIC bundle_count=<int>                   skills in cli/skills bundle
"""

import os
import re
import sys

from evaluator import read_file as read_file_corp, evaluate_research, evaluate_prd, RESEARCH_FILE, PRD_FILE
from solo_workflow_evaluator import (
    read_file as read_file_solo, evaluate_solo_skill,
    SKILL_FILE, HANDBOOK_FILE, WORKFLOW_FILE, BASE_HANDBOOK_FILE, AGENTS_FILE,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, ".agents", "skills")
META_FILE = os.path.join(REPO_ROOT, "cli", "src", "skills-meta.mjs")
BUNDLE_DIR = os.path.join(REPO_ROOT, "cli", "skills")

# The ten lifecycle stages of the product-operations continuum.
# Each stage is matched against a skill's identity text (name + description)
# and body headings. A stage is "covered" when at least one skill matches.
LIFECYCLE_STAGES = {
    "market_research": ["市场", "竞品", "调研", "TAM", "pricing", "商业模式",
                        "market", "competitor", "research"],
    "user_research": ["用户", "访谈", "JTBD", "RICE", "Kano", "痛点",
                      "user research", "interview", "insight"],
    "requirements": ["PRD", "需求", "规格", "状态机", "BDD", "验收",
                     "prd", "requirements", "spec"],
    "security_compliance": ["安全", "合规", "STRIDE", "威胁模型", "隐私",
                          "security", "compliance", "threat model",
                          "data classification", "consent"],
    "prototype": ["原型", "交互", "mockup", "prototype", "UI", "wireframe"],
    "data_experiment": ["指标", "SQL", "A/B", "漏斗", "留存", "归因",
                        "metric", "funnel", "retention", "experiment"],
    "operations_growth": ["运营", "增长", "拉新", "激活", "促活", "召回",
                          "裂变", "分发", "传播", "AARRR", "ASO", "SEO",
                          "growth", "distribution", "monetization", "campaign",
                          "community", "用户运营"],
    "communication": ["汇报", "周报", "述职", "沟通", "话术", "Release Notes",
                     "report", "communication", "stakeholder"],
    "customer_success": ["客户成功", "客服", "流失挽留", "churn", "NPS",
                        "CSAT", "customer success", "deflection", "save flow"],
    "solo_indie": ["独立开发", "indie", "solo", "微SaaS", "MVP", "一人公司",
                   "独立开发者"],
}

# Keyword sets used to detect a skill whose PRIMARY focus is operations/growth
# (as opposed to merely mentioning one word in passing).
OPS_KEYWORDS = re.compile(
    r"运营|增长|拉新|激活|促活|召回|裂变|分发|传播|AARRR|ASO|SEO|内容营销|"
    r"渠道|私域|增长黑客|growth|hacking|distribution|monetiz|campaign|"
    r"community|user ops|retention ops|lifecycle ops",
    re.IGNORECASE,
)

# Trigger-vocabulary concepts used to detect ROUTING AMBIGUITY between skills.
# The agent router sees only frontmatter descriptions before loading a skill.
# A pair of skills is "ambiguous" when both descriptions advertise the same
# trigger concept (e.g. both claim 留存/funnel); the router cannot tell them
# apart. A pair is "resolved" when BOTH sides carry an explicit pointer to
# the sibling (its id in the description or opening body) scoping the
# boundary. Frozen vocabulary: any keyword of a concept matching both
# descriptions makes the pair ambiguous.
TRIGGER_CONCEPTS = {
    "interview": ["interview", "访谈"],
    "retention": ["retention", "留存"],
    "funnel": ["funnel", "漏斗"],
    "growth": ["growth", "增长"],
    "churn": ["churn", "流失", "取消"],
    "support": ["support", "支持", "工单"],
    "report": ["report", "汇报", "周报", "述职"],
    "research": ["research", "调研", "竞品", "市场"],
    "prototype": ["prototype", "原型"],
    "prd": ["prd", "需求"],
    "metric": ["metric", "指标"],
    "data": ["data", "sql", "数据"],
    "experiment": ["ab test", "实验", "显著"],
    "security": ["security", "隐私", "gdpr", "合规"],
    "pricing": ["pricing", "定价", "变现"],
    "onboarding": ["onboarding", "激活"],
    "viral": ["viral", "病毒", "k 因子", "k-factor"],
    "comms": ["沟通", "干系人", "stakeholder", "高管"],
    "evidence": ["证据"],
    "mvp": ["mvp", "一页", "契约"],
}

# Directed lifecycle handoff chain. An edge is "documented" when the
# SOURCE skill's SKILL.md references the TARGET skill by its id, i.e. a
# user finishing stage A knows which skill to invoke for stage B.
# Without these pointers the skills are isolated silos.
HANDOFF_EDGES = [
    ("pm-market-competitor", "pm-user-insight"),    # 市场机会 → 真实用户取证
    ("pm-user-insight", "pm-prd-copilot"),          # 洞察与优先级 → PRD
    ("pm-prd-copilot", "pm-prototype-builder"),     # PRD → 可点击原型
    ("pm-prd-copilot", "pm-security-compliance"),   # PRD 红队 → 安全合规加固
    ("pm-security-compliance", "pm-prototype-builder"),  # 合规约束 → 原型落地
    ("pm-prototype-builder", "pm-data-analyst"),    # 原型过审 → 埋点与指标
    ("pm-data-analyst", "pm-operations"),           # 指标基线 → 增长动作
    ("pm-operations", "pm-report-polisher"),        # 运营结果 → 高管汇报
    ("pm-report-polisher", "pm-market-competitor"), # 复盘结论 → 下一轮调研
    ("pm-operations", "pm-customer-success"),       # 留存/流失 → 个体挽留与成功
    ("pm-customer-success", "pm-user-insight"),     # 流失访谈 → 证据回流研究
]
# The solo hub is an overlay: it must point into the main chain (any stage).
MAIN_CHAIN_IDS = {
    "pm-market-competitor", "pm-user-insight", "pm-prd-copilot",
    "pm-prototype-builder", "pm-data-analyst", "pm-operations",
    "pm-report-polisher", "pm-customer-success",
    "pm-security-compliance",
}


def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_frontmatter(text):
    """Return (fields_dict, body) from a SKILL.md. Fields are loose key: value."""
    fields = {}
    body = text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if m:
        block, body = m.group(1), text[m.end():]
        key = None
        for line in block.splitlines():
            km = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
            if km:
                key = km.group(1)
                fields[key] = km.group(2).strip()
            elif key and (line.startswith((" ", "\t")) or line.lstrip().startswith("-")):
                # folded continuation (e.g. `description: >-`); check raw
                # leading whitespace, NOT the stripped line
                fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields, body


def skill_quality(skill_id, text):
    """Craft score 0..1 for a single SKILL.md."""
    fields, body = parse_frontmatter(text)
    score = 0.0
    if fields.get("name") == skill_id:
        score += 0.25
    elif fields.get("name"):
        score += 0.10
    desc = fields.get("description", "")
    if len(desc) >= 40:
        score += 0.20
    elif desc:
        score += 0.10
    words = len(re.findall(r"[\w\u4e00-\u9fff]+", body))
    if words >= 500:
        score += 0.20
    elif words >= 250:
        score += 0.10
    sections = len(re.findall(r"^##\s", body, re.MULTILINE))
    if sections >= 5:
        score += 0.15
    elif sections >= 2:
        score += 0.08
    if re.search(r"(When|当|trigger|触发|Use this skill)", fields.get("description", "") + body[:400],
                 re.IGNORECASE):
        score += 0.10
    guard = re.search(r"(红队|边界|红线|降级|guardrail|anti-?pattern|禁止|严禁)", body,
                      re.IGNORECASE)
    if guard:
        score += 0.10
    return min(1.0, score)


def skill_identity(skill_id, text, meta_desc):
    """Identity text = the skill's stated purpose (name + descriptions),
    NOT body prose. A stage/ops focus is claimed by what the skill
    advertises itself to do; passing mentions in the body don't count."""
    fields, _ = parse_frontmatter(text)
    return " ".join([skill_id, fields.get("name", ""), fields.get("description", ""),
                     meta_desc])


def stage_covered(stage, identities):
    kws = LIFECYCLE_STAGES[stage]
    for ident in identities:
        if any(k.lower() in ident.lower() for k in kws):
            return True
    return False


def docs_quality_score():
    """Repo reference-doc quality 0..1: the dual-track composite (AGENTS.md
    SOP 3 declares a >=90 quality baseline) — corporate feasibility research
    + enterprise PRD, averaged with the solo-track handbook/workflow scores.
    Mirrors dual_track_evaluator's composition exactly."""
    r_content = read_file_corp(RESEARCH_FILE)
    p_content = read_file_corp(PRD_FILE)
    if not p_content:
        return 0.0
    r_score, _ = evaluate_research(r_content) if r_content else (0.0, {})
    p_score, _ = evaluate_prd(p_content)
    corp = r_score + p_score
    skill_content = read_file_solo(SKILL_FILE)
    handbook_content = read_file_solo(HANDBOOK_FILE)
    if not skill_content or not handbook_content:
        return 0.0
    solo, _ = evaluate_solo_skill(
        skill_content, handbook_content,
        read_file_solo(WORKFLOW_FILE), read_file_solo(BASE_HANDBOOK_FILE),
        read_file_solo(AGENTS_FILE))
    return min(1.0, (corp + solo) / 200.0)


def trigger_disambiguation(disk_skills):
    """Routing-ambiguity check 0..1. For each unordered pair of skills whose
    frontmatter descriptions share at least one TRIGGER_CONCEPTS keyword,
    require an explicit sibling pointer in BOTH directions (sibling id in the
    description or the first 500 chars of body). Returns (fraction, n_pairs);
    (1.0, 0) when no pair is ambiguous."""
    views = {}
    for sid, text in disk_skills.items():
        fields, body = parse_frontmatter(text)
        views[sid] = (fields.get("description", "").lower(), body.lower())
    n_pairs = resolved = 0
    sids = sorted(views)
    for i, a in enumerate(sids):
        for b in sids[i + 1:]:
            shared = {k for k, ws in TRIGGER_CONCEPTS.items()
                      if any(w in views[a][0] and w in views[b][0] for w in ws)}
            if not shared:
                continue
            n_pairs += 1
            a_points = b in views[a][0] or b in views[a][1][:500]
            b_points = a in views[b][0] or a in views[b][1][:500]
            if a_points and b_points:
                resolved += 1
    if n_pairs == 0:
        return 1.0, 0
    return resolved / n_pairs, n_pairs


def main():
    # ---- discover skills on disk -------------------------------------------
    disk_skills = {}
    if os.path.isdir(SKILLS_DIR):
        for entry in sorted(os.listdir(SKILLS_DIR)):
            skill_md = os.path.join(SKILLS_DIR, entry, "SKILL.md")
            if os.path.isfile(skill_md):
                disk_skills[entry] = read_file(skill_md)

    # ---- CLI registry -------------------------------------------------------
    meta_text = read_file(META_FILE)
    registered = {m.group(1): m.group(3)
                  for m in re.finditer(
                      r"id:\s*'([\w-]+)',\s*\n\s*name:\s*'([\w-]+)',\s*\n\s*title:\s*'([^']*)',\s*\n\s*desc:\s*'([^']*)'",
                      meta_text)}
    registered_ids = set(registered)

    # ---- CLI bundle ---------------------------------------------------------
    bundle_ids = set()
    if os.path.isdir(BUNDLE_DIR):
        bundle_ids = {e for e in sorted(os.listdir(BUNDLE_DIR))
                      if os.path.isfile(os.path.join(BUNDLE_DIR, e, "SKILL.md"))}

    # ---- per-skill quality --------------------------------------------------
    qualities = {sid: skill_quality(sid, text) for sid, text in disk_skills.items()}
    avg_quality = (sum(qualities.values()) / len(qualities)) if qualities else 0.0

    # ---- lifecycle coverage -------------------------------------------------
    identities = []
    for sid, text in disk_skills.items():
        meta_desc = registered.get(sid, "")
        identities.append(skill_identity(sid, text, meta_desc))
    covered = [s for s in LIFECYCLE_STAGES if stage_covered(s, identities)]
    lifecycle_coverage = len(covered) / len(LIFECYCLE_STAGES)

    # ---- operations focus (产品运营不分家 core demand) -----------------------
    # Full credit requires a skill whose identity text is operations-centric
    # (>=3 distinct ops keyword hits), not a passing mention.
    ops_hits = 0
    for sid, text in disk_skills.items():
        meta_desc = registered.get(sid, "")
        ident = skill_identity(sid, text, meta_desc)
        hits = len(set(OPS_KEYWORDS.findall(ident)))
        ops_hits = max(ops_hits, hits)
    if ops_hits >= 3:
        ops_coverage = 1.0
    elif ops_hits == 2:
        ops_coverage = 0.6
    elif ops_hits == 1:
        ops_coverage = 0.3
    else:
        ops_coverage = 0.0

    # ---- lifecycle handoff routing -------------------------------------------
    documented = 0
    for src, tgt in HANDOFF_EDGES:
        if src in disk_skills and tgt in disk_skills[src]:
            documented += 1
    solo_text = disk_skills.get("pm-solo-builder", "")
    if solo_text and any(t in solo_text for t in MAIN_CHAIN_IDS):
        documented += 1
    total_edges = len(HANDOFF_EDGES) + 1
    handoff_coverage = documented / total_edges

    # ---- three-surface sync -------------------------------------------------
    disk_set = set(disk_skills)
    all_surfaces = disk_set | registered_ids | bundle_ids
    if all_surfaces:
        sync_ratio = sum(1 for s in all_surfaces
                         if s in disk_set and s in registered_ids and s in bundle_ids) / len(all_surfaces)
    else:
        sync_ratio = 0.0

    # ---- trigger disambiguation (routing clarity) ---------------------------
    disambiguation, n_amb_pairs = trigger_disambiguation(disk_skills)

    # ---- reference-doc quality (AGENTS.md SOP 3 dual-track baseline) --------
    docs_quality = docs_quality_score()

    # ---- composite ----------------------------------------------------------
    ecosystem_score = 100.0 * (0.22 * lifecycle_coverage
                               + 0.18 * avg_quality
                               + 0.13 * ops_coverage
                               + 0.13 * sync_ratio
                               + 0.13 * handoff_coverage
                               + 0.09 * disambiguation
                               + 0.12 * docs_quality)

    print(f"METRIC ecosystem_score={ecosystem_score:.2f}")
    print(f"METRIC lifecycle_coverage={lifecycle_coverage:.3f}")
    print(f"METRIC ops_coverage={ops_coverage:.3f}")
    print(f"METRIC avg_skill_quality={avg_quality:.3f}")
    print(f"METRIC cli_sync={sync_ratio:.3f}")
    print(f"METRIC handoff_coverage={handoff_coverage:.3f}")
    print(f"METRIC trigger_disambiguation={disambiguation:.3f}")
    print(f"METRIC docs_quality={docs_quality:.3f}")
    print(f"METRIC ambiguous_pairs={n_amb_pairs}")
    print(f"METRIC handoff_documented={documented}")
    print(f"METRIC skill_count={len(disk_set)}")
    print(f"METRIC registered_count={len(registered_ids)}")
    print(f"METRIC bundle_count={len(bundle_ids)}")

    print("stages covered: " + ", ".join(covered), file=sys.stderr)
    uncovered = [s for s in LIFECYCLE_STAGES if s not in covered]
    if uncovered:
        print("stages MISSING: " + ", ".join(uncovered), file=sys.stderr)
    missing = [f"{s}→{t}" for s, t in HANDOFF_EDGES
               if not (s in disk_skills and t in disk_skills[s])]
    if solo_text and not any(t in solo_text for t in MAIN_CHAIN_IDS):
        missing.append("pm-solo-builder→(main chain)")
    if missing:
        print("handoff edges MISSING: " + ", ".join(missing), file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
