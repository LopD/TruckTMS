<template>
  <div class="layout"> 
    <div class="content">

      <!-- Navigation Bar -->
      <Navbar ></Navbar>

      
      <!-- page content-->
      <router-view/>

      <ScrollToTopButton></ScrollToTopButton>
    </div>
    
    <!-- Footer -->
    <Footer></Footer>
  </div>
</template>

<style lang="scss">
@import '../node_modules/bulma'; 
</style>

<script>
import LogOutButton from './components/LogOutButton.vue';

import Navbar from './components/Global/Navbar.vue';
import Footer from './components/Global/Footer.vue';
import ScrollToTopButton from './components/Global/ScrollToTopButton.vue';

export default {
  name: 'App',
  data() {
    return {
      mobileMenuOpen: false,
    }
  },
  components: {
    LogOutButton,
    Navbar,
    Footer,
    ScrollToTopButton
  },
  computed: {
  },
  methods: {
  }
}
</script>