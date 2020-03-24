FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf \
    && rm /etc/nginx/nginx.conf
    
COPY ["project.template", "/etc/nginx/conf.d/project.template"]
COPY ["nginx.conf", "/etc/nginx/"]
