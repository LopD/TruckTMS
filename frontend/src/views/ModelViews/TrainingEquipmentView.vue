<template>
  <div class="container mt-5">
    <div class="box">
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <h1 class="title">Training Equipment Management</h1>
          </div>
        </div>
        <div class="level-right">
          <div class="level-item">
            <button class="button is-primary" @click="goToForm()">
              <span class="icon">
                <i class="fas fa-plus"></i>
              </span>
              <span>New Equipment</span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Filter Panel Component -->
      <FilterPanel
        :text-filters="[
          { key: 'name', label: 'Name', placeholder: 'Search by name...' },
          { key: 'hall_name', label: 'Hall name', placeholder: 'Search by hall name...' }
        ]"
        :select-filters="[
          { 
            key: 'status', 
            label: 'Status', 
            options: [
              { value: 'ACTIVE', label: 'Active' },
              { value: 'NOT ACTIVE', label: 'NOT Active' },
              { value: 'NOT USABLE', label: 'Not Usable' }
            ]
          }
        ]"
        :initial-filters="currentFilters"
        @filter-change="handleFilterChange"
      />

      <!-- Loading State -->
      <div v-if="loading" class="has-text-centered">
        <button class="button is-loading is-large is-ghost"></button>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="notification is-danger">
        <button class="delete" @click="error = null"></button>
        {{ error }}
      </div>

      <!-- Table -->
      <div v-else-if="equipment.length > 0" class="table-container">
        <table class="table is-fullwidth is-striped is-hoverable">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Status</th>
              <th>Hall</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in equipment" :key="item.id">
              <td>{{ item.id }}</td>
              <td>{{ item.name }}</td>
              <td>
                <span 
                  class="tag" 
                  :class="{
                    'is-success': item.status === 'ACTIVE',
                    'is-warning': item.status === 'NOT ACTIVE',
                    'is-danger': item.status === 'NOT USABLE'
                  }"
                >
                  {{ item.status }}
                </span>
              </td>
              <td>{{ getHallName(item.hall) }}</td>
              <td>
                <button 
                  class="button is-small is-info"
                  @click="goToForm(item.id)"
                >
                  <span class="icon is-small">
                    <i class="fas fa-edit"></i>
                  </span>
                  <span>Edit</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <nav class="pagination is-centered" role="navigation" aria-label="pagination">
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
        No training equipment found.
      </div>
    </div>
  </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axiosApi from '@/axios'
import FilterPanel from '@/components/forms/FilterPanel.vue'

const router = useRouter()
const equipment = ref([])
const halls = ref({})
const loading = ref(false)
const error = ref(null)
const count = ref(0)
const nextUrl = ref(null)
const previousUrl = ref(null)
const currentPage = ref(1)
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
  equipment.value = response.data.results
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


const fetchEquipment = async (filters = {}) => {
  loading.value = true
  error.value = null
  
  try {
    const queryString = buildQueryString(filters)
    const url = `/inventory-management/training-equipment/${queryString}`
    
    const response = await axiosApi.get(url)
    mapResponseToValues(response)
    
    updateCurrentPage(url)

    // Fetch hall names for display
    await fetchHallNames()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load training equipment'
    console.error('Error fetching equipment:', err)
  } finally {
    loading.value = false
  }
}

const handleFilterChange = (filters) => {
  currentFilters.value = filters
  fetchEquipment(filters)
}

const fetchHallNames = async () => {
  try {
    const response = await axiosApi.get('/inventory-management/hall/?page_size=10')
    response.data.results.forEach(hall => {
      halls.value[hall.id] = hall.name
    })
  } catch (err) {
    console.error('Error fetching hall names:', err)
  }
}

const getHallName = (hallId) => {
  return halls.value[hallId] || `Hall #${hallId}`
}

const loadPage = (url) => {
  if (url) {
    loading.value = true
    error.value = null

    axiosApi.get(url)
      .then(response => {
        mapResponseToValues(response)
        
        updateCurrentPage(url)
      })
      .catch(err => {
        error.value = err.response?.data?.message || 'Failed to load training equipment'
        console.error('Error fetching training equipment:', err)
      })
      .finally(() => {
        loading.value = false
      })
  }
}

const goToForm = (id = null) => {
  if (id) {
    router.push({ name: 'training-equipment-edit', params: { id } })
  } else {
    router.push({ name: 'training-equipment-create' })
  }
}

onMounted(() => {
  fetchEquipment()
})
</script>

<style scoped>
.table-container {
  overflow-x: auto;
}
</style>