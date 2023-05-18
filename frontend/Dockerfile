FROM node

WORKDIR /frontend

# install app dependencies
COPY package.json /frontend

RUN npm install

# add app
COPY . /frontend
EXPOSE 3000

# start app
CMD ["npm", "start"]
