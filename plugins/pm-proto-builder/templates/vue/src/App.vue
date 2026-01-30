<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// 菜单数据 - 由爬虫自动生成
const menuData = ref([
  // {{MENU_DATA}}
])

const route = useRoute()
const router = useRouter()
const isCollapse = ref(false)

const activeMenu = computed(() => route.path)

const handleMenuSelect = (path) => {
  if (path) router.push(path)
}
</script>

<template>
  <el-container style="height: 100vh">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '200px'" style="background: #001529">
      <div style="height: 60px; line-height: 60px; text-align: center; color: #fff; font-size: 18px">
        {{ isCollapse ? 'P' : '{{PROJECT_TITLE}}' }}
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        background-color="#001529"
        text-color="#fff"
        active-text-color="#1890ff"
        @select="handleMenuSelect"
      >
        <template v-for="item in menuData" :key="item.path || item.name">
          <el-sub-menu v-if="item.children?.length" :index="item.name">
            <template #title>{{ item.name }}</template>
            <el-menu-item v-for="child in item.children" :key="child.path" :index="child.path">
              {{ child.name }}
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item v-else :index="item.path">{{ item.name }}</el-menu-item>
        </template>
      </el-menu>
    </el-aside>

    <!-- 主区域 -->
    <el-container>
      <el-header style="background: #fff; display: flex; align-items: center; box-shadow: 0 1px 4px rgba(0,21,41,.08)">
        <el-icon style="cursor: pointer; font-size: 20px" @click="isCollapse = !isCollapse">
          <component :is="isCollapse ? 'Expand' : 'Fold'" />
        </el-icon>
      </el-header>
      <el-main style="background: #f0f2f5; padding: 20px">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
.el-menu { border-right: none; }
</style>
