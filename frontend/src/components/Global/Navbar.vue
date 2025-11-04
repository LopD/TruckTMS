<template>
    <!-- Navigation Bar -->
  <nav class="navbar">
    <div class="container">
      <!-- <div class="logo">
        <router-link to="/" class="">
          <img src="@/assets/static/images/KMS_logo.png" alt="KMS Express Inc. Logo" />
        </router-link>
      </div> -->
      
      <!-- Burger icon -->
      <div class="burger" @click="toggleMenu">
        <div class="bar" />
        <div class="bar" />
        <div class="bar" />
      </div>
      
      <div class="nav-links" :class="{ open: isOpen }">
        <router-link to="/" class="nav-link">HOME</router-link>
        <!-- <router-link to="/services" class="nav-link">SERVICES</router-link> -->
        <router-link to="/about-us" class="nav-link">ABOUT US</router-link>
        <!-- <router-link to="/contact-us" class="nav-link">CONTACT US</router-link> -->
        <!-- <router-link to="/request-quote" class="nav-link request-a-quote">REQUEST A QUOTE</router-link> -->
        <router-link to="/log-in" class="nav-link log-in" >LOG IN</router-link>
        <!-- hidden="true" -->
        <LogOutButton />
        
      </div>
    </div>
  </nav>
</template>

<script setup>
import LogOutButton from '@/components/LogOutButton.vue';
import { ref } from 'vue'

const isOpen = ref(false)

function toggleMenu() {
  isOpen.value = !isOpen.value
}
</script>

<style src="@/assets/static/css/navbar.css"></style>
<style scoped>
/* Burger icon */
.burger {
  display: none;
  flex-direction: column;
  cursor: pointer;
}

.burger .bar {
  width: 25px;
  height: 3px;
  background-color: black;
  margin: 4px 0;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-links.open {
  display: block;
}

/* Mobile styles */
@media (max-width: 768px) {
  .burger {
    display: flex;
  }

  .nav-links {
    display: none;
    flex-direction: column;
  }

  .nav-links.open {
    display: flex;
  }
}
</style>
