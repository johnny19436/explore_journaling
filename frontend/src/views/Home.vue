<template>
  <div class="physics-container" ref="physicsContainer">
    <div v-for="journal in journals" 
         :key="journal._id" 
         class="journal-bubble"
         :id="'journal-' + journal._id"
         @click="showJournalDetail(journal)">
      <div class="journal-content">
        <h3>{{ journal.title }}</h3>
        <p class="author">{{ journal.author }}</p>
      </div>
    </div>

    <!-- Add Journal Button -->
    <button class="add-journal-btn" @click="showCreateForm">
      <i class="fas fa-plus"></i>
    </button>

    <!-- Create Journal Modal -->
    <div class="modal" v-if="showCreateModal" @click.self="closeCreateForm">
      <div class="create-form">
        <h2>New Journal Entry</h2>
        <form @submit.prevent="submitJournal">
          <div class="form-group">
            <input 
              type="text" 
              v-model="newJournal.title" 
              placeholder="Title"
              required
            >
          </div>
          <div class="form-group">
            <textarea 
              v-model="newJournal.content" 
              placeholder="Write your journal entry..."
              required
            ></textarea>
          </div>
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="closeCreateForm">Cancel</button>
            <button type="submit" class="submit-btn">Create</button>
          </div>
        </form>
        <button class="close-btn" @click="closeCreateForm">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal" v-if="selectedJournal" @click.self="closeJournal">
      <div class="modal-content">
        <h2>{{ selectedJournal.title }}</h2>
        <p class="modal-content-text">{{ selectedJournal.content }}</p>
        <div class="modal-footer">
          <span class="author">By {{ selectedJournal.author }}</span>
          <span class="date">{{ formatDate(selectedJournal.created_at) }}</span>
        </div>
        <button class="close-btn" @click="closeJournal">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Matter from 'matter-js';
import axios from 'axios';

export default {
  name: 'Home',
  data() {
    return {
      journals: [],
      engine: null,
      render: null,
      selectedJournal: null,
      bubbles: {},
      mouseConstraint: null,
      runner: null,
      pollInterval: null,
      showCreateModal: false,
      newJournal: {
        title: '',
        content: ''
      }
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    },
    async initPhysics() {
      if (this.journals.length === 0) return;

      const Engine = Matter.Engine,
            Runner = Matter.Runner,
            Bodies = Matter.Bodies,
            Mouse = Matter.Mouse,
            MouseConstraint = Matter.MouseConstraint,
            World = Matter.World;

      const container = this.$refs.physicsContainer;
      const headerHeight = 80; // Match the container's top offset
      
      // Calculate bounds based on container
      const bounds = {
        width: window.innerWidth,
        height: window.innerHeight - headerHeight
      };
      
      this.engine = Engine.create({
        gravity: { x: 0, y: 1, scale: 0.001 }
      });

      // Create mouse control with correct offset
      const mouse = Mouse.create(container);
      mouse.element.removeEventListener("mousewheel", mouse.mousewheel);
      mouse.element.removeEventListener("DOMMouseScroll", mouse.mousewheel);
      
      // Update mouse position to account for container offset
      const mouseConstraint = MouseConstraint.create(this.engine, {
        mouse: mouse,
        constraint: {
          stiffness: 0.2,
          render: { visible: false }
        }
      });

      // Adjust mouse position for container offset
      const mousePixelRatio = mouse.pixelRatio || 1;
      mouse.mouseup = function(event) {
        const position = {
          x: event.pageX * mousePixelRatio,
          y: (event.pageY - headerHeight) * mousePixelRatio
        };
        Mouse.setOffset(mouse, { x: 0, y: headerHeight });
        Mouse.setPosition(mouse, position);
      };
      mouse.mousedown = mouse.mouseup;
      mouse.mousemove = mouse.mouseup;

      // Create walls using adjusted bounds
    //   const walls = [
    //     Bodies.rectangle(bounds.width/2, bounds.height + headerHeight, bounds.width, 60, { 
    //       isStatic: true
    //     }),
    //     Bodies.rectangle(0, bounds.height/2 + headerHeight, 60, bounds.height, { 
    //       isStatic: true
    //     }),
    //     Bodies.rectangle(bounds.width, bounds.height/2 + headerHeight, 60, bounds.height, { 
    //       isStatic: true
    //     })
    //   ];
      const walls = [
        Bodies.rectangle(bounds.width/2, bounds.height, bounds.width, 60, { 
        isStatic: true
        }),
        Bodies.rectangle(0, bounds.height/2, 60, bounds.height, { 
        isStatic: true
        }),
        Bodies.rectangle(bounds.width, bounds.height/2, 60, bounds.height, { 
        isStatic: true
        })
      ];

      World.add(this.engine.world, [...walls, mouseConstraint]);
      this.mouseConstraint = mouseConstraint;
      
      this.runner = Runner.create();
      Runner.run(this.runner, this.engine);

      this.addJournalBubbles();
    },

    addJournalBubbles() {
      const container = this.$refs.physicsContainer;
      const radius = 83;
      const minSpacing = radius * 2.2; // Minimum space between circles
      
      // Shuffle journals for random order
      const shuffledJournals = [...this.journals].sort(() => Math.random() - 0.5);
      
      // Keep track of used positions
      const usedPositions = [];
      
      shuffledJournals.forEach((journal, index) => {
        let x, y;
        let attempts = 0;
        let validPosition = false;
        
        // Try to find a position that doesn't overlap with existing circles
        while (!validPosition && attempts < 50) {
          // Random position within container width
          x = radius + Math.random() * (container.clientWidth - radius * 2);
          // Random height above viewport, higher for later circles
          y = -radius - (Math.random() * 500) - (index * 100);
          
          // Check distance from all existing positions
          validPosition = usedPositions.every(pos => {
            const dx = x - pos.x;
            const dy = y - pos.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            return distance >= minSpacing;
          });
          
          attempts++;
        }
        
        // Store the valid position
        usedPositions.push({ x, y });

        const bubble = Matter.Bodies.circle(x, y, radius, {
          friction: 0.8,
          restitution: 0.2,
          density: 1.5,
          frictionAir: 0.02,
          label: journal._id,
          render: { visible: false }
        });

        this.bubbles[journal._id] = bubble;
        
        setTimeout(() => {
          Matter.World.add(this.engine.world, bubble);
          
          // No initial velocity - let gravity do the work
          Matter.Body.setVelocity(bubble, {
            x: 0,
            y: 0
          });
        }, index * 200);
      });

      this.updatePositions();
    },

    updatePositions() {
      requestAnimationFrame(() => {
        Object.entries(this.bubbles).forEach(([id, body]) => {
          const element = document.getElementById(`journal-${id}`);
          if (element) {
            element.style.transform = `translate(${
              body.position.x - element.clientWidth/2}px, ${
              body.position.y - element.clientHeight/2}px)`;
          }
        });
        this.updatePositions();
      });
    },

    showJournalDetail(journal) {
      if (!this.mouseConstraint.body) {
        this.selectedJournal = journal;
      }
    },

    closeJournal() {
      this.selectedJournal = null;
    },

    async loadJournals() {
      try {
        const response = await axios.get('http://localhost:3000/api/journals');
        // Compare with existing journals to find new ones
        const newJournals = response.data.filter(newJournal => 
          !this.journals.some(existingJournal => existingJournal._id === newJournal._id)
        );
        
        // Update journals array
        this.journals = response.data;

        // If physics not initialized, initialize it
        if (!this.engine) {
          await this.$nextTick();
          this.initPhysics();
        } else if (newJournals.length > 0) {
          // Add only new journals as bubbles
          this.addNewJournalBubbles(newJournals);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },

    addNewJournalBubbles(newJournals) {
      const container = this.$refs.physicsContainer;
      const radius = 83;
      
      newJournals.forEach((journal) => {
        // Random x position
        const x = radius + Math.random() * (container.clientWidth - radius * 2);
        // Start from top
        const y = -radius - 100;

        const bubble = Matter.Bodies.circle(x, y, radius, {
          friction: 0.8,
          restitution: 0,
          density: 1.5,
          frictionAir: 0.02,
          label: journal._id,
          render: { visible: false }
        });

        this.bubbles[journal._id] = bubble;
        Matter.World.add(this.engine.world, bubble);
      });
    },

    showCreateForm() {
      this.showCreateModal = true;
    },

    closeCreateForm() {
      this.showCreateModal = false;
      this.newJournal = { title: '', content: '' };
    },

    async submitJournal() {
      try {
        const response = await axios.post('http://localhost:3000/api/journals', this.newJournal);
        const newJournal = response.data;
        
        // Add new journal to the list
        this.journals.push(newJournal);
        
        // Create new bubble for the journal
        this.addNewJournalBubbles([newJournal]);
        
        // Close the form
        this.closeCreateForm();
      } catch (error) {
        console.error('Error:', error);
      }
    }
  },

  mounted() {
    this.loadJournals();
    // Poll for new journals periodically
    this.pollInterval = setInterval(() => {
      this.loadJournals();
    }, 5000); // Check every 5 seconds
  },

  beforeDestroy() {
    if (this.render) Matter.Render.stop(this.render);
    if (this.runner) Matter.Runner.stop(this.runner);
    if (this.engine) Matter.Engine.clear(this.engine);
    clearInterval(this.pollInterval);
  }
}
</script>

<style scoped>
.physics-container {
  position: fixed;
  top: 80px; /* Reduced from 100px */
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: calc(100% - 80px);
  background: #f5f5f7;
  z-index: 1;
  overflow: hidden;
}

.journal-bubble {
  position: absolute;
  width: 148px;
  height: 148px;
  border-radius: 50%;
  background: #fff;
  cursor: grab;
  padding: 8px;
  text-align: center;
  user-select: none;
  will-change: transform;
  display: flex;
  align-items: center;
  justify-content: center;
}

.journal-bubble:active {
  cursor: grabbing;
}

.journal-content {
  width: 100%;
}

.journal-content h3 {
  font-size: 0.8rem;
  font-weight: 500;
  margin: 0 0 2px;
  color: #1d1d1f;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.journal-content .author {
  font-size: 0.65rem;
  color: #86868b;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Dark mode styles */
:deep(.dark-mode) .journals-container {
  background: #1c1c1e;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

:deep(.dark-mode) .journal-bubble {
  background: #2c2c2e;
}

:deep(.dark-mode) .journal-bubble:active {
  cursor: grabbing;
}

:deep(.dark-mode) .journal-content h3 {
  color: #f5f5f7;
}

:deep(.dark-mode) .journal-content .author {
  color: #98989d;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: grid;
  place-items: center;
  z-index: 1000;
  overflow: hidden;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 20px;
  position: relative;
  max-width: 600px;
  width: 90%;
}

.modal-content h2 {
  margin: 0 0 20px;
  color: #1d1d1f;
}

.modal-content-text {
  line-height: 1.6;
  color: #424245;
  margin-bottom: 20px;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  color: #86868b;
  font-size: 0.9rem;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  color: #86868b;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 5px;
  transition: all 0.3s ease;
}

.close-btn:hover {
  color: #1d1d1f;
  transform: rotate(90deg);
}

:deep(.dark-mode) .close-btn:hover {
  color: #f5f5f7;
}

.add-journal-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #0071e3;
  color: white;
  border: none;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 100;
}

.add-journal-btn:hover {
  transform: scale(1.1);
  background: #0077ED;
}

.create-form {
  background: white;
  padding: 30px;
  border-radius: 20px;
  position: relative;
  max-width: 600px;
  width: 90%;
}

.create-form h2 {
  margin: 0 0 20px;
  color: #1d1d1f;
}

.form-group {
  margin-bottom: 20px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #d2d2d7;
  border-radius: 8px;
  font-size: 14px;
}

.form-group textarea {
  height: 150px;
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.cancel-btn {
  padding: 8px 16px;
  background: #f5f5f7;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.submit-btn {
  padding: 8px 16px;
  background: #0071e3;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style> 