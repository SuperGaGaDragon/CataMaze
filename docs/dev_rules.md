# CataMaze Development Rules

## Core Constraints

### 1. Code File Size Limit
**任何单个代码文件不得超过 200 行**

- 包括 Python 文件（.py）、JavaScript 文件（.js）、HTML/CSS 等
- 超过 200 行时必须拆分为多个文件
- 拆分原则：按功能模块拆分，保持单一职责
- 示例：
  - `engine.py` 过长 → 拆分为 `engine_core.py`, `engine_state.py`, `engine_tick.py`
  - `api/routes.py` 过长 → 拆分为 `api/game_routes.py`, `api/watch_routes.py`

### 2. Documentation Requirements
**每完成一个 stage 文档，必须创建对应的 summary 文件**

- 路径：`docs/implementation/summarys/stageXy_summary.md`
- 格式：X = stage number (0-6), y = sub-stage (a-e)
- 示例：完成 `stage1b.md` 后创建 `stage1b_summary.md`
- Summary 内容必须包含：
  - 执行时间
  - 任务目标
  - 完成内容（checklist）
  - 遇到的问题
  - 未完成项
  - 下一步计划

### 3. Version Control
**完成每个 stage 后，统一提交并推送**

```bash
cd /Users/alex_1/desktop/catamaze
git add .
git commit -m "Stage Xy complete: [description]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
git push
```

- 不要只推送单个文件，统一 `git add .`
- Commit message 格式：`Stage Xy complete: [简短描述]`
- 必须包含 Co-Authored-By 标签

### 4. Uncertainty Handling
**任何不确定的规则或需求，先在 docs/ 记录提问**

- 不要自作主张修改需求或规则
- 在 `docs/questions.md` 中记录疑问
- 格式：
  ```markdown
  ## [Date] Stage Xy - [Question Title]

  **Context**: [背景说明]

  **Question**: [具体问题]

  **Options Considered**: [考虑的选项]

  **Decision**: [待定 / 已决定]
  ```

### 5. Implementation Approach
**按步骤写代码，不要自己设计架构**

- 严格按照 stage 文档的 Instructions 执行
- 不要跳过步骤或合并步骤
- 不要添加文档未要求的功能
- 遇到 stage 文档不清楚的地方，参考 `catamaze.md` 和其他 docs/

### 6. Testing and Validation
**代码完成后必须能运行**

- 确保没有语法错误
- 确保依赖正确安装（requirements.txt）
- 关键模块需要简单的手动测试
- Stage 1 之后的代码需要确保 API 能正常启动

### 7. Database Operations
**数据库操作必须安全且可追溯**

- 使用 SQLAlchemy ORM，不要写原生 SQL
- 使用 Alembic 管理数据库迁移
- 首次启动自动建表（通过 `create_all()`）
- 不要手动删除数据库，使用代码管理

### 8. Error Handling
**所有 API 端点必须有错误处理**

- 捕获常见异常（KeyError, ValueError, SQLAlchemy errors）
- 返回友好的错误信息
- 使用标准的 HTTP 状态码
- 不要暴露内部实现细节

### 9. Configuration Management
**环境变量通过 .env 管理**

- DATABASE_URL 必须从环境变量读取
- 不要硬编码敏感信息
- 使用 python-dotenv 加载配置

### 10. Code Style
**保持代码清晰简洁**

- 使用有意义的变量名
- 函数/类名遵循 Python PEP 8 规范
- 添加必要的注释（但不要过度注释）
- 保持一致的缩进和格式

## Stage Workflow

每个 stage 的标准流程：

1. **读取 stage 文档**：仔细阅读 `docs/implementation/stageXy.md`
2. **执行 Instructions**：按顺序完成所有步骤
3. **完成 Checklist**：确保所有项目都完成
4. **创建 Summary**：在 `summarys/` 中创建总结文档
5. **提交代码**：`git add . && git commit && git push`
6. **进入下一步**：读取下一个 stage 文档

## Reference Documents

- **catamaze.md**: 游戏功能与架构总览
- **进度追踪.md**: Stage 总览与进度追踪
- **architecture.md**: 模块职责详解
- **data_models.md**: 数据结构定义
- **api_spec.md**: API 端点规范
- **dev_rules.md**: 本文档，开发规则
