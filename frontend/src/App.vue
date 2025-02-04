<template>
  <div id="app">
    <header class="app-header">
      <img src="@/logo_removebg.png" alt="Logo" class="logo" />
      <nav class="center-section" v-if="isLoggedIn">
        <router-link to="/">Home</router-link>
      </nav>
      
      <template v-if="isLoggedIn">
        <span class="username">{{ username }}</span>
        <button class="logout-btn" @click="logout">
          <i class="fas fa-sign-out-alt"></i>
        </button>
      </template>
    </header>
    
    <main class="app-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isAuthenticated: false
    }
  },
  computed: {
    isLoggedIn() {
      return this.isAuthenticated && !!localStorage.getItem('token')
    },
    username() {
      const user = localStorage.getItem('user')
      return user ? JSON.parse(user).username : ''
    }
  },
  methods: {
    async logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.isAuthenticated = false
      await this.$router.push('/login')
      window.location.reload()
    },
    checkAuth() {
      this.isAuthenticated = !!localStorage.getItem('token')
    }
  },
  created() {
    this.checkAuth()
  },
  watch: {
    $route() {
      this.checkAuth()
    }
  }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  font-family: Arial, sans-serif;
  /* max-width: 800px; */
  margin: 0 auto;
  min-height: 100vh;
  transition: all 0.3s ease;
  background: #2c3e50;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px;
  padding-left: 20px;
  padding-right: 20px;
  /* background-color: #3e5871; */
  background-color: #175da3;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.logo {
  height: 45px;
  margin-right: 20px;
  margin-left: 10px;
}

.center-section {
  display: flex;
  gap: 20px;
}

.username {
  margin-right: 15px;
  color: #86868b;
}

.logout-btn {
  background: none;
  border: none;
  color: #0071e3;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 8px;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(0, 113, 227, 0.1);
}

.app-content {
  padding: 0 20px;
  padding-top: 80px;
}

nav a {
  color: #1d1d1f;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

nav a:hover {
  background: rgba(0, 0, 0, 0.05);
}

nav a.router-link-active {
  color: #0071e3;
  background: rgba(0, 113, 227, 0.1);
}
</style> 