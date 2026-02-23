<template>
  <a-layout class="dashboard">
    <a-layout-sider width="230" theme="light" class="sider">
      <div class="sider-inner">
        <div>
          <div class="company-block">
            <span class="company-name">{{ config.organizationName }}</span>
          </div>

          <div class="profile-block">
            <a-avatar size="large" src="https://i.pravatar.cc/100" />
            <div class="profile-meta">
              <div class="profile-name">{{ user.fullName }}</div>
              <div class="profile-email">{{ user.emailAddress }}</div>
            </div>
          </div>

          <a-menu mode="inline" :default-selected-keys="['issues']" class="menu">
            <a-menu-item key="issues"><BugOutlined />Issues</a-menu-item>
            <a-menu-item key="projects"><ProjectOutlined />Projects</a-menu-item>
            <a-menu-item key="settings"><SettingOutlined />Settings</a-menu-item>
            <a-menu-item key="analytics"><LineChartOutlined />Analytics</a-menu-item>
            <a-menu-item key="notifications"><BellOutlined />Notifications</a-menu-item>
            <a-menu-item key="system"><DatabaseOutlined />System</a-menu-item>
          </a-menu>
        </div>

        <div class="bottom-menu">
          <a-divider />
          <a-menu mode="inline" selectable="false" class="menu">
            <a-menu-item key="github"><StarOutlined />Star Us on Github</a-menu-item>
            <a-menu-item key="help"><CustomerServiceOutlined />Help & Support</a-menu-item>
            <a-menu-item key="docs"><BookOutlined />Docs</a-menu-item>
          </a-menu>
        </div>
      </div>
    </a-layout-sider>

    <a-layout>
      <a-layout-header class="header">
        <div class="header-title">Dashboard</div>
      </a-layout-header>

      <a-layout-content class="content">
        <router-view></router-view>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup>
import { projectListAPI } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { useConfigStore } from '@/stores/config'
import { useProjectStore } from '@/stores/projects'
import {
  BugOutlined,
  ProjectOutlined,
  SettingOutlined,
  LineChartOutlined,
  BellOutlined,
  DatabaseOutlined,
  StarOutlined,
  CustomerServiceOutlined,
  BookOutlined,
} from '@ant-design/icons-vue'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

// const stats = [
//   { title: 'Open Issues', value: '128' },
//   { title: 'Active Projects', value: '12' },
//   { title: 'System Health', value: '98%' },
//   { title: 'New Notifications', value: '7' },
// ]

const router = useRouter()

const configStore = useConfigStore()
const authStore = useAuthStore()
const projectStore = useProjectStore()

const { config } = storeToRefs(configStore)
const { user } = storeToRefs(authStore)

const loadProjects = async () => {
  try {
    const { data } = await projectListAPI()
    if (data.length == 0) {
      router.push({ name: 'project-new' })
      return
    }
    projectStore.setProjects(data)
  } catch (error) {
    console.log(error)
  }
}

onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f6f8fb;
}

.sider {
  border-right: 1px solid #edf1f5;
  background: #fff;
}

.sider-inner {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.company-block {
  height: 44px;
  display: flex;
  align-items: center;
  padding: 0 14px;
  border-bottom: 1px solid #f0f0f0;
}

.company-name {
  font-weight: 600;
}

.profile-block {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 10px 14px;
  border-bottom: 1px solid #f0f0f0;
}

.profile-meta {
  line-height: 1.2;
}

.profile-name {
  font-weight: 600;
  font-size: 13px;
}

.profile-email {
  font-size: 11px;
  color: #8c8c8c;
}

.menu {
  border-right: none !important;
}

.menu :deep(.ant-menu-item) {
  height: 34px !important;
  line-height: 34px !important;
  padding: 0 14px !important;
  margin: 3px 8px !important;
  border-radius: 6px;
}

.menu :deep(.ant-menu-item .anticon) {
  font-size: 14px;
  margin-right: 8px;
}

.menu :deep(.ant-menu-item:hover) {
  background: #f5f7fa;
}

.menu :deep(.ant-menu-item-selected) {
  background: #e6f4ff !important;
  color: #1677ff !important;
}

.menu :deep(.ant-divider) {
  margin: 8px 12px;
}

.header {
  height: 42px;
  padding: 0 18px;
  background: #fff;
  border-bottom: 1px solid #edf1f5;
  display: flex;
  align-items: center;
}

.header-title {
  font-weight: 600;
  font-size: 13px;
}

.content {
  padding: 14px 18px;
}

.stat-card {
  border-radius: 8px;
  border: 1px solid #edf1f7;
  padding: 10px !important;
}

.stat-label {
  font-size: 11px;
  color: #8c8c8c;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  margin-top: 2px;
}

.main-card {
  margin-top: 14px;
  border-radius: 8px;
  border: 1px solid #edf1f7;
}
</style>
