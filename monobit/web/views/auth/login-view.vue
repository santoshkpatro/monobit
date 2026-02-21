<template>
  <div class="login-wrapper">
    <a-card class="login-card" :bordered="false">
      <div class="header">
        <lock-outlined class="icon" />
        <h2>Login</h2>
      </div>

      <a-form layout="vertical" :model="form" @finish="onFinish" hideRequiredMark>
        <a-form-item
          name="email"
          label="Email"
          :rules="[{ required: true, message: 'Please enter your email' }]"
        >
          <a-input v-model:value="form.email" placeholder="Enter email">
            <template #prefix>
              <user-outlined />
            </template>
          </a-input>
        </a-form-item>

        <a-form-item
          name="password"
          label="Password"
          :rules="[{ required: true, message: 'Please enter your password' }]"
        >
          <a-input-password v-model:value="form.password" placeholder="Enter password">
            <template #prefix>
              <lock-outlined />
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-button type="primary" block html-type="submit"> Login </a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup>
import { LockOutlined, UserOutlined } from '@ant-design/icons-vue'
import { reactive } from 'vue'

const form = reactive({
  email: '',
  password: '',
})

const onFinish = () => {
  console.log('Form submitted:', form)
}
</script>

<style scoped>
.login-wrapper {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
}

.login-card {
  width: 360px;
}

.header {
  text-align: center;
  margin-bottom: 24px;
}

.icon {
  font-size: 28px;
  margin-bottom: 8px;
  color: #1677ff;
}

h2 {
  margin: 0;
  font-weight: 500;
}
</style>
