<template>
    <div>
      <p v-if="status === 'loading'">Verifying your email...</p>
      <p v-else>{{ message }}</p>
    </div>
</template>
  
<script>
  import axios from 'axios'
  
  export default {
    name: 'ConfirmEmailView',
    data() {
      return {
        status: 'loading',
        message: ''
      }
    },
    mounted() {
      const token = this.$route.query.token
  
      if (!token) {
        this.status = 'error'
        this.message = 'No verification token provided.'
        return
      }
  
      axios.get(`http://localhost:8000/email-verify/?token=${token}`)
        .then(response => {
          console.log(response)
        //   const { access, refresh } = response.data
          //edit:
          const access = response.data['access']
          const refresh = response.data['refresh']

          // Store tokens and update Axios headers
          localStorage.setItem('access_token', access)
          localStorage.setItem('refresh_token', refresh)
          axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
          
          // update authentication state
          this.$store.commit('SetIsAuthenticated',true)
  
          this.status = 'success'
          this.message = 'Email verified! Redirecting...'
  

          const payload = JSON.parse(atob(access.split('.')[1]))  // Dekodiranje JWT payload-a
          // console.log('payload=>'+payload)
          // console.log('payload=>'+JSON.stringify(payload) )
          const userId = payload.user_id  // Pretpostavljamo da 'id' postoji u payload-u tokena
          const userGroups = payload.groups

          setTimeout(() => {
            // this.$router.push('/')
            if (userGroups != null && userGroups.length > 0 && userGroups[0].length > 0) {
                localStorage.setItem('activeRole',userGroups[0]) // set the active role of the user 
                this.$router.push(`/`+userGroups[0]+`/home`)
            }
            else {
                this.$router.push(`/NotFound`)
            }
          }, 2500)
        })
        .catch(() => {
          this.status = 'error'
          this.message = 'Invalid or expired confirmation link.'
        })
    }
  }
</script>
  