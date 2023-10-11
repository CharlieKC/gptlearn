# pull official base image
FROM node:20

# set working directory
WORKDIR /usr/src/app

# install and cache app dependencies
COPY package.json .
COPY package-lock.json .

# RUN npm install
RUN npm ci

COPY . .

# start app
CMD ["npm", "run", "dev"]
