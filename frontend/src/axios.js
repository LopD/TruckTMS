/**
 * Handles Adding tokens to requests and refreshing tokens when they expire.
*/


import axios from 'axios'

// Create an instance
const axiosApi = axios.create({
  // baseURL: axios.defaults.baseURL, // Django backend URL is set in main.js
  baseURL: 'http://localhost:8000', // Django backend URL is set in main.js
  headers: {
    // 'Content-Type': 'application/json', // do not set he content type as you may send other forms of content, let axios figure it out
  }
})

// Attach access token if available
axiosApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Auto refresh access token on 401
axiosApi.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Prevent infinite loop
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh_token')

      if (refreshToken) {
        try {
          //'http://localhost:8000/api/token/refresh/'
          const res = await axios.post('/api/token/refresh/', {
            refresh: refreshToken,
          })

          const newAccess = res.data.access
          localStorage.setItem('access_token', newAccess)
          axiosApi.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`
          originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
          return axiosApi(originalRequest)
        } catch (refreshError) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          return Promise.reject(refreshError)
        }
      }
    }

    return Promise.reject(error)
  }
)

export default axiosApi
