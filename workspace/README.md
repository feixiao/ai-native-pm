# 🔒 本地生产工作台 (Local Production Workspace)

> **隐私与安全保护声明**：  
> 本目录及其所有子文件已在根目录 `.gitignore` 中完成全局隔离规则配置。**所有在此处生产的项目需求、客户访谈、商业秘密、产品原型与数据分析文档均仅保存在本地，绝对不会被上传或提交至远程 Git 仓库。**

---

## 一、 为什么设立本工作台？(Why Workspace?)

在以往的产品规划与开发实践中，文档管理常面临 **三大核心污染痛点**：
1. **公私混杂污染**：私有商业机密、客户原始访谈音频/逐字稿、内部草稿与公开代码库混在一起，易发生 Git 误提交泄密；
2. **双轨心智污染**：大厂企业级 TPM 的重度交底 PRD（40+页、RACI、状态机）与独立开发者（Solo Builder）的一页纸 MVP 契约、Micro-Spec 混在同一目录，导致方法论错配与提示词退化；
3. **跨项目跨类型污染**：不同业务线（如车机座舱 vs 桌面宠伴）混杂，或需求、原型、接口、SQL 脚本全部堆在单一平铺文件夹中，上下文严重串扰。

为此，本工作台建立 **“严格沙盒隔离、双轨各行其道、阶段流水编号、永不上传远程”** 的本地工作空间体系。

---

## 二、 目录结构全景图 (Directory Architecture)

```
workspace/                                  # 🔒 本地工作台根目录 (已 gitignore，永不上上传)
│
├── corporate/                              # 🏢 轨道 A：企业与工业级 TPM 空间 (Corporate & Industrial)
│   └── <project-slug>/                     # 单个业务线项目独立沙盒 (如: cockpit-ivi, audio-vivid)
│       ├── 01-research/                    # 市场扫描、竞品逆向拆解、行业政策与准入合规
│       ├── 02-user-insights/               # B端客户调研、JTBD 痛点挖掘、需求池 (Backlog)
│       ├── 03-prd-specs/                   # 工业级 PRD、全量状态机流转图、异常降级矩阵
│       ├── 04-prototypes/                  # 单文件带 PM 调试栏原型 (.html)、交互设计说明 (Design Brief)
│       ├── 05-architecture-handoff/        # 研发交接：OpenAPI 契约、数据保留边界、RACI 协同矩阵
│       ├── 06-qa-acceptance/               # BDD 验收用例表、边缘场景清单、架构与 QA 毒舌红队自审
│       └── 07-data-metrics/                # 北极星/护栏指标体系、生产级埋点方案表、业务漏斗 SQL
│
├── solo/                                   # 🚀 轨道 B：独立开发者 / 一人公司空间 (Solo Builder & Indie)
│   └── <project-slug>/                     # 单个独立项目沙盒 (如: pixel-pet, video-flow, micro-saas)
│       ├── 01-validation/                  # 机会卡 (Opportunity Card)、The Mom Test 真实取证、代偿行为验证
│       ├── 02-spike/                       # <=4h 极速技术探针报告、核心断点可行性验证脚本 (Spike Log)
│       ├── 03-contract/                    # 《一页纸 MVP 契约》(内嵌自发酵传播抓手、两周止损门禁与非目标)
│       ├── 04-agent-specs/                 # 喂给 Claude Code / Cursor 的阶梯式 Micro-Specs (Slice 1/2/3)
│       ├── 05-sprints/                     # 单问题周冲刺日志 (Weekly Sprints)、周末五选一冷血决策门
│       └── 06-metrics-cash/                # 防破产 Quota 熔断配置、Stripe 边际账单、单用户单位经济效益 (UE)
│
├── shared/                                 # 🧩 跨项目通用沉淀区 (避免不同项目重复造轮子)
│   ├── templates/                          # 个人/团队定制的专用文档模板
│   ├── interview-scripts/                  # 沉淀的通用非引导访谈提纲话术库
│   └── cheat-sheets/                       # 行业专有名词表、平台合规禁令、常用 SQL/API 代码片段
│
└── archive/                                # 📦 归档与止损隔离区 (彻底隔离非活跃项目，避免干扰视线)
    ├── corporate/                          # 企业已交付结项或暂停推进的项目
    └── solo/                               # 独立开发触发 14 天两周死线终止 (Drop-dead) 或已售出的项目
```

---

## 三、 五大防污染隔离机制 (Anti-Pollution Guardrails)

| 隔离维度 | 核心规则 | 隔离效果 |
| :--- | :--- | :--- |
| **1. 轨道隔离 (Track)** | 强制区分 `corporate/` 与 `solo/`。 | 大厂 TPM 的 40 页交底 PRD 不会污染独立开发者的极简一页纸；独立开发者的 Micro-Spec 碎切片也不会稀释大厂标准。 |
| **2. 命名空间隔离 (Project)** | 每个项目必须且只能使用单独的 `<project-slug>` 目录。 | 项目 A（如车机座舱）的概念、缩写和 API 永远不会被误带入项目 B（如个人微 SaaS）。 |
| **3. 阶段流水隔离 (Phase)** | 统一使用数字前缀文件夹（如 `01-research`、`03-prd-specs`）。 | 原型代码 (`.html`)、数据脚本 (`.sql`) 与规格文档 (`.md`) 物理分流，告别文件大杂烩。 |
| **4. 状态隔离 (Status)** | 未推进、已结项、或触发 14 天止损门禁的项目，一律剪切移至 `archive/`。 | 日常开发工作区永远只保留当前正在冲刺的 1~2 个核心项目，消除认知负荷。 |
| **5. 通用资产隔离 (Shared)** | 跨项目的公用组件、模板、常用 SQL 提取至 `shared/`。 | 避免在各项目中到处复制粘贴副本，杜绝版本碎片化。 |

---

## 四、 命名与归档规范 (Naming Conventions)

在生成和保存文档时，遵循以下命名准则：

1. **项目目录名**：统一采用全小写英文与中划线，如 `cockpit-audio-vivid`、`pixel-desktop-pet`。
2. **企业级工业 PRD**：`03-prd-specs/PRD_<MODULE>_<NAME>_v1.0.md`（如 `PRD_AUDIO_UPMIX_v1.0.md`）。
3. **独立开发者一页契约**：`03-contract/ONE_PAGE_MVP_CONTRACT.md`。
4. **阶梯式 Micro-Spec**：`04-agent-specs/MICRO_SPEC_SLICE_<N>_<FEATURE>.md`（如 `MICRO_SPEC_SLICE_1_AUTH_PIPELINE.md`）。
5. **交互原型文件**：`04-prototypes/<feature-slug>-prototype.html`（强制包含顶部 `🛠️ PM 评审状态切换器`）。
6. **周冲刺日志**：`05-sprints/SPRINT_WEEK_<YYWW>_<QUESTION>.md`。

---

## 五、 与内置 PM 技能库自动路由对齐 (Skills Routing Table)

当调用 `.agents/skills/` 下的垂直技能时，输出文件建议直接沉淀至对应目录：

| 调用技能 | 企业级项目推荐路由 (`workspace/corporate/<project>/`) | 独立开发项目推荐路由 (`workspace/solo/<project>/`) |
| :--- | :--- | :--- |
| **`pm-market-competitor`** | `01-research/competitor-teardown.md` | `01-validation/market-opportunity-card.md` |
| **`pm-user-insight`** | `02-user-insights/interview-synthesis.md` | `01-validation/mom-test-evidence.md` |
| **`pm-prd-copilot`** | `03-prd-specs/PRD_<FEATURE>_v1.0.md` | *(独立开发轨通常跳过，直接转为一页契约)* |
| **`pm-prototype-builder`** | `04-prototypes/<feature>-prototype.html` | `04-prototypes/mvp-prototype.html` (可选验证) |
| **`pm-solo-builder`** | *(企业轨不推荐使用)* | `01-validation/`, `02-spike/`, `03-contract/`, `04-agent-specs/` |
| **`pm-data-analyst`** | `07-data-metrics/metrics-framework.md` | `06-metrics-cash/quota-runway-metrics.md` |
| **`pm-report-polisher`** | `workspace/corporate/<project>/06-qa-acceptance/` 或项目根周报 | `05-sprints/weekly-decision-log.md` |
