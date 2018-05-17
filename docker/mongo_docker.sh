sudo docker run --restart=always --name p-mongo -p 27017:27017 -v ${PWD}/data_mongo:/data/db -d mongo
