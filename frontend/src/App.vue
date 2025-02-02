<template>
  <div id="app">
    <header class="app-header">
      <div class="left-section">
        <!-- Remove theme switcher -->
      </div>
      
      <nav class="center-section" v-if="isLoggedIn">
        <router-link to="/">Home</router-link>
      </nav>
      
      <div class="right-section">
        <template v-if="isLoggedIn">
          <span class="username">{{ username }}</span>
          <button class="logout-btn" @click="logout">
            <i class="fas fa-sign-out-alt"></i>
          </button>
        </template>
      </div>
    </header>
    
    <main class="app-content">
      <router-view/>
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
html {
  background: #fff;
}

#app {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  min-height: 100vh;
  transition: all 0.3s ease;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  margin-bottom: 20px;
}

.left-section, .right-section {
  flex: 1;
  display: flex;
  align-items: center;
}

.right-section {
  justify-content: flex-end;
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
  border-radius: 50%;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(0, 113, 227, 0.1);
}

.app-content {
  padding: 0 20px;
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