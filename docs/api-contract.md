# SipWise API 接口文档

本地 API 为 `http://127.0.0.1:8000/api/v1`，交互文档为 [Swagger UI](http://127.0.0.1:8000/docs)。Vue 统一调用相对地址 `/api/v1`，开发时 Vite 将请求转给 FastAPI。接口修改由昊翰和 Yichi 在同一 PR 核对，连同响应样例和调用方一起更新。

本文件描述 MVP 契约。表中 **已可调用** 的三个接口随启动骨架交付，后续接口的字段与状态码用于两人并行实现。

## 1. 接口清单

| 方法与路径（均加 `/api/v1`） | 成功响应 | 实现阶段 / 主负责人 |
|---|---|---|
| `GET /health` | 200 · 服务、数据库与配方数据源状态 | **已可调用** |
| `GET /cocktails/search?name=Negroni` | 200 · `CocktailSummary[]` | **已可调用（本地样例）** · M1 昊翰接真实 API |
| `GET /cocktails/{cocktail_id}` | 200 · `CocktailDetail` | **已可调用（本地样例）** · M1 昊翰接真实 API |
| `GET /cocktails?ingredient=Gin` 或 `?alcoholic=false` | 200 · `CocktailSummary[]` | M1 · 昊翰 |
| `GET /cocktails/random` | 200 · `CocktailDetail` | M1 · 昊翰 |
| `GET /logs?month=2026-11` | 200 · `DrinkLog[]` | M2 · Yichi |
| `POST /logs` | 201 · `DrinkLog` | M2 · Yichi |
| `PATCH /logs/{log_id}` | 200 · `DrinkLog` | M2 · Yichi |
| `DELETE /logs/{log_id}` | 204 · 空响应体 | M2 · Yichi |
| `GET /stats/summary?month=2026-11` | 200 · `StatsSummary` | M2 · 昊翰 |
| `GET /preferences` | 200 · `Preferences` | M3 · 昊翰 |
| `PUT /preferences` | 200 · 更新后的 `Preferences` | M3 · 昊翰 |
| `POST /plans/generate` | 200 · `PlanDraft` | M3 · 昊翰 |
| `POST /plans` | 200 · `SavedPlan` | M3 · 昊翰 |
| `GET /plans?week=2026-11-16` | 200 · `SavedPlan` 或 JSON `null` | M3 · 昊翰 |

## 2. 通用约定

- 请求和响应使用 JSON。无匹配结果的列表返回 `[]`。删除成功使用 204。
- 配方 ID 保持 TheCocktailDB 的字符串格式。日志 ID 是整数。日期用 `YYYY-MM-DD`，月份用 `YYYY-MM`。饮用时间必须带 UTC 偏移，服务端转成 UTC 保存和返回，日历月份按应用时区划分。MVP 默认 `Asia/Shanghai`，前端按同一时区展示。周从周一开始。
- 可空的值使用 JSON `null`。酒精或热量未知时，前端展示「无法估算」。
- 错误体为 `{"error":{"code":"NOT_FOUND","message":"Cocktail not found"}}`。调用方依据 HTTP 状态与 `code` 决定界面行为。
- 约定错误如下。骨架已实现 404 和 422。500 及代理未连通时，前端使用通用失败提示。

| 状态码 / code | 场景 |
|---|---|
| `404 NOT_FOUND` | 配方或日志 ID 不存在 |
| `409 DRAFT_EXPIRED` | 计划草稿已失效，需要重新生成 |
| `422 VALIDATION_ERROR` | 格式错误、必填值缺失或不满足业务约束 |
| `502 UPSTREAM_INVALID_RESPONSE` | 配方 API 返回无法解析的数据 |
| `503 UPSTREAM_UNAVAILABLE` | 配方 API 超时或暂不可用。LLM 失败走计划回退响应 |

## 3. 健康检查、配方与故事

`GET /health` 当前返回 `{"status":"ok","database":"ok","catalog":"fixture"}`。接入真实配方服务后可使用 `"catalog":"live"`。健康检查确认本地数据库可访问。用搜索或详情请求验证第三方服务。

搜索参数 `name` 去除首尾空白后长度为 1–100。样例数据支持忽略大小写的名称匹配。筛选端点每次接收 `ingredient` 或 `alcoholic` 中一个参数。布尔值 `false` 仅匹配明确的无酒精配方，`true` 仅匹配明确的含酒精配方。过滤结果返回摘要，点开详情后再查原料和故事。实现随机接口时，将固定路径 `/random` 放在动态路径 `/{cocktail_id}` 前注册。

`CocktailSummary` 包含 `id`、`name`、`image_url`、`alcohol_type`。其中 `alcohol_type` 取 `alcoholic`、`non_alcoholic`、`optional` 或 `unknown`。搜索 Negroni 的样例响应为：

```json
[
  {"id":"11003","name":"Negroni","image_url":null,"alcohol_type":"alcoholic"}
]
```

`CocktailDetail` 包含摘要字段以及下列字段。以下 JSON 与骨架中 Negroni 的完整详情对应：

```json
{
  "id": "11003",
  "name": "Negroni",
  "image_url": null,
  "alcohol_type": "alcoholic",
  "category": "Ordinary Drink",
  "glass": "Old-fashioned glass",
  "ingredients": [
    {"name": "Gin", "measure": "1 oz"},
    {"name": "Campari", "measure": "1 oz"},
    {"name": "Sweet Vermouth", "measure": "1 oz"}
  ],
  "instructions": "Stir the ingredients with ice, then garnish and serve.",
  "recipe_source_url": "https://www.thecocktaildb.com/drink/11003-negroni-cocktail",
  "story": {
    "summary": "一种流传较广的说法将这款鸡尾酒的起源追溯到佛罗伦萨，与 Americano 的改配有关。",
    "source_title": "Liquor.com · Negroni",
    "source_url": "https://www.liquor.com/recipes/negroni/"
  }
}
```

`image_url`、`category`、`glass`、`instructions`、各原料的 `measure` 以及 `story` 可空。正式版本使用同序号的上游原料和用量字段，保留原始顺序。故事由团队核实并按配方 ID 关联。骨架的 Margarita（`11007`）用于验证 `story: null` 的状态。

参考 [TheCocktailDB API](https://www.thecocktaildb.com/api.php)、[Negroni 配方](https://www.thecocktaildb.com/drink/11003-negroni-cocktail)和 [Negroni 背景资料](https://www.liquor.com/recipes/negroni/)。

## 4. 饮用日志与统计

`POST /logs` 请求示例：

```json
{
  "cocktail_id": "11003",
  "consumed_at": "2026-11-12T19:30:00+08:00",
  "servings": 1,
  "rating": 4,
  "flavor_tags": ["bitter", "herbal"],
  "notes": "第一次尝试"
}
```

- `cocktail_id`、`consumed_at`、`servings` 必填。份数为正的有限数值，评分是 1–5 的整数或 `null`。省略评分或备注时用 `null`，省略标签时用 `[]`。
- `DrinkLog` 返回上述字段，加上整数 `id`、`estimated_kcal` 和 `estimated_alcohol_grams`。两个估算字段分别由后端填入数值或 `null`。
- PATCH 只更新提交的字段。可用 `null` 清除评分、备注，用空数组清空标签。配方或份数变化时重算估算。GET 按饮用时间倒序，同一时间按日志 ID 倒序。计划保存由独立端点处理。

`GET /stats/summary?month=2026-11` 响应示例：

```json
{
  "month": "2026-11",
  "log_count": 2,
  "estimated_kcal": 160,
  "estimated_kcal_log_count": 1,
  "estimated_alcohol_grams": null,
  "estimated_alcohol_log_count": 0,
  "flavors": [{"tag":"bitter","count":2}]
}
```

两个合计只加该指标已知的日志。该指标无可用值时合计为 `null`，覆盖条数为 0。风味计数按每条日志的去重标签累加。历史评分也可作为推荐的排序信号。

## 5. 偏好与周计划

`Preferences` 为一份本地偏好。PUT 提交完整对象，GET 在首次保存前返回以下默认结构：

```json
{
  "preferred_flavors": [],
  "available_ingredients": [],
  "disliked_ingredients": [],
  "prefer_non_alcoholic": false,
  "max_alcoholic_drink_days": 0,
  "max_kcal_per_drink": null
}
```

`max_alcoholic_drink_days` 为 0–7 的整数，默认 0，用户可显式调整。`max_kcal_per_drink` 为正整数或 `null`。设置硬上限时，无法估算的候选不能被判定为满足限制。偏好无酒精用于排序，明确的饮用天数限制和忌用配料用于筛选。

`POST /plans/generate` 提交 `{"week_start":"2026-11-16"}`，由后端读取当前已保存偏好。响应 `PlanDraft` 包含：

| 字段 | 类型与规则 |
|---|---|
| `draft_id` | 字符串。服务端按草稿 ID 保存候选、周起点与约束 |
| `week_start` | 周一日期 |
| `status` | `draft` 表示模型生成并验证成功，`fallback` 表示显示规则排序候选 |
| `candidates` | `CocktailSummary[]`，按推荐顺序，可能为空 |
| `items` | `PlanItem[]`。成功草稿覆盖全周，回退时返回空数组供用户手动排期 |
| `message` | 可空字符串。回退时提供可展示的简短说明 |

`PlanItem` 包含 `date`、`type`、`cocktail_id`、`reason`。类型为 `cocktail`、`alcohol_free` 或 `no_drink`。前两种携带候选配方 ID，第三种的 ID 为 `null`。仅明确无酒精的配方可用于 `alcohol_free`；`cocktail` 使用明确含酒精配方。`reason` 是字符串或 `null`。

`POST /plans` 提交 `draft_id`、`week_start` 和 7 个 `items`。前端将用户没有安排的日期填为 `no_drink`。后端按草稿约束验证日期完整且唯一、配方 ID、类型和整周限制，然后在一笔 SQLite 事务中替换该周计划。草稿仅存在于当前进程，重启后需要重新生成。保存和查询返回 `SavedPlan`，字段为 `week_start` 与按日期升序排列的 `items`。
