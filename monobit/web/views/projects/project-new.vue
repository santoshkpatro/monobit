<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import { projectCreateAPI } from '@/api'
import { useProjectStore } from '@/stores/projects'
import { useRouter } from 'vue-router'

const router = useRouter()
const projectStore = useProjectStore()
const loading = ref(false)

const formState = ref({
  name: '',
  description: '',
  applicationUrl: '',
})

const rules = {
  name: [
    { required: true, message: 'Project name is required' },
    { min: 3, message: 'Minimum 3 characters' },
  ],
  applicationUrl: [
    {
      validator: (_, value) => {
        if (!value) return Promise.resolve() // allow empty
        const urlPattern = /^(https?:\/\/)[^\s$.?#].[^\s]*$/gm
        return urlPattern.test(value) ? Promise.resolve() : Promise.reject('Must be a valid URL')
      },
      trigger: 'blur',
    },
  ],
}

const formRef = ref()

const submit = async () => {
  try {
    await formRef.value.validate()
  } catch {
    return
  }

  loading.value = true

  const payload = {
    ...formState.value,
    description: formState.value.description || null,
    applicationUrl: formState.value.applicationUrl || null,
  }

  try {
    const { data } = await projectCreateAPI(payload)
    projectStore.addProject(data)

    message.success('Project created successfully')

    formState.value = {
      name: '',
      description: '',
      applicationUrl: '',
    }

    router.push({ name: 'project-onboarding', params: { projectId: data.id } })
  } catch (error) {
    message.error('Failed to create project', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="wrapper">
    <div class="card">
      <h2>Create New Project</h2>

      <a-form ref="formRef" :model="formState" :rules="rules" layout="vertical">
        <a-form-item label="Project Name" name="name">
          <a-input v-model:value="formState.name" placeholder="My Awesome App" />
        </a-form-item>

        <a-form-item label="Description" name="description">
          <a-textarea
            v-model:value="formState.description"
            :rows="3"
            placeholder="Optional description"
          />
        </a-form-item>

        <a-form-item label="Application URL (optional)" name="applicationUrl">
          <a-input v-model:value="formState.applicationUrl" placeholder="https://example.com" />
        </a-form-item>

        <a-form-item>
          <a-button type="primary" block :loading="loading" @click="submit">
            Create Project
          </a-button>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  height: 100vh;
  background: #f7f8fa;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px;
}

.card {
  width: 420px;
  background: #ffffff;
  padding: 36px;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
}

h2 {
  margin-bottom: 24px;
  font-weight: 600;
  letter-spacing: -0.4px;
}
</style>
