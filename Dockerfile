FROM ubuntu

# install necessary tools
RUN apt update
RUN yes | apt install python3-pip
RUN yes | apt install git

# create application folder
ENV APP_DIR "/app"

# clone from repository
RUN git clone https://github.com/AskNowQA/DeutscheQA $APP_DIR && \
    cd $APP_DIR && \
    git checkout master && \
    git checkout 616b276766ba6602eda73894a2b00af2f0797b44

# install dependencies
RUN pip3 install -r /app/requirements.txt
RUN python3 -m spacy download de

# export port
EXPOSE 8200

# run application
ENTRYPOINT /usr/bin/python3 $APP_DIR/app.py
