FROM ubuntu

# install necessary tools
RUN apt update
RUN yes | apt install python3-pip
RUN yes | apt install git
RUN pip3 install flask flask_bootstrap requests wikipedia

# create application folder
ENV APP_DIR "/app"

# clone from repository
RUN git clone https://github.com/AskNowQA/AskNowUI $APP_DIR

# export port
EXPOSE 8300

# run application
ENTRYPOINT /usr/bin/python3 $APP_DIR/app.py
