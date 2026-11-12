# SipWise 开发与 GitHub 协作手册

适用仓库 [EachJohnnn/SipWise](https://github.com/EachJohnnn/SipWise) · MVP · 2026-11-12

**负责人 A 为昊翰，负责人 B 为 Yichi。** A 和 B 是模块负责人的代称，建 Issue 时分配给实际 GitHub 账号。提交日期待课程公布，本手册按依赖关系和验收条件排期。

## 1. MVP 范围

SipWise 是本地运行的单用户 Web 应用。Vue 3、Axios 和 ECharts 负责界面与图表，FastAPI 提供 JSON API，SQLite 保存当前这台电脑上的配方缓存、饮用记录、偏好和已保存计划。TheCocktailDB 和 LLM 由 FastAPI 调用。两人各有一套本地数据库，通过 GitHub 同步代码和测试样例。

| 功能 | MVP 验收范围 |
|---|---|
| 配方探索 | 支持按名称或单一原料找酒、按含酒精类型筛选、随机探索。详情展示图片、杯型、原料及原始用量、制作说明、来源和有出处的背景故事 |
| 饮用日历 | 新增、查看、修改、删除实际饮用记录。记录日期、份数、可选评分、风味标签和备注 |
| 统计与偏好 | 展示基础风味统计，以及有数据支持的热量和纯酒精估算。偏好包含风味、现有原料和计划限制 |
| AI 每周计划 | 从真实配方筛选和排序，生成可编辑的草稿。后端验证后保存，支持鸡尾酒、无酒精饮品和无饮品日期。模型失败时展示规则排序结果 |
| 本地数据 | 数据在同一台机器重启后可重新打开。账号登录、身份认证、按用户隔离和跨设备同步放入后续版本 |

最终演示走一条完整路径：**搜 Negroni → 打开配方和故事 → 记录实际饮用 → 查看统计 → 生成、修改并保存下一周计划**。

## 2. 开发阶段与验收

采用企业团队常见的分阶段交付方式。开工前约定需求与接口，每个功能进入 Issue，经过实现、审查和验证后合并。每阶段结束时，两人在 `main` 上走一遍验收流程并在对应 Milestone 留下结果。某个阶段仍在收尾时，下一阶段里依赖已满足的任务可以开始。

| 阶段 / GitHub Milestone | 交付物 | 阶段验收 |
|---|---|---|
| M0 · 需求与设计 | MVP 范围、API 示例、数据模型、仓库基础规则、Issue 分派 | 两人确认配方 ID、故事来源、日志时间、周计划状态和缺失值约定。确定演示配方与候选数据 |
| M1 · 基础架构、配方和故事 | Vue、FastAPI、SQLite 启动流程，Discover 页面，配方详情与故事数据 | 两人均能从全新克隆启动项目。搜索并打开 Negroni，配方和故事均有出处。无故事的配方仍可完整展示 |
| M2 · 日历与统计 | 饮用日志 CRUD、日历、摄入估算和基础风味统计 | 新增后重启仍可见。修改或删除后统计更新。缺失数据清楚显示，摄入统计按实际日志计算 |
| M3 · AI 每周计划 | 偏好、候选排序、LLM 草稿、审阅与保存、失败回退 | 用户能生成、编辑和重开计划。错误 ID 或超限请求被拦截。仅保存计划时，实际摄入统计保持原值 |
| M4 · 测试与交付 | 核心回归用例、启动说明、演示数据、发布版本 | 两人各自从全新克隆按 README 跑通演示。检查错误提示和回退，确认用于提交的 Git tag |

本地开工顺序见 [README](../README.md)，字段和 JSON 样例见 [API 接口文档](api-contract.md)。启动骨架已提供，D03 和 D04 从本地样例扩展到真实服务和完整 Discover。

先安排 M0、M1，后续根据两人每周可投入时间和课程日期填 GitHub Milestone。每次阶段验收后复盘 Issue 实际用时，重新分配下一阶段尚未开工的任务。

## 3. 模块负责人和可直接建成 GitHub Issue 的清单

A 主责配方服务和 AI 业务逻辑。B 主责 Discover、日历业务及 Planner 界面。统计由 A 负责，减少 B 在 M2 同时做日历、统计和界面的压力。两人都提交 Python 代码和测试，自己的代码由搭档审查。表中的任务编号用于文档依赖，建 Issue 后可替换为实际的 `#编号`。

工作量用相对点数估计，1 点为小改动，2–3 点为一个小模块，5 点为含前后端的完整功能。各阶段初始估算均衡，**A 与 B 各 23 点**。如果某个 5 点任务卡住一个阶段，先拆成可独立验收的 PR，再把其中一项转给有空的成员。

| 编号 | 阶段 | 负责人 / 点数 | Issue 标题与交付 | 依赖 | 验收条件 |
|---|---|---|---|---|---|
| D01 | M0 | A / 3 | 草拟数据模型、路由和服务端配置约定，建立 Milestone 与 Issue 分派并复核仓库规则（骨架已由 Yichi 于 2026-11-12 提交） | 无 | `main` 有 README 和忽略规则。接口草案包含配方、日志、统计、偏好、周计划。Issue 与 Milestone 齐全 |
| D02 | M0 | B / 3 | 验证演示需求，整理页面流程、响应样例和测试清单 | 无，和 D01 联合定稿 | 两人确认页面对应的 API、故事的展示位置和首批样例 |
| D03 | M1 | A / 5 | 在 FastAPI/SQLite 骨架上接入真实配方服务，完成搜索、筛选、详情、随机和缓存 | D01、D02 | 规范化配方字段。区分空搜索与上游故障。按 ID 读取完整配方 |
| D04 | M1 | B / 5 | 在 Vue 骨架上完成 Discover 搜索、筛选、随机和详情页 | D01、D02，联调依赖 D03 | 先用示例 JSON 开发，随后接真实 API。空结果与失败均有界面状态 |
| D05 | M1 | A / 2 | 实现按配方 ID 关联故事，在详情响应返回来源 | D03 的详情结构 | 同一响应能返回真实配方和对应故事。无故事返回 `null` |
| D06 | M1 | B / 2 | 整理首批故事并完成详情页展示 | D02，联调依赖 D05 | 完成 3 款可查证故事，逐条核对配方 ID、出处和起源措辞 |
| D07 | M2 | B / 5 | 完成日志模型、CRUD API 和日历界面 | D03，接口由 D01、D02 约定 | 能新增、编辑、删除并按月加载。校验份数、评分和配方 ID |
| D08 | M2 | A / 3 | 建立原料参考数据，计算热量和纯酒精估算 | D03，和 D07 对齐日志字段 | 支持明确用量的样例。缺数据返回未知。验证份数缩放 |
| D09 | M2 | A / 2 | 实现风味及摄入汇总 API 和基础 Insights 视图 | D07、D08 | 修改或删除后重新查询统计，结果同步更新。显示估算覆盖条数 |
| D10 | M3 | A / 3 | 保存偏好，筛选与排序真实配方，生成 LLM 草稿和规则回退 | D03、D09 | 候选携带真实 ID。LLM 异常、非法输出或候选不足时有明确结果 |
| D11 | M3 | A / 2 | 验证整周计划并保存，支持重开与更新 | D10 | 保存前重验日期、ID、条目类型和限制。同周重复保存时更新同一计划 |
| D12 | M3 | B / 3 | 实现 Planner 页面、偏好输入、草稿编辑、保存和回退视图 | 可用样例先做，联调依赖 D10、D11 | 从界面完成生成、编辑、保存和重开，能处理空候选和模型失败 |
| D13 | M3 | B / 2 | 测试非法 ID、重复日期、超限和计划对日志的影响 | D10、D11、D12 | 记录可复现测试结果。验证计划保存不创建饮用日志 |
| D14 | M4 | A / 3 | 完成 API 回归、配置与 README 启动说明 | M1–M3 | 用干净环境复跑后端测试。记录外部服务与环境变量配置 |
| D15 | M4 | B / 3 | 完成演示脚本、浏览器回归和交付打包 | M1–M3 | 从全新克隆走完演示，记录预期行为与实测结果，双方确认发布版本 |

D07 建议拆成「后端 CRUD」和「Vue 日历」两个 PR。M2 开始时，B 先给出可运行的日志接口和样例，A 先用样例实现汇总，待 SQLite 流程合入再做真实联调。

## 4. 配方与故事放在哪里

把老师提出的要求放进 **M1 的 Discover → 配方详情**。先展示配方和制作说明，旁边或下方展示「背后的故事」。M3 的推荐卡片复用同一个详情入口。

- **配方**来自 TheCocktailDB。列表可使用摘要，详情按 `idDrink` 查询。将同序号的原料与用量配对，保留顺序和原始单位，缺用量时保留空值。在详情标注配方及图片出处。
- **故事**由团队根据可查证资料用自己的话撰写。TheCocktailDB 的公开 V1 文档和样例未提供可依赖的鸡尾酒故事字段。先覆盖 Negroni 和另外两款由团队核实的演示配方。起源说法有争议时，用「一种常见说法」等明确措辞。
- **数据关联**使用 `backend/app/data/cocktail_stories.json`，以 TheCocktailDB 配方 ID 为键。保存 `summary`、`source_title`、`source_url`。FastAPI 组合配方和故事，Vue 直接渲染返回值。无故事时显示「暂无经核实的背景故事」。
- **验收对照**打开 Negroni（`11003`），配方链接指向 TheCocktailDB，故事链接指向历史资料。再打开一款未收录故事的鸡尾酒，确认它的原料和步骤依然可见。LLM 的个性化推荐理由显示在 Planner，由该功能单独生成。

首个可核实案例见 [TheCocktailDB · Negroni 配方](https://www.thecocktaildb.com/drink/11003-negroni-cocktail) 和 [Liquor.com · Negroni 背景](https://www.liquor.com/recipes/negroni/)。字段和查询方式见 [TheCocktailDB API 文档](https://www.thecocktaildb.com/api.php) 和 [完整配方字段说明](https://www.thecocktaildb.com/AGENTS.md#understanding-drink-records)。

## 5. 开发接口与数据约定

### 目录与职责

| 路径 | 内容 |
|---|---|
| `frontend/src/views/`、`components/`、`api/` | 页面、复用组件、Axios 请求封装 |
| `backend/app/routers/`、`schemas/` | FastAPI 路由和输入输出校验 |
| `backend/app/services/`、`models/` | 配方、日志、统计、推荐业务逻辑和 SQLite 数据模型 |
| `backend/app/data/` | 经核实的故事数据和带来源的原料参考数据 |
| `backend/tests/` | 单元和 API 测试、可提交的模拟数据 |
| `docs/` | 本手册、双方核准的接口示例和演示流程 |

### 接口约定

路径以 `/api/v1` 为前缀。下表是实施起点。D01 和 D02 一起核准 [接口文档](api-contract.md) 中的请求、响应与错误示例。双方先按样例并行开发，接口有变动时在同一个 PR 更新样例和相关测试。

| API | 输入与结果 |
|---|---|
| `GET /cocktails/search?name=Negroni` | 按名称返回摘要数组。没有结果时返回空数组 |
| `GET /cocktails?ingredient=Gin`、`GET /cocktails?alcoholic=false` | 按单一原料或含酒精状态筛选。摘要点开后按 ID 查详情 |
| `GET /cocktails/random`、`GET /cocktails/{id}` | 返回完整配方、`recipe_source_url` 和可空的 `story` |
| `GET /logs?month=YYYY-MM`、`POST /logs` | 按月列出日志。新增时提交 `cocktail_id`、`consumed_at`、`servings`、可选评分、风味标签和备注 |
| `PATCH /logs/{id}`、`DELETE /logs/{id}` | 修改或删除实际日志。修改用量或配方时重算估算字段 |
| `GET /stats/summary?month=YYYY-MM` | 返回记录数、估算总量、热量与酒精各自的覆盖条数及风味分布 |
| `GET /preferences`、`PUT /preferences` | 获取或更新本地偏好，包括风味、现有原料和计划约束 |
| `POST /plans/generate` | 返回可编辑草稿、草稿 ID 和可替换的候选配方，或返回规则排序结果。生成过程不写入计划表 |
| `GET /plans?week=YYYY-MM-DD`、`POST /plans` | 查询某周的计划。提交草稿 ID 与已确认的整周安排，校验后在同一事务中保存。重复保存同一周会替换该周安排 |

详情响应中的故事结构示意：

```json
{
  "id": "11003",
  "name": "Negroni",
  "recipe_source_url": "https://www.thecocktaildb.com/drink/11003-negroni-cocktail",
  "story": {
    "summary": "一种流传较广的说法将这款鸡尾酒的起源追溯到佛罗伦萨，与 Americano 的改配有关。",
    "source_title": "Liquor.com · Negroni",
    "source_url": "https://www.liquor.com/recipes/negroni/"
  }
}
```

完整配方还包含图片、酒精分类、杯型、原料数组和制作说明。保留上游酒精分类中的可选或未知情况，无法确认无酒精的配方不得进入无酒精计划项。后端以稳定字符串保存上游配方 ID。

### 数据与业务边界

| 表 | 用途与规则 |
|---|---|
| `cocktails` | 以配方 ID 为主键缓存标准化配方。其他表用该 ID 关联 |
| `drink_logs` | 仅存实际饮用记录。份数大于零，可选评分为 1–5。API 接收带时区时间，按约定的应用时区划分日历月份 |
| `user_preferences` | 本机一份偏好，供 UI 与推荐流程读取 |
| `weekly_plan_items` | 以周一为周起点、日期为条目定位，同一天最多一条。`no_drink` 的配方 ID 为空，其他类型须指向真实且符合类型的配方 |

- 估算由 Python 根据原料参考数据和份数计算，热量和酒精分别判断能否估算。未知值返回 `null`。统计展示已知小计及覆盖条数，整组没有可用估算时显示未知。
- LLM 草稿先做结构校验，再检查日期、短名单中的配方 ID、条目类型和整周限制。FastAPI 在内存按草稿 ID 保留候选、周起点和约束。保存时使用该服务端记录校验用户修改。进程重启后，未保存草稿需要重新生成，已保存计划可正常查看。生成成功和规则回退在 API 中使用明确的状态值。
- 错误响应提供可识别的错误码。配方或日志不存在返回 404，字段校验失败返回 422，草稿已失效返回 409。上游响应异常与服务暂时不可用分别处理，前端对应展示提示。

## 6. GitHub 操作

### 首次初始化

A 邀请搭档成为仓库协作者，由搭档接受并确认可以推送。A 先完成一次最小初始化提交，再由 B 克隆。若开工时仓库已经有提交，先同步现有 `main`，后续变更走普通 PR。

```bash
git clone https://github.com/EachJohnnn/SipWise.git
cd SipWise
git switch -c main
```

空仓库初始化时，按 [README](../README.md) 将启动骨架放入仓库根目录，验收后执行：

```bash
git add README.md .gitignore backend frontend docs
git commit -m "chore: bootstrap SipWise local development"
git push -u origin main
```

搭档随后运行前两条命令克隆并进入仓库。双方用 `git remote -v` 确认远端，用首次功能分支推送验证写权限。

### 每个功能的日常流程

1. 在 GitHub 创建 Issue，填负责人、Milestone、依赖和验收条件。存在前置依赖时链接实际 Issue。
2. 工作区干净时，从最新的 `main` 建分支。以 `feature/cocktail-detail` 为例：

   ```bash
   git switch main
   git pull --ff-only origin main
   git switch -c feature/cocktail-detail
   ```

3. 实现和验证后，提交具体文件，再推送分支：

   ```bash
   git status
   git add <本次修改的文件路径>
   git commit -m "feat: add cocktail detail endpoint"
   git push -u origin feature/cocktail-detail
   ```

4. 打开目标为 `main` 的 PR。在描述中写改动、复现步骤和测试结果，填 `Closes #实际编号`。搭档负责审查和复跑相关流程。
5. 如遇冲突，作者在自己的分支执行 `git fetch origin` 和 `git merge origin/main`，与搭档核对冲突部分，解决后复跑相关测试并推送。通过审查后可以 squash merge，两人再同步 `main`。

初始化后，团队按 PR 流程合并功能。仓库权限允许时，可配置 `main` 需要一个审批。README 记录两端的运行版本和命令。将 `.env`、密钥、本地 SQLite 数据库及其辅助文件、`.venv` 和 `node_modules` 加入忽略规则。提交 `.env.example` 和合成测试数据，供搭档独立启动与验证。

## 7. 验收与发布

| 检查 | 预期结果 |
|---|---|
| 配方详情与故事 | 有来源的样例能点击出处，无故事时显示清晰状态。配方原料和用量能与上游对应 |
| 搜索为空或上游超时 | 空搜索和外部故障分别显示合适反馈 |
| 日志 CRUD | 正份数与有效评分可保存。非法输入被拒绝。重启后数据仍在，修改与删除反映在统计中 |
| 摄入与风味 | 用可重复的参考样例验证份数缩放、未知值和覆盖条数。风味随评分与标签更新 |
| AI 计划 | 使用模拟 LLM 测非法 JSON、无效 ID、重复日期和超限。无可用模型时仍能看规则推荐 |
| 端到端 | 用真实配方和已配置模型跑一次完整演示，再断开或模拟服务失败验证回退。记录模型、候选及结果，便于复现。上线演示前使用同一组偏好对照规则排序与 AI 草稿，人工检查风味理由是否对应候选，以及是否满足无酒精和日期约束 |

每个 PR 的完成条件是验收条件可复现、相关测试通过、搭档完成审查。交付前从全新克隆跑完流程，在通过验证的 `main` 提交打 `v0.1.0` 标签。课程尚未确定截止日，Milestone 日期由两人根据实际进度填写。课题提出的顺序与异步请求对比可在主流程验收后加入性能实验。

## 项目依据

- [SipWise Research Proposal](https://chatgpt.com/library?file_id=libfile_03a6f707b63881918d50c0e2f8f9fdd7&account_id=personal)提供系统架构、核心流程和四个开发阶段。
- 本手册加入开工前设计确认、GitHub 审查与验收流程，以及老师提出的配方与背景故事展示。
