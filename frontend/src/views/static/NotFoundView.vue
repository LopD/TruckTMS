<!-- src/views/NotFound.vue -->
<template>
    <section class="section has-text-centered">
      <div class="container">
        <h1 class="title">404 - Page Not Found</h1>
        <p class="subtitle">Redirecting to the home page in {{ countdown }} seconds...</p>
        <h1 >404 - Page Not Found</h1>
        <p >Redirecting to the home page in {{ countdown }} seconds...</p>
      </div>
    </section>
</template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const countdown = ref(10)
  
  onMounted(() => {
    const interval = setInterval(() => {
      countdown.value--
      if (countdown.value === 0) {
        clearInterval(interval)
        // router.push('/')
        // router.push({ name: 'home'})
      }
    }, 1000)
  })
  </script>
  
  <style scoped>
  .section {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  </style>
  