<template>
  <h1>POSTMAN DOES NOT WORK IF YOU DONT HAVE INTERNET</h1>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axiosApi from '@/axios'
import FilterPanel from '@/components/forms/FilterPanel.vue'
import axios from 'axios'

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
  axiosApi.get('finance-management/test/')
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