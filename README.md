# DeutscheQA


## Run DeutscheQA within docker container
You could build and run docker with the following instructions.

### Build docker image

`sudo docker build -t asknow .`

### Run docker container

`sudo docker run -d -p 8200:8200 --name fhg_asknow asknow`

## Run the UI part within docker container
After entering the "ui" directory of the project, you could build and run docker with the following instructions.

### Build docker image

`sudo docker build -t asknowui .`

### Run docker container

`sudo docker run -d -p 8300:8300 --name fhg_asknowui asknowui`
