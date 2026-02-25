---
name: git-merge-flow
description: 自动化分支合并流水线，将特性分支代码依次合并到开发分支和测试分支，冲突时自动调用 git-conflict-resolver 插件处理。触发场景：(1) 用户说"合并到测试分支"、"提测"、"合代码" (2) 用户运行 /git-merge-flow (3) 用户说"把代码合到 dev"、"合并分支"
---

# Git Merge Flow - 分支合并流水线

自动化将特性分支代码依次合并到开发分支、测试分支，处理冲突并推送，最后切回特性分支。

## 执行流程

### Step 1: 环境检查

确认当前目录是 Git 仓库且有远程仓库：

```bash
git rev-parse --is-inside-work-tree
git remote -v
```

- 不是 Git 仓库 → 告知用户并退出
- 没有远程仓库 → 警告用户，询问是否继续（本地合并不推送）

### Step 2: 判断当前分支是否为特性分支

```bash
git branch --show-current
```

**非特性分支黑名单**（命中任一则拒绝执行）：

| 分支名模式 | 说明 |
|-----------|------|
| `main`, `master` | 主分支 |
| `dev`, `develop`, `development` | 开发分支 |
| `test`, `testing` | 测试分支 |
| `stage`, `staging`, `pre`, `preview` | 预发布分支 |
| `prod`, `production` | 生产分支 |
| `release`, `release/*` | 发布分支 |
| `hotfix/*` | 热修复分支 |

判断逻辑：
1. 精确匹配上述分支名（不区分大小写）
2. `release/*` 和 `hotfix/*` 使用前缀匹配

**命中黑名单**：告知用户当前不是特性分支，请先切换到特性分支再执行：
```
当前分支 dev 不是特性分支，无法执行合并流水线。
请先切换到你的特性分支（如 feature/xxx、fix/xxx），再运行此命令。
```

### Step 3: 检查工作区是否干净

```bash
git status --porcelain
```

如果有未提交的变更，使用 AskUserQuestion 询问：

```
AskUserQuestion({
  questions: [{
    question: "工作区有未提交的变更，需要先处理才能切换分支。如何处理？",
    header: "工作区",
    options: [
      { label: "自动 stash", description: "执行 git stash，合并完成后自动 pop 恢复" },
      { label: "我自己处理", description: "退出流水线，你手动 commit 或 stash 后再来" }
    ],
    multiSelect: false
  }]
})
```

- 选择 stash → 执行 `git stash push -m "git-merge-flow auto stash"` 并记住需要在最后恢复
- 选择自己处理 → 退出

### Step 4: 自动检测仓库中的开发/测试分支

检测远程分支，确定实际存在的开发分支和测试分支：

```bash
git fetch --all --prune
git branch -r
```

**开发分支候选**（按优先级）：`dev`, `develop`, `development`
**测试分支候选**（按优先级）：`test`, `testing`, `stage`, `staging`

从远程分支列表中匹配，取第一个存在的。如果都不存在则标记为"未检测到"。

### Step 5: 询问合并策略

根据检测到的分支构造选项。假设检测到开发分支为 `dev`，测试分支为 `test`，当前特性分支为 `feature/auth`：

```
AskUserQuestion({
  questions: [{
    question: "选择合并策略（当前分支：feature/auth）：",
    header: "合并策略",
    options: [
      { label: "feature/auth → dev → test（推荐）", description: "完整流水线：合并到开发分支，再从开发分支合并到测试分支" },
      { label: "feature/auth → dev", description: "仅合并到开发分支" },
      { label: "feature/auth → test", description: "仅合并到测试分支" }
    ],
    multiSelect: false
  }]
})
```

**动态构造选项**：
- 如果只检测到开发分支，不展示含测试分支的选项
- 如果只检测到测试分支，不展示含开发分支的选项
- 如果都没检测到，只提供"自定义目标分支"选项（用户在 Other 中输入）
- 用户选 Other 时，解析输入的分支名作为目标

### Step 6: 执行合并流程

记录当前特性分支名，用于最后切回：

```bash
FEATURE_BRANCH=$(git branch --show-current)
```

#### 6a. 合并特性分支到开发分支

```bash
git checkout dev
git pull origin dev
git merge $FEATURE_BRANCH --no-edit
```

**检查合并结果**：

```bash
# 检查是否有冲突
git diff --name-only --diff-filter=U
```

- **无冲突**：合并成功，告知用户，继续下一步
- **有冲突**：进入冲突处理流程（见 Step 7）

#### 6b. 合并开发分支到测试分支（如果策略包含此步）

```bash
git checkout test
git pull origin test
git merge dev --no-edit
```

同上检查冲突。

#### 6c. 推送

合并完成后推送：

```bash
git push origin dev
git push origin test
```

如果 Step 1 检测到没有远程仓库，跳过推送。

#### 6d. 切回特性分支

```bash
git checkout $FEATURE_BRANCH
```

如果 Step 3 执行了 stash，恢复：

```bash
git stash pop
```

### Step 7: 冲突处理

当合并产生冲突时：

**检测 git-conflict-resolver 插件是否安装**：

```bash
SCRIPT=$(find ~/.claude -name "parse_conflicts.py" -path "*/git-conflict-resolver/*" 2>/dev/null | head -1)
```

如果找不到，尝试在项目目录查找：

```bash
SCRIPT=$(find . -name "parse_conflicts.py" -path "*/git-conflict-resolver/*" 2>/dev/null | head -1)
```

**已安装插件**（SCRIPT 不为空）：

告知用户检测到冲突，将调用 git-conflict-resolver 处理：
```
合并 feature/auth 到 dev 时产生了冲突，检测到已安装 git-conflict-resolver 插件，正在调用冲突解决...
```

然后执行 resolve 命令的完整流程：
1. 运行 `python3 $SCRIPT` 获取结构化 JSON
2. 按照 conflict-resolver agent 的工作流程处理冲突（展示概览 → 逐文件处理 → git add → 完成）
3. 冲突全部解决后，执行 `git commit --no-edit` 完成合并提交
4. 继续流水线的下一步

**注意**：resolve 流程中 agent 最后会询问是否执行 `git merge --continue`，在此场景下应该执行它来完成合并。

**未安装插件**（SCRIPT 为空）：

```
合并 feature/auth 到 dev 时产生了冲突。

未检测到 git-conflict-resolver 插件，请手动解决冲突：
1. 查看冲突文件：git diff --name-only --diff-filter=U
2. 手动编辑解决冲突
3. git add <resolved-files>
4. git merge --continue

当前停留在 dev 分支，冲突解决完成后可重新运行此命令继续。

💡 推荐安装 git-conflict-resolver 插件，自动智能解决合并冲突。
```

退出流水线（不切回特性分支，因为用户需要在当前分支解决冲突）。

### Step 8: 汇总报告

全部完成后输出：

```markdown
# 合并流水线完成

## 执行结果
- ✅ feature/auth → dev（无冲突 / N 个冲突已解决）
- ✅ dev → test（无冲突 / N 个冲突已解决）
- ✅ 已推送 dev、test 到远程
- ✅ 已切回 feature/auth

## 提醒
- 如需查看合并结果：git log --oneline --graph dev..test
- 如需回滚：git checkout dev && git reset --hard HEAD~1
```

## 注意事项

1. **合并用 `--no-edit`**：自动接受默认合并信息，不弹编辑器
2. **pull 前先 fetch**：确保拿到最新远程分支
3. **冲突中断时不切分支**：冲突未解决时停留在当前分支，不要切回特性分支
4. **stash 恢复**：只有在全部流程成功完成后才 pop stash，冲突中断时不恢复
5. **推送顺序**：先推送开发分支，再推送测试分支
6. **分支不存在时**：如果本地没有目标分支，用 `git checkout -b dev origin/dev` 创建本地追踪分支
7. **合并策略是 merge 不是 rebase**：使用 `git merge` 保留完整的合并历史
