FROM nginx:stable

RUN apt-get update && apt-get install -y tor

COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /usr/share/nginx/html/index.html
COPY juisy-melons.jpg /usr/share/nginx/html/juisy-melons.jpg
COPY torrc /etc/tor/torrc

EXPOSE 8080 9050 4243

# Start both Tor and Nginx
CMD service tor start && nginx -g 'daemon off;'