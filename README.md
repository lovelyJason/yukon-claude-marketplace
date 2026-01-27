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

### 方式三：借助本作者的另一客户端软件,通过界面添加

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
