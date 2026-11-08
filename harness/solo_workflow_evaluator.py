#!/usr/bin/env python3
"""
Evaluation Harness for:
AI-Native Solo Builder PM Workflow Skill (.agents/skills/pm-solo-builder/SKILL.md)
and supporting handbook guides (01-pm-handbook/07-independent-product.md & 08-solo-builder-vs-corporate-pm.md).

Outputs:
METRIC score=<float 0.0-100.0>
METRIC workflow_completeness=<float 0.0-30.0>
METRIC ai_native_score=<float 0.0-30.0>
METRIC guardrails_score=<float 0.0-20.0>
METRIC templates_score=<float 0.0-20.0>
METRIC total_words=<int>
"""

import os
import re
import sys

SKILL_FILE = ".agents/skills/pm-solo-builder/SKILL.md"
HANDBOOK_FILE = "01-pm-handbook/08-solo-builder-vs-corporate-pm.md"
WORKFLOW_FILE = "02-ai-skills/07-solo-ai-workflow.md"
BASE_HANDBOOK_FILE = "01-pm-handbook/07-independent-product.md"
AGENTS_FILE = "AGENTS.md"
def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def check_contains(pattern, text, flags=re.IGNORECASE):
    return bool(re.search(pattern, text, flags=flags))

def count_matches(pattern, text, flags=re.IGNORECASE):
    return len(re.findall(pattern, text, flags=flags))

def evaluate_solo_skill(content, handbook_content="", workflow_content="", base_content="", agents_content=""):
    combined = "\n".join([content, handbook_content, workflow_content, base_content, agents_content])
    if not content.strip():
        return 0.0, {
            "workflow_completeness": 0.0,
            "ai_native_score": 0.0,
            "red_team_rigor": 0.0,
            "guardrails_score": 0.0,
            "templates_score": 0.0,
            "total_words": 0
        }

    # 1. Workflow Completeness (Max 25.0)
    w_score = 0.0
    # Mode 1: Personal constraint filter (5.0)
    if check_contains(r"(个人约束|可用工时|时间约束|约束过滤|现实约束)", content):
        w_score += 2.5
    if check_contains(r"(机会卡|Opportunity\s*Card|可达性|交付负担)", content):
        w_score += 2.5

    # Mode 2: Evidence grading & Novel/Compensatory Behavior (5.0)
    if check_contains(r"(Mom\s*Test|妈妈测试|非引导|假阳性|客套)", content) and check_contains(r"(Level\s*[0-4]|证据分级|事实证据|证据级别)", content):
        w_score += 2.5
    if check_contains(r"(新交互|新物种|代偿行为|脆弱习惯|绿野仙踪|Concierge|Smoke\s*Test)", combined):
        w_score += 2.5

    # Mode 3: Technical Feasibility Spike Gate (5.0)
    if check_contains(r"(技术探针|可行性探针|Spike\s*Gate|Spike|技术验尸|可行性门禁)", combined):
        w_score += 2.5
    if check_contains(r"(≤\s*4\s*小时|4\s*小时内|探针阻断|探针不通.*不立|验证单点)", combined):
        w_score += 2.5

    # Mode 4: One-Page MVP contract with Distribution Hook (5.0)
    if check_contains(r"(一页\s*MVP\s*契约|One-Page\s*(MVP)?\s*Contract)", content) and check_contains(r"(薄切片|Thin\s*Slice|垂直切片|单一闭环)", content):
        w_score += 2.5
    if check_contains(r"(内嵌分发|分发抓手|传播钩子|自发酵|零成本分发|Distribution\s*Hook)", combined):
        w_score += 2.5

    # Mode 5: 1-Problem Weekly Sprint & Decision Gate (5.0)
    if check_contains(r"(单问题|周冲刺|1-Problem|Weekly\s*Sprint)", content):
        w_score += 2.5
    if check_contains(r"(决策门|继续|缩小|转向|暂停|停止|Continue|Pivot|Stop)", content):
        w_score += 2.5

    w_score = min(25.0, w_score)

    # 2. AI-Native & Agentic Rigor (Max 25.0)
    ai_score = 0.0
    # AI Partner Personas (5.0)
    if check_contains(r"(AI\s*(合伙人|教练|副驾驶|Co-Founder|Agent\s*Personas?|角色分身))", combined):
        ai_score += 2.5
    if check_contains(r"(严苛访谈|冷血\s*CFO|架构极简|反向用户|审查官)", combined):
        ai_score += 2.5

    # Prompt-to-Spec with Progressive Micro-Spec Ladder (10.0)
    if check_contains(r"(Claude\s*Code|Cursor|Codex|Coding\s*Agent|生成代码|Spec|任务规格)", combined) and check_contains(r"(零歧义|Prompt-to-Spec|代码生成规格|Task\s*Prompt)", combined):
        ai_score += 5.0
    if check_contains(r"(阶梯式|Micro-Spec|切片阶梯|分步(下发|喂给|递进)|渐进式切片|Step-by-Step)", combined):
        ai_score += 5.0

    # Turn-to-Artifact Contract & Actionability (5.0)
    if check_contains(r"(对话即决策|输出即交付|单次交付|结构化卡片|Artifact)", combined):
        ai_score += 2.5
    if check_contains(r"(拒绝套话|拒绝空谈|直接输出|无废话)", combined):
        ai_score += 2.5

    # Cost, Token & Budget Guardrails (5.0)
    if check_contains(r"(Token|API\s*费用|边际成本|个人账单|防破产|限流|Rate\s*Limit|Quota)", combined):
        ai_score += 2.5
    if check_contains(r"(支持黑洞|每小时成本|沉没预算|现金上限)", combined):
        ai_score += 2.5

    ai_score = min(25.0, ai_score)

    # 3. Red Team Rigor & Two-Phase Decoupling (Max 15.0)
    rt_score = 0.0
    # Two-Phase Decoupled Red Team (7.5)
    if check_contains(r"(双阶段(红队|排雷)|两阶段红队|前置.*红队|解耦.*红队|Two-Phase\s*Red-Team)", combined):
        rt_score += 3.5
    if check_contains(r"(需求(与|及)?商业红队|Phase\s*1.*商业|商业排雷)", combined) and check_contains(r"(架构(与|及)?支持红队|Phase\s*2.*架构|技术排雷)", combined):
        rt_score += 4.0

    # 11-Dimension Red-Team Stress Test (7.5)
    if check_contains(r"(红队|压力测试|Red-Team|自检|质询)", content):
        rt_score += 3.5
    if check_contains(r"(没人需要|架构过载|专家自嗨|沉没执念|支持拖垮|边际成本|数据雷区|虚荣指标)", combined):
        rt_score += 4.0

    rt_score = min(15.0, rt_score)

    # 4. Solo Guardrails & Anti-Patterns (Max 15.0)
    g_score = 0.0
    # Anti-Big-PRD & Anti-Horizontal-Blocks (5.0)
    if check_contains(r"(严禁.*大\s*PRD|拒绝.*大\s*PRD|不写.*大\s*PRD|不需要大\s*PRD)", combined):
        g_score += 2.5
    if check_contains(r"(严禁.*(微服务|权限系统|横向积木|半成品平台|用户中心)|先做完.*再说)", combined):
        g_score += 2.5

    # Non-Goals fencing (5.0)
    if check_contains(r"(Non-Goals|绝对不做|坚决不做|非目标|排除清单)", content):
        g_score += 2.5
    if check_contains(r"(围栏|边界|不做的清单)", combined):
        g_score += 2.5

    # Hard Stop & Drop-dead date (5.0)
    if check_contains(r"(止损|Drop-dead|死线|复查日期|停止条件)", combined):
        g_score += 2.5
    if check_contains(r"(冷血砍项目|及时止损|冷血裁决|封存项目)", combined):
        g_score += 2.5

    g_score = min(15.0, g_score)

    # 5. Standard Templates & Artifacts (Max 20.0)
    t_score = 0.0
    # Opportunity Card template (4.0)
    if check_contains(r"```markdown\s*#\s*机会卡", content):
        t_score += 4.0
    # One-Page Contract template with Distribution Hook (4.0)
    if check_contains(r"```markdown\s*#.*(MVP\s*契约|One-Page\s*Contract)", content):
        t_score += 2.0
    if check_contains(r"(内嵌自发酵|分发抓手|自传播|Built-in\s*Distribution)", content):
        t_score += 2.0
    # Sprint Card template (4.0)
    if check_contains(r"```markdown\s*#.*(周冲刺卡|Sprint\s*Card)", content):
        t_score += 4.0
    # Step-by-Step Micro-Spec template (4.0)
    if check_contains(r"```(markdown|yaml)?\s*#.*(Coding\s*Agent|Spec|任务规格|Task\s*Prompt)", combined):
        t_score += 2.0
    if check_contains(r"(切片\s*1|Slice\s*1|Micro-Spec|阶梯式任务)", combined):
        t_score += 2.0
    # Spike Gate / Novel Evidence Artifact template (4.0)
    if check_contains(r"(技术探针卡|Spike\s*Card|探针记录|绿野仙踪记录|代偿行为卡)", combined):
        t_score += 4.0

    t_score = min(20.0, t_score)

    total_score = round(w_score + ai_score + rt_score + g_score + t_score, 2)
    total_words = len(content) + len(handbook_content) + len(workflow_content) + len(base_content) + len(agents_content)

    details = {
        "workflow_completeness": round(w_score, 2),
        "ai_native_score": round(ai_score, 2),
        "red_team_rigor": round(rt_score, 2),
        "guardrails_score": round(g_score, 2),
        "templates_score": round(t_score, 2),
        "total_words": total_words
    }

    return total_score, details

def main():
    skill_content = read_file(SKILL_FILE)
    handbook_content = read_file(HANDBOOK_FILE)
    workflow_content = read_file(WORKFLOW_FILE)
    base_content = read_file(BASE_HANDBOOK_FILE)
    agents_content = read_file(AGENTS_FILE)

    if not skill_content:
        print("ERROR: Skill file not found", file=sys.stderr)
        sys.exit(1)

    score, details = evaluate_solo_skill(
        skill_content, handbook_content, workflow_content, base_content, agents_content
    )

    print(f"METRIC score={score:.2f}")
    print(f"METRIC workflow_completeness={details['workflow_completeness']:.2f}")
    print(f"METRIC ai_native_score={details['ai_native_score']:.2f}")
    print(f"METRIC red_team_rigor={details['red_team_rigor']:.2f}")
    print(f"METRIC guardrails_score={details['guardrails_score']:.2f}")
    print(f"METRIC templates_score={details['templates_score']:.2f}")
    print(f"METRIC total_words={details['total_words']}")

    sys.exit(0)

if __name__ == "__main__":
    main()
