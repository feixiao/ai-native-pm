#!/usr/bin/env python3
"""
Evaluation Harness for:
1. Agent Skills Store Feasibility Research (docs/research/agent-skills-store-feasibility.md)
2. Agent Skills Store MVP PRD (docs/prd/agent-skills-store-mvp.md)

Outputs:
METRIC score=<float 0.0-100.0>
METRIC research_score=<float 0.0-40.0>
METRIC prd_score=<float 0.0-60.0>
METRIC edge_case_count=<int>
METRIC acceptance_criteria_count=<int>
METRIC mermaid_diagram_count=<int>
METRIC total_words=<int>
"""

import os
import re
import sys

RESEARCH_FILE = "docs/research/agent-skills-store-feasibility.md"
PRD_FILE = "docs/prd/agent-skills-store-mvp.md"

def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def count_matches(pattern, text, flags=re.IGNORECASE):
    return len(re.findall(pattern, text, flags=flags))

def check_contains(pattern, text, flags=re.IGNORECASE):
    return bool(re.search(pattern, text, flags=flags))

def evaluate_research(content):
    if not content.strip():
        return 0.0, {}

    score = 0.0
    details = {}

    # 1. Market Sizing & Ecosystem (Max 8.0)
    # Check TAM/SAM/SOM, Agent landscape (Claude Code, Cursor, Codex, OpenClaw, etc.)
    s1 = 0.0
    if check_contains(r"(TAM|SAM|SOM|市场规模|年复合增长率|CAGR)", content):
        s1 += 2.0
    if check_contains(r"(Claude\s*Code|Cursor|Codex|OpenClaw|Hermes|Windsurf)", content):
        s1 += 2.0
    if check_contains(r"(驱动力|增长动力|生态演进|Agent\s*Skills|SKILL\.md)", content):
        s1 += 2.0
    if check_contains(r"(平台风险|模型厂商下场|基座模型|平台锁死)", content):
        s1 += 2.0
    s1 = min(8.0, s1)
    score += s1
    details["research_market"] = s1

    # 2. Three Verticals In-depth Analysis (Max 12.0)
    s2 = 0.0
    # Dev track (4.0)
    dev_pts = 0.0
    if check_contains(r"(研发|开发|代码生成|重构|单元测试|CI/CD|DevOps|架构)", content):
        dev_pts += 1.0
    if check_contains(r"(开发者付费意愿|开源平替|代码泄露|知识产权|私有代码安全)", content):
        dev_pts += 1.5
    if check_contains(r"(CLI|IDE\s*插件|终端集成|工作流)", content):
        dev_pts += 1.5
    s2 += min(4.0, dev_pts)

    # PM track (4.0)
    pm_pts = 0.0
    if check_contains(r"(产品经理|PRD|竞品调研|用户访谈|数据分析|JTBD)", content):
        pm_pts += 1.5
    if check_contains(r"(Notion|Jira|Figma|Linear|飞书)", content):
        pm_pts += 1.0
    if check_contains(r"(企业采购|个人自费|团队协同|复购)", content):
        pm_pts += 1.5
    s2 += min(4.0, pm_pts)

    # Stock Investment track (4.0)
    stock_pts = 0.0
    if check_contains(r"(股票|投资|量化|财报分析|回测|因子|10-K|公告提取)", content):
        stock_pts += 1.0
    if check_contains(r"(合规|监管|证券法|投顾资质|非投资建议|免责声明|SEC|证监会)", content):
        stock_pts += 1.5
    if check_contains(r"(行情数据源|API\s*成本|延迟|幻觉风险|实盘风险)", content):
        stock_pts += 1.5
    s2 += min(4.0, stock_pts)

    s2 = min(12.0, s2)
    score += s2
    details["research_verticals"] = s2

    # 3. Skillry.dev Deep Tear-down (Max 8.0)
    s3 = 0.0
    if check_contains(r"skillry(\.dev)?", content):
        s3 += 2.0
    if check_contains(r"(9\.99|79|169|买断|订阅制|单品定价|4\.99)", content):
        s3 += 2.0
    if check_contains(r"(Skillry\s*(软肋|缺点|劣势|不足|局限|破局)|无执行沙盒|提示词泄露|套壳)", content):
        s3 += 2.0
    if check_contains(r"(护城河|差异化|核心壁垒|沙盒验证|数据闭环|垂直生态)", content):
        s3 += 2.0
    s3 = min(8.0, s3)
    score += s3
    details["research_skillry_benchmark"] = s3

    # 4. Business Model & Unit Economics (Max 6.0)
    s4 = 0.0
    if check_contains(r"(抽成|佣金比例|Take\s*Rate|分成比例|订阅分成)", content):
        s4 += 2.0
    if check_contains(r"(CAC|LTV|客单价|毛利率|Stripe|支付成本)", content):
        s4 += 2.0
    if check_contains(r"(冷启动|双边市场|供给端|需求端|创作者激励)", content):
        s4 += 2.0
    s4 = min(6.0, s4)
    score += s4
    details["research_business_model"] = s4

    # 5. Feasibility Verdict & Go/No-Go Decision Matrix (Max 6.0)
    s5 = 0.0
    if check_contains(r"(可行性结论|战略研判|Go\s*/\s*No-Go|结论|准入条件)", content):
        s5 += 2.0
    if check_contains(r"(决策矩阵|评估维度|评分表|红线)", content):
        s5 += 2.0
    if check_contains(r"(里程碑|验证路径|阶段演进|Phase\s*0|MVP\s*验证)", content):
        s5 += 2.0
    s5 = min(6.0, s5)
    score += s5
    details["research_verdict"] = s5

    # Overall length and depth bonus/cap
    words = len(content)
    if words < 1500:
        score *= (words / 1500.0)

    return round(score, 2), details

def evaluate_prd(content):
    if not content.strip():
        return 0.0, {}

    score = 0.0
    details = {}

    # 1. Document Metadata, Background & Metrics (Max 10.0)
    s1 = 0.0
    if check_contains(r"(文档状态|负责人|目标版本|优先级)", content):
        s1 += 2.0
    if check_contains(r"(变更记录|Changelog|版本历史)", content):
        s1 += 2.0
    if check_contains(r"(用户痛点|业务背景|JTBD|Why)", content):
        s1 += 2.0
    if check_contains(r"(成功衡量指标|Success\s*Metrics|北极星指标)", content) and check_contains(r"(护栏指标|Guardrail\s*Metrics)", content):
        s1 += 2.0
    if check_contains(r"(明确不做|Out\s*of\s*Scope|Non-Goals)", content):
        s1 += 2.0
    s1 = min(10.0, s1)
    score += s1
    details["prd_foundation"] = s1

    # 2. System Architecture & Skill Specification (Max 10.0)
    s2 = 0.0
    if check_contains(r"(SKILL\.md|规范|元数据|frontmatter|标准包格式)", content):
        s2 += 2.5
    if check_contains(r"(CLI|命令行|npx|curl|安装流程|token\s*鉴权)", content):
        s2 += 2.5
    if check_contains(r"(沙盒|Sandbox|权限隔离|网络白名单|代码执行安全)", content):
        s2 += 2.5
    if check_contains(r"(版权保护|防抄袭|DRM|代码加密|运行时鉴权)", content):
        s2 += 2.5
    s2 = min(10.0, s2)
    score += s2
    details["prd_architecture"] = s2

    # 3. User Flows & State Machines (Max 10.0)
    s3 = 0.0
    mermaid_blocks = count_matches(r"```mermaid", content)
    if mermaid_blocks >= 1:
        s3 += 2.5
    if mermaid_blocks >= 2:
        s3 += 2.5
    if check_contains(r"(sequenceDiagram|时序图)", content):
        s3 += 1.5
    if check_contains(r"(状态机|State\s*Machine|状态流转表)", content):
        s3 += 2.0
    # check state transition table rows
    if count_matches(r"\|.*(待审核|已发布|已下架|已购买|生效中|已过期|已退款).*", content) >= 3:
        s3 += 1.5
    s3 = min(10.0, s3)
    score += s3
    details["prd_flows"] = s3

    # 4. Functional Specifications & Edge Cases (Max 10.0)
    s4 = 0.0
    if check_contains(r"(功能需求|功能详述|What|核心模块)", content):
        s4 += 2.0
    if check_contains(r"(搜索与筛选|浏览目录|详情页|代码预览)", content):
        s4 += 2.0
    if check_contains(r"(创作者后台|Skill\s*上传|自动化校验|沙盒测试)", content):
        s4 += 2.0
    if check_contains(r"(合规审核|免责确认|股票风控|投资免责)", content):
        s4 += 2.0
    edge_case_patterns = count_matches(r"(异常边界|Edge\s*Case|降级处理|异常分支|超时|网络中断|并发重复)", content)
    if edge_case_patterns >= 4:
        s4 += 2.0
    elif edge_case_patterns >= 2:
        s4 += 1.0

    s4 = min(10.0, s4)
    score += s4
    details["prd_specs"] = s4

    # 5. Acceptance Criteria (Given/When/Then) (Max 8.0)
    s5 = 0.0
    given_matches = count_matches(r"(Given|前置条件)", content)
    when_matches = count_matches(r"(When|触发动作|当)", content)
    then_matches = count_matches(r"(Then|预期结果|那么)", content)
    b_count = min(given_matches, when_matches, then_matches)

    if b_count >= 6:
        s5 = 8.0
    elif b_count >= 4:
        s5 = 6.0
    elif b_count >= 2:
        s5 = 4.0
    elif b_count >= 1:
        s5 = 2.0
    score += s5
    details["prd_acceptance_criteria"] = s5

    # 6. Telemetry & Tracking Table (Max 4.0)
    s6 = 0.0
    if check_contains(r"(埋点|Tracking|事件表|Event)", content):
        s6 += 2.0
    if count_matches(r"\|.*(event_name|click|install|purchase|view|search).*", content) >= 3 or \
       count_matches(r"\|.*(事件名称|触发时机|上报属性|参数).*", content) >= 3:
        s6 += 2.0
    s6 = min(4.0, s6)
    score += s6
    details["prd_telemetry"] = s6

    # 7. Red Team Review & QA Matrix (Max 8.0)
    s7 = 0.0
    if check_contains(r"(红队|Red\s*Team|架构师|QA总监|挑刺|边界审查)", content):
        s7 += 2.0
    if check_contains(r"(法律合规风险|穿透责任|代客理财|合规声明)", content):
        s7 += 2.0
    if check_contains(r"(代码注入|供应链安全|恶意脚本|提权)", content):
        s7 += 2.0
    if check_contains(r"(盗版扩散|离线克隆|逆向破解|版权水印)", content):
        s7 += 2.0
    s7 = min(8.0, s7)
    score += s7
    details["prd_red_team"] = s7

    # Overall length check
    words = len(content)
    if words < 2500:
        score *= (words / 2500.0)

    return round(score, 2), details

def main():
    research_content = read_file(RESEARCH_FILE)
    prd_content = read_file(PRD_FILE)

    r_score, r_details = evaluate_research(research_content)
    p_score, p_details = evaluate_prd(prd_content)

    combined = research_content + "\n" + prd_content

    # Count metrics
    mermaid_count = count_matches(r"```mermaid", combined)
    edge_cases = count_matches(r"(Edge\s*Case|异常边界|极端场景|降级处理)", combined)
    bdd_matches = min(
        count_matches(r"(Given|前置条件)", combined),
        count_matches(r"(When|当|触发条件)", combined),
        count_matches(r"(Then|那么|预期结果)", combined)
    )

    # Placeholders penalty (use word boundaries to avoid matching JTBD as TBD)
    placeholders = count_matches(r"(\bTODO\b|(?<!J)\bTBD\b|待确定|待补充|\bxxx\b)", combined)
    penalty = min(20.0, placeholders * 2.0)

    total_score = max(0.0, min(100.0, r_score + p_score - penalty))

    total_words = len(re.findall(r"\w+", combined))

    # Print METRIC outputs
    print(f"METRIC score={total_score:.2f}")
    print(f"METRIC research_score={r_score:.2f}")
    print(f"METRIC prd_score={p_score:.2f}")
    print(f"METRIC edge_case_count={edge_cases}")
    print(f"METRIC acceptance_criteria_count={bdd_matches}")
    print(f"METRIC mermaid_diagram_count={mermaid_count}")
    print(f"METRIC total_words={total_words}")

    # Exit 0
    sys.exit(0)

if __name__ == "__main__":
    main()
