#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# Install nginx if not already installed
sudo apt-get update
if [[ ! -f "/etc/init.d/nginx" ]]; then
	sudo apt-get install -y nginx
fi

# Create deployment folders
sudo mkdir -p "/data/web_static/releases/test/"
sudo mkdir -p "/data/web_static/shared/"

# Create fakehtml file
sudo sh -c 'echo "Hello World!" > "/data/web_static/releases/test/index.html"'

# Re-create symbolic link
sudo ln -fs "/data/web_static/releases/test/" "/data/web_static/current"

# Update /data ownership
sudo chown -R ubuntu "/data/"
sudo chgrp -R ubuntu "/data/"

sudo sh -c "printf %s 'server {
	listen 80 default_server;
	listen [::]:80 default_server;
	add_header X-Served_By $HOSTNAME;
	root /var/www/html;
	index index.html index.htm;

	location /hbnb_static {
		alias /data/web_static/current;
		index index.html index.htm;
	}

	location /redirect_me {
		return 301 http://cuberule.com/;
	}

	error_page 404 /404.html;
	location /404 {
		root /var/www/html;
		internal;
	}
}' > /etc/nginx/sites-available/default"

sudo service nginx restart
