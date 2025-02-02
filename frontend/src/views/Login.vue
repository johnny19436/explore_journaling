<template>
  <div class="auth-container">
    <div class="auth-form">
      <h1>Welcome Back</h1>
      <p class="subtitle">Sign in to continue</p>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <input 
            type="email" 
            v-model="credentials.email" 
            placeholder="Email"
            required
          >
        </div>
        <div class="form-group">
          <input 
            type="password" 
            v-model="credentials.password" 
            placeholder="Password"
            required
          >
        </div>
        <button type="submit">Sign In</button>
        <p class="auth-link">
          New to Journal? <router-link to="/signup">Create an account</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      credentials: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('/api/auth/login', this.credentials);
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        this.$router.push('/');
      } catch (error) {
        console.error('Login error:', error);
        alert('Invalid credentials');
      }
    }
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.auth-form {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #1d1d1f;
}

.subtitle {
  color: #86868b;
  margin-bottom: 32px;
}

.form-group {
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 15px;
  border: 1px solid #d2d2d7;
  border-radius: 12px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #0071e3;
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
}

button {
  width: 100%;
  padding: 15px;
  background: #0071e3;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background: #0077ED;
  transform: translateY(-1px);
}

.auth-link {
  margin-top: 24px;
  text-align: center;
  color: #86868b;
}

.auth-link a {
  color: #0071e3;
  text-decoration: none;
  font-weight: 500;
}

/* Dark mode styles */
:deep(.dark-mode) .auth-form {
  background: rgba(30, 30, 30, 0.8);
}

:deep(.dark-mode) h1 {
  color: #f5f5f7;
}

:deep(.dark-mode) input {
  background: rgba(40, 40, 40, 0.8);
  border-color: #424245;
  color: white;
}

:deep(.dark-mode) input::placeholder {
  color: #86868b;
}

:deep(.dark-mode) .auth-link {
  color: #86868b;
}

:deep(.dark-mode) .auth-link a {
  color: #2997ff;
}
</style> 