# SipWise

双人课程项目，使用 Vue 3、FastAPI 和 SQLite。本启动版本能通过网页搜索两条本地鸡尾酒样例，并显示配方详情与背景故事。开发阶段、接口和后续分工见 [开发手册](docs/development-plan.md)与 [API 接口文档](docs/api-contract.md)。

## 1. 克隆仓库

骨架已于 2026-11-12 提交到 `main`（`chore: bootstrap SipWise local development`），仓库不再是空的，直接克隆即可：

```bash
git clone git@github.com:EachJohnnn/SipWise.git
cd SipWise
```

**必须使用上面的 SSH 地址。** 国内网络下 `github.com:443` 被阻断，HTTPS 克隆会报 `Failed to connect to github.com port 443`。首次使用前把本机公钥加到 GitHub（Settings → SSH and GPG keys），验证方式：

```bash
ssh -T git@github.com   # 应返回 Hi <用户名>!
```

两人均已是协作者，权限对等。克隆后确认根目录能看到 `README.md`、`backend/`、`frontend/` 和 `docs/`，然后执行第 2、3 节的启动与验收。

之后所有改动都走分支 + PR，不再直接提交到 `main`：

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/<本次功能>
```

## 2. 本机启动

准备 Git、Python 3.12 和 Node.js 22.x（至少 22.12）或 24.x。项目在本机运行，SQLite 由 Python 内置模块访问，数据库文件由 FastAPI 启动时创建。这个阶段只需启动两个本地进程。Docker、云部署、LLM 和第三方 API 密钥留到相应功能阶段。

macOS 自带的 `python3` 可能仍是 3.9，创建虚拟环境时指定版本，避免依赖装不上：`python3.12 -m venv .venv`。国内网络安装后端依赖可加清华源 `-i https://pypi.tuna.tsinghua.edu.cn/simple`。

**终端 A · FastAPI**

从仓库根目录执行。macOS 与 WSL 使用下面的 Bash 命令：

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**终端 B · Vue**

打开另一个终端，从仓库根目录执行：

```bash
cd frontend
npm ci
npm run dev
```

打开 [SipWise 网页](http://127.0.0.1:5173) 和 [FastAPI Swagger](http://127.0.0.1:8000/docs)。如后端端口有冲突，修改启动命令的端口和 `frontend/vite.config.js` 的代理目标，使两边一致。终端使用 `Ctrl+C` 停止服务。

## 3. 两个人都验收一次

1. 网页显示「FastAPI 与 SQLite 已连接 · 本地样例」。
2. 搜 `Negroni`，点结果，看到三种原料、制作说明和有出处的故事。
3. 搜 `Margarita`，点结果，看到缺失用量的提示和「暂无经核实的背景故事」。
4. 搜一个不存在的酒名，看到空结果提示。
5. 在 Swagger 执行 `GET /api/v1/health`，看到 `catalog: fixture`。本地 SQLite 文件在 `backend/var/sipwise.sqlite3`。

也可以直接验证 Vite 代理和详情接口：

```bash
curl -fsS http://127.0.0.1:5173/api/v1/health
curl -fsS 'http://127.0.0.1:8000/api/v1/cocktails/search?name=Negroni'
curl -fsS http://127.0.0.1:8000/api/v1/cocktails/11003
```

## 4. 从骨架分头开发

| 人 | 第一条分支 | 先修改哪里 | 第一次提交的验收条件 |
|---|---|---|---|
| 昊翰 | `feature/cocktail-api` | `backend/app/routers/cocktails.py`。新增 `backend/app/services/cocktail_service.py` 封装 TheCocktailDB，完成字段映射与缓存，并移除骨架中自动写入样例的启动逻辑 | 搜索和详情切到真实配方数据，返回字段仍符合接口文档。真实调用与异常处理可独立测试 |
| Yichi | `feature/discover-ui` | `frontend/src/App.vue`。按页面和组件整理搜索、结果和详情，继续调用 `frontend/src/api/client.js` | 对着现有样例接口完成列表和详情。加载、无结果、缺故事和失败状态均可验证 |

两人都从最新 `main` 创建自己的分支。前端合并前用骨架样例开发，后端接通真实数据后一起回归搜索和详情。故事来源确认后，Yichi 提交文字与来源，昊翰在详情接口按配方 ID 合入。

后续 M2 由 Yichi 负责日志 API 与日历，昊翰负责估算与统计。M3 再加入偏好与计划。两人通过 GitHub 同步代码、接口文档、依赖锁文件和测试样例。各自 SQLite 数据、虚拟环境、依赖安装目录和密钥留在本机。

## 5. 首次会改到的文件

| 文件 | 作用 |
|---|---|
| `backend/requirements.txt` | 固定后端直接依赖 |
| `backend/app/main.py` | 创建 FastAPI、启动数据库、挂载路由和健康检查 |
| `backend/app/database.py` | 创建并访问本地 SQLite，写入启动样例 |
| `backend/app/routers/cocktails.py`、`schemas.py` | 搜索与详情接口、请求和响应结构 |
| `backend/app/data/cocktails_fixture.json` | 可重复的两条配方样例 |
| `frontend/package.json`、`package-lock.json` | 固定前端依赖，供 `npm ci` 使用 |
| `frontend/vite.config.js` | 开发服务器与 `/api` 代理 |
| `frontend/src/App.vue`、`src/api/client.js` | 可验收的初始界面和 Axios 客户端 |
| `.gitignore` | 排除本地 SQLite、环境文件、依赖与构建产物 |
