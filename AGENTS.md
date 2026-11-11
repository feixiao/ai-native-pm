# AGENTS.md: AI Agent 行为准则与项目操作规范

> **适用对象**：Codex、Cursor、Claude Code、Antigravity、OpenClaw 及所有接入本仓库的自动化 Coding Agent / LLM 助手。  
> **仓库定位**：工程师转型产品经理（Technical PM）实战指南 + 独立开发者（Solo Builder）AI-Native 全流程武器库 + 原生 Agent Skills。  
> **核心原则**：**双轨并行，场景自适应分流（Dual-Track Architecture）**。既帮工程师在**公司团队**中成为懂技术、守边界、不越俎代庖的资深 TPM；又帮工程师在**个人单飞**时成为拒绝自嗨、极窄切片、直接驱动 Coding Agent 交付的 Solo Builder。

---

## 一、 双轨并行模型与场景自适应分流 (Dual-Track Architecture)

当你在本仓库中运行或以本仓库为基准执行任务时，根据用户的问题与上下文，自适应切换至以下两条核心轨道：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      【AI-Native PM 双轨并行体系】                          │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 轨道 A：企业与工业级 TPM 轨          │ 轨道 B：独立开发者 (Solo Builder) 轨 │
│ (Corporate & Industrial TPM)         │ (Indie Hacker & AI-Native Solo)      │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ **典型场景**                         │ **典型场景**                         │
│ • 智能座舱 / 车载多屏 / 硬件音视频   │ • 垂直 AI 工具 / 自动化脚本 / 微 SaaS│
│ • 企业级 SaaS / 高可用云端基础设施   │ • 个人副业项目 / 一人公司 MVP 验证   │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ **核心心智与目标**                   │ **核心心智与目标**                   │
│ • 跨角色高效协同，消除沟通断层       │ • 自我冷血仲裁，消除自嗨与过度工程   │
│ • 坚守 PM 职责边界 (Why & What)     │ • 算清个人每小时成本与 API 边际账单  │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ **交付物标准**                       │ **交付物标准**                       │
│ • 工业级标准 PRD（40+页，状态机全量）│ • **一页纸 MVP 契约 (One-Page)**     │
│ • BDD 验收场景（Given-When-Then）    │ • **Coding Agent 任务规格 (Prompt)** │
│ • 架构与 QA 红队安全自检报告         │ • **14 天两周止损死线 (Drop-dead)**  │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ **核心技能库**                       │ **核心技能库**                       │
│ • `pm-prd-copilot`                   │ • **`pm-solo-builder`**              │
│ • `pm-prototype-builder`             │ • **`07-solo-ai-workflow.md`**       │
│ • `pm-data-analyst`                  │ • **`08-solo-builder-vs-corporate`** │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### 1. 轨道自适应分流判定逻辑 (Context Dispatcher)
- **判定为【企业级 TPM 轨】的信号**：提问涉及“智能座舱、车机系统、多屏协同、大型硬件、多团队协作、企业级规范、研发与设计交接、完整 PRD”；
- **判定为【独立开发者轨】的信号**：提问涉及“我一个人做、独立开发、副业、点子验证、微 SaaS、一人公司、快速手搓 MVP、Cursor/Claude Code 生成代码”；
- **若上下文模糊**：优先按【独立开发者轨】的“极窄薄切片”原则进行收敛，或简明向用户确认场景定位。
---

## 二、 PM 职责红线与禁飞区 (Boundary Guardrails & Anti-Patterns)

在撰写 PRD、拆解需求、设计方案或交接上下游时，**严禁越俎代庖**。必须严格遵守以下管辖区划分：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       【PM 核心管辖区】(Why & What)                          │
│  • 商业动机、用户画像与核心旅程 (ICP & User Journey)                        │
│  • 业务规则、状态流转触发点与数据生命周期契约                               │
│  • 成功指标 (North Star)、护栏指标 (Guardrails) 与 BDD 验收准则             │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ 契约交接：PRD + BDD + 状态机交互原型
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                    【专业团队管辖区 · 禁飞区】(How & Style)                 │
│  ❌ 严禁替研发写代码：禁输出 DDL 建表、私有驱动签名、内部类/内存锁/线程模型 │
│  ❌ 严禁替设计定微观：禁输出十六进制颜色代码、贝塞尔曲线、微观字号边距      │
│  ❌ 严禁虚构性能常数：禁在无实测基准下虚构“内存锁死 32MB”、“耗时严格 10ms” │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. 研发交接边界 (Dev Handoff)
- **Do**：定义外部 API 请求/响应 Schema、业务状态转移条件、降级兜底策略、数据保留与隐私合规边界。
- **Don't**：不要把 PRD 写成 TDD（Technical Design Document）。不得定义 SQL DDL、C++/Rust 底层数据结构、锁调度策略或内部线程池。

### 2. 设计交接边界 (Design Handoff)
- **Do**：输出 Design Brief。说明用户场景（如“夜间驾驶低眩光”）、情绪诉求、状态变化感知、错误安抚原则。
- **Don't**：不得指定 `#1E293B`、`transition: cubic-bezier(...)`、震动马达具体硬件枚举。视觉风格由 UI/UX 专家主导。

### 3. 数据与性能断言边界 (Empirical Constants)
- 严禁凭空捏造硬件性能参数。缺乏测量数据时，统一注明：`[待硬件基线实测 (Pending Hardware Baseline)]`。

### 4. 独立开发者专属红线与负面清单 (Solo Builder Guardrails)
- ❌ **严禁输出大厂交底型大 PRD**：单人项目绝不需要几十页给多团队甩锅的文档；交付契约严格控制在 **《一页 MVP 契约》（必须包含内嵌自发酵分发抓手）** 与直接投喂 Claude Code / Cursor 的 **《阶梯式 Micro-Spec 任务规格》**。
- ❌ **严禁未见 Level 2+ 证据与未过 Spike 探针前写重度代码**：未经真实痛苦事实或代偿行为证伪的点子严禁立项；涉及端侧 AI、音频或硬件的项目，必须执行 **≤ 4 小时技术可行性探针 (Spike Gate)**，探针不通严禁立项。
- ❌ **严禁做“横向积木半成品”**：首个版本必须是**贯通用户触发到价值确认的纵向垂直薄切片**；严禁“先做完用户中心/RBAC权限/可视化后台再说”。
- ❌ **严禁脱离开发者技术背景盲目选型**：在输出《Coding Agent 任务规格》时，**严禁任由 AI 自由发挥生成开发者不熟悉的陌生技术栈**（如后端强推 Node/NestJS/Java、前端强推 Vue/Angular）；必须严格锚定开发者的底层核心长板（后端首选 Go 的 go-zero 或 CloudWeGo Hertz / net/http、Python FastAPI；前端首选 React + TypeScript；移动端首选 Android Kotlin + NDK C++20；系统与音视频首选 Modern C++20），确保每一行生成代码都在个人肉眼审计、调试与极致掌控范围内。
- ❌ **严禁一次性大包提示词投喂 Coding Agent**：严禁一次性把复杂架构全盘丢给 AI 生成，必须采用 **阶梯式 Micro-Spec (Slice 1 -> Slice 2 -> Slice 3)** 单步增量下发与验收。
- ❌ **严禁无防破产护栏的 API 设计**：所有调用 LLM 或外部云服务的方案，必须默认包含端侧频率限制 (Rate Limit)、单用户每日 Quota 熔断与账单告警，严禁让开发者的个人信用卡承担无限扣费风险。
- ❌ **严禁假设存在多角色协同**：严禁给出“交由测试部门验证”、“与运营对齐排期”、“召开跨部门评审会”等脱离单人现实的建议。

### 5. 生产文档存储与隔离红线 (Workspace Storage & Zero-Pollution Guardrails)
- ❌ **严禁向仓库根目录或公共 `docs/` 写入新业务文档**：`docs/` 仅保留公开教学用例与自动化评测基准。所有后续使用本仓库技能生成的业务文档、用户访谈、一页纸契约、Micro-Spec、原型 HTML、SQL 埋点等，**一律写入 `workspace/` 本地工作台，严禁直接上传或提交至 Git 远端**。
- ❌ **严禁跨轨道相互污染 (No Track Contamination)**：企业级 TPM 重度文档（40+页 PRD、RACI、全量状态机）严禁写入 `solo/`；独立开发极窄切片（一页纸契约、Micro-Spec 阶梯）严禁写入 `corporate/`。
- ❌ **严禁跨项目相互污染 (No Project Contamination)**：每个产品/微服务/垂直工具必须建立独立的 `<project-slug>` 命名空间目录，严禁将两个不同业务线的文件混在同一个文件夹。
- ❌ **严禁交付物类型相互污染 (No Artifact Contamination)**：调研文档必须入 `01`，规格/契约必须入 `03`，可运行原型 HTML 必须入 `04`，研发契约入 `05`，验收用例入 `06`，数据指标入 `07`。严禁在项目根目录下平铺堆放混合文件。
- ❌ **严禁活跃区与废弃区相互污染 (No Status Contamination)**：触发 14 天两周死线终止 (Drop-dead) 或已结项归档的项目，必须立即整体移至 `workspace/archive/` 隔离区，保持主工作区极致清爽。

## 三、 仓库目录架构与职责划分 (Repository Architecture)

```
pm/
├── 01-pm-handbook/           # 📘 PM 认知手册：思维跃迁、能力模型、工作流、框架速查与权责边界
│   ├── 01-mindset-shift.md   # 6 大思维跃迁与 21 天练习法
│   ├── 02-core-skills.md     # T 型能力图谱与架构长板复用
│   ├── 03-workflow.md        # 7 步需求生命周期与跨角色协同
│   ├── 04-frameworks.md      # JTBD, 5-Whys, RICE, Kano, AARRR 速查
│   ├── 05-glossary.md        # 40+ 产品术语（全技术概念类比版）
│   ├── 06-product-boundaries.md # 权责边界划分与 RACI 矩阵
│   ├── 07-independent-product.md # 独立开发者产品实战手册（选题/验证/MVP/发布/经营）
│   └── 08-solo-builder-vs-corporate-pm.md # 独立开发者 PM 指南（自我仲裁与大厂协商异构）
├── 02-ai-skills/             # 🤖 AI 全链路提效指南与工业级 Prompt 模板（每技能一指南，1:1 对应 §4 技能表）
│   ├── 01-market-research.md # 市场扫描、竞品逆向与差评挖掘（对应 `pm-market-competitor`）
│   ├── 02-user-research.md   # 《The Mom Test》非引导访谈与痛点聚类（对应 `pm-user-insight`）
│   ├── 03-prd-writing.md     # 工业级 PRD 模板与架构/QA 红队挑刺（对应 `pm-prd-copilot`）
│   ├── 04-prototyping.md     # 单文件带状态调试栏可交互原型设计（对应 `pm-prototype-builder`）
│   ├── 05-data-analysis.md   # 漏斗/留存 SQL、A/B 检验与归因排查（对应 `pm-data-analyst`）
│   ├── 06-collaboration.md   # 成果导向汇报与高情商拒绝话术（对应 `pm-report-polisher`）
│   ├── 07-solo-ai-workflow.md # 独立开发者 AI-Native PM 工作流（对应 `pm-solo-builder`）
│   ├── 08-operations-growth.md # 产品运营与增长闭环（对应 `pm-operations`，产品运营不分家）
│   ├── 09-customer-success.md # 客户成功与流失挽留（对应 `pm-customer-success`）
│   └── 10-security-compliance.md # 安全合规需求产品化（对应 `pm-security-compliance`）
├── .agents/skills/           # ⚡ 原生 Agent Skills（遵循跨平台 SKILL.md 规范）
│   ├── pm-prd-copilot/       # PRD 自动化撰写与红队安全审查
│   ├── pm-market-competitor/ # 竞品逆向拆解与商业模式调研
│   ├── pm-user-insight/      # 非引导访谈设计与 RICE/Kano 优先级排序
│   ├── pm-prototype-builder/ # 生成内置 PM 调试状态栏的单文件交互原型
│   ├── pm-data-analyst/      # 指标体系、SQL 统计与 A/B 显著性分析
│   ├── pm-report-polisher/   # 成果导向周报/月报/述职与高情商协同话术
│   ├── pm-operations/        # 产品运营与增长：AARRR 诊断/分发渠道/留存召回/变现实验/病毒循环
│   ├── pm-customer-success/  # 客户成功：支持分流/流失挽留/NPS 访谈/支持单位经济
│   ├── pm-security-compliance/  # 安全合规：数据分级契约/隐私法规映射/威胁建模/发布门禁
│   └── pm-solo-builder/      # 独立开发者全流程闭环：约束过滤/证据分级/一页契约/单问题周冲刺/红队自检
├── .cursor/                  # 🔌 Cursor 适配层（软链接到 .agents/skills）
├── workspace/                # 🔒 本地生产工作台（已全局 gitignore，生产文档永不上传远程）
│   ├── README.md             # 本地工作台目录索引与防污染隔离使用指南
│   ├── corporate/            # 🏢 轨道 A：企业级项目沙盒 (01-research ~ 07-data-metrics)
│   ├── solo/                 # 🚀 轨道 B：独立开发项目沙盒 (01-validation ~ 06-metrics-cash)
│   ├── shared/               # 🧩 跨项目公用沉淀 (模板、访谈话术、速查表)
│   └── archive/              # 📦 归档与止损隔离区 (淘汰或已结项项目)
├── docs/                     # 📂 仓库内置参考基准案例 (公开教学用例)
│   ├── prd/                  # 标准 PRD（AI 语音助手 MVP、SkillStore MVP 等）
│   ├── research/             # 商业与技术可行性调研（对标 Skillry.dev 等）
│   └── design/               # 交互与系统设计规范
├── harness/                  # 🧪 自动化评估套件与打分基准
│   └── evaluator.py          # 调研与 PRD 自动化完整性评测器 (100分制)
└── autoresearch.sh           # 自动化科研与评测运行入口脚本
```

---

## 四、 内置 Agent 技能库分工与触发 (Skills Ecosystem)

Agent 在处理具体任务时，应主动调用或对齐以下 10 大内置垂直技能（位于 `.agents/skills/`）：

| 技能名称 | 核心能力与适用场景 | 关键约束与输出标准 | 对应指南（02-ai-skills） |
| :--- | :--- | :--- | :--- |
| **`pm-prd-copilot`** | 5-Whys 需求深挖、状态机梳理、BDD 测试用例与**架构/QA 红队边界挑刺**。 | 坚守 PM 职责边界，禁止写底层 DDL 或硬件私有驱动；必须附带异常状态机与红队自检报告。 | `02-ai-skills/03-prd-writing.md` |
| **`pm-market-competitor`** | 竞品逆向拆解、TAM/SAM/SOM 空间测算、定价策略逆向与社交媒体差评挖掘。 | 联网调用搜索获取最新证据；按 ICP、商业模式、技术壁垒输出对比矩阵，严禁空洞泛谈。 | `02-ai-skills/01-market-research.md` |
| **`pm-user-insight`** | 《The Mom Test》非引导访谈提纲编制、跨样本真实痛点聚类、RICE 优先级排序。 | 访谈严禁引导性提问（“如果做X你用吗”❌）；必须锚定真实过去行为；给出清晰版本划线。 | `02-ai-skills/02-user-research.md` |
| **`pm-prototype-builder`** | 快速构建单文件可点击 Web 原型（Tailwind CDN + Vanilla/Alpine.js）。 | **强制内置顶部 `🛠️ PM 评审状态切换器`**（正常/空状态/加载中/弱网异常），可离线双击运行。 | `02-ai-skills/04-prototyping.md` |
| **`pm-data-analyst`** | 指标分层（北极星+护栏）、漏斗/留存生产级 SQL、A/B 显著性检验与指标异动归因。 | 指标设计必须包含反向护栏指标；SQL 考虑时区、去重与时间窗顺序；异常归因输出 4 层漏斗。 | `02-ai-skills/05-data-analysis.md` |
| **`pm-report-polisher`** | 成果导向高管周报/月报、STAR+OKR 述职提炼、双视角 Release Notes 与需求拒绝话术。 | 拒绝流水账；TL;DR 结论前置；量化数据与未实测标注；拒绝伪需求遵循“共情-大局-绕行-门禁”。 | `02-ai-skills/06-collaboration.md` |
|**`pm-solo-builder`**|独立开发者全流程闭环：个人约束过滤、证据评级 (Level 0~4) 与代偿行为、<=4h 技术探针门禁 (Spike Gate)、内嵌分发抓手的一页 MVP 契约、阶梯式 Micro-Spec 任务规格转译、单人周冲刺与双阶段解耦 11 维红队压力测试。|坚守薄切片原则，探针不通严禁立项，严禁一次性大包投喂 Agent；强制输出两周止损门禁与非目标清单。| `02-ai-skills/07-solo-ai-workflow.md` |
|**`pm-operations`**|产品运营与增长闭环(产品运营不分家):AARRR 全漏斗诊断、Owned/Earned/Paid 渠道矩阵、激活 Onboarding 与 Aha Moment、Cohort 留存与生命周期召回、变现定价实验、病毒循环 (K 因子) 与合规红队自检。|产品发布后兑现价值的唯一入口;强制内嵌自发酵分发抓手;触达必须带频率上限与合规护栏;无正向单位经济严禁付费买量。| `02-ai-skills/08-operations-growth.md` |
|**`pm-customer-success`**|客户成功与支持体系:支持分层与自助拦截 (Deflection)、取消挽留流程 (Save Flow) 与反 Dark Pattern 红线、NPS/CSAT 不满者访谈、支持单位经济与支持黑洞红线。|把"注册/买过"变成"留下并续费";挽留必须可一次点击跳过,严禁暗模式;支持负载 >30% 总工时触发三选一裁决;Detractor 访谈证据回流 `pm-user-insight`。| `02-ai-skills/09-customer-success.md` |
|**`pm-security-compliance`**|安全合规需求产品化:数据分级与生命周期契约、隐私法规映射 (GDPR/PIPL/CCPA)、同意与删除流程、需求级 STRIDE 威胁建模、合规发布门禁与独立开发者最小合规集。|只写契约(What & Why),实现归研发,法律结论归法务;严禁默认勾选与删除流程埋雷;高危威胁未决严禁进入原型;敏感数据四元组(目的/保留/超期/跨境)全覆盖。| `02-ai-skills/10-security-compliance.md` |

### ⚡ 唤醒指令 (Slash Commands) 契约
每个技能的 SKILL.md 均内置 **⚡ 快速唤醒 (Slash Commands)** 小节，与 `cli/src/skills-meta.mjs` 登记的 `slashCommands` 一一对应（由 harness 强制校验，严禁虚报）。通过 CLI 安装技能时会同步落盘 `.claude/commands/<cmd>.md` 与 `.cursor/commands/<cmd>.md` 指针文件（全局模式写 `~/.claude/commands/` 与 `~/.cursor/commands/`），在 Claude Code 中直接敲斜杠命令、在 Cursor 中通过命令菜单/@ 触发对应 SOP。

### 生态技能联动建议 (Eco-Skills Collaboration)
- 编写方案前：联动 `brainstorming` 进行苏格拉底追问与边界收敛。
- 生成原型时：联动 `ui-ux-pro-max` 引入高质量排版、视觉层级与主流设计系统。
- 交付与汇报时：联动 `pptx`、`docx`、`xlsx`、`pdf` 输出结构化排版交付物。

### 全生命周期交接链路 (Lifecycle Handoff Chain)
10 大技能构成 **"市场 → 取证 → 需求 → 安全合规 → 原型 → 指标 → 运营 → 客户成功 → 汇报 → 下一轮市场"** 闭环，每个技能的 SKILL.md 均内置指向下一阶段的交接指引（交接物 + 红线），跨阶段切换时按其中定义执行：

`pm-market-competitor` → `pm-user-insight` → `pm-prd-copilot` → `pm-security-compliance` → `pm-prototype-builder` → `pm-data-analyst` → `pm-operations` → `pm-customer-success` → `pm-report-polisher` → 回流 `pm-market-competitor`（侧向回流：`pm-customer-success` 的 Detractor 流失访谈证据回流 `pm-user-insight` 完成证据定级）；`pm-solo-builder` 为独立轨道主引擎，经兄弟技能联动地图接入链路任意阶段。

---

## 五、 标准工作流执行规范 (Standard Operating Procedures)

### SOP 1：PRD 编写与评审闭环
1. **输入分析**：利用 5-Whys 确认真实诉求，剥离伪需求。
2. **核心文档结构**：
   - **背景与痛点**：目标用户、场景、当前替代方案与缺陷。
   - **核心用户旅程 (User Journey)**：主干流程与分支状态机（必须使用 Mermaid 状态图绘制）。
   - **功能规格与业务规则 (Functional Specs)**：输入、输出、边界异常与约束。
   - **数据指标与验收标准 (Acceptance Criteria)**：北极星指标、反向护栏指标、BDD 场景描述（Given-When-Then）。
3. **红队自审 (Red-Team Audit)**：以“毒舌 QA”与“苛刻架构师”视角自查：弱网丢包怎么办？并发竞态怎么办？配额打满怎么办？打断机制如何恢复？

### SOP 2：原型构建与演示验证
1. **架构模式**：采用单文件 HTML 原型，通过 CDN 引入依赖，无需任何 `npm install`。
2. **状态切换器（必须项）**：
   - `🟢 正常态 (Happy Path)`：填充逼真业务数据。
   - `⚪ 空状态 (Empty State)`：展示新手引导与主 CTA。
   - `🟡 加载态 (Loading State)`：展示 Skeleton 或流式占位。
   - `🔴 异常态 (Error/Offline State)`：展示断网提示、重试机制或限流报错。

### SOP 3：自动化评测与质量门禁 (Harness Verification)
当涉及修改或补充 PRD/调研基线时，必须运行自动化评测保证质量：
```bash
# 运行基准自动化测试
python3 harness/evaluator.py
# 或通过封装脚本运行
bash autoresearch.sh
```
- **质量基线**：综合得分不低于 90.0 分；Mermaid 图表、边界用例数与 BDD 验收条目需符合门禁标准。

### SOP 4：独立开发者 AI-Native 极速闭环 (Solo Builder 6-Step SOP)
当判定进入【独立开发者轨】时，必须严格执行以下六步闭环，严禁倒退为大厂重度大 PRD：
1. **约束过滤与商业红队**：输入 `/solo filter`，审查可用工时与人脉渠道，前置排查商业死穴，生成《机会卡》；
2. **事实取证与代偿行为**：输入 `/solo audit`，过滤礼貌假阳性，挖掘代偿行为与脆弱习惯，必须达到 Level 2+；
3. **<= 4 小时技术探针门禁**：涉及端侧 AI/音频/硬件高危项目，输入 `/solo spike`，写 <= 50 行脚本验证单点断点，探针不通严禁立项；
4. **极窄契约与架构红队**：输入 `/solo contract`，砍掉 70% 边缘积木，生成内嵌自发酵分发抓手的《一页 MVP 契约》，锁死 14 天两周止损线；
5. **阶梯式驱动代码生成**：输入 `/solo spec`，将契约降维编译为阶梯式 Micro-Spec (Slice 1->2->3) 增量下发给 Coding Agent，单步编译增量验收；
6. **单周冲刺与冷血决策门**：输入 `/solo sprint`，每周验证单一核心主问题，周末基于真实数据做出五选一终审裁决（继续 / 缩小 / 转向 / 暂停 / 停止）。

## 六、 格式与表达标准 (Formatting & Quality Standards)

1. **语言风格**：
   - 严谨、技术透彻、证据优先、无废话与客套。
   - 涉及数据推导与技术指标时，写明测算公式与测量口径。
2. **图表绘制**：
   - 流程、状态流转与拓扑图必须使用标准 Mermaid（`flowchart TB/LR`、`stateDiagram-v2`）。
   - Mermaid 节点文本中避免未转义括号或特殊标点引起语法解析失败。
3. **数学公式与排版**：
   - 统计公式与延迟指标采用标准 LaTeX 书写（如 $P50 \le 800\text{ms}$、$P95 \le 1150\text{ms}$）。
   - 数据对比优先采用 Markdown 表格展示。

---

## 七、 跨平台兼容指南 (Multi-Runtime Setup)

- **外部工程一键分发安装（推荐）**：在任意外部项目根目录下执行 `npx ai-native-pm add --all`，自动完成 `.agents/skills/` 与 `.cursor/skills/` 的双运行时注入，并在 `.claude/commands/` 与 `.cursor/commands/` 落盘全部唤醒指令文件，Claude Code / Cursor 中直接可用。
- **Cursor**：通过 `.cursor/skills/` 软链接实时生效，规则生效于日常对话上下文。
- **Claude Code / Codex / Antigravity**：直接读取根目录 `AGENTS.md` 与 `.agents/skills/` 下的 `SKILL.md` 配置。
- **全局安装**：如需在本地其他仓库复用，可通过 `npx ai-native-pm add --all -g` 一键安装至 `~/.cursor/skills/`、`~/.agents/skills/`、`~/.claude/commands/` 与 `~/.cursor/commands/`。
