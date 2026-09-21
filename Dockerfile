# syntax=docker/dockerfile:1

# Build stage. Node is needed to produce dist/ and nothing after that.
FROM node:24-alpine AS build
WORKDIR /app

# Manifests first so the dependency layer caches independently of source edits.
COPY portfolio-site/package.json portfolio-site/package-lock.json ./
RUN npm ci

COPY portfolio-site/ ./
RUN npm run build

# Runtime stage. Carries dist/ and nginx, no Node and no build toolchain.
# nginx-unprivileged runs as uid 101 and listens on 8080, which avoids
# fighting the root-owned pid and cache paths in the stock nginx image.
FROM nginxinc/nginx-unprivileged:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY portfolio-site/nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -q --spider http://127.0.0.1:8080/ || exit 1
