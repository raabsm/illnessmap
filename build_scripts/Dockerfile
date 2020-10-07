FROM mongo:latest

WORKDIR /usr/src/build

RUN apt-get update && apt-get install -y python3 python3-pip
#RUN apt-get -y install python3.8-dev

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["./build.sh"]
CMD [""]

