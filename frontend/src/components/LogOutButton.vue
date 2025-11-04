<template>
    <button v-if="this.$store.state.isAuthenticated" @click="logOut" class="nav-link log-out">LOG OUT</button>
</template>

<script>
import axios from 'axios';
import { toast } from 'bulma-toast';
import axiosApi from '@/axios';

export default {
    name: 'LogOutButton',
    data() {
      return {
      }
    },
    components: {
    },
    computed: {
    },
    methods: {
      logOut() {
        // axios
        axiosApi.post("/log-out/")
          .then( response => {
              console.log(response)
              if (response.data != null && response.data['message'] != null) {
                toast({
                    message: response.data['message'],
                    type: 'is-success',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: 'bottom-right',
                })
              }
              // this.$store.commit('RemoveToken');
              this.$store.commit('SetIsAuthenticated',false)
              localStorage.removeItem('access_token')
              localStorage.removeItem('refresh_token')
              localStorage.removeItem('activeRole')
              this.$router.push(`/`)
          })
          .catch( error => {
              console.log(error)
              if (error.response != null && error.response.data['message'] != null) {
                  toast({
                      message: error.response.data['message'],
                      type: 'is-danger',
                      dismissible: true,
                      pauseOnHover: true,
                      duration: 2000,
                      position: 'bottom-right',
                  })
              }
              this.$store.commit('RemoveToken');
              this.$router.push(`/`)
          })
      },
    }
  }
</script>

<style scoped>
.log-out {
  color: white;
  background-color: black;
}
</style>