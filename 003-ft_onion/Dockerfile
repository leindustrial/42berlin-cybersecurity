FROM nginx:stable

RUN apt-get update && apt-get install -y tor
RUN apt-get update && apt-get install -y openssh-server

COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /usr/share/nginx/html/index.html
COPY juisy-melons.jpg /usr/share/nginx/html/juisy-melons.jpg
COPY torrc /etc/tor/torrc

RUN mkdir -p /run/sshd
RUN chmod 0755 /run/sshd
RUN echo "Port 4243" >> /etc/ssh/sshd_config
RUN useradd -m lola && echo "lola:lolapasswd" | chpasswd && mkdir -p /home/lola.ssh


# Start both Tor and Nginx
CMD service tor start && nginx -g 'daemon off;'
CMD ["sh", "-c", "service ssh start && service tor start && nginx -g 'daemon off;'"]
