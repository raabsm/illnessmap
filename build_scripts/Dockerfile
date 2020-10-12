FROM mongo:latest

WORKDIR /usr/src/build

RUN apt-get update

COPY . .

ENTRYPOINT ["./wait-for-it.sh", "$HOST:$PORT", "--", "./build.sh"]
CMD [""]

