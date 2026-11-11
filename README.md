# 🚀 工程师转型产品经理 & 独立开发者实战武器库 (AI-Native PM)

> 专为拥有深厚工程背景的技术人打造的 **双轨产品实战指南（企业级 TPM + 独立开发者 Solo Builder） + AI 全流程武器库 + 原生可挂载 Agent Skills**。

---

## ⚡ 外部业务工程一键安装 (Install into Any Project in 3 Seconds)

怕在不同业务项目中使用时**上下文串味、缺少真实代码与架构感知**？无需克隆本仓库，在你的任意外部业务工程（Go / Python / React / Rust / C++ / Java 等）根目录下直接运行 `npx ai-native-pm`，3 秒将 100% 自包含的 PM Agent 技能注入本地！

```bash
# 🎯 交互式选择所需技能并安装到当前项目
npx ai-native-pm add

# 🚀 一键全量安装全部 8 款 PM 技能
npx ai-native-pm add --all

# 📌 按需单独安装特定技能（如仅安装 PRD 审查或 Solo Builder 闭环）
npx ai-native-pm add pm-prd-copilot pm-solo-builder

# 🌐 全局安装（对本机所有项目永久生效）
npx ai-native-pm add --all -g

# 📋 查看当前项目中已安装技能与状态
npx ai-native-pm list
```

> **✨ 零上下文污染 + 自动工程感知**：技能安装后 100% 独立运行在你的业务工程中，**彻底消除原仓库历史背景干扰**；动笔前自动扫描目标项目的包配置（`package.json`、`go.mod` 等）与既有文档，生成贴合真实业务的高水准 PRD。天然无缝兼容 **Cursor** (`.cursor/skills/`) 与 **Claude Code / Antigravity / Codex** (`.agents/skills/`)。

---
## 🧭 双轨并行体系：如何在两种角色间自如切换？

本仓库不做脱离场景的空洞理论，而是针对技术人的两种典型工作形态提供**双轨模型（Dual-Track）**：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      【AI-Native PM 双轨并行体系】                          │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 轨道 A：企业与工业级 TPM 轨          │ 轨道 B：独立开发者 (Solo Builder) 轨 │
│ (Corporate & Industrial TPM)         │ (Indie Hacker & AI-Native Solo)      │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • **定位**：智能座舱 / 硬件音视频 / 大型SaaS │ • **定位**：垂直 AI 工具 / 独立微SaaS / 副业MVP │
│ • **心智**：坚守 Why & What，不替研发写代码  │ • **心智**：冷血自我仲裁，砍掉 70% 边缘需求   │
│ • **交付**：40+页工业级 PRD、BDD、红队自检  │ • **交付**：一页 MVP 契约、Prompt-to-Spec     │
│ • **防线**：研发交接边界、车规安全门禁      │ • **防线**：14 天两周止损死线、单用户 Quota 熔断│
│ • **工具**：`pm-prd-copilot`                 │ • **工具**：`pm-solo-builder` (含 /solo 指令) │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### ⚡ 3 种角色切换方式
1. **自然语言自动嗅探**：聊“智能座舱/硬件平台/多部门协作/企业规范” ➔ 自动切入 **企业 TPM 模式**；聊“我自己想做/独立开发/副业/单人MVP” ➔ 自动切入 **独立开发者模式**。
2. **显式前缀咒语**：在提问前加上 `【角色：企业级 TPM】` 或 `【角色：独立开发者】`，一秒锁定思考框架。
3. **极速斜杠指令 (Slash Commands)**：针对独立开发者，直接敲 `/solo filter`、`/solo audit`、`/solo spike`、`/solo contract`、`/solo spec`、`/solo sprint`、`/solo redteam`。
---

## 🎯 为什么要建这个仓库？

从硬核工程师转型产品经理，最大的优势是**懂技术边界、逻辑严密、架构抽象能力强**；最大的陷阱则是**用工程实现的确定性思维去套用模糊的商业与用户问题**（解法先行、沉迷技术优雅、忽视 ROI 与商业闭环）。

本仓库不做空洞的理论堆砌，而是提供三套可直接用于日常工作的实用系统：
1. **📘 第一部分：产品经理入门手册 (`01-pm-handbook/`)** —— 帮你完成从 `How to build` 到 `Why & What to build` 的底层心智切换，掌握 PM 核心工作流、方法论框架与行业语言。
2. **🤖 第二部分：AI 赋能产品全流程技能指南 (`02-ai-skills/`)** —— 覆盖从市场调研、用户访谈、PRD 撰写与红队挑刺、15 分钟生成可交互原型，到自助 SQL/Python 数据分析的全套 SOP 与即插即用提示词模板。
3. **⚡ 第三部分：内置可挂载的 AI Agent Skills (`.agents/skills/` & `.cursor/skills/`)** —— 遵循 Antigravity / Claude Code / Cursor 标准规范封装的 8 个自动化产品经理 Agent 技能包，在当前工作区对话时可自动激活执行。

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
| **06. 产品工作的边界** | [06-product-boundaries.md](./01-pm-handbook/06-product-boundaries.md) | **产品工作的边界与权责划分**：以端侧 AI 语音伴侣与 Mock 车控为例，拆解 Why & What 禁飞区、范围防护、RACI 矩阵，以及全 AI 化出 PRD（含红队自检）与可交互原型（内置状态切换器）的边界守则 |
| **07. 独立开发产品手册** | [07-independent-product.md](./01-pm-handbook/07-independent-product.md) | **独立开发者产品实战手册**：从个人约束选题、问题验证与证据分级，到薄切片 MVP、一人周循环、小范围发布、指标分层、红队自检与 30 天起步计划 |
| **08. 独立开发 vs 大厂协商** | [08-solo-builder-vs-corporate-pm.md](./01-pm-handbook/08-solo-builder-vs-corporate-pm.md) | **独立开发者的 PM 之道**：从“内部撕扯协调”到“自我无情仲裁”，六大维度剧烈蜕变、一页 MVP 契约、单人周冲刺与 11 维自检红队军规 |

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
| **07. 独立开发 AI 工作流** | [07-solo-ai-workflow.md](./02-ai-skills/07-solo-ai-workflow.md) | Claude Code, Cursor, Codex | **独立开发者 AI-Native PM 工作流与实战 Prompt 模板库**：个人约束机会卡、Mom-Test 事实定级、一页契约切片、Prompt-to-Spec 代码转译与单周冷血决策门 |

---

### ⚡ `.agents/skills/` & `.cursor/skills/`：可直接触发的 AI Agent 技能插件

本仓库已在 `.agents/skills/`（并软链接至 `.cursor/skills/`）配置好 8 个工业级标准 Agent 技能包，天然跨平台兼容 **Cursor**、**Claude Code** 与 **Antigravity / Codex** 等支持 `SKILL.md` 规范的 Agent 环境。无需手动配置提示词，直接用自然语言即可唤醒对应 SOP：

| Skill 名称 | 解决的核心场景 | 对应常见 PM 自定义技能 | 如何一句话触发使用 |
| :--- | :--- | :--- | :--- |
| **`pm-prd-copilot`** | 5-Whys 需求校验、状态机推演与**架构/QA 红队边界挑刺** | `prd-generator` | *“帮我写一份【实时音视频弱网自动降级】的 PRD，并做红队架构与 QA 边界审查”* |
| **`pm-market-competitor`** | 竞品逆向拆解、TAM/SAM/SOM 测算、定价策略与真实差评挖掘 | `competitor-teardown` | *“联网调研【某竞品A与竞品B】的商业模式、核心工作流、定价策略和差评痛点”* |
| **`pm-user-insight`** | 《The Mom Test》非引导访谈提纲、原声痛点聚类、RICE/Kano 优先级排序 | `user-research-synthesizer` | *“设计一份针对【海外直播运维】的非引导性用户访谈提纲”* 或 *“用 RICE 模型帮我给这几个需求排优先级”* |
| **`pm-prototype-builder`** | 15 分钟生成单文件可交互 HTML 原型，内置 **PM 状态调试切换栏** | `vibe-prototyping` | *“根据刚才的 PRD，帮我生成一个带【PM 多状态调试切换栏】的单文件可交互 HTML 原型”* |
| **`pm-data-analyst`** | 指标体系设计（北极星/护栏）、A/B 实验显著性检验、留存/漏斗归因分析 | `csv-data-summarizer` | *“帮我检验这组 A/B 测试数据是否显著”* 或 *“排查为什么今天首帧接通率下跌了 15%”* |
| **`pm-report-polisher`** | 成果导向高管周报/月报、STAR+OKR 晋升述职、双视角 Release Notes 与需求拒绝话术 | `pm-report-polisher` | *“根据这几条零散的工作日志，帮我生成一份成果导向的高管周报”* 或 *“用 STAR 法则帮我提炼本年度晋升述职报告”* |
| **`pm-solo-builder`** | 独立开发者全闭环：个人约束过滤、证据评级 (Level 0~4) 与代偿行为、≤4h 技术探针 (Spike Gate)、内嵌分发抓手的一页契约、阶梯式 Micro-Spec 代码转译、单周决策门与双阶段红队排雷 | `solo-builder` | 支持快捷指令：`/solo filter [点子]`、`/solo spike [棘刺]`、`/solo contract [解法]`、`/solo spec [契约]`、`/solo sprint [周数据]`、`/solo redteam [方案]` |
| **`pm-operations`** | 产品运营与增长闭环(产品运营不分家):AARRR 漏斗诊断、获客渠道矩阵、激活 Onboarding、留存召回、变现定价实验、病毒循环 (K 因子) 与合规红队 | `growth-ops` | *"我们的 7 日留存从 28% 掉到 19% 了,帮我定位漏损层并给出本周唯一运营动作"* 或 支持快捷指令:`/ops [漏斗数据]`、`/growth [渠道]`、`/retention [Cohort 矩阵]` |
| **`pm-customer-success`** | 客户成功与支持体系:支持分层与自助拦截 (Deflection)、取消挽留流程 (Save Flow) 与反 Dark Pattern 红线、NPS/CSAT 不满者访谈、支持单位经济与支持黑洞裁决 | `customer-success` | *"我们的取消率连续三周上升,帮我设计一个体面的挽留流程并核算支持单位经济"* 或 支持快捷指令:`/cs [支持工单]`、`/save [取消流程]`、`/churn [流失数据]` |

#### 🌐 推荐联动的通用开源生态技能 (Eco-Skills)
在日常工作流中,本仓库的 9 大垂直 PM 技能可与以下通用生态技能协同组合:
- **`brainstorming`**（头脑风暴与苏格拉底追问）：在调用 `pm-prd-copilot` 动笔前，让 AI 扮演挑剔总监连续反问，强制收敛业务闭环与边界。
- **`ui-ux-pro-max`**（现代设计规范与组件库）：与 `pm-prototype-builder` 结合，确保生成的 Web 原型具备现代主流 SaaS / Mobile 审美与专业配色。
- **`pptx`**（演示文稿生成）：配合 `pm-report-polisher`，将立项方案、季度规划或述职内容直接转换为标准的演示文稿交付物。
- **`docx` / `xlsx` / `pdf`**（文档与表格处理）：自动读取客户原声工单表、导出指标计算结果，或一键生成排版规范的交付文档。

**全生命周期交接链路**：9 大技能内置阶段交接指引，构成 `市场 → 取证 → 需求 → 原型 → 指标 → 运营 → 客户成功 → 汇报 → 下一轮市场` 闭环（`pm-market-competitor` → `pm-user-insight` → `pm-prd-copilot` → `pm-prototype-builder` → `pm-data-analyst` → `pm-operations` → `pm-customer-success` → `pm-report-polisher` → 回流调研；侧向：`pm-customer-success` 的 Detractor 流失访谈回流 `pm-user-insight`）；`pm-solo-builder` 为独立轨道主引擎，经兄弟技能联动地图接入任意阶段。

#### 🔌 跨环境多 IDE 即插即用说明
为避免不同工具对配置目录的差异，项目已做多端兼容映射：
- **任意外部项目一键安装**：推荐直接在目标项目根目录执行 `npx ai-native-pm add --all`，自动完成双运行时配置。
- **Cursor**：通过根目录 `.cursor/skills/` 软链接无缝生效。
- **Claude Code / Codex / Antigravity**：通过根目录 `.agents/skills/` 原生加载生效，并严格遵循根目录下的 [AGENTS.md](./AGENTS.md) 智能体准则与禁飞区红线。
- **个人全局复用**：若需在其他本地项目中全局使用，可执行 `npx ai-native-pm add --all -g`，或直接软链接至 `~/.cursor/skills/` 或 `~/.agents/skills/`。

### 📂 `docs/`：工业级实战研究与产品需求文档 (PRD & Feasibility)

| 交付类型 | 文档路径 | 核心业务与技术架构亮点 |
| :--- | :--- | :--- |
| **商业与技术可行性调研** | [agent-skills-store-feasibility.md](./docs/research/agent-skills-store-feasibility.md) | **对标 Skillry.dev** 深度拆解面向研发 (Dev)、产品 (PM) 与股票量化 (Stock) 垂直赛道的可行性；含 TAM/SAM/SOM 空间测算、中美证券法（SEC 出版者豁免与中国证券法 120 条）、BYOK 金融数据架构、三年期财务模型（第 8 个月打平，Year 3 EBITDA $2.28M）与五大运营黄金军规。 |
| **工业级标准 MVP PRD** | [agent-skills-store-mvp.md](./docs/prd/agent-skills-store-mvp.md) | **AI Agent 垂直技能交易市场 (SkillStore) 完整需求基线**：PostgreSQL 16 DDL (8张业务表)、OpenAPI 契约 (8个接口)、Docker Seccomp/AST 安全沙盒、4 套 Mermaid 图表、5 大场景 ASCII 线框图、11 套 BDD 验收用例、STRIDE 威胁模型、`skillstore.lock` 冲突协议、敏捷 Sprint 排期与 15 款种子技能字典。 |
| **端云协同语音助手总 PRD** | [PRD_AI_AUDIO_AGENT_v1.0.md](./docs/prd/PRD_AI_AUDIO_AGENT_v1.0.md) | Pixel 10 与 Mac 双平台端云协同 AI 语音陪伴助手 PoC 业务与协同总纲；含双环架构流、本地分流/离线保底、数据边界与全链路验收指标。 |
| **客户端 MVP PRD** | [PRD_AI_AUDIO_AGENT_CLIENT_MVP_v1.0.md](./docs/prd/PRD_AI_AUDIO_AGENT_CLIENT_MVP_v1.0.md) | Pixel 10 与 Mac 客户端 MVP 需求规范；含端侧意图路由、本地独立记忆 CRUD、Mock 车控日志、打断/离线状态机与平台生命周期边界。 |
| **服务端 MVP PRD** | [PRD_AI_AUDIO_AGENT_SERVER_MVP_v1.0.md](./docs/prd/PRD_AI_AUDIO_AGENT_SERVER_MVP_v1.0.md) | 云端实时语音对话服务 MVP 需求规范；含会话鉴权、流式回复、插话取消、断线防护、临时上下文清理与服务发布门禁。 |
| **座舱 Audio Vivid 空间音频 PRD** | [PRD_SMART_COCKPIT_AUDIO_VIVID_v1.0.md](./docs/prd/PRD_SMART_COCKPIT_AUDIO_VIVID_v1.0.md) | 智能座舱 7.1.4 物理扬声器 Audio Vivid 三维声系统规范；声音对象与床子通道解析、Audio Focus 四级安全强占、弱网平滑降级状态机与红队自审。 |
| **座舱系统级 Upmix 引擎 PRD** | [PRD_SMART_COCKPIT_SYSTEM_UPMIX_v1.0.md](./docs/prd/PRD_SMART_COCKPIT_SYSTEM_UPMIX_v1.0.md) | 底层全音源三维上混引擎；AudioAttributes 白名单过滤、原生空间声自动 Bypass、声场宽度控制、抗相位梳状滤波与 AEC 回声消除回采。 |
| **座舱音效评估与质量门禁 PRD** | [PRD_SMART_COCKPIT_AUDIO_QUALITY_EVALUATION_v1.0.md](./docs/prd/PRD_SMART_COCKPIT_AUDIO_QUALITY_EVALUATION_v1.0.md) | 客观频响/失真 AP 扫频仪测量、ITU-R BS.1534 MUSHRA 金耳朵双盲评测规程、四工况动态路噪压测与 OTA 自动化阻断流水线。 |
| **座舱多屏互动飞屏系统 PRD** | [PRD_SMART_COCKPIT_MULTI_SCREEN_INTERACTION_v1.0.md](./docs/prd/PRD_SMART_COCKPIT_MULTI_SCREEN_INTERACTION_v1.0.md) | 5 屏拓扑（仪表/中控/副驾/双后排）、三指飞屏流转协议、4 音区焦点仲裁、D 档防窥与行车安全阻断门禁、BDD 用例与红队报告。 |
| **Pixel 10 桌面 AI 灵动宠伴 PRD** | [PRD_PIXEL10_DESKTOP_AI_PET_MVP_v1.0.md](./docs/prd/PRD_PIXEL10_DESKTOP_AI_PET_MVP_v1.0.md) | Pixel 10 桌面常驻 AI 宠伴与极速语音速记；兼容 Codex Pet 开源生态、<=4h 技术探针实测、内嵌自发酵传播抓手、双阶段解耦红队自检与阶梯式 Micro-Spec 冲刺排期。 |
| **Pixel 10 交互与设计规范** | [UI_SPEC_AI_AUDIO_AGENT_PIXEL10.md](./docs/design/UI_SPEC_AI_AUDIO_AGENT_PIXEL10.md) | 端云协同 AI 语音伴侣交互设计规范；涵盖 4 种主形态（悬浮灵动球/沉浸对话/微表情/锁屏卡片）、状态转换动效与微交互规范。 |

---
## 🛠️ 快速上手路线：根据你的当下角色选用

### 路线 A：如果你在公司做产品 / 面临跨团队交付 (TPM 轨)
1. **刚接到模糊需求**：先看 [01-mindset-shift.md](./01-pm-handbook/01-mindset-shift.md)，用 `pm-user-insight` 剥离伪需求。
2. **需要竞品分析**：调用 `pm-market-competitor` 产出 TAM/SAM/SOM 与定价拆解矩阵。
3. **撰写交付级 PRD**：调用 `pm-prd-copilot` 生成带状态机与 BDD 的标准 PRD，并执行**「架构与 QA 红队自审」**。
4. **评审会演示**：调用 `pm-prototype-builder` 输出带状态调试栏的单文件交互原型。
5. **数据与复盘**：调用 `pm-data-analyst` 做漏斗归因，用 `pm-report-polisher` 提炼成果周报。

### 路线 B：如果你单飞做独立产品 / 验证副业灵感 (Solo Builder 轨)
1. **约束过滤与商业红队**：输入 `/solo filter [点子]`，让 AI CFO 审查每周工时与渠道，前置排查商业死穴，生成《机会卡》。
2. **事实取证与代偿行为**：把用户吐槽或屏幕观察丢给 AI 输入 `/solo audit [原话/代偿]`，挖掘真实代偿代价，必须拿到 Level 2+ 证据。
3. **<= 4 小时技术探针门禁**：涉及端侧 AI/音频/硬件高危项目，输入 `/solo spike [技术棘刺]`，写 <= 50 行脚本验证单点断点，探针不通严禁立项！
4. **极窄契约与架构红队**：输入 `/solo contract [解法]`，砍掉 70% 边缘功能，生成内嵌自发酵分发抓手的《一页 MVP 契约》，锁死 14 天两周止损线。
5. **阶梯式驱动代码生成**：输入 `/solo spec [契约]`，生成阶梯式 Micro-Spec (Slice 1->2->3) 增量喂给 Claude Code / Cursor，杜绝大包幻觉。
6. **周末生杀决策**：输入 `/solo sprint [周数据]`，让商业裁判五选一裁决（继续 / 缩小 / 转向 / 暂停 / 停止），无证据立即冷血归档！
