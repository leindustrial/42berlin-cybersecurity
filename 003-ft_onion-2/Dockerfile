FROM nginx:stable

RUN apt-get update && apt-get install -y openssh-server

COPY index.html /usr/share/nginx/html/index.html
COPY juisy-melons.jpg /usr/share/nginx/html/juisy-melons.jpg
COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /run/sshd
RUN chmod 0755 /run/sshd
RUN echo "Port 4242" >> /etc/ssh/sshd_config
RUN useradd -m onion && echo "onion:onionpasswd" | chpasswd && mkdir -p /home/onion.ssh

# Start both Tor and Nginx
CMD ["sh", "-c", "service ssh start && nginx -g 'daemon off;'"]
