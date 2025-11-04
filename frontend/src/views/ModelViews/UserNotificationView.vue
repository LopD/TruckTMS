<template>
  <div class="container mt-5">
    <div class="box">
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <h1 class="title">My Notifications</h1>
          </div>
        </div>
        <div class="level-right">
          <div class="level-item">
            <div class="buttons">
              <button 
                class="button is-small"
                :class="{ 'is-primary': filterUnread, 'is-light': !filterUnread }"
                @click="toggleUnreadFilter"
              >
                <span class="icon is-small">
                  <i class="fas fa-envelope"></i>
                </span>
                <span>Unread Only</span>
              </button>
              <button 
                class="button is-small is-info"
                @click="markAllAsRead"
                :disabled="unreadCount === 0 || markingAll"
                :class="{ 'is-loading': markingAll }"
              >
                <span class="icon is-small">
                  <i class="fas fa-check-double"></i>
                </span>
                <span>Mark All as Read</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Filter Panel Component -->
      <FilterPanel
        :text-filters="[
          { key: 'text', label: 'Text', placeholder: 'Search by text...' }
        ]"
        :select-filters="[
          { 
            key: 'status', 
            label: 'Status', 
            options: [
              { value: 'SENT', label: 'Sent' },
              { value: 'NOT SENT', label: 'NOT Sent' },
              { value: 'ERROR', label: 'Error' }
            ]
          },
          { 
            key: 'type', 
            label: 'Type', 
            options: [
              { value: 'HINT', label: 'Hint' },
              { value: 'IMPORTANT', label: 'Important' },
              { value: 'INFO', label: 'Informative' },
              { value: 'ERROR', label: 'Error occurances' }
            ]
          }
        ]"
        :initial-filters="currentFilters"
        @filter-change="handleFilterChange"
      />

      <!-- Stats -->
      <div class="level mb-4">
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Total</p>
            <p class="title">{{ count }}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Unread</p>
            <p class="title has-text-danger">{{ unreadCount }}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Read</p>
            <p class="title has-text-success">{{ readCount }}</p>
          </div>
        </div>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="has-text-centered">
        <button class="button is-loading is-large is-ghost"></button>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="notification is-danger">
        <button class="delete" @click="error = null"></button>
        {{ error }}
      </div>

      <!-- Notifications List -->
      <div v-else-if="notifications.length > 0">
        <div 
          v-for="notification in notifications" 
          :key="notification.id"
          class="notification-item box mb-3"
          :class="{
            'is-unread': !notification.viewed_at,
            'is-read': notification.viewed_at
          }"
        >
          <div class="is-mobile"> <!-- class = "level is-mobile"-->
            <div class="level-left" style="flex: 1; min-width: 0;">
              <div class="level-item" style="flex-shrink: 0;">
                <span 
                  class="icon is-large"
                  :class="getTypeColor(notification.type)"
                >
                  <i class="fas fa-2x" :class="getTypeIcon(notification.type)"></i>
                </span>
              </div>
              <div class="level-item" style="flex: 1; min-width: 0;">
                <div style="width: 100%;">
                  <div class="level is-mobile mb-2">
                    <div class="level-left">
                      <span 
                        class="tag" 
                        :class="getTypeTagClass(notification.type)"
                      >
                        {{ notification.type }}
                      </span>
                      <!-- <span 
                        class="tag ml-2" 
                        :class="getStatusTagClass(notification.status)"
                      >
                        {{ notification.status }}
                      </span> -->
                      <span 
                        v-if="!notification.viewed_at" 
                        class="tag is-danger ml-2"
                      >
                        NEW
                      </span>
                    </div>
                    <div class="level-right">
                      <small class="has-text-grey">
                        {{ formatDateTime(notification.created_at) }}
                      </small>
                    </div>
                  </div>
                  <p class="notification-text">{{ notification.text }}</p>
                  <div v-if="notification.viewed_at" class="mt-2">
                    <small class="has-text-success">
                      <span class="icon is-small">
                        <i class="fas fa-check"></i>
                      </span>
                      Read {{ formatDateTime(notification.viewed_at) }}
                    </small>
                  </div>
                </div>
              </div>
            </div>
            <div class="level-right" style="flex-shrink: 0;">
              <button 
                v-if="!notification.viewed_at"
                class="button is-small is-success"
                @click="markAsRead(notification.id)"
                :disabled="markingRead[notification.id]"
                :class="{ 'is-loading': markingRead[notification.id] }"
              >
                <span class="icon is-small">
                  <i class="fas fa-check"></i>
                </span>
                <span>Mark as Read</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <nav class="pagination is-centered mt-5" role="navigation" aria-label="pagination">
          <button 
            class="pagination-previous" 
            :disabled="!previousUrl"
            @click="loadPage(previousUrl)"
          >
            Previous
          </button>
          <button 
            class="pagination-next"
            :disabled="!nextUrl"
            @click="loadPage(nextUrl)"
          >
            Next
          </button>
          <ul class="pagination-list">
            <li>
              <span class="pagination-link is-current">
                Page {{ currentPage }} ({{ count }} total items)
              </span>
            </li>
          </ul>
        </nav>
      </div>

      <!-- Empty State -->
      <div v-else class="notification is-info is-light">
        <p class="has-text-centered">
          <span class="icon is-large">
            <i class="fas fa-3x fa-bell-slash"></i>
          </span>
        </p>
        <p class="has-text-centered mt-3">
          {{ filterUnread ? 'No unread notifications' : 'No notifications found' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axiosApi from '@/axios'
import {getUserIdFromToken} from '@/JWTutils'
import FilterPanel from '@/components/forms/FilterPanel.vue'

const notifications = ref([])
const loading = ref(false)
const error = ref(null)
const count = ref(0)
const nextUrl = ref(null)
const previousUrl = ref(null)
const currentPage = ref(1)
const filterUnread = ref(false)
const markingRead = ref({})
const markingAll = ref(false)
const currentUserId = ref(null)
const currentFilters = ref({})

const buildQueryString = (filters) => {
  const params = new URLSearchParams()
  
  for (const [key, value] of Object.entries(filters)) {
    if (value !== '' && value !== null && value !== undefined) {
      params.append(key, value)
    }
  }
  
  return params.toString() ? `?${params.toString()}` : ''
}

function mapResponseToValues(response) {
  notifications.value = response.data.results
  count.value = response.data.count
  nextUrl.value = response.data.next
  previousUrl.value = response.data.previous
}

function updateCurrentPage(url) {
  if (url.includes('page=')) {
      const match = url.match(/page=(\d+)/)
      currentPage.value = match ? parseInt(match[1]) : 1
    } else {
      currentPage.value = 1
    }
}

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.viewed_at).length
})

const readCount = computed(() => {
  return notifications.value.filter(n => n.viewed_at).length
})


const fetchNotifications = async (filters = {}) => {
  loading.value = true
  error.value = null
  
  try {
    const userId = currentUserId.value || getUserIdFromToken()
    
    if (!userId) {
      error.value = 'Unable to get user ID from token'
      return
    }
    
    currentUserId.value = userId
    
    let queryString = buildQueryString(filters)
    if (queryString ) {
      queryString = `${queryString}&ordering=-created_at&userprofile=${userId}`
    }
    else {
      queryString = `?ordering=-created_at&userprofile=${userId}`
    }
    if (filterUnread.value) {
      queryString += '&viewed_at__isnull=true'
    }

    const url = `/notification-management/user-notification/${queryString}`
    // let fetchUrl = url || `/notification-management/user-notification/?ordering=-created_at&userprofile=${userId}`
    // if (!url && filterUnread.value) {
    //   fetchUrl += '&viewed_at__isnull=true'
    // }
    // const response = await axiosApi.get(fetchUrl)
    
    const response = await axiosApi.get(url)
    mapResponseToValues(response)
    
    updateCurrentPage(url)
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load notifications'
    console.error('Error fetching notifications:', err)
  } finally {
    loading.value = false
  }
}

const handleFilterChange = (filters) => {
  currentFilters.value = filters
  fetchNotifications(filters)
}

const markNotificationAsRead = async (notificationId, userId) => {
  axiosApi.patch(`/notification-management/user-notification/${notificationId}/`, {
    viewed_at: new Date().toISOString(),
    userprofile: userId
  })
}

const markAsRead = async (notificationId) => {
  markingRead.value[notificationId] = true
  
  try {
    await markNotificationAsRead(notificationId, currentUserId.value)
    
    // Update local state
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.viewed_at = new Date().toISOString()
    }
    
    // Decrement the unread count in store
    store.dispatch('usernotifications/decrementUnreadCount')
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to mark notification as read'
    console.error('Error marking notification as read:', err)
  } finally {
    markingRead.value[notificationId] = false
  }
}

const markAllAsRead = async () => {
  markingAll.value = true
  
  try {
    const unreadNotifications = notifications.value.filter(n => !n.viewed_at)
    const updatePromises = unreadNotifications.map(n => 
      // axiosApi.patch(`/notification-management/user-notification/${n.id}/`, {
      //   viewed_at: new Date().toISOString()
      // })
      // axiosApi.put(`/notification-management/user-notification/${n.id}/`, {
      //   viewed_at: new Date().toISOString(),
      //   userpofile: currentUserId
      // })
      markNotificationAsRead(n.id,currentUserId.value)
    )
    
    await Promise.all(updatePromises)
    
    // Refresh notifications
    await fetchNotifications()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to mark all notifications as read'
    console.error('Error marking all as read:', err)
  } finally {
    markingAll.value = false
  }
}

const toggleUnreadFilter = () => {
  filterUnread.value = !filterUnread.value
  fetchNotifications()
}

const loadPage = (url) => {
  if (url) {
    fetchNotifications(url)
  }
}

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  // Less than 1 minute
  if (diff < 60000) {
    return 'Just now'
  }
  // Less than 1 hour
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000)
    return `${minutes} minute${minutes > 1 ? 's' : ''} ago`
  }
  // Less than 24 hours
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours} hour${hours > 1 ? 's' : ''} ago`
  }
  // Less than 7 days
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000)
    return `${days} day${days > 1 ? 's' : ''} ago`
  }
  
  return date.toLocaleString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getTypeIcon = (type) => {
  const iconMap = {
    'HINT': 'fa-lightbulb',
    'IMPORTANT': 'fa-exclamation-circle',
    'INFO': 'fa-info-circle',
    'ERROR': 'fa-times-circle'
  }
  return iconMap[type] || 'fa-bell'
}

const getTypeColor = (type) => {
  const colorMap = {
    'HINT': 'has-text-warning',
    'IMPORTANT': 'has-text-danger',
    'INFO': 'has-text-info',
    'ERROR': 'has-text-danger'
  }
  return colorMap[type] || 'has-text-grey'
}

const getTypeTagClass = (type) => {
  const classMap = {
    'HINT': 'is-warning',
    'IMPORTANT': 'is-danger',
    'INFO': 'is-info',
    'ERROR': 'is-danger'
  }
  return classMap[type] || 'is-light'
}

const getStatusTagClass = (status) => {
  const classMap = {
    'SENT': 'is-success',
    'NOT SENT': 'is-warning',
    'ERROR': 'is-danger'
  }
  return classMap[status] || 'is-light'
}

onMounted(() => {
  fetchNotifications()
})
</script>

<style scoped>
.notification-item {
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
}

.notification-item.is-unread {
  background-color: #fffbeb;
  border-left-color: #f59e0b;
}

.notification-item.is-read {
  background-color: #f5f5f5;
  border-left-color: #48c78e;
}

.notification-item:hover {
  box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1), 0 0 0 1px rgba(10, 10, 10, 0.02);
  transform: translateY(-2px);
}

.notification-text {
  font-size: 1rem;
  line-height: 1.5;
  word-wrap: break-word;
}

@media screen and (max-width: 768px) {
  .level-right {
    margin-top: 1rem;
  }
}
</style>