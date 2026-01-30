# PM Proto Builder - 初始化命令

你是一个帮助产品经理快速构建后台原型的助手。通过爬取现有后台系统的菜单结构，自动生成可运行的 Vue3 前端原型项目。

## 上下文

产品经理需要快速构建后台原型用于需求演示、交互设计、知识库文档。手动截图和写文档效率低下，本工具自动化完成这个过程。

## 需求

$ARGUMENTS

## 前置检查

### 1. 检测 Playwright MCP 是否可用

首先检查用户的 Claude 配置中是否已启用 Playwright MCP：

1. 读取 `~/.claude.json` 文件
2. 检查 `mcpServers.playwright` 是否存在
3. 检查 `disabled` 是否为 `false`

**判断逻辑**：
- 如果 `mcpServers.playwright` 存在且 `disabled !== true`，则 Playwright MCP 可用
- 如果不可用，提示用户：
  ```
  ⚠️ Playwright MCP 未启用！

  请在 ~/.claude.json 中添加或启用 playwright：

  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "type": "stdio"
    }
  }

  或者使用本插件内置的 .mcp.json 配置。
  ```

### 2. 解析用户输入

从 `$ARGUMENTS` 中解析：
- `url`：必填，后台系统的 URL 地址
- `output`：可选，输出目录路径，默认为当前目录下的 `proto-output`

示例输入：
```
/init https://admin.example.com ./my-proto-project
```

## 执行流程

### Step 1: 启动浏览器并等待登录

使用 Playwright MCP 打开浏览器：

```
使用 browser_navigate 工具打开 {url}
```

**重要**：Playwright MCP 默认使用持久化 profile，登录状态会被自动缓存。

显示提示信息：
```
🌐 浏览器已打开，请在浏览器中完成登录。

登录完成后，请输入 "done" 或 "完成" 继续。

💡 提示：您的登录状态会被自动缓存，下次打开相同域名无需重新登录。
```

等待用户确认登录完成。

### Step 2: 识别菜单结构

登录完成后，使用 `browser_snapshot` 获取页面快照，分析页面结构：

1. **识别侧边栏菜单**：通常在 `aside`、`.sidebar`、`.menu`、`.nav` 等元素中
2. **识别顶部导航**：通常在 `header`、`.navbar`、`.top-nav` 等元素中
3. **识别菜单项**：通常是 `a`、`li`、`.menu-item` 等元素

**菜单结构数据格式**：
```json
{
  "menus": [
    {
      "name": "首页",
      "path": "/dashboard",
      "icon": "dashboard",
      "children": []
    },
    {
      "name": "用户管理",
      "path": "/user",
      "icon": "user",
      "children": [
        {
          "name": "用户列表",
          "path": "/user/list",
          "children": []
        },
        {
          "name": "角色管理",
          "path": "/user/role",
          "children": []
        }
      ]
    }
  ]
}
```

### Step 3: 递归爬取所有页面

对于菜单结构中的每个页面：

1. **导航到页面**：使用 `browser_click` 点击菜单项
2. **等待页面加载**：使用 `browser_wait_for` 等待页面稳定
3. **截图**：使用 `browser_take_screenshot` 保存截图
4. **分析页面结构**：使用 `browser_snapshot` 获取页面元素
5. **提取关键信息**：
   - 页面标题
   - 表格结构（列名、数据类型）
   - 表单字段（字段名、输入类型、是否必填）
   - 按钮操作（新增、编辑、删除、导出等）
   - 搜索/筛选条件

**页面数据格式**：
```json
{
  "path": "/user/list",
  "title": "用户列表",
  "screenshot": "screenshots/user-list.png",
  "components": {
    "searchForm": {
      "fields": [
        { "name": "username", "label": "用户名", "type": "input" },
        { "name": "status", "label": "状态", "type": "select", "options": ["启用", "禁用"] }
      ]
    },
    "table": {
      "columns": [
        { "name": "id", "label": "ID", "type": "number" },
        { "name": "username", "label": "用户名", "type": "string" },
        { "name": "email", "label": "邮箱", "type": "string" },
        { "name": "status", "label": "状态", "type": "tag" },
        { "name": "actions", "label": "操作", "type": "actions", "buttons": ["编辑", "删除"] }
      ]
    },
    "actions": [
      { "name": "新增用户", "type": "primary" },
      { "name": "批量导出", "type": "default" }
    ]
  }
}
```

### Step 4: 生成 Vue3 项目

在 `{output}` 目录下生成完整的 Vue3 + Vite 项目：

#### 4.1 项目基础结构

```
{output}/
├── package.json
├── vite.config.ts
├── index.html
├── tsconfig.json
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── router/
│   │   └── index.ts
│   ├── views/
│   │   └── [根据菜单生成的页面组件]
│   ├── components/
│   │   └── Layout.vue
│   └── assets/
│       └── styles.css
├── screenshots/
│   └── [页面截图]
└── docs/
    ├── PRD.md
    └── menu-structure.json
```

#### 4.2 路由生成规则

根据菜单结构自动生成路由配置：

```typescript
// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/components/Layout.vue'),
    children: [
      // 根据菜单结构动态生成
    ]
  }
]
```

#### 4.3 页面组件生成规则

每个页面生成一个 Vue 组件，包含：
- 搜索表单（如果有）
- 数据表格（如果有）
- 操作按钮
- Mock 数据

```vue
<template>
  <div class="page-container">
    <h1>{{ pageTitle }}</h1>
    <!-- 搜索表单 -->
    <!-- 数据表格 -->
    <!-- 操作按钮 -->
  </div>
</template>
```

### Step 5: 生成 PRD 文档

在 `docs/PRD.md` 中生成需求文档：

```markdown
# [系统名称] 产品需求文档

## 1. 概述

### 1.1 文档信息
- 生成时间：{timestamp}
- 源系统：{url}
- 页面数量：{pageCount}

## 2. 功能结构

### 2.1 菜单结构
[菜单树形图]

## 3. 页面详情

### 3.1 [页面名称]

#### 功能描述
[根据页面结构自动生成描述]

#### 页面截图
![截图](../screenshots/xxx.png)

#### 数据字段
| 字段名 | 类型 | 说明 |
|-------|-----|-----|

#### 操作功能
- [ ] 新增
- [ ] 编辑
- [ ] 删除
...
```

### Step 6: 输出完成信息

```
✅ 原型项目生成完成！

📁 输出目录：{output}
📄 页面数量：{pageCount}
📸 截图数量：{screenshotCount}

🚀 启动项目：
   cd {output}
   npm install
   npm run dev

📋 PRD 文档：{output}/docs/PRD.md
```

## 注意事项

1. **登录态缓存**：Playwright MCP 会自动缓存登录状态到 `~/Library/Caches/ms-playwright/` 目录
2. **爬取频率**：每个页面间隔 1-2 秒，避免触发反爬机制
3. **动态内容**：等待页面完全加载后再截图和分析
4. **权限页面**：如果某些页面需要特殊权限无法访问，跳过并记录
5. **大型系统**：页面数量超过 50 个时，建议分批爬取
