---
name: secret-scan
description: 扫描代码中的硬编码密钥、API Key、数据库密码等敏感信息。触发场景：(1) 用户说"检查敏感信息"、"扫描密钥"、"安全检查" (2) 用户运行 /secret-scan (3) 用户问"代码里有没有泄露密码" (4) 代码审查时检查安全风险
---

# Secret Scan - 密钥扫描器

扫描代码库中硬编码的敏感信息，防止密钥泄露到版本控制系统。

## 扫描目标

### 1. API Keys & Tokens

| 类型 | 正则模式 | 示例 |
|------|---------|------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | AKIAIOSFODNN7EXAMPLE |
| AWS Secret Key | `[0-9a-zA-Z/+]{40}` | wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY |
| GitHub Token | `gh[pousr]_[A-Za-z0-9_]{36,}` | ghp_xxxxxxxxxxxx |
| GitLab Token | `glpat-[A-Za-z0-9\-]{20,}` | glpat-xxxxxxxxxxxx |
| Slack Token | `xox[baprs]-[0-9a-zA-Z-]+` | xoxb-xxxx-xxxx |
| Stripe Key | `sk_live_[0-9a-zA-Z]{24,}` | sk_live_xxxxxxxxxxxx |
| Google API Key | `AIza[0-9A-Za-z\-_]{35}` | AIzaSyxxxxxxxxxxxxxxxxx |
| OpenAI API Key | `sk-[A-Za-z0-9]{48,}` | sk-xxxxxxxxxxxx |
| 微信 AppSecret | `[0-9a-f]{32}` (上下文含 wechat/weixin) | 32位十六进制 |
| 阿里云 AccessKey | `LTAI[A-Za-z0-9]{12,}` | LTAIxxxxxxxxxxxx |
| 腾讯云 SecretId | `AKID[A-Za-z0-9]{32}` | AKIDxxxxxxxxxxxx |

### 2. 数据库凭证

| 类型 | 模式特征 |
|------|---------|
| MySQL | `mysql://user:password@host` |
| PostgreSQL | `postgres://user:password@host` |
| MongoDB | `mongodb://user:password@host` 或 `mongodb+srv://` |
| Redis | `redis://:password@host` |

### 3. 私钥文件

| 类型 | 特征 |
|------|------|
| RSA 私钥 | `-----BEGIN RSA PRIVATE KEY-----` |
| DSA 私钥 | `-----BEGIN DSA PRIVATE KEY-----` |
| EC 私钥 | `-----BEGIN EC PRIVATE KEY-----` |
| OpenSSH 私钥 | `-----BEGIN OPENSSH PRIVATE KEY-----` |
| PGP 私钥 | `-----BEGIN PGP PRIVATE KEY BLOCK-----` |

### 4. 其他敏感信息

| 类型 | 模式 |
|------|------|
| JWT Token | `eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*` |
| Basic Auth | `Basic [A-Za-z0-9+/=]{10,}` |
| Bearer Token | `Bearer [A-Za-z0-9_\-\.]+` |
| 密码变量 | `password\s*[=:]\s*['"][^'"]+['"]` |
| Secret 变量 | `secret\s*[=:]\s*['"][^'"]+['"]` |

## 执行流程

### Step 1: 确定扫描范围

询问用户或使用默认：
- 默认扫描当前目录
- 可指定特定目录或文件
- 可排除 node_modules、.git、dist 等

### Step 2: 执行扫描

使用 Grep 工具扫描以下模式：

```bash
# AWS Key
grep -rn "AKIA[0-9A-Z]{16}" --include="*.{js,ts,jsx,tsx,vue,py,go,java,rb,php,env,json,yaml,yml,xml,conf,config}"

# GitHub Token
grep -rn "gh[pousr]_[A-Za-z0-9_]{36,}" ...

# 数据库连接串
grep -rn "(mysql|postgres|mongodb|redis)://[^:]+:[^@]+@" ...

# 私钥文件
grep -rn "BEGIN.*PRIVATE KEY" ...

# 通用密码模式
grep -rn "(password|passwd|pwd|secret|token|api_key|apikey)\s*[=:]\s*['\"][^'\"]+['\"]" ...
```

### Step 3: 过滤误报

排除以下情况：
- `.example`、`.sample`、`.template` 文件
- 注释中的示例
- 测试文件中的 mock 数据
- `xxx`、`your-key-here`、`placeholder` 等占位符
- 环境变量引用 `process.env.XXX`

### Step 4: 生成报告

```markdown
# 🔐 密钥扫描报告

## 扫描信息
- 扫描时间：{timestamp}
- 扫描目录：{path}
- 扫描文件数：{fileCount}

## ⚠️ 发现的敏感信息

### 🔴 高危（需立即处理）

| 文件 | 行号 | 类型 | 内容摘要 |
|-----|-----|------|---------|
| src/config.js | 12 | AWS Secret Key | `wJalrXUtn...` (已脱敏) |
| .env.production | 5 | 数据库密码 | `password=...` |

### 🟡 中危（建议处理）

| 文件 | 行号 | 类型 | 内容摘要 |
|-----|-----|------|---------|
| src/api.ts | 45 | 硬编码 Token | `Bearer xxx...` |

### 🟢 低危/待确认

| 文件 | 行号 | 类型 | 说明 |
|-----|-----|------|-----|
| test/mock.js | 10 | Mock API Key | 测试文件，可能是 mock 数据 |

## 💡 修复建议

### 1. 移除已泄露的密钥
如果密钥已经提交到 Git 历史，需要：
1. **立即轮换密钥**（在云服务商后台生成新密钥）
2. 使用 git-filter-repo 清除历史
   ```bash
   pip install git-filter-repo
   git filter-repo --invert-paths --path 敏感文件路径
   ```

### 2. 使用环境变量
```javascript
// ❌ 错误
const API_KEY = 'sk-xxxxxxxxxxxx'

// ✅ 正确
const API_KEY = process.env.API_KEY
```

### 3. 添加 .gitignore
确保以下文件被忽略：
```gitignore
.env
.env.local
.env.*.local
*.pem
*.key
config/secrets.json
```

### 4. 使用 pre-commit 钩子
安装 detect-secrets 预防未来泄露：
```bash
pip install detect-secrets
detect-secrets scan > .secrets.baseline
```

添加 pre-commit 配置：
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```
```

## 严重程度定义

| 级别 | 定义 | 示例 |
|-----|------|------|
| 🔴 高危 | 直接暴露可用密钥，可能导致资金损失或数据泄露 | AWS Key、数据库密码、支付密钥 |
| 🟡 中危 | 暴露内部服务凭证，需配合其他信息才能利用 | 内部 API Token、测试环境密码 |
| 🟢 低危 | 可能是误报，或仅在特定条件下有风险 | 测试 Mock、示例代码、已过期密钥 |

## 扫描排除规则

默认排除以下路径：
- `node_modules/`
- `.git/`
- `dist/`
- `build/`
- `vendor/`
- `*.min.js`
- `*.bundle.js`
- `package-lock.json`
- `yarn.lock`
- `pnpm-lock.yaml`

## 常见误报处理

### 1. 环境变量引用
```javascript
// 不是泄露，是正确用法
const key = process.env.API_KEY
```

### 2. 类型定义
```typescript
// 不是泄露，是类型声明
interface Config {
  apiKey: string
  secretKey: string
}
```

### 3. 文档示例
```markdown
<!-- 不是泄露，是文档示例 -->
API_KEY=your-api-key-here
```

### 4. 测试 Mock
```javascript
// 低风险，但建议使用明显的假数据
const mockKey = 'test-api-key-12345'
```

## 注意事项

1. **扫描后立即处理**：发现泄露后，第一时间轮换密钥
2. **检查 Git 历史**：即使当前代码没有，历史提交可能有
3. **定期扫描**：建议在 CI 中集成自动扫描
4. **团队培训**：确保团队成员了解密钥管理最佳实践
