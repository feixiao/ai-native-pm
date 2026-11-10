#!/usr/bin/env python3
"""
Dual-Track Comprehensive Evaluation Harness for:
1. Corporate / Industrial TPM Track (Feasibility Research & Enterprise PRD in harness/evaluator.py)
2. Solo Builder Track (AI-Native Solo PM Workflow & Guide in harness/solo_workflow_evaluator.py)

Outputs:
METRIC score=<float 0.0-100.0> (Harmonic/Composite score across both tracks)
METRIC corporate_tpm_score=<float 0.0-100.0>
METRIC solo_builder_score=<float 0.0-100.0>
METRIC research_score=<float 0.0-40.0>
METRIC prd_score=<float 0.0-60.0>
METRIC workflow_completeness=<float 0.0-30.0>
METRIC ai_native_score=<float 0.0-30.0>
"""

import os
import re
import sys

def validate_integrity():
    checked_files = 0
    broken_links = []
    mermaid_blocks = 0
    invalid_mermaids = []
    
    known_types = ["flowchart", "graph", "sequenceDiagram", "stateDiagram", "classDiagram", "gantt", "pie", "erDiagram", "journey", "gitGraph"]
    
    scan_dirs = ["01-pm-handbook", "02-ai-skills", ".agents", "docs"]
    for s_dir in scan_dirs:
        if not os.path.exists(s_dir):
            continue
        for root, dirs, files in os.walk(s_dir):
            for f in files:
                if f.endswith(".md"):
                    checked_files += 1
                    f_path = os.path.join(root, f)
                    with open(f_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        
                        # 1. Check relative markdown links
                        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
                        for text, target in links:
                            if target.startswith("http") or target.startswith("#") or target.startswith("mailto"):
                                continue
                            clean_target = target.split("#")[0]
                            if not clean_target:
                                continue
                            target_path = os.path.normpath(os.path.join(root, clean_target))
                            if not os.path.exists(target_path):
                                broken_links.append((f_path, target))
                        
                        # 2. Check Mermaid blocks
                        m_blocks = re.findall(r"```mermaid(.*?)```", content, re.DOTALL)
                        for b in m_blocks:
                            mermaid_blocks += 1
                            stripped = b.strip()
                            first_line = stripped.split("\n")[0].strip() if stripped else ""
                            if not any(first_line.startswith(t) for t in known_types):
                                invalid_mermaids.append((f_path, first_line))

    if broken_links:
        print(f"ERROR: Found {len(broken_links)} broken relative markdown links:", file=sys.stderr)
        for bl in broken_links[:5]:
            print(f"  {bl[0]} -> {bl[1]}", file=sys.stderr)
        sys.exit(1)

    if invalid_mermaids:
        print(f"ERROR: Found {len(invalid_mermaids)} invalid Mermaid blocks:", file=sys.stderr)
        for im in invalid_mermaids[:5]:
            print(f"  {im[0]} -> {im[1]}", file=sys.stderr)
        sys.exit(1)

    return checked_files, mermaid_blocks
from evaluator import read_file as read_file_corp, evaluate_research, evaluate_prd, RESEARCH_FILE, PRD_FILE
from solo_workflow_evaluator import (
    read_file as read_file_solo,
    evaluate_solo_skill,
    SKILL_FILE,
    HANDBOOK_FILE,
    WORKFLOW_FILE,
    BASE_HANDBOOK_FILE,
    AGENTS_FILE,
)
def main():
    # 1. Run Corporate TPM evaluation
    r_content = read_file_corp(RESEARCH_FILE)
    p_content = read_file_corp(PRD_FILE)
    
    if not p_content:
        print(f"ERROR: Corporate PRD baseline missing: {PRD_FILE}", file=sys.stderr)
        sys.exit(1)

    if r_content:
        r_score, r_details = evaluate_research(r_content)
    else:
        # Research baseline is optional; PRD is the hard gate.
        r_score, r_details = 0.0, {}
    p_score, p_details = evaluate_prd(p_content)
    corp_score = round(r_score + p_score, 2)

    # 2. Run Solo Builder evaluation
    skill_content = read_file_solo(SKILL_FILE)
    handbook_content = read_file_solo(HANDBOOK_FILE)
    workflow_content = read_file_solo(WORKFLOW_FILE)
    base_content = read_file_solo(BASE_HANDBOOK_FILE)
    agents_content = read_file_solo(AGENTS_FILE)
    
    if not skill_content or not handbook_content:
        print(f"ERROR: Solo files missing: {SKILL_FILE} or {HANDBOOK_FILE}", file=sys.stderr)
        sys.exit(1)

    solo_score, solo_details = evaluate_solo_skill(
        skill_content, handbook_content, workflow_content, base_content, agents_content
    )

    # 3. Calculate composite dual-track score (equal weight 50% / 50%)
    composite_score = round((corp_score + solo_score) / 2.0, 2)

    print(f"METRIC score={composite_score:.2f}")
    print(f"METRIC corporate_tpm_score={corp_score:.2f}")
    print(f"METRIC solo_builder_score={solo_score:.2f}")
    print(f"METRIC research_score={r_score:.2f}")
    print(f"METRIC prd_score={p_score:.2f}")
    print(f"METRIC workflow_completeness={solo_details['workflow_completeness']:.2f}")
    print(f"METRIC ai_native_score={solo_details['ai_native_score']:.2f}")
    print(f"METRIC red_team_rigor={solo_details['red_team_rigor']:.2f}")
    print(f"METRIC guardrails_score={solo_details['guardrails_score']:.2f}")
    print(f"METRIC templates_score={solo_details['templates_score']:.2f}")

    # 4. Run Link Integrity & Mermaid Validity Gate
    checked_files, mermaid_blocks = validate_integrity()
    print(f"METRIC link_integrity=100.00")
    print(f"METRIC mermaid_validity=100.00")

    sys.exit(0)
if __name__ == "__main__":
    main()
