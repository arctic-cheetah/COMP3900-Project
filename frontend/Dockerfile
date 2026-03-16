# Build stage
FROM node:20-alpine AS build
WORKDIR /app/frontend

COPY package.json ./
RUN npm install

COPY . .
ARG VITE_API_URL=http://localhost:5001
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Serve stage
FROM nginx:alpine
COPY --from=build /app/frontend/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 6969
CMD ["nginx", "-g", "daemon off;"]
