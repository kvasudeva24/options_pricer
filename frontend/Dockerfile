# Stage 1: Build the React app
FROM node:20-alpine AS build

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# CRA outputs to /app/build, so we copy that to Nginx's root
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 3000