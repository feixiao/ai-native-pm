# 🚀 工程师转型产品经理：实战入门手册 & AI 提效技能库

> 专为拥有深厚工程背景（系统编程、音视频多媒体、高并发分布式架构）的技术人打造的 **产品经理（PM）转型认知框架 + AI 全流程实战武器库 + 可直接调用的 Agent Skills**。

---

## 🎯 为什么要建这个仓库？

从硬核工程师转型产品经理，最大的优势是**懂技术边界、逻辑严密、架构抽象能力强**；最大的陷阱则是**用工程实现的确定性思维去套用模糊的商业与用户问题**（解法先行、沉迷技术优雅、忽视 ROI 与商业闭环）。

本仓库不做空洞的理论堆砌，而是提供三套可直接用于日常工作的实用系统：
1. **📘 第一部分：产品经理入门手册 (`01-pm-handbook/`)** —— 帮你完成从 `How to build` 到 `Why & What to build` 的底层心智切换，掌握 PM 核心工作流、方法论框架与行业语言。
2. **🤖 第二部分：AI 赋能产品全流程技能指南 (`02-ai-skills/`)** —— 覆盖从市场调研、用户访谈、PRD 撰写与红队挑刺、15 分钟生成可交互原型，到自助 SQL/Python 数据分析的全套 SOP 与即插即用提示词模板。
3. **⚡ 第三部分：内置可挂载的 AI Agent Skills (`.agents/skills/`)** —— 遵循 Antigravity / Claude Code 标准规范封装的 5 个自动化产品经理 Agent 技能包，在当前工作区对话时可自动激活执行。

---

## 📂 仓库目录与阅读导航

### 📘 `01-pm-handbook/`：思维切换与基本功手册

| 章节 | 文件路径 | 核心解决的问题 |
| :--- | :--- | :--- |
| **01. 思维切换指南** | [01-mindset-shift.md](./01-pm-handbook/01-mindset-shift.md) | 深度拆解工程师转 PM 的 **6 大核心思维跃迁**（问题先行、ROI 算账、成果导向、灰度决策、小白视角、利益对齐）+ **21 天刻意练习清单** |
| **02. 核心能力模型** | [02-core-skills.md](./01-pm-handbook/02-core-skills.md) | PM 的 **T 型能力图谱**、6 大硬技能与 4 大软技能、如何把你的音视频/架构技术长板变成降维打击优势 + **精选必读书单核心精髓速查** |
| **03. 日常工作流** | [03-workflow.md](./01-pm-handbook/03-workflow.md) | PM 的一天/一周节奏、**需求全生命周期 7 步标准闭环**（含每阶段核心交付物）、跨角色协作避坑指南、如何在评审会上建立专业权威 |
| **04. 方法论框架速查** | [04-frameworks.md](./01-pm-handbook/04-frameworks.md) | 像查设计模式一样查产品框架：**JTBD、5-Whys、RICE 优先级评分、Kano 模型、北极星指标、AARRR 海盗模型、漏斗与同期群分析** |
| **05. 术语表（工程师版）** | [05-glossary.md](./01-pm-handbook/05-glossary.md) | **40+ 产品与商业核心术语**，全部使用工程师熟悉的分布式系统、网络协议与研发概念进行精准类比映射 |

---

### 🤖 `02-ai-skills/`：AI 全链路产品提效指南（含 Prompt 模板库）

| 阶段 | 文件路径 | 核心工具链 | 核心提效场景与杀手锏 |
| :--- | :--- | :--- | :--- |
| **01. 市场与竞品调研** | [01-market-research.md](./02-ai-skills/01-market-research.md) | Perplexity, Deep Research, NotebookLM, Claude | 30 分钟扫描陌生赛道全景、竞品定价逆向工程、抓取 G2/GitHub 差评挖掘未满足痛点 (Unmet Needs) |
| **02. 用户研究与需求挖掘** | [02-user-research.md](./02-ai-skills/02-user-research.md) | 飞书妙记, Otter.ai, Claude / Gemini 长上下文 | 生成符合《The Mom Test》的非引导性访谈提纲、10+ 份访谈录音跨样本痛点聚类、还原真实 JTBD |
| **03. PRD 撰写与红队评审** | [03-prd-writing.md](./02-ai-skills/03-prd-writing.md) | Claude 3.7, ChatPRD, Mermaid | **工业级标准 PRD 模板** + **独门红队挑刺法**（让 AI 扮演毒舌架构师与 QA 总监，在评审会前找出所有并发与异常边界漏洞） |
| **04. 快速原型与交互验证** | [04-prototyping.md](./02-ai-skills/04-prototyping.md) | Claude Artifacts, v0.dev, Bolt.new, Lovable | 告别静态线框图：15 分钟生成带 **「PM 多状态调试切换栏」**（正常/空状态/弱网报错）的可点击前端原型 |
| **05. 数据分析与实验决策** | [05-data-analysis.md](./02-ai-skills/05-data-analysis.md) | Claude Code, Python/SQL Copilot, Julius AI | 自然语言秒写复杂漏斗与 Cohort 留存 SQL、用决策树寻找产品 Aha Moment、A/B 测试显著性检验、指标异动归因排查 |
| **06. 团队协作与项目管理** | [06-collaboration.md](./02-ai-skills/06-collaboration.md) | Notion AI, Linear, 飞书 AI | 会议录音秒转可执行 Action Items、Epic 自动拆解为敏捷 User Stories、高情商拒绝伪需求话术、成果导向高管周报生成 |

---

### ⚡ `.agents/skills/`：可直接触发的 AI Agent 技能插件

本仓库已在 `.agents/skills/` 下配置好 5 个标准 Agent 技能包。当你在本仓库目录下使用 Antigravity CLI / IDE 时，直接用自然语言下达产品任务，Agent 会自动按专业 SOP 执行：

| Skill 名称 | 配置文件路径 | 如何一句话触发使用 |
| :--- | :--- | :--- |
| **`pm-prd-copilot`** | [.agents/skills/pm-prd-copilot/SKILL.md](./.agents/skills/pm-prd-copilot/SKILL.md) | *“帮我写一份【实时音视频弱网自动降级】的 PRD，并做红队架构与 QA 边界审查”* |
| **`pm-market-competitor`** | [.agents/skills/pm-market-competitor/SKILL.md](./.agents/skills/pm-market-competitor/SKILL.md) | *“联网调研【某竞品A与竞品B】的定价策略、核心架构边界和社区用户差评痛点”* |
| **`pm-user-insight`** | [.agents/skills/pm-user-insight/SKILL.md](./.agents/skills/pm-user-insight/SKILL.md) | *“设计一份针对【海外直播运维】的非引导性用户访谈提纲”* 或 *“用 RICE 模型帮我给这几个需求排优先级”* |
| **`pm-prototype-builder`** | [.agents/skills/pm-prototype-builder/SKILL.md](./.agents/skills/pm-prototype-builder/SKILL.md) | *“根据刚才的 PRD，帮我生成一个带【PM 多状态调试切换栏】的单文件可交互 HTML 原型”* |
| **`pm-data-analyst`** | [.agents/skills/pm-data-analyst/SKILL.md](./.agents/skills/pm-data-analyst/SKILL.md) | *“帮我检验这组 A/B 测试数据是否显著”* 或 *“排查为什么今天首帧接通率下跌了 15%”* |

---

### 📂 `docs/`：工业级实战研究与产品需求文档 (PRD & Feasibility)

| 交付类型 | 文档路径 | 核心业务与技术架构亮点 |
| :--- | :--- | :--- |
| **商业与技术可行性调研** | [agent-skills-store-feasibility.md](./docs/research/agent-skills-store-feasibility.md) | **对标 Skillry.dev** 深度拆解面向研发 (Dev)、产品 (PM) 与股票量化 (Stock) 垂直赛道的可行性；含 TAM/SAM/SOM 空间测算、中美证券法（SEC 出版者豁免与中国证券法 120 条）、BYOK 金融数据架构、三年期财务模型（第 8 个月打平，Year 3 EBITDA $2.28M）与五大运营黄金军规。 |
| **工业级标准 MVP PRD** | [agent-skills-store-mvp.md](./docs/prd/agent-skills-store-mvp.md) | **AI Agent 垂直技能交易市场 (SkillStore) 完整需求基线**：PostgreSQL 16 DDL (8张业务表)、OpenAPI 契约 (8个接口)、Docker Seccomp/AST 安全沙盒、4 套 Mermaid 图表、5 大场景 ASCII 线框图、11 套 BDD 验收用例、STRIDE 威胁模型、`skillstore.lock` 冲突协议、敏捷 Sprint 排期与 15 款种子技能字典。 |
| **端侧 AI 语音伴侣 PRD** | [android-pixel10-voice-companion-mvp.md](./docs/prd/android-pixel10-voice-companion-mvp.md) | 针对 Google Pixel 10 (Tensor G5) 端侧离线全双工 AI 语音虚拟伴侣 (Her Pocket) MVP PRD；含 Oboe C++ AAudio AEC、Sherpa-onnx、Gemma-3-4B-IT、Kokoro-82M 低延迟管道与温控长续航防崩溃策略。 |

---
## 🛠️ 快速上手路线：当你接到第一个产品任务时怎么用？

1. **刚接到业务方/老板抛来的一个模糊想法时**：
   👉 先看 [01-mindset-shift.md](./01-pm-handbook/01-mindset-shift.md) 克制“直接想代码怎么写”的冲动，调用 `pm-user-insight` 用 `5-Whys` 和 `JTBD` 搞清楚真实痛点。
2. **需要调研市面上别人是怎么做的**：
   👉 调用 `pm-market-competitor` 或参考 [01-market-research.md](./02-ai-skills/01-market-research.md)，1 小时拿出有深度的竞品拆解与差异化切口。
3. **准备动笔写 PRD 和画原型参加需求评审**：
   👉 调用 `pm-prd-copilot` 生成标准 PRD 并执行**「红队边界自检」**；随后调用 `pm-prototype-builder` 生成一个带状态切换栏的交互 HTML 原型带去评审会现场演示。
4. **功能上线后验证效果与向老板汇报**：
   👉 调用 `pm-data-analyst` 跑出漏斗、留存与 A/B 实验结论，再用 [06-collaboration.md](./02-ai-skills/06-collaboration.md) 生成结构化的成果周报与复盘报告。
