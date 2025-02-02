FROM node:14

WORKDIR /app

# Copy package files first to leverage Docker cache
COPY package*.json ./
RUN npm install

# Copy config files
COPY .eslintrc.js .
COPY .eslintignore .
COPY vue.config.js .

# Create necessary directories and copy their contents
COPY public public/
COPY src src/

EXPOSE 8080

# Development mode: use serve instead of build
CMD ["npm", "run", "serve"] 