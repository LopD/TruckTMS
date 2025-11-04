<template>
  <div class="dashboard-container">
    <aside class="menu sidebar">
      <p class="menu-label">Navigation</p>
      
      <ul class="menu-list">
        <li 
          v-for="route in allowedRoutes"
          :key="route.name"
          >
          <router-link
            :to="`/logged-in/${route.path}`"
            active-class="is-active"
          >
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            {{ formatTitle(route.name) }}
            <span 
              v-if="route.name === 'user-notification' && unreadCount > 0" 
              class="tag is-danger is-rounded notification-badge"
            >
              {{ unreadCount }}
            </span>
          </router-link>
        </li>
      </ul>
      
      <!-- <ul class="menu-list">
        <li>
          <router-link to="/logged-in/logged-in-home" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            HOME
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/hall" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Halls
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/training-equipment" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Training equipment
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/tender" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Tenders
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/supplier" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Suppliers
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/maintainer" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Maintainers
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/maintenance-appointment" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Maintenance appointments
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/financial-record" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Finance records
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/user-notification" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Notifications
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/maintenance-request" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Maintenance requests
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/membership-type" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Membership types
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/membership" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Memberships
          </router-link>
        </li>
        <li>
          <router-link to="/logged-in/financial-report" active-class="is-active">
            <span class="icon"><i class="fas fa-chart-line"></i></span>
            Financial reports
          </router-link>
        </li>
        
      </ul> -->
      <p class="menu-label">Account</p>
      <ul class="menu-list">
        <li>
          <a @click="logout">
            <span class="icon"><i class="fas fa-sign-out-alt"></i></span>
            Logout
          </a>
        </li>
      </ul>
    </aside>
    
    <main class="main-content">
      
      <div class="content-area">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
// import router from '@/router'
import { getUserGroupsFromToken } from '@/JWTutils'
import { useStore } from 'vuex'
import { computed, onMounted, onBeforeUnmount } from 'vue'

const router = useRouter()
const store = useStore()
const userGroups = getUserGroupsFromToken() || []
const unreadCount = computed(() => store.getters['usernotifications/unreadCount'])

const logout = () => {
  // localStorage.removeItem('isLoggedIn')
  router.push('/')
}

// find the parent /logged-in route
const loggedInRoute = router.options.routes
  .find(r => r.path === '/logged-in')

// compute allowed child routes
const allowedRoutes = computed(() => {
  if (!loggedInRoute?.children) return []
  return loggedInRoute.children.filter(route => {
    if (route.meta !== null && route.meta !== undefined && route.meta.isInNavBar == false) return false

    const allowedGroups = route.meta?.groups
    if (!allowedGroups) return true // visible to everyone
    return allowedGroups.some(g => userGroups.includes(g))
  })
})

// 
function capitalizeFirstLetter(val) {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
}
const formatTitle = (name) => capitalizeFirstLetter(name.replaceAll('-', ' '))

// Fetch notifications on mount and set up polling
let intervalId = null
const userNotificationsFetchTimeout = 30000 // every 30 seconds check if a new user notification appeared
onMounted(() => {
  store.dispatch('usernotifications/fetchUnreadCount')
  // Refresh every 30 seconds
  intervalId = setInterval(() => {
    store.dispatch('usernotifications/fetchUnreadCount')
  }, userNotificationsFetchTimeout) 
})

// Clean up interval on unmount
onBeforeUnmount(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})



</script>

<style scoped>
.dashboard-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 250px;
  /* background-color: #f5f5f5; */
  padding: 1.5rem;
  border-right: 1px solid #dbdbdb;
  overflow-y: auto;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.menu-list a {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.menu-list a.is-active {
  background-color: #3273dc;
  color: white;
}

.notification-badge {
  margin-left: 8px;
  font-size: 0.75rem;
  min-width: 20px;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
</style>