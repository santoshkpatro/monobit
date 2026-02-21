// http.js
import axios from 'axios'
import camelcaseKeys from 'camelcase-keys'
import snakecaseKeys from 'snakecase-keys'

// Deep convert to camelCase
const toCamel = (data) => camelcaseKeys(data, { deep: true })

// Deep convert to snake_case
const toSnake = (data) => snakecaseKeys(data, { deep: true })

const isFormData = (val) => val instanceof FormData

const http = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

http.interceptors.request.use((config) => {
  if (config.data && !isFormData(config.data)) {
    config.data = toSnake(config.data)
  }

  if (config.params) {
    config.params = toSnake(config.params)
  }

  return config
})

http.interceptors.response.use((response) => {
  if (response.data) {
    response.data = toCamel(response.data)
  }

  return response
})

export const configAPI = () => http.get('/config')
export const authStatusAPI = () => http.get('/auth/me')
