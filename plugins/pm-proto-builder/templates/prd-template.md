# {{SYSTEM_NAME}} 产品需求文档

## 1. 文档信息

| 属性 | 值 |
|-----|-----|
| 生成时间 | {{TIMESTAMP}} |
| 源系统地址 | {{SOURCE_URL}} |
| 页面数量 | {{PAGE_COUNT}} |
| 生成工具 | PM Proto Builder |

---

## 2. 系统概述

### 2.1 系统简介

{{SYSTEM_DESCRIPTION}}

### 2.2 功能架构

```
{{MENU_TREE}}
```

---

## 3. 菜单结构

{{MENU_STRUCTURE}}

---

## 4. 页面详情

{{PAGE_DETAILS}}

---

## 5. 数据字典

### 5.1 公共字段

| 字段名 | 类型 | 说明 |
|-------|-----|-----|
| id | number | 唯一标识 |
| createTime | datetime | 创建时间 |
| updateTime | datetime | 更新时间 |
| createBy | string | 创建人 |
| updateBy | string | 更新人 |

### 5.2 业务字段

{{DATA_DICTIONARY}}

---

## 6. 接口清单

{{API_LIST}}

---

## 7. 附录

### 7.1 截图目录

所有页面截图存放在 `screenshots/` 目录下。

### 7.2 原型项目

可运行的原型项目位于当前目录，启动方式：

```bash
npm install
npm run dev
```

---

> 本文档由 PM Proto Builder 自动生成，仅供需求演示和交互设计使用。
