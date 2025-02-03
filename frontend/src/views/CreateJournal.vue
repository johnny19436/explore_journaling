<template>
  <div class="create-container">
    <div class="create-form">
      <h1>New Journal Entry</h1>
      <p class="subtitle">Share your thoughts</p>
      <form @submit.prevent="submitJournal">
        <div class="form-group">
          <input 
            type="text" 
            v-model="journal.title" 
            placeholder="Title"
            required
          >
        </div>
        <div class="form-group">
          <textarea 
            v-model="journal.content" 
            placeholder="Write your journal entry..."
            required
          ></textarea>
        </div>
        <button type="submit">Create Entry</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreateJournal',
  data() {
    return {
      journal: {
        title: '',
        content: ''
      }
    }
  },
  methods: {
    async submitJournal() {
      try {
        // await axios.post('http://localhost:3000/api/journals', this.journal);
        await axios.post('/api/journals', this.journal);
        this.$router.push('/');
      } catch (error) {
        console.error('Error:', error);
      }
    }
  }
}
</script>

<style scoped>
.create-container {
  min-height: calc(100vh - 100px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.create-form {
  width: 100%;
  max-width: 800px;
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

input, textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #d2d2d7;
  border-radius: 12px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  font-family: inherit;
}

textarea {
  height: 300px;
  resize: vertical;
  line-height: 1.6;
}

input:focus, textarea:focus {
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

/* Dark mode styles */
:deep(.dark-mode) .create-form {
  background: rgba(30, 30, 30, 0.8);
}

:deep(.dark-mode) h1 {
  color: #f5f5f7;
}

:deep(.dark-mode) input,
:deep(.dark-mode) textarea {
  background: rgba(40, 40, 40, 0.8);
  border-color: #424245;
  color: white;
}

:deep(.dark-mode) input::placeholder,
:deep(.dark-mode) textarea::placeholder {
  color: #86868b;
}

:deep(.dark-mode) button {
  background: #2997ff;
}

:deep(.dark-mode) button:hover {
  background: #0071e3;
}
</style> 