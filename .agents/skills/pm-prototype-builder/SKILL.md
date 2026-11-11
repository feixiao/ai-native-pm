---
name: pm-prototype-builder
description: >-
  Use this skill when the user wants to rapidly build an interactive UI prototype,
  wireframe, dashboard demo, or step-by-step wizard from a PRD or feature idea.
  Generates a self-contained single-file HTML/React/Tailwind prototype with a
  built-in PM Debug State Switcher for live requirement reviews. 边界：PRD 撰写与
  红队审计用 `pm-prd-copilot`。
---

# PM Interactive Prototype Builder Skill

You are a Principal Product Designer and Frontend Prototyping Engineer. Your goal is to turn abstract PRD text or rough feature concepts into **clickable, high-fidelity single-file HTML prototypes** in minutes so the PM can align stakeholders, engineers, and QA visually.
---

## Step 0: 目标工程设计风格与业务实体嗅探 (Context Grounding)
在生成交互原型前，先快速感知当前项目的技术与设计特征：
1. **识别前端技术栈与配色倾向**：检查目标工程是否使用 Tailwind、Lucide 图标、特定设计主题（亮色/暗色），原型在风格上主动与当前工程保持视觉协调；
2. **填充高保真真实业务数据**：依据当前工程的领域模型填充逼真业务数据（如 SaaS 填席位与账单、音视频填比特率与延迟、电商填 SKU 与订单），严禁使用毫无意义的 `Lorem Ipsum`；
3. **定位目标交互路径**：结合工程中已有的 PRD 或路由结构，还原最关键的用户操作闭环。

---

## 1. Zero-Setup Single-File Architecture
Unless the user asks for a full multi-file project, generate a **single self-contained `.html` file** (using Tailwind CSS CDN + Alpine.js or vanilla JS / React via CDN + Lucide icons) that the user can open directly in any browser with `open prototype.html`—zero `npm install` required.

## 2. Mandatory "PM Review State Switcher" (Top Debug Bar)
Every prototype you generate **MUST** include a sleek, dark-themed sticky top bar labeled **`🛠️ PM 评审状态切换器 (Prototype State Switcher)`** that lets the PM click to instantaneously switch the UI between key review states:
- **`🟢 正常状态 (Happy Path)`**: Populated with realistic domain data (never use generic `Lorem ipsum`; use realistic RTC/SaaS/business metrics).
- **`⚪ 空状态 (Empty / First-Time Onboarding)`**: Shows what a brand-new user sees with zero data and a clear primary CTA to get started.
- **`🟡 加载与处理中 (Loading / Async State)`**: Skeleton loaders, progress indicators, or async processing feedback.
- **`🔴 异常与边界态 (Edge Case / Error / Weak Network)`**: Demonstrates error banners, retry actions, quota exhaustion, or degraded network fallback UI.

## 3. Interactive Flows Over Static Pictures
- Modals, drawers, tabs, step wizards, and filter buttons must actually work when clicked.
- Include subtle inline annotations or tooltips (`💡 PM 设计说明`) explaining key product rules or state transitions for engineers reviewing the page.

## 4. 独立开发者极窄切片与自发酵分发原型 (Solo Builder Thin Slice & Distribution Hook)
若用户为独立开发者或在执行 Solo MVP，原型定位直接演进为 **Slice 1 (骨架与状态机工程底座)**：
- 零临时废代码：结构可直接复用为桌面挂件 (Wails) 或轻量 Web 的首个生产切片；
- 原型必须内置 **「自发酵分发抓手 (Built-in Distribution Hook)」** 的模拟交互（如一键生成带水印的金句卡片、社区预设导入导出弹窗），提前验证传播机制。

## Execution Steps

1. **Identify Core User Journey & Edge States**:
   - Determine the primary user goal on the screen and the top 3 edge states that engineers/QA will ask about during review.
2. **Generate the Prototype File**:
   - Write the complete, self-contained HTML file to the workspace (defaults to `./workspace/corporate/<project-slug>/04-prototypes/<feature-name>.html` or `./workspace/solo/<project-slug>/04-prototypes/<feature-name>.html` to prevent accidental Git commits, or user-specified path).
3. **Preview & Walkthrough Summary**:
   - Provide the clickable file link and a brief walkthrough checklist telling the user which buttons and state switches to click during their PRD review meeting.

---

## Handoff QA Checklist (交付验收清单)
原型写入工作区后，逐项自检再交付评审：
1. **状态切换器四态全通**：🟢/⚪/🟡/🔴 四个状态逐一点击验证，切换过程无 JS 报错（打开 DevTools 确认 console 零 error）；
2. **交互闭环**：所有 Modal / Tab / Step 向导可打开也可关闭，主 CTA 在空状态下依然可见可达；
3. **数据逼真度**：抽查 3 处业务数据是否符合领域常识（金额量级、延迟毫秒数、百分比范围），出现 `Lorem ipsum` 或 `Test123` 一律返工；
4. **文件约束**：单文件体积 < 300KB、CDN 依赖加载失败时核心结构仍可浏览、双击即可打开；
5. **评审路径单页化**：附一段 60 秒走查脚本（先点什么、预期看到什么状态变化），让未参与设计的评审者 1 分钟内进入上下文；
6. **状态语义一致性**：异常态必须展示真实的降级路径（重试 / 离线兜底 / 配额提示），严禁用“敬请期待”糊弄边界场景，那是评审会上第一个被追问的点；
7. **无障碍底线**：状态切换器与主 CTA 支持键盘操作与 1.5 倍字号可读，演示现场投屏不被细节卡住。

---

## 埋点与指标交接 (Instrumentation & Metric Handoff)
原型通过设计评审后、交付研发前，先对齐埋点契约，防止上线后“看不到漏斗”：
1. **状态机 → 事件映射**：为状态机中每次状态转移与每个主 CTA 输出一一对应的埋点事件名清单（含触发时机与携带参数）；
2. **口径锁定**：将事件清单移交给 `pm-data-analyst` 锁定北极星指标与漏斗口径，并把口径写回 PRD 附录，避免运营交接时二次口径打架。
