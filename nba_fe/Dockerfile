from node:alpine

RUN mkdir /web

WORKDIR /web

COPY package.json /web/package.json
RUN npm install

COPY . /web
RUN ls -a /web
EXPOSE  3000

CMD [ "npm", "start" ]