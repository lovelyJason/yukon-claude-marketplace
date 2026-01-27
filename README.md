# My Claude Plugins

个人 Claude Code 插件和技能集合。

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

## 插件列表

| 插件 | 说明 | 分类 |
|------|------|------|
| git-commit | 根据 Git 暂存区变更自动生成符合 Angular 规范的 commit message | productivity |

## 安装使用

### 方式一：CLI

```bash
claude plugin marketplace add lovelyJason/claude-plugins
```

### 方式二：Claude REPL

```
/plugin marketplace add lovelyJason/claude-plugins
```

### 安装插件

```bash
claude plugin install git-commit@lovelyJason/claude-plugins

# REPL环境
/plugin install git-commit@lovelyJason/claude-plugins
```
