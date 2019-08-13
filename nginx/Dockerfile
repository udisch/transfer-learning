FROM nginx

WORKDIR /app

COPY static/ /app/

COPY default.conf /etc/nginx/conf.d

# Install nodejs
RUN apt-get update
RUN apt-get install -y curl
# RUN apt-get -y install python-software-properties
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs

# Install angular-cli
RUN npm install -g @angular/cli

# Build frontend
RUN ng build

RUN cp -r /app/dist/frontend/* /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT service nginx start && tail -f /var/log/nginx/access.log
