FROM node:16-alpine AS build-container

# Build stage
WORKDIR /app
COPY . .
RUN npm ci && npm run build --prod

# Serve stage
FROM nginx:alpine
COPY --from=build-container /app/dist/sapi /usr/share/nginx/html
COPY /nginx.conf  /etc/nginx/conf.d/default.conf
EXPOSE 80