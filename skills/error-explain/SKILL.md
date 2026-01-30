---
name: error-explain
description: 解析报错堆栈，定位问题根因并给出修复建议。触发场景：(1) 用户粘贴报错信息 (2) 用户说"这个报错什么意思"、"帮我看看这个错误" (3) 用户运行 /error-explain
---

# Error Explain - 报错解析助手

解析各类报错堆栈，定位问题根因，给出具体修复建议和示例代码。

## 支持的错误类型

### JavaScript/TypeScript
- 语法错误（SyntaxError）
- 类型错误（TypeError）
- 引用错误（ReferenceError）
- 范围错误（RangeError）
- 编译错误（TSC errors）
- ESLint/Prettier 错误

### Node.js
- 模块找不到（MODULE_NOT_FOUND）
- 权限错误（EACCES、EPERM）
- 端口占用（EADDRINUSE）
- 内存溢出（ENOMEM、heap out of memory）
- 文件系统错误（ENOENT、EEXIST）

### 前端框架
- Vue：组件渲染错误、响应式警告、生命周期错误
- React：Hooks 规则违反、渲染错误、Hydration 不匹配
- Nuxt：SSR 错误、路由错误、插件错误
- Next.js：构建错误、API 路由错误、Image 组件错误

### 构建工具
- Webpack：模块解析、loader 配置、chunk 分割
- Vite：依赖预构建、HMR 失败、配置错误
- Rollup：Tree-shaking 问题、external 配置

### 小程序
- 微信小程序：API 调用错误、组件错误、网络请求错误
- uniapp：条件编译错误、平台兼容性问题

### 数据库/后端
- MySQL/PostgreSQL：SQL 语法、连接错误、约束冲突
- MongoDB：查询错误、索引问题
- Redis：连接超时、内存限制

### 网络请求
- CORS 跨域错误
- SSL/TLS 证书错误
- 超时错误
- HTTP 状态码错误（4xx、5xx）

## 分析流程

```
1. 识别错误类型和来源
2. 解析堆栈信息，定位出错文件和行号
3. 分析错误上下文和可能原因
4. 给出具体修复方案
5. 提供预防措施和最佳实践
```

## 输出格式

### 🔴 错误概述
简明描述错误含义，一句话说清问题本质。

### 📍 定位信息
- **出错文件**：具体文件路径和行号
- **错误类型**：错误分类
- **触发场景**：什么操作导致的

### 🔍 原因分析
列出可能的原因，按概率排序：
1. 最可能的原因（80%）
2. 次可能的原因（15%）
3. 其他可能（5%）

### ✅ 修复方案

**方案一（推荐）**
```javascript
// 修复前
问题代码

// 修复后
正确代码
```

**方案二（备选）**
如有其他解决思路，一并给出。

### 🛡️ 预防措施
- 如何避免同类问题再次发生
- 相关的 ESLint 规则或 TypeScript 配置
- 推荐的最佳实践

## 示例

### 示例 1：TypeError

**用户输入：**
```
TypeError: Cannot read properties of undefined (reading 'map')
    at UserList (src/components/UserList.vue:15:23)
```

**输出：**

#### 🔴 错误概述
尝试对 `undefined` 值调用 `map` 方法，说明数据未正确初始化或异步数据未返回。

#### 📍 定位信息
- **出错文件**：`src/components/UserList.vue` 第 15 行
- **错误类型**：TypeError - 类型错误
- **触发场景**：组件渲染时访问未定义的数组

#### 🔍 原因分析
1. **数据初始值为 undefined**（80%）：响应式数据声明时未设置默认值
2. **异步数据未就绪**（15%）：接口返回前就尝试渲染
3. **接口返回格式错误**（5%）：后端返回的不是数组

#### ✅ 修复方案

**方案一：设置默认值（推荐）**
```javascript
// 修复前
const users = ref()

// 修复后
const users = ref([])
```

**方案二：添加空值保护**
```vue
<template>
  <div v-if="users?.length">
    <div v-for="user in users" :key="user.id">{{ user.name }}</div>
  </div>
</template>
```

#### 🛡️ 预防措施
- 始终为数组类型的响应式数据设置 `[]` 默认值
- 使用 TypeScript 强制类型声明：`const users = ref<User[]>([])`
- 添加 loading 状态，数据未就绪时显示骨架屏

---

### 示例 2：CORS 错误

**用户输入：**
```
Access to fetch at 'https://api.example.com/users' from origin 'http://localhost:3000'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present.
```

**输出：**

#### 🔴 错误概述
浏览器阻止了跨域请求，服务端未配置 CORS 响应头。

#### 📍 定位信息
- **请求地址**：`https://api.example.com/users`
- **请求来源**：`http://localhost:3000`
- **错误类型**：CORS Policy 违规

#### 🔍 原因分析
1. **后端未配置 CORS**（70%）：服务端缺少 Access-Control-Allow-Origin 头
2. **配置了但不匹配**（20%）：允许的 origin 不包含当前域名
3. **预检请求失败**（10%）：OPTIONS 请求未正确处理

#### ✅ 修复方案

**方案一：后端配置 CORS（推荐）**

Node.js/Express：
```javascript
const cors = require('cors')
app.use(cors({
  origin: ['http://localhost:3000'],
  credentials: true
}))
```

**方案二：开发环境代理**

Vite 配置：
```javascript
// vite.config.js
export default {
  server: {
    proxy: {
      '/api': {
        target: 'https://api.example.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
}
```

#### 🛡️ 预防措施
- 开发环境统一使用代理，避免跨域
- 生产环境确保同源或正确配置 CORS
- 敏感接口使用 `credentials: true` 时需配合 `Access-Control-Allow-Credentials`

## 执行步骤

1. 接收用户粘贴的报错信息
2. 识别错误类型（JavaScript/Node/框架/构建工具等）
3. 解析堆栈，提取关键信息（文件、行号、错误消息）
4. 如需要，读取相关源码文件获取上下文
5. 分析可能原因并排序
6. 给出具体修复代码示例
7. 补充预防措施和最佳实践

## 注意事项

- 如果报错信息不完整，主动询问用户补充
- 如果涉及具体业务代码，请求用户提供相关文件
- 对于模糊的错误，列出多种可能并说明排查方法
- 始终提供可直接复制使用的代码示例
