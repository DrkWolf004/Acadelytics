FROM node:20-alpine AS build
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install
COPY frontend/. .
COPY .env /app/.env
RUN npm run build

FROM node:20-alpine AS runtime
RUN npm install -g serve
WORKDIR /app
COPY --from=build /app/frontend/dist ./dist
EXPOSE 4173
CMD ["serve", "-s", "dist", "-l", "4173"]
