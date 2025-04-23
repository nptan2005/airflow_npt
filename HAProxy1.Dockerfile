# Sử dụng hình ảnh chính thức của HAProxy
FROM haproxy:latest

# Copy file cấu hình haproxy.cfg vào container
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

# Copy chứng chỉ SSL
COPY server.pem /usr/local/etc/haproxy/server.pem

# Expose port cho TLS/SSL
EXPOSE 443
