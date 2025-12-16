# Stage 1: Build
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production Server
FROM nginx:stable-alpine
# Vite builds to the 'dist' folder by default
COPY --from=build /app/dist /usr/share/nginx/html
# Copy a custom nginx config if you have one, or use default
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]