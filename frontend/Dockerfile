FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Expose port 5173 for Vite dev server (or for preview)
EXPOSE 5173

# Normally we'd build for production, but for preview we can run Vite to expose it externally
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
