# Yukon Claude Marketplace

Claude Code 插件集合，封装了一些实用的开发工具和技能。

## 插件一览

## Skills（技能集合）

> 安装 `dev-skills` 即可获得以下所有技能

### 🔀 git-commit

> 根据 Git 暂存区变更，自动生成符合 **Angular Commit 规范** 的提交信息。

**功能特性：**

- 自动分析 `git diff --cached` 暂存区变更内容
- 遵循 Angular 规范，智能识别变更类型（feat / fix / refactor / docs 等）
- 自动推断 scope 范围
- 生成中文 commit message，支持 body 和 footer
- 用户确认后自动执行 `git commit`

**使用方式：**

```
/git-commit
```

**重启 claude 会话：**

<img width="618" height="741" alt="image" src="https://github.com/user-attachments/assets/e56b9a5d-848e-4fc9-8f4c-0672d3bc496e" />

---

### 🐛 error-explain

> 解析各类报错堆栈，定位问题根因，给出具体修复建议和示例代码。

**功能特性：**

- 支持 JavaScript/TypeScript、Node.js、Vue/React/Nuxt/Next 等框架错误
- 支持 Webpack/Vite/Rollup 构建工具错误
- 支持微信小程序、uniapp 错误
- 支持数据库（MySQL/MongoDB/Redis）和网络请求（CORS/SSL）错误
- 按概率排序可能原因
- 提供修复前后代码对比
- 附带预防措施和最佳实践

**使用方式：**

```
/error-explain
```

或直接粘贴报错信息，AI 会自动识别。

---

### ✨ prompt-optimize

> 优化用户的 AI Prompt，让输出更精准、更符合预期。

**功能特性：**

- 分析 Prompt 结构完整性（角色/目标/上下文/格式/约束）
- 检查清晰度和歧义问题
- 提供优化建议和改进版本
- 内置代码生成、代码审查、文档生成等 Prompt 模板
- 支持 Few-shot 示例优化

**使用方式：**

```
/prompt-optimize
```

或说"帮我优化这个 prompt"。

---

## Plugins（插件）

### 🔍 refactor-suggest

> 分析指定文件或目录的代码质量，识别坏味道（Code Smells），给出具体重构建议和示例代码。

**功能特性：**

- 检测过长函数、深层嵌套、参数过多、重复代码等常见坏味道
- 识别文件/模块级问题：职责不单一、过度耦合、循环依赖
- 前端专项检测（Vue/React/小程序）：巨型组件、Props 透传、副作用散落等
- 按严重程度分级（🔴 严重 / 🟡 建议 / 🔵 提示）
- 每个问题附带重构前后的代码对比示例
- 内置 Code Smell Detector Agent 进行结构化检测

**使用方式：**

```
/refactor-suggest
```

---

### 🗑️ dead-code

> 检测项目中的dead code，包括未使用的导出、未引用的文件、废弃的路由页面，输出可安全删除的清单。

**功能特性：**

- 检测未使用的导出（export 但从未被 import）
- 检测未引用的文件（整个文件无任何引用）
- 检测废弃的路由/页面（路由存在但无入口跳转）
- 检测未调用的内部函数
- 检测未使用的 npm 依赖
- 按置信度分级（🟢 高 / 🟡 中 / 🔴 低）
- 支持 Vue/Nuxt/React/Next/小程序等多种项目类型
- 输出可直接执行的删除命令

**使用方式：**

```
/dead-code
```

---

## 安装使用

### 方式一：CLI

```bash
claude plugin marketplace add lovelyJason/claude-plugins
```

### 方式二：Claude REPL

```
/plugin marketplace add lovelyJason/claude-plugins
```

### 方式三：借助本作者的另一客户端软件，通过界面添加

https://github.com/lovelyJason/mcp-switch

<img width="900" height="600" alt="image" src="https://github.com/user-attachments/assets/8c22fcd7-5b7d-438d-a8c9-fd128d3a5121" />

<img width="900" height="600" alt="image" src="https://github.com/user-attachments/assets/463e17d3-8c4b-43db-a621-e550b7841547" />

安装完成

<img width="900" height="600" alt="image" src="https://github.com/user-attachments/assets/a8f7a09a-599b-4535-873f-d2ec7ad96f58" />

### 安装skills

```bash
claude plugin install dev-skills@lovelyJason/claude-plugins

# REPL环境
/plugin install dev-skills@lovelyJason/claude-plugins
```

## 安装plugins

```bash
claude plugin install dead-code@yukon-claude-marketplace

# REPL环境
/plugin install dead-code@yukon-claude-marketplace
```