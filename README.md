# DeutscheQA


## Run application within docker container
You could build and run docker with following instructions.

### Build docker image

`sudo docker build -t asknow .`

### Run docker container

`sudo docker run -d -p 8200:8200 --name fhg_asknow asknow`