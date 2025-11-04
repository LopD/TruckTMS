<template>
  <div class="box mb-4">
    <div class="level mb-3">
      <div class="level-left">
        <div class="level-item">
          <h2 class="subtitle is-5 mb-0">
            <span class="icon-text">
              <span class="icon">
                <i class="fas fa-filter"></i>
              </span>
              <span>Filters</span>
            </span>
          </h2>
        </div>
      </div>
      <div class="level-right">
        <div class="level-item">
          <button 
            class="button is-small" 
            :class="{ 'is-primary': showFilters, 'is-light': !showFilters }"
            @click="showFilters = !showFilters"
          >
            <span class="icon is-small">
              <i :class="showFilters ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
            </span>
            <span>{{ showFilters ? 'Hide' : 'Show' }} Filters</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="showFilters" class="filter-content">
      <div class="columns is-multiline">
        <!-- Text Filters -->
        <div 
          v-for="filter in textFilters" 
          :key="filter.key"
          class="column is-half-tablet is-one-third-desktop"
        >
          <div class="field">
            <label class="label is-small">{{ filter.label }}</label>
            <div class="control">
              <input 
                class="input is-small" 
                type="text" 
                :placeholder="filter.placeholder || `Search ${filter.label.toLowerCase()}...`"
                v-model="localFilters[filter.key]"
                @input="debouncedApplyFilters"
              >
            </div>
          </div>
        </div>

        <!-- Number Filters -->
        <div 
          v-for="filter in numberFilters" 
          :key="filter.key"
          class="column is-half-tablet is-one-third-desktop"
        >
          <div class="field">
            <label class="label is-small">{{ filter.label }}</label>
            <div class="field has-addons">
              <div class="control is-expanded">
                <input 
                  class="input is-small" 
                  type="number" 
                  :placeholder="`Min ${filter.label.toLowerCase()}`"
                  v-model.number="localFilters[`${filter.key}_min`]"
                  @input="debouncedApplyFilters"
                >
              </div>
              <div class="control is-expanded">
                <input 
                  class="input is-small" 
                  type="number" 
                  :placeholder="`Max ${filter.label.toLowerCase()}`"
                  v-model.number="localFilters[`${filter.key}_max`]"
                  @input="debouncedApplyFilters"
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Date Filters -->
        <div 
          v-for="filter in dateFilters" 
          :key="filter.key"
          class="column is-half-tablet is-one-third-desktop"
        >
          <div class="field">
            <label class="label is-small">{{ filter.label }}</label>
            <div class="field has-addons">
              <div class="control is-expanded">
                <input 
                  class="input is-small" 
                  type="date" 
                  :placeholder="`From`"
                  v-model="localFilters[`${filter.key}_after`]"
                  @change="applyFilters"
                >
              </div>
              <div class="control is-expanded">
                <input 
                  class="input is-small" 
                  type="date" 
                  :placeholder="`To`"
                  v-model="localFilters[`${filter.key}_before`]"
                  @change="applyFilters"
                >
              </div>
            </div>
          </div>
        </div>

        <!-- DateTime Filters -->
        <div 
          v-for="filter in dateTimeFilters" 
          :key="filter.key"
          class="column is-half-tablet is-one-third-desktop"
        >
          <div class="field">
            <label class="label is-small">{{ filter.label }}</label>
            <div class="field has-addons">
              <div class="control is-expanded">
                <input 
                  class="input is-small" 
                  type="datetime-local" 
                  :placeholder="`From`"
                  v-model="localFilters[`${filter.key}_after`]"
                  @change="applyFilters"
                >
              </div>
              <div class="control is-expanded">
                <input 
                  class="input is-small" 
                  type="datetime-local" 
                  :placeholder="`To`"
                  v-model="localFilters[`${filter.key}_before`]"
                  @change="applyFilters"
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Select Filters -->
        <div 
          v-for="filter in selectFilters" 
          :key="filter.key"
          class="column is-half-tablet is-one-third-desktop"
        >
          <div class="field">
            <label class="label is-small">{{ filter.label }}</label>
            <div class="control">
              <div class="select is-small is-fullwidth">
                <select 
                  v-model="localFilters[filter.key]"
                  @change="applyFilters"
                >
                  <option value="">All {{ filter.label }}</option>
                  <option 
                    v-for="option in filter.options" 
                    :key="option.value" 
                    :value="option.value"
                  >
                    {{ option.label }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Boolean Filters -->
        <div 
          v-for="filter in booleanFilters" 
          :key="filter.key"
          class="column is-half-tablet is-one-third-desktop"
        >
          <div class="field">
            <label class="label is-small">{{ filter.label }}</label>
            <div class="control">
              <div class="select is-small is-fullwidth">
                <select 
                  v-model="localFilters[filter.key]"
                  @change="applyFilters"
                >
                  <option value="">All</option>
                  <option value="true">Yes</option>
                  <option value="false">No</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="field is-grouped mt-4">
        <div class="control">
          <button 
            class="button is-primary is-small"
            @click="applyFilters"
          >
            <span class="icon is-small">
              <i class="fas fa-check"></i>
            </span>
            <span>Apply Filters</span>
          </button>
        </div>
        <div class="control">
          <button 
            class="button is-light is-small"
            @click="clearFilters"
          >
            <span class="icon is-small">
              <i class="fas fa-times"></i>
            </span>
            <span>Clear All</span>
          </button>
        </div>
        <div class="control ml-auto">
          <span class="tag is-info is-light">
            {{ activeFilterCount }} active filter{{ activeFilterCount !== 1 ? 's' : '' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const USE_TZ = false // should the Z part of the datetime string be cut

const props = defineProps({
  textFilters: {
    type: Array,
    default: () => []
    // Example: [{ key: 'name', label: 'Name', placeholder: 'Search by name...' }]
  },
  numberFilters: {
    type: Array,
    default: () => []
    // Example: [{ key: 'capacity', label: 'Capacity' }]
  },
  dateFilters: {
    type: Array,
    default: () => []
    // Example: [{ key: 'created_at', label: 'Created Date' }]
  },
  dateTimeFilters: {
    type: Array,
    default: () => []
    // Example: [{ key: 'starts_at', label: 'Start Time' }]
  },
  selectFilters: {
    type: Array,
    default: () => []
    // Example: [{ key: 'status', label: 'Status', options: [{ value: 'ACTIVE', label: 'Active' }] }]
  },
  booleanFilters: {
    type: Array,
    default: () => []
    // Example: [{ key: 'is_verified', label: 'Email Verified' }]
  },
  initialFilters: {
    type: Object,
    default: () => ({})
  },
  collapsed: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['filter-change'])

const showFilters = ref(!props.collapsed)
const localFilters = ref({ ...props.initialFilters })

let debounceTimeout = null

const activeFilterCount = computed(() => {
  return Object.values(localFilters.value).filter(v => v !== '' && v !== null && v !== undefined).length
})

const debouncedApplyFilters = () => {
  if (debounceTimeout) {
    clearTimeout(debounceTimeout)
  }
  debounceTimeout = setTimeout(() => {
    applyFilters()
  }, 500)
}

function cutTimezone(dateString) {
  if (dateString == null) return date;
  const indexOfZ = dateString.indexOf("Z") === -1 ? dateString.length() : dateString.indexOf("Z")
  return dateString.substring(0,indexOfZ)
} // 2222-02-22T22:22:00.000Z

const applyFilters = () => {
  const cleanedFilters = {}
  
  for (const [key, value] of Object.entries(localFilters.value)) {
    if (value !== '' && value !== null && value !== undefined) {
      // Convert date/datetime to ISO string for API
      if (key.includes('_after') || key.includes('_before')) {
        if (key.includes('_after') || key.includes('_before')) {
          // Check if it's a date or datetime-local input
          const inputValue = value
          if (inputValue.includes('T')) {
            // datetime-local format
            cleanedFilters[key] = new Date(inputValue).toISOString()
            if (USE_TZ === false) {
              cleanedFilters[key] = cutTimezone(cleanedFilters[key])
            }
          } else {
            // date format
            cleanedFilters[key] = new Date(inputValue + 'T00:00:00').toISOString()
            if (USE_TZ === false) {
              cleanedFilters[key] = cutTimezone(cleanedFilters[key])
            }
          }
        }
      } else {
        cleanedFilters[key] = value
      }
    }
  }
  
  emit('filter-change', cleanedFilters)
}

const clearFilters = () => {
  localFilters.value = {}
  applyFilters()
}

// Watch for external filter changes
watch(() => props.initialFilters, (newFilters) => {
  localFilters.value = { ...newFilters }
}, { deep: true })
</script>

<style scoped>
.filter-content {
  padding-top: 1rem;
  border-top: 1px solid #dbdbdb;
}

.field.has-addons .control.is-expanded {
  flex-grow: 1;
}

.field.has-addons .control.is-expanded:first-child input {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.field.has-addons .control.is-expanded:last-child input {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  border-left: 0;
}
</style>