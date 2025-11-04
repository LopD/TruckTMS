<template>
  <div class="container mt-5">
    <div class="box">
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <h1 class="title">Financial Records Management</h1>
          </div>
        </div>
        <div class="level-right">
          <div class="level-item">
            <div class="dropdown" :class="{ 'is-active': showDropdown }">
              <div class="dropdown-trigger" hidden="true">
                <button 
                  class="button is-success" 
                  @click="showDropdown = !showDropdown"
                >
                  <span class="icon">
                    <i class="fas fa-plus"></i>
                  </span>
                  <span>New Record</span>
                  <span class="icon is-small">
                    <i class="fas fa-angle-down"></i>
                  </span>
                </button>
              </div>
              <div class="dropdown-menu">
                <div class="dropdown-content">
                  <a 
                    class="dropdown-item" 
                    @click="goToForm('SalaryInvoice')"
                  >
                    <span class="icon">
                      <i class="fas fa-money-bill-wave"></i>
                    </span>
                    <span>Salary Invoice</span>
                  </a>
                  <a 
                    class="dropdown-item" 
                    @click="goToForm('MembershipInvoice')"
                  >
                    <span class="icon">
                      <i class="fas fa-user-check"></i>
                    </span>
                    <span>Membership Invoice</span>
                  </a>
                  <a 
                    class="dropdown-item" 
                    @click="goToForm('MaintenanceInvoice')"
                  >
                    <span class="icon">
                      <i class="fas fa-tools"></i>
                    </span>
                    <span>Maintenance Invoice</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filter Panel Component -->
      <FilterPanel
        :text-filters="[
          { key: 'name', label: 'Name', placeholder: 'Search by hall name...' }
        ]"
        :number-filters="[
          { key: 'transaction_amount', label: 'Transaction amount' }
        ]"
        :date-time-filters="[
          { key: 'start_date', label: 'Start date' }
        ]"
        :select-filters="[
          { 
            key: 'record_type', 
            label: 'Invoice Type', 
            options: [
              { value: 'SalaryInvoice', label: 'Salary Invoice' },
              { value: 'MaintenanceInvoice', label: 'Maintenance Invoice' },
              { value: 'MembershipInvoice', label: 'Membership Invoice' }
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
      <div v-else-if="records.length > 0" class="table-container">
        <table class="table is-fullwidth is-striped is-hoverable">
          <thead>
            <tr>
              <th>ID</th>
              <th>Record Type</th>
              <th>Transaction Amount</th>
              <th>Details</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in records" :key="record.id">
              <td>{{ record.id }}</td>
              <td>
                <span 
                  class="tag" 
                  :class="{
                    'is-info': record.record_type === 'SalaryInvoice',
                    'is-success': record.record_type === 'MembershipInvoice',
                    'is-warning': record.record_type === 'MaintenanceInvoice'
                  }"
                >
                  {{ formatRecordType(record.record_type) }}
                </span>
              </td>
              <td>
                <span 
                  class="tag" 
                  :class="{
                    'is-danger': parseFloat(record.transaction_amount) < 0,
                    'is-success': parseFloat(record.transaction_amount) >= 0
                  }"
                >
                  {{ formatAmount(record.transaction_amount) }}
                </span>
              </td>
              <td>
                <span class="is-size-7">{{ getRecordDetails(record) }}</span>
              </td>
              <td>{{ formatDateTime(record.created_at) }}</td>
              <td>
                <button 
                  class="button is-small is-info"
                  @click="goToEditForm(record)"
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
        No financial records found.
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
const records = ref([])
const loading = ref(false)
const error = ref(null)
const count = ref(0)
const nextUrl = ref(null)
const previousUrl = ref(null)
const currentPage = ref(1)
const showDropdown = ref(false)
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
  records.value = response.data.results
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

const fetchRecords = async (filters = {}) => {
  loading.value = true
  error.value = null
  
  try {
    const queryString = buildQueryString(filters)
    const url = `/finance-management/financial-record/${queryString}`
    const response = await axiosApi.get(url)
    mapResponseToValues(response)
    
    updateCurrentPage(url)
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load financial records'
    console.error('Error fetching records:', err)
  } finally {
    loading.value = false
  }
}

const handleFilterChange = (filters) => {
  currentFilters.value = filters
  fetchRecords(filters)
}

const formatRecordType = (type) => {
  const typeMap = {
    'SalaryInvoice': 'Salary Invoice',
    'MembershipInvoice': 'Membership Invoice',
    'MaintenanceInvoice': 'Maintenance Invoice'
  }
  return typeMap[type] || type
}

const formatAmount = (amount) => {
  const value = parseFloat(amount)
  return `$${Math.abs(value).toFixed(2)}`
}

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getRecordDetails = (record) => {
  if (record.record_type === 'SalaryInvoice' && record.record_value) {
    return `UserProfile: ${record.record_value.userprofile}`
  } else if (record.record_type === 'MembershipInvoice' && record.record_value) {
    return `Membership: ${record.record_value.membership}`
  } else if (record.record_type === 'MaintenanceInvoice' && record.record_value) {
    return `Maintenance Report: ${record.record_value.maintenancereport}`
  }
  return 'N/A'
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
        error.value = err.response?.data?.message || 'Failed to load financial records'
        console.error('Error fetching financial records:', err)
      })
      .finally(() => {
        loading.value = false
      })
 
    fetchRecords(url)
  }
}

const goToForm = (recordType) => {
  showDropdown.value = false
  router.push({ name: 'financial-record-create', params: { type: recordType } })
}

const goToEditForm = (record) => {
  router.push({ 
    name: 'financial-record-edit', 
    params: { type: record.record_type, id: record.id } 
  })
}

onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.table-container {
  overflow-x: auto;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>