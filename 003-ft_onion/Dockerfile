FROM nginx:stable

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir -p /var/run/sshd
RUN echo "root:rootpasswd" | chpasswd
#RUN id -u lolale &>/dev/null || useradd -m -p $(openssl passwd -1 'lolalepasswd') lolale
#RUN id -u lolale &>/dev/null || useradd -m lolale
#RUN echo "lolale:lolalepasswd" | chpasswd
#RUN mkdir -p /home/lolale/.ssh
#RUN chmod 700 /home/lolale/.ssh

COPY sshd_config /etc/ssh/sshd_config
COPY index.html /usr/share/nginx/html/index.html
COPY juicy-melons.jpg /usr/share/nginx/html/juicy-melons.jpg
COPY nginx.conf /etc/nginx/nginx.conf


# Start both Tor and Nginx
CMD ["sh", "-c", "service ssh start && nginx -g 'daemon off;'"]
