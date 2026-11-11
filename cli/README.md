# 🚀 ai-native-pm CLI

> **One-Command AI-Native PM Skills Toolkit & Installer for Cursor, Claude Code, Antigravity, and Codex.**

Zero configuration. Install production-grade, self-contained Technical PM & Solo Builder agent skills into any codebase in 3 seconds.

```bash
# Interactive skill selection in your current project
npx ai-native-pm add

# Install all 10 PM skills in one click
npx ai-native-pm add --all

# Selectively install specific skills
npx ai-native-pm add pm-prd-copilot pm-solo-builder

# Install globally for all projects on your machine
npx ai-native-pm add --all -g

# List available skills & local installation status
npx ai-native-pm list
```

---

## ⚡ The 10 Included PM Skills

| Skill ID | Category | Core Capability | Golden Trigger |
| :--- | :--- | :--- | :--- |
| **`pm-prd-copilot`** | Requirements | 5-Whys problem space validation, Mermaid state machines, BDD test cases, and Red-Team Architecture/QA auditing. | *"帮我写一份【实时音视频弱网自动重连】的 PRD，并做红队架构与 QA 边界审查"* |
| **`pm-solo-builder`** | Solo Founder | 6-stage indie loop: personal constraint filter, Mom-Test evidence grading (Level 0-4), <=4h spike gate, One-Page contract, progressive Micro-Spec ladder, and weekly decision gates. | *"/solo contract 我想做一个极简的本地日志分析工具，帮我收敛为一页 MVP 契约"* |
| **`pm-prototype-builder`** | Prototyping | Instant single-file clickable HTML prototypes with built-in PM Review State Switcher (Happy path / Empty / Loading / Error). | *"根据刚才的 PRD，帮我生成一个带【PM 多状态调试切换栏】的单文件可交互 HTML 原型"* |
| **`pm-market-competitor`** | Strategy | Competitor teardown, TAM/SAM/SOM sizing, monetization reverse-engineering, and real user review complaint mining. | *"联网调研【某竞品A与竞品B】的商业模式、核心工作流、定价策略和差评痛点"* |
| **`pm-user-insight`** | User Research | *The Mom Test* non-leading interview guides, raw feedback JTBD extraction, and RICE / Kano quantitative feature prioritization. | *"用 RICE 模型帮我给这几个待办需求排优先级，并划定 MVP 切片线"* |
| **`pm-data-analyst`** | Data & Metrics | 3-tier metric hierarchy (North Star + Guardrails), ClickHouse/Postgres funnel & retention SQL, A/B test significance, and metric drop diagnosis. | *"帮我排查为什么今天核心注册转化率下跌了 12%，并写出 ClickHouse 漏斗分析 SQL"* |
| **`pm-report-polisher`** | Ops & Alignment | Outcome-driven weekly/monthly executive updates, STAR+OKR promotion reviews, dual-perspective release notes, and high-EQ refusal scripts. | *"根据这几条零散的工作日志，帮我生成一份成果导向的高管周报，结论前置"* |
| **`pm-operations`** | Growth & Ops | AARRR funnel diagnosis, Owned/Earned/Paid channel matrix, activation Onboarding & Aha Moment, cohort retention & lifecycle recall, monetization pricing experiments, viral loop (K-factor) & compliance red team. | *"我们的 7 日留存从 28% 掉到 19% 了，帮我定位漏损层并给出本周唯一运营动作"* |
| **`pm-customer-success`** | Customer Success | Support deflection triage (L0/L1/L2), churn-rescue Save Flow with anti-dark-pattern red lines, NPS/CSAT detractor interviews, support unit economics & the 30% support-black-hole decision gate. | *"取消率连续三周上升，帮我设计一个体面的挽留流程并核算支持单位经济"* |
| **`pm-security-compliance`** | Security & Compliance | Data classification & lifecycle contracts, GDPR/PIPL/CCPA productization, consent & deletion flows, requirement-level STRIDE threat modeling, compliance release gates & the minimal solo-compliance set. | *"我们要出海欧洲并收集位置数据，帮我写数据分级契约与 GDPR 产品约束清单"* |

---

## 🔌 Multi-Runtime Compatibility

`ai-native-pm` automatically writes skills to `.agents/skills/<name>/SKILL.md`, generates corresponding `.cursor/skills/<name>` mappings, and materializes every advertised slash command as a `.claude/commands/<cmd>.md` file:
- **Cursor**: Instant auto-activation via `.cursor/skills/`.
- **Claude Code**: Native recognition via `.agents/skills/`, plus ready-to-type slash commands in `.claude/commands/`.
- **Antigravity / Codex**: Direct compatibility with standard `SKILL.md` specifications.

---

## 🛠️ CLI Commands & Options

```bash
npx ai-native-pm add [skills...]     # Install selected skills (or all with --all)
npx ai-native-pm list                # List all skills and local installation status
npx ai-native-pm info <skill>        # Show full skill details & golden trigger card
npx ai-native-pm update [skills...]  # Update installed skills to latest upstream version

# Flags:
--all, -a                            # Apply to all skills
--global, -g                         # Target user global directory (~/.agents/skills, ~/.cursor/skills, ~/.claude/commands)
--force, -f                          # Overwrite existing files without prompt
--dir, -d <path>                     # Target directory (default: process.cwd())
```

License: MIT
