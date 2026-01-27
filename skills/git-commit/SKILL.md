---
name: git-commit
description: 根据 Git 暂存区变更自动生成符合 Angular 规范的 commit message。触发场景：(1) 用户说"帮我生成commit"、"写commit message"、"提交代码" (2) 用户运行 /git-commit 或 /commit (3) 用户问"这些改动怎么提交" (4) 用户完成代码修改后需要提交
---

# Git Commit Message Generator

根据 Git 暂存区的代码变更，自动生成符合 Angular Commit 规范的提交信息。

## 工作流程

```
1. 检查 Git 状态 (git status)
2. 获取暂存区 diff (git diff --cached) 和未暂存 diff (git diff)
3. 分析代码变更内容和意图
4. 生成符合 Angular 规范的 commit message
5. 提供给用户确认或修改
```

## Angular Commit 规范

### 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

| Type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档变更 |
| style | 代码格式（不影响代码运行的变动） |
| refactor | 重构（既不是新增功能，也不是修复 bug） |
| perf | 性能优化 |
| test | 测试相关 |
| build | 构建系统或外部依赖变更 |
| ci | CI 配置变更 |
| chore | 其他杂项（不修改 src 或 test 的变动） |
| revert | 回退某次提交 |

### Scope 范围

根据项目结构确定，常见值：
- 模块名：`auth`、`user`、`api`
- 目录名：`components`、`hooks`、`utils`
- 功能域：`login`、`dashboard`、`settings`

### Subject 标题

- 使用中文简洁描述变更内容
- 结尾不加句号
- 不超过 50 个字符

### Body 正文（可选）

- 解释变更的动机
- 与之前行为的对比
- 每行不超过 72 个字符

### Footer 页脚（可选）

- Breaking Changes：`BREAKING CHANGE: xxx`
- 关闭 Issue：`Closes #123`

## 分析策略

### 1. 判断 Type

根据变更内容判断：
- 新增文件/函数/类 → `feat`
- 修改已有逻辑修复问题 → `fix`
- 仅修改 .md 文件 → `docs`
- 仅格式化、调整空格缩进 → `style`
- 重命名、拆分、合并代码 → `refactor`
- 添加/修改测试文件 → `test`
- package.json、配置文件变更 → `build` 或 `chore`

### 2. 确定 Scope

优先级：
1. 如果只改动单个模块/目录，使用该名称
2. 如果改动多个相关模块，使用共同父级或功能域
3. 如果改动分散，可省略 scope

### 3. 撰写 Subject

提取变更核心意图，用简洁中文描述：
- 添加xxx
- 修复xxx
- 更新xxx
- 移除xxx
- 重构xxx
- 优化xxx

## 示例

### 示例 1：新增功能

变更：新增用户登录 API
```
feat(auth): 添加用户登录接口

- 新增 POST /api/auth/login 接口
- 实现 JWT token 生成
- 添加密码校验
```

### 示例 2：修复 Bug

变更：修复分页参数错误
```
fix(pagination): 修复分页页码计算错误

修复计算页偏移量时的差一错误，
偏移量之前从1开始，应从0开始。

Closes #42
```

### 示例 3：重构

变更：拆分大型组件
```
refactor(components): 拆分 UserProfile 为多个子组件

将 Avatar、UserInfo、UserActions 提取为独立文件，
提升可维护性和复用性。
```

### 示例 4：多文件变更

变更：升级依赖 + 适配代码
```
build(deps): 升级 React 至 v18

- 更新 react 和 react-dom 到 18.2.0
- 从 ReactDOM.render 迁移到 createRoot
- 更新 TypeScript 类型定义
```

## 执行步骤

1. 运行 `git status` 查看当前状态
2. 运行 `git diff --cached` 查看已暂存的变更
3. 运行 `git diff` 查看未暂存的变更
4. 分析变更内容，确定 type、scope、subject
5. 生成 commit message 并展示给用户
6. 如果用户确认，执行 `git commit -m "message"`

## 注意事项

- 如果没有暂存的变更，提示用户先 `git add`
- 如果变更内容复杂，可生成多行 body
- 如果有破坏性变更，必须在 footer 标注 BREAKING CHANGE
- 默认使用中文撰写 commit message，除非用户明确要求英文
