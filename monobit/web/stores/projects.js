import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useProjectStore = defineStore('project', () => {
  const projectList = ref([])

  const setProjects = (projectList) => {
    projectList.value = projectList
  }

  return {
    projectList,
    setProjects,
  }
})
