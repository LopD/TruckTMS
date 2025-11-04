import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bulma-toast';

// custom elements
import axiosApi from './axios'  // custom axios API 
import axios from 'axios';

// default axios settings
axios.defaults.baseURL = 'http://localhost:8000'; // Django backend URL
//NOTE: change the base URL in axios.js when deploying the site 
axios.headers = {'Content-Type': 'application/json',};

const app = createApp(App)
    .use(store)
    .use(router);

// Optional: Attach to globalProperties for easy use in components
app.config.globalProperties.$api = axiosApi

app.mount('#app')
