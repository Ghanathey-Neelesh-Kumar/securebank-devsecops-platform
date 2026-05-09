FROM nginxinc/nginx-unprivileged:1.27-alpine

ENV BACKEND_UPSTREAM=http://backend:5000

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY src/ /usr/share/nginx/html/

EXPOSE 8080

