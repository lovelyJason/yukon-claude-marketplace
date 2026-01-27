# My Claude Plugins

Jasonhuang 的个人 Claude Code 插件集合，包含实用的开发工具和技能。

## Skills 一览

### 🔀 git-commit

> 根据 Git 暂存区变更，自动生成符合 **Angular Commit 规范** 的提交信息。

**功能特性：**

- 自动分析 `git diff --cached` 暂存区变更内容
- 遵循angular规范，智能识别变更类型（feat / fix / refactor / docs 等）
- 自动推断 scope 范围
- 生成中文 commit message，支持 body 和 footer
- 用户确认后自动执行 `git commit`

**使用方式：**

```
/git-commit
```

**重启claude会话：**

<img width="618" height="741" alt="image" src="https://github.com/user-attachments/assets/e56b9a5d-848e-4fc9-8f4c-0672d3bc496e" />

---

## 项目结构

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json       # 插件清单
├── skills/
│   └── git-commit/
│       └── SKILL.md           # Git Commit 生成器
├── agents/
└── commands/
```

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

### 安装插件

```bash
claude plugin install git-commit@lovelyJason/claude-plugins

# REPL环境
/plugin install git-commit@lovelyJason/claude-plugins
```
