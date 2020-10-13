FROM mongo:3.6

WORKDIR /usr/src/build

RUN apt-get update

COPY . .

ENTRYPOINT ./wait-for-it.sh $HOST:$PORT -t 120 -- ./build.sh
CMD [""]

