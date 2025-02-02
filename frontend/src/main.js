import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'
import CreateJournal from './views/CreateJournal.vue'
import Login from './views/Login.vue'
import Signup from './views/Signup.vue'
import axios from 'axios'

Vue.use(VueRouter)
Vue.config.productionTip = false

const routes = [
  { 
    path: '/', 
    component: Home,
    meta: { requiresAuth: true }
  },
  { 
    path: '/create', 
    component: CreateJournal,
    meta: { requiresAuth: true }
  },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!localStorage.getItem('token')) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

// Set base URL for development
if (process.env.NODE_ENV === 'development') {
  axios.defaults.baseURL = 'http://localhost:3000'
}

// Add axios interceptor for authentication
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    // Make sure token is properly formatted
    config.headers.Authorization = token.startsWith('Bearer ') ? token : `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

axios.interceptors.response.use(response => {
  return response
}, error => {
  if (error.response && error.response.status === 401) {
    console.log('Token expired or invalid, redirecting to login')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }
  return Promise.reject(error)
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app') 