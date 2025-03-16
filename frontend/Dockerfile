FROM node:18

WORKDIR /app

RUN npm install -g pnpm

COPY package.json pnpm-lock.yaml ./
RUN pnpm i

COPY . .

RUN pnpm run build

CMD ["pnpm", "run", "start"]
