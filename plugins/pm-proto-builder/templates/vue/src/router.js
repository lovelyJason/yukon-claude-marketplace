import { createRouter, createWebHistory } from 'vue-router'

// 页面组件 - 由爬虫自动生成
// {{ROUTE_IMPORTS}}

const routes = [
  { path: '/', redirect: '/dashboard' },
  // {{ROUTES}}
]

export default createRouter({
  history: createWebHistory(),
  routes
})
