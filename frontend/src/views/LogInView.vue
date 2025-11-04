<template>
    <div class="login-container">
      <div class="login-form-wrapper">
        <div class="login-header">
          <h1 class="login-title">Log In</h1>
          <!-- <p class="login-subtitle">Welcome back! Please enter your credentials to continue.</p> -->
        </div>
        
        <form class="login-form" @submit.prevent="submitForm">
          
          <!-- Username -->
          <!-- <div class="form-group">
            <label for="username">Username</label>
            <input
              type="username"
              id="username"
              v-model="username"
              class="form-control"
              placeholder="Enter your username"
              required
            />
          </div> -->
          
          <!-- Email -->
          <div class="form-group">
            <label for="email">Email Address</label>
            <input
              type="email"
              id="email"
              v-model="email"
              class="form-control"
              placeholder="Enter your email"
              required
              @blur="validateEmail"
            />
            <p v-if="this.email && !isValidEmail" style="color: red;">Please enter a valid email address.</p>
          </div>
          
          <!-- Password -->
          <div class="form-group">
            <label for="password">Password</label>
            <div class="password-input-wrapper">
              <input
                :type="showPassword ? 'text' : 'password'"
                id="password"
                v-model="password"
                class="form-control"
                placeholder="Enter your password"
                required
              />
              <button 
                type="button" 
                class="toggle-password" 
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
            <!-- <div class="password-actions">
              <a href="#" class="forgot-password">Forgot password?</a>
            </div> -->
          </div>
          
          <!-- <div class="form-group remember-me">
            <label class="checkbox-container">
              <input type="checkbox" v-model="rememberMe" />
              <span class="checkbox-text">Remember me</span>
            </label>
          </div> -->
          
          <button type="submit" class="login-button" :disabled="isLoading">
            {{ isLoading ? 'Logging in...' : 'Log In' }}
          </button>
          
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </form>
        
        <!-- <div class="social-login">
          <p class="or-divider"><span>Or continue with</span></p>
          <div class="social-buttons">
            <button class="social-button google">
              <span class="social-icon">G</span>
              <span>Google</span>
            </button>
            <button class="social-button facebook">
              <span class="social-icon">f</span>
              <span>Facebook</span>
            </button>
          </div>
        </div> -->
        
        <div class="signup-prompt">
          Don't have an account? <router-link to="/sign-up" class="signup-link">Sign up</router-link>
          <!-- <a href="#" class="signup-link">Sign up</a> -->
        </div>
        <!-- <div class="login-for-employees-only-note"> 
            <p >Regular users can not sign up.</p>
            <p >This page is for employees only.</p>
        </div> -->
      </div>
    </div>
  </template>
  
<script>
// libs
import axios from 'axios';
import { toast } from 'bulma-toast';

// custom api
import axiosApi from '@/axios';

  export default {
    name: 'LoginPage',
    data() {
      return {
        // username: '',   // testing purposes only
        email: '',
        isValidEmail: true,
        password: '',
        rememberMe: false,
        showPassword: false,
        isLoading: false,
        errorMessage: '',
        errors: [], // will only be logged
        unauthMessage: '',
      }
    },
    methods: {
      submitForm() {

        // Reset error message
        this.errorMessage = '';
        this.errors = []
        this.unauthMessage = ""    
        
        // Set loading state
        this.isLoading = true;
        
        // Validate inputs
        if (!this.validateEmail()) {
          this.isLoading = false;
          return;
        }
        if (!this.email || !this.password) {
          this.errorMessage = 'Please enter both email and password.';
          this.isLoading = false;
          return;
        }

        // create and send form
        const formData = {
            email: this.email,
            password: this.password,
        }
        
        // remove access and refresh tokens
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');

        // axios
        axios.post("core/log-in/",formData)
            .then( response => {
              // console.log(response)
              // const token = response.data.jwt  //old
              
              const access = response.data['access']
              const refresh = response.data['refresh']
              // console.log('access token=>'+access + 'refresh token=>'+refresh+'\n\n')
              localStorage.setItem('access_token', access);
              localStorage.setItem('refresh_token', refresh);

              // update authentication state
              this.$store.commit('SetIsAuthenticated',true)
            
              const payload = JSON.parse(atob(access.split('.')[1]))  // Dekodiranje JWT payload-a
              
              const userId = payload.user_id  // Pretpostavljamo da 'id' postoji u payload-u tokena
              const userGroups = payload.groups
              
              this.$router.push({name:'logged-in'})
              // this.$router.push('/logged-in');
              //! TODO: Redirect to proper home page
              // if (userGroups != null && userGroups.length > 0 && userGroups[0].length > 0) {
              //   localStorage.setItem('activeRole',userGroups[0]) // set the active role of the user 
              //   localStorage.setItem('userId',userId) // set the active role of the user 
              //   this.$router.push({name:'logged-in'})
              // }
              // else {
              //   this.$router.push(`/NotFound`)
              // }
                
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
                    this.errorMessage = error.response.data['message'];
                }
                this.email = '';
                this.password = '';
                this.rememberMe = false;
                this.showPassword = false;
                this.isLoading = false;
            })
        }, //submitForm()
        validateEmail() {
          const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          this.isValidEmail = emailPattern.test(this.email);
          this.isValidEmail = ( this.email.length <= 0 ) ? false : this.isValidEmail;
          return this.isValidEmail;
        },
    }
  }
</script>
  
<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.login-form-wrapper {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 420px;
  padding: 40px 30px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  color: #252525;
  margin-bottom: 12px;
}

.login-subtitle {
  font-size: 16px;
  color: #6e6e6e;
  line-height: 1.5;
}

.login-for-employees-only-note {
  font-size: 16px;
  color: #6e6e6e;
  line-height: 1.5;
}

.form-group {
  margin-bottom: 24px;
}

label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #3a3a3a;
  margin-bottom: 8px;
}

.form-control {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;
  border: 1px solid #d9dbe9;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.2s;
}

.form-control:focus {
  border-color: #4a6cf7;
  box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.15);
}

.password-input-wrapper {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #6e6e6e;
  font-size: 14px;
  cursor: pointer;
  padding: 4px;
}

.password-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

.forgot-password {
  font-size: 14px;
  color: #4a6cf7;
  text-decoration: none;
}

.remember-me {
  display: flex;
  align-items: center;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-text {
  margin-left: 8px;
  font-size: 14px;
  color: #3a3a3a;
}

.login-button {
  display: block;
  width: 100%;
  padding: 14px;
  background-color: #4a6cf7;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #3a5ceb;
}

.login-button:disabled {
  background-color: #a4afdc;
  cursor: not-allowed;
}

.error-message {
  margin-top: 16px;
  color: #e53935;
  font-size: 14px;
  text-align: center;
}

.or-divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 24px 0;
  color: #6e6e6e;
  font-size: 14px;
}

.or-divider::before,
.or-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #d9dbe9;
}

.or-divider span {
  margin: 0 10px;
}

.social-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.social-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background-color: white;
  border: 1px solid #d9dbe9;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.social-button:hover {
  background-color: #f5f7fa;
}

.social-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  font-weight: bold;
}

.signup-prompt {
  text-align: center;
  font-size: 14px;
  color: #6e6e6e;
}

.signup-link {
  color: #4a6cf7;
  font-weight: 600;
  text-decoration: none;
}
</style>