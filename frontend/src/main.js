import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'
import CreateJournal from './views/CreateJournal.vue'
import Login from './views/Login.vue'
import Signup from './views/Signup.vue'

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

// Add axios interceptor for authentication
import axios from 'axios'
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app') 