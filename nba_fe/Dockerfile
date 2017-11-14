from node:alpine

RUN mkdir /web

COPY . /web

WORKDIR /web

RUN npm install

EXPOSE  3000

CMD [ "npm", "start" ]
