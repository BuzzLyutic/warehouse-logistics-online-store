# nginx/Dockerfile

# Stage 1: Build Frontend
FROM node:16 as build

WORKDIR /app
ARG FRONTEND_DIR

COPY ${FRONTEND_DIR}/package*.json ./
RUN npm install

COPY ${FRONTEND_DIR}/. .
RUN npm run build

# Stage 2: Setup Nginx
FROM nginx:alpine

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Copy the React build from Stage 1
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]