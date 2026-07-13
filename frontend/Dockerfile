FROM node:20-alpine AS build
ARG VITE_BASE_URL=http://localhost:5000/api
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install
COPY frontend/. .
RUN if [ ! -f .env ]; then printf 'VITE_BASE_URL=%s\n' "$VITE_BASE_URL" > .env; fi && npm run build

FROM node:20-alpine AS runtime
RUN npm install -g serve
WORKDIR /app
COPY --from=build /app/frontend/dist ./dist
EXPOSE 4173
CMD ["serve", "-s", "dist", "-l", "4173"]
