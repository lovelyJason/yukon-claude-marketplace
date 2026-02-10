---
name: ai-editor-setup
description: 配置 AI 编辑器相关的 gitignore 规则、清理已提交的敏感文件、设置 shell 权限。触发场景：(1) 用户说"配置 AI 编辑器"、"忽略 claude 配置" (2) 用户运行 /ai-editor-setup (3) 用户问"怎么忽略 .cursor 目录"
---

# AI Editor Setup - AI 编辑器配置助手

一键配置 AI 编辑器相关的 gitignore 规则、清理已提交的敏感文件、设置编辑器权限。

## 功能概述

1. **添加 gitignore 规则**：将 AI 编辑器的配置目录/文件加入 .gitignore
2. **清理已提交文件**：如果这些文件已被 git 追踪，从仓库中删除（保留本地）
3. **配置 shell 权限**：询问用户是否配置编辑器的 shell 命令权限

## 忽略策略

**核心原则**：只忽略**本地缓存和敏感配置文件**，保留**团队共享的 commands、skills、rules**。

### 应该忽略的（本地缓存/敏感配置）

| 编辑器 | 需忽略的文件 | 原因 |
|-------|-------------|------|
| Claude Code | `.claude/settings.local.json`<br>`.claude/todos.local.json`<br>`.claude/plugins/`<br>`.claude/statsig/` | 本地权限配置、插件缓存 |
| Cursor | `.cursor/index/`<br>`.cursor/cache/`<br>`.cursor/logs/`<br>`.cursor/mcp.json` | 索引缓存、日志、MCP 本地配置 |
| Windsurf | `.windsurf/cache/`<br>`.windsurf/logs/` | 缓存和日志 |
| Aider | `.aider.chat.history.md`<br>`.aider.input.history`<br>`.aider.tags.cache.v3/` | 聊天历史、缓存 |

### 不应该忽略的（团队共享）

| 文件 | 用途 | 建议 |
|-----|------|------|
| `.cursorrules` | Cursor AI 行为规则 | 团队共享 |
| `.cursor/rules/` | Cursor 规则目录 | 团队共享 |
| `.cursor/commands/` | Cursor 自定义命令 | 团队共享 |
| `.windsurfrules` | Windsurf AI 行为规则 | 团队共享 |
| `.windsurf/rules/` | Windsurf 规则目录 | 团队共享 |
| `.claude/commands/` | Claude Code 自定义命令 | 团队共享 |
| `.claude/settings.json` | Claude Code 项目级配置 | 团队共享（注意不是 settings.local.json） |
| `CLAUDE.md` | Claude Code 项目说明 | 团队共享 |
| `.clinerules` | Cline AI 行为规则 | 团队共享 |
| `.github/copilot-instructions.md` | Copilot 指令 | 团队共享 |
| `.aider.conf.yml` | Aider 项目配置 | 团队共享 |

## 执行流程

### Step 1: 检测当前目录

确认当前目录是 Git 仓库：

```bash
git rev-parse --is-inside-work-tree
```

如果不是 Git 仓库，提示用户并退出。

### Step 2: 扫描已存在的 AI 编辑器配置

检测当前项目中存在哪些 AI 编辑器的配置：

```bash
# 检测存在的 AI 编辑器配置
ls -la | grep -E "^\.(claude|cursor|windsurf|copilot|cline|aider|continue|gemini|agent|amazonq|q|augment|codex|junie|cody|tabnine|supermaven)" 2>/dev/null

# 检测单独的规则文件
ls -la | grep -E "^\.(cursorrules|cursorignore|windsurfrules|clinerules|aiderignore|continuerules)" 2>/dev/null
```

### Step 3: 一次性询问用户

使用 AskUserQuestion 一次性收集信息：

```
AskUserQuestion({
  questions: [
    {
      question: "需要忽略哪些 AI 编辑器的配置？",
      header: "选择编辑器",
      options: [
        { label: "全部（推荐）", description: "忽略所有常见 AI 编辑器配置" },
        { label: "仅已检测到的", description: "只忽略当前项目中存在的配置" },
        { label: "自定义选择", description: "在 Other 中列出需要忽略的编辑器" }
      ],
      multiSelect: false
    },
    {
      question: "如果这些文件已被 git 追踪，是否从仓库中删除？（本地文件会保留）",
      header: "清理已追踪文件",
      options: [
        { label: "是，删除已追踪的", description: "执行 git rm --cached 移除追踪" },
        { label: "否，只改 gitignore", description: "仅添加忽略规则，不处理已追踪文件" }
      ],
      multiSelect: false
    },
    {
      question: "是否配置 Claude Code 的 shell 命令权限？（允许所有 bash 命令）",
      header: "Shell 权限",
      options: [
        { label: "是，允许所有命令", description: "在 .claude/settings.local.json 添加 allow 规则" },
        { label: "否，跳过", description: "不修改权限配置" }
      ],
      multiSelect: false
    }
  ]
})
```

### Step 4: 更新 .gitignore

根据用户选择，添加对应的忽略规则。

**关键**：只忽略**缓存、日志、本地敏感配置**，保留 commands/、rules/、skills/ 等团队共享目录！

```bash
# AI 编辑器 gitignore 规则（只忽略缓存和本地敏感配置）
cat >> .gitignore << 'EOF'

# ===== AI Editors (本地缓存/敏感配置，不提交) =====

# Claude Code - 只忽略本地配置，保留 commands/、settings.json、CLAUDE.md
.claude/settings.local.json
.claude/todos.local.json
.claude/plugins/
.claude/statsig/

# Cursor - 只忽略缓存和日志，保留 rules/、commands/
.cursor/index/
.cursor/cache/
.cursor/logs/
.cursor/mcp.json

# Windsurf - 只忽略缓存和日志，保留 rules/
.windsurf/cache/
.windsurf/logs/

# Aider - 忽略聊天历史和缓存，保留 .aider.conf.yml
.aider.chat.history.md
.aider.input.history
.aider.tags.cache.v3/
EOF
```

**不要忽略这些团队共享文件**：
- `.cursorrules`、`.cursor/rules/`、`.cursor/commands/`
- `.windsurfrules`、`.windsurf/rules/`
- `.claude/commands/`、`.claude/settings.json`、`CLAUDE.md`
- `.clinerules`、`.github/copilot-instructions.md`
- `.aider.conf.yml`

**注意**：添加前先检查 .gitignore 是否已包含这些规则，避免重复。

### Step 5: 清理已追踪文件（如果用户选择）

如果用户选择清理已追踪的文件：

**关键**：只清理缓存和本地敏感配置，不清理 commands/、rules/ 等团队共享目录！

```bash
# 检查哪些缓存/本地配置已被追踪
git ls-files | grep -E "^\.claude/(settings\.local\.json|todos\.local\.json|plugins/|statsig/)"
git ls-files | grep -E "^\.cursor/(index/|cache/|logs/|mcp\.json)"
git ls-files | grep -E "^\.windsurf/(cache/|logs/)"
git ls-files | grep -E "^\.aider\.(chat\.history|input\.history|tags\.cache)"
```

**执行策略**：一次 Bash 调用完成所有清理

```bash
# 获取所有已追踪的缓存/本地配置文件（保留 commands/、rules/ 等共享目录）
TRACKED_FILES=$(git ls-files | grep -E "(\.claude/(settings\.local\.json|todos\.local\.json|plugins/|statsig/)|\.cursor/(index/|cache/|logs/|mcp\.json)|\.windsurf/(cache/|logs/)|\.aider\.(chat\.history|input\.history|tags\.cache))")

if [ -n "$TRACKED_FILES" ]; then
  echo "$TRACKED_FILES" | xargs git rm --cached -r
  echo "已从 git 追踪中移除以下文件："
  echo "$TRACKED_FILES"
else
  echo "没有需要清理的已追踪文件"
fi
```

**不会被清理的文件**（团队共享）：
- `.cursorrules`、`.cursor/rules/`、`.cursor/commands/`
- `.windsurfrules`、`.windsurf/rules/`
- `.claude/commands/`、`.claude/settings.json`
- `CLAUDE.md`、`.clinerules`
- `.github/copilot-instructions.md`
- `.aider.conf.yml`

### Step 6: 配置 Shell 权限（如果用户选择）

如果用户选择配置 Claude Code 的 shell 权限：

#### 6.1 检查/创建配置文件

```bash
mkdir -p .claude
```

#### 6.2 更新 settings.local.json

读取现有配置（如果存在），添加 allow 规则：

```json
{
  "permissions": {
    "allow": [
      "Bash(*)"
    ]
  }
}
```

如果已有配置，需要合并而不是覆盖：

```javascript
// 伪代码逻辑
const existing = readJSON('.claude/settings.local.json') || {}
existing.permissions = existing.permissions || {}
existing.permissions.allow = existing.permissions.allow || []

if (!existing.permissions.allow.includes('Bash(*)')) {
  existing.permissions.allow.push('Bash(*)')
}

writeJSON('.claude/settings.local.json', existing)
```

### Step 7: 提交变更（可选）

询问用户是否提交这些变更：

```
完成配置！变更如下：
- .gitignore: 添加了 AI 编辑器忽略规则
- 已从 git 追踪移除 X 个文件/目录
- .claude/settings.local.json: 已配置 shell 权限

是否提交这些变更？
```

## 输出示例

```markdown
# AI 编辑器配置完成

## 已添加 .gitignore 规则
- .claude/
- .cursor/
- .windsurf/
- ... (共 15 条规则)

## 已从 Git 追踪移除
- .claude/settings.local.json
- .cursor/rules

## Shell 权限配置
- .claude/settings.local.json 已添加 `Bash(*)` 权限

---
建议执行 `git status` 确认变更，然后提交。
```

## 注意事项

1. **只忽略本地配置**：不要忽略团队共享的规则文件（如 `.cursorrules`、`.claude/commands/`）
2. **安全提醒**：`settings.local.json` 可能包含 API Key 等敏感信息，务必忽略
3. **权限风险**：`Bash(*)` 允许所有命令，请确保了解风险
4. **保留本地**：`git rm --cached` 只移除追踪，不删除本地文件

## 常见问题

### Q: 为什么 .claude/settings.local.json 需要忽略？
A: 这个文件包含本地的权限配置，每个开发者的设置可能不同，不应该提交到仓库。

### Q: .cursorrules / .windsurfrules 应该忽略吗？
A: **不应该忽略**。这些是团队共享的 AI 行为规则，应该提交到仓库让团队成员共享。

### Q: .claude/commands/ 应该忽略吗？
A: **不应该忽略**。自定义命令是团队共享的，应该提交到仓库。

### Q: 已经提交到远程仓库的本地配置怎么办？
A: 执行本技能后，需要 push 到远程。其他人 pull 后，这些文件会从仓库消失，但如果他们本地有同名文件，不会被删除。
