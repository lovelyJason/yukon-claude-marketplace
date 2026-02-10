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

## 支持的 AI 编辑器

| 编辑器 | 配置路径 | 说明 |
|-------|---------|------|
| Claude Code | `.claude/` | 包含 settings.local.json 等本地配置 |
| Cursor | `.cursor/` `.cursorignore` `.cursorindexingignore` `.cursorrules` | AI 代码编辑器 |
| Windsurf | `.windsurf/` `.windsurfrules` | Codeium 的 AI 编辑器 |
| GitHub Copilot | `.copilot/` `.github/copilot-instructions.md` | GitHub 官方 AI 助手 |
| Cline | `.cline/` `.clinerules` `.clineignore` | VS Code AI 插件 |
| Aider | `.aider*` `.aiderignore` | 终端 AI 编程工具 |
| Continue | `.continue/` `.continuerules` `.continueignore` | 开源 AI 编程助手 |
| Gemini | `.gemini/` | Google AI 编辑器 |
| Agent | `.agent/` | 通用 AI Agent 配置 |
| Amazon Q | `.amazonq/` `.q/` | AWS AI 编程助手 |
| Augment | `.augment/` `.augmentignore` | Augment Code AI |
| Codex | `.codex/` | OpenAI Codex 配置 |
| JetBrains AI | `.junie/` | JetBrains IDE AI 功能 |
| Sourcegraph Cody | `.cody/` | Sourcegraph AI 助手 |
| Tabnine | `.tabnine/` | AI 代码补全工具 |
| Supermaven | `.supermaven/` | AI 代码补全工具 |

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

根据用户选择，添加对应的忽略规则：

```bash
# 完整的 AI 编辑器 gitignore 规则
cat >> .gitignore << 'EOF'

# ===== AI Editors =====
# Claude Code
.claude/

# Cursor
.cursor/
.cursorrules
.cursorignore
.cursorindexingignore

# Windsurf
.windsurf/
.windsurfrules

# GitHub Copilot
.copilot/
.github/copilot-instructions.md

# Cline
.cline/
.clinerules
.clineignore

# Aider
.aider*
.aiderignore

# Continue
.continue/
.continuerules
.continueignore

# Google Gemini
.gemini/

# Generic Agent
.agent/

# Amazon Q
.amazonq/
.q/

# Augment
.augment/
.augmentignore

# OpenAI Codex
.codex/

# JetBrains Junie
.junie/

# Sourcegraph Cody
.cody/

# Tabnine
.tabnine/

# Supermaven
.supermaven/
EOF
```

**注意**：添加前先检查 .gitignore 是否已包含这些规则，避免重复。

### Step 5: 清理已追踪文件（如果用户选择）

如果用户选择清理已追踪的文件：

```bash
# 检查哪些 AI 编辑器文件已被追踪
git ls-files | grep -E "^\.(claude|cursor|windsurf|copilot|cline|aider|continue|gemini|agent|amazonq|q|augment|codex|junie|cody|tabnine|supermaven)"

# 从 git 中移除追踪（保留本地文件）
git rm -r --cached .claude/ .cursor/ .windsurf/ 2>/dev/null
# ... 对所有已追踪的目录执行
```

**执行策略**：一次 Bash 调用完成所有清理

```bash
# 获取所有已追踪的 AI 编辑器文件，然后一次性移除
TRACKED_FILES=$(git ls-files | grep -E "^\.(claude|cursor|windsurf|copilot|cline|aider|continue|gemini|agent|amazonq|q|augment|codex|junie|cody|tabnine|supermaven|cursorrules|cursorignore|windsurfrules|clinerules|aiderignore|continuerules)")

if [ -n "$TRACKED_FILES" ]; then
  echo "$TRACKED_FILES" | xargs git rm --cached -r
  echo "已从 git 追踪中移除以下文件："
  echo "$TRACKED_FILES"
else
  echo "没有需要清理的已追踪文件"
fi
```

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

1. **安全提醒**：settings.local.json 可能包含 API Key 等敏感信息，务必忽略
2. **团队共享**：.cursorrules/.windsurfrules 等规则文件是否需要共享取决于团队约定
3. **权限风险**：`Bash(*)` 允许所有命令，请确保了解风险
4. **保留本地**：`git rm --cached` 只移除追踪，不删除本地文件

## 常见问题

### Q: 为什么 .claude/settings.local.json 需要忽略？
A: 这个文件包含本地的权限配置，每个开发者的设置可能不同，不应该提交到仓库。

### Q: 规则文件（如 .cursorrules）应该忽略吗？
A: 取决于团队：
- 如果是个人习惯配置 → 忽略
- 如果是团队共享的 AI 提示规范 → 不忽略，但建议用 CLAUDE.md 等标准文件代替

### Q: 已经提交到远程仓库的文件怎么办？
A: 执行本技能后，需要 push 到远程。其他人 pull 后，这些文件会从仓库消失，但如果他们本地有同名文件，不会被删除。
