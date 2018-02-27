# DeutscheQA

 
## Run DeutscheQA within docker container
Build and Run using the following instructions.

### Build docker image

`sudo docker build -t asknow .`

### Run docker container

`sudo docker run -d -p 8200:8200 --name fhg_asknow asknow`

## Run the UI part within docker container
After entering the "ui" directory of the project, Build and Run docker using the following instructions.

### Build docker image

`sudo docker build -t asknowui .`

### Run docker container

`sudo docker run -d -p 8300:8300 --name fhg_asknowui asknowui`
