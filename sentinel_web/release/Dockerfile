FROM node:alpine as build

WORKDIR /app
COPY package.json yarn.lock tslint.json tsconfig.json /app/
RUN yarn install

COPY config /app/config 
COPY public /app/public
COPY src /app/src

RUN yarn build

RUN mkdir -p /config
COPY release /config

FROM nginx:1.13-alpine

RUN mkdir -p /app

COPY --from=build /app/config/deploy /usr/share/nginx/html
COPY --from=build /config/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /config/config_and_run.sh /app
COPY --from=build /config/config.js.tmpl /app

RUN chmod +x /app/config_and_run.sh
ENTRYPOINT /app/config_and_run.sh 
