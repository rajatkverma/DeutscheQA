FROM ubuntu

# install necessary tools
RUN apt update
RUN yes | apt install python3-pip
RUN yes | apt install git

# create application folder
ENV APP_DIR "/app"

# clone from repository
RUN git clone https://github.com/AskNowQA/DeutscheQA $APP_DIR

# install dependencies
RUN pip3 install -r /app/requirements.txt

# export port
EXPOSE 8200

# run application
ENTRYPOINT /usr/bin/python3 $APP_DIR/app.py
