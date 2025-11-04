<template>
    <div class="signup-container">
      <div v-if="!isLoginSuccess" class="signup-form-wrapper">
        <div class="signup-header">
          <h1 class="signup-title">Sign Up</h1>
          <p class="signup-subtitle">Create an account to get started with our services.</p>
        </div>
        
        <form class="signup-form" @submit.prevent="handleSignup">
          
          <!-- First name and Last name-->
          <div class="form-row">
            <div class="form-group">
              <label for="firstName">First Name</label>
              <input
                type="text"
                id="firstName"
                v-model="firstName"
                class="form-control"
                placeholder="Enter your first name"
                required
              />
            </div>
            
            <div class="form-group">
              <label for="lastName">Last Name</label>
              <input
                type="text"
                id="lastName"
                v-model="lastName"
                class="form-control"
                placeholder="Enter your last name"
                required
              />
            </div>
          </div>
          
          <!-- Username -->
          <div class="form-group">
            <label for="username">Username</label>
            <input
              type="text"
              id="username"
              v-model="username"
              class="form-control"
              placeholder="Enter your username"
              required
            />
          </div>

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
                placeholder="Create a password"
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
            <div class="password-strength" v-if="password">
              <div class="strength-meter" :class="passwordStrength"></div>
              <span class="strength-text">{{ passwordStrengthText }}</span>
            </div>
          </div>
          
          <!-- Confirm password -->
          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <div class="password-input-wrapper">
              <input
                :type="showConfirmPassword ? 'text' : 'password'"
                id="confirmPassword"
                v-model="confirmPassword"
                class="form-control"
                placeholder="Confirm your password"
                required
              />
              <button 
                type="button" 
                class="toggle-password" 
                @click="showConfirmPassword = !showConfirmPassword"
              >
                {{ showConfirmPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
            <div class="password-match" v-if="password && confirmPassword">
              <span :class="{'match': passwordsMatch, 'no-match': !passwordsMatch}">
                {{ passwordsMatch ? 'Passwords match' : 'Passwords do not match' }}
              </span>
            </div>
          </div>
          
          <!-- Choose role -->
          <div class="form-group">
            <div v-for="role in roles" :key="role.value">
              <input 
                type="radio" 
                :id="role.value" 
                name="role" 
                :value="role.value" 
                v-model="selectedRole"
              >
              <label :for="role.value">{{ role.label }}</label>
            </div>
          </div>


          <!-- TOS checkbox -->
          <div class="form-group terms-checkbox">
            <label class="checkbox-container">
              <input type="checkbox" v-model="agreeToTerms" required />
              <span class="checkbox-text">
                I agree to the <a :href="privacyPolicyHref" target="_blank" class="terms-link" rel="noopener noreferrer">Privacy Policy</a>
              </span>
            </label>
          </div>
          
          <button type="submit" class="signup-button" :disabled="isLoading || !formValid">
            {{ isLoading ? 'Creating Account...' : 'Create Account' }}
          </button>
          
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </form>
        
        <div class="login-prompt">
          Already have an account? <router-link to="/log-in" class="login-link">Log in</router-link>
        </div>
      </div>
      <div v-else>
        <h1 class="signup-title">Success!</h1>
        <p class="signup-subtitle">Please verify your email to log in.</p>
      </div>
    </div>
</template>
  
<script>
import axiosApi from '@/axios';
import axios from 'axios';
import { toast } from 'bulma-toast';

  export default {
    name: 'SignupPage',
    data() {
      return {
        firstName: '',
        lastName: '',
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        showPassword: false,
        showConfirmPassword: false,
        agreeToTerms: false,
        isLoading: false,
        isValidEmail: true,
        isLoginSuccess: false,

        selectedRole: 'coach', // default
        roles: [
          { label: 'Coach', value: 'coach' },
          { label: 'Member', value: 'member' },
          // later you can just add here: { label: 'Admin', value: 'admin' }
        ],

        errorMessage: ''
      };
    },
    computed: {
      passwordStrength() {
        if (!this.password) return '';
        
        const length = this.password.length;
        const hasUpperCase = /[A-Z]/.test(this.password);
        const hasLowerCase = /[a-z]/.test(this.password);
        const hasNumbers = /\d/.test(this.password);
        const hasSpecialChars = /[!@#$%^&*(),.?":{}|<>]/.test(this.password);
        
        const strength = [
          length >= 8,
          hasUpperCase,
          hasLowerCase,
          hasNumbers,
          hasSpecialChars
        ].filter(Boolean).length;
        
        if (strength <= 2) return 'weak';
        if (strength <= 4) return 'medium';
        return 'strong';
      },
      passwordStrengthText() {
        const strengthMap = {
          weak: 'Weak password',
          medium: 'Medium strength',
          strong: 'Strong password'
        };
        return strengthMap[this.passwordStrength] || '';
      },
      passwordsMatch() {
        return this.password && this.confirmPassword && this.password === this.confirmPassword;
      },
      formValid() {
        return (
          this.firstName &&
          this.lastName &&
          this.username &&
          this.email &&
          this.password &&
          this.confirmPassword &&
          this.passwordsMatch &&
          this.agreeToTerms &&
          this.isValidEmail && 
          this.selectedRole
        );
      },
      privacyPolicyHref() {
        // Resolve the path using vue-router
        return this.$router.resolve({ name: 'privacy-policy' }).href;
      }
    },
    methods: {
      handleSignup() {

        // Reset error message
        this.errorMessage = '';
        
        // Set loading state
        this.isLoading = true;
        
        // Basic validation
        if (!this.formValid) {
          this.errorMessage = 'Please complete all fields.';
          this.isLoading = false;
          return;
        }
        
        
        // create and send form, note: the backend is in python that uses snake case
        const formData = {
          'first_name': this.firstName,
          'last_name': this.lastName,
          username: this.username,
          email: this.email,
          password: this.password,
          confirmPassword: this.confirmPassword,
          passwordsMatch: this.passwordsMatch,
          agreeToTerms: this.agreeToTerms,
          selectedRole: this.selectedRole
        }
        // axiosApi
        //http://localhost:8000
        axios.post("core/sign-up/",formData)
            .then( response => {
                console.log(response)
                this.isLoginSuccess = true
                this.isLoading = false
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
                // this.email = '';
                this.password = '';
                this.confirmPassword = '';
                // this.rememberMe = false;
                // this.showPassword = false;
                this.isLoading = false;
            })
        },
        validateEmail() {
          const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          this.isValidEmail = emailPattern.test(this.email);
          this.isValidEmail = ( this.email.length <= 0 ) ? false : this.isValidEmail;
          return this.isValidEmail;
        },
    }
  };
</script>
  
<style scoped>
  .signup-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f7fa;
    padding: 20px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }
  
  .signup-form-wrapper {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    width: 100%;
    max-width: 480px;
    padding: 40px 30px;
  }
  
  .signup-header {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .signup-title {
    font-size: 28px;
    font-weight: 700;
    color: #252525;
    margin-bottom: 12px;
  }
  
  .signup-subtitle {
    font-size: 16px;
    color: #6e6e6e;
    line-height: 1.5;
  }
  
  .form-row {
    display: flex;
    gap: 16px;
    margin-bottom: 0;
  }
  
  .form-row .form-group {
    flex: 1;
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
  
  .password-strength {
    margin-top: 8px;
    display: flex;
    align-items: center;
  }
  
  .strength-meter {
    height: 4px;
    flex: 1;
    border-radius: 2px;
    margin-right: 8px;
  }
  
  .strength-meter.weak {
    background-color: #e53935;
  }
  
  .strength-meter.medium {
    background-color: #ffb74d;
  }
  
  .strength-meter.strong {
    background-color: #4caf50;
  }
  
  .strength-text {
    font-size: 12px;
    color: #6e6e6e;
  }
  
  .password-match {
    margin-top: 8px;
    font-size: 12px;
  }
  
  .match {
    color: #4caf50;
  }
  
  .no-match {
    color: #e53935;
  }
  
  .terms-checkbox {
    margin-top: 16px;
  }
  
  .checkbox-container {
    display: flex;
    align-items: flex-start;
    cursor: pointer;
  }
  
  .checkbox-text {
    margin-left: 8px;
    font-size: 14px;
    color: #3a3a3a;
    line-height: 1.4;
  }
  
  .terms-link {
    color: #4a6cf7;
    text-decoration: none;
  }
  
  .signup-button {
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
    margin-top: 8px;
  }
  
  .signup-button:hover {
    background-color: #3a5ceb;
  }
  
  .signup-button:disabled {
    background-color: #a4afdc;
    cursor: not-allowed;
  }
  
  .error-message {
    margin-top: 16px;
    color: #e53935;
    font-size: 20px;
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
  
  .login-prompt {
    text-align: center;
    font-size: 14px;
    color: #6e6e6e;
  }
  
  .login-link {
    color: #4a6cf7;
    font-weight: 600;
    text-decoration: none;
  }
  
  @media (max-width: 600px) {
    .form-row {
      flex-direction: column;
      gap: 0;
    }
  }
</style>