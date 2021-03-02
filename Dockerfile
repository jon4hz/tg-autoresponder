FROM python:3.8-alpine
LABEL Author="jon4hz" 
LABEL version="1"
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN mkdir /usr/src/app/data
RUN pip install --upgrade pip &&\ 
    pip install --no-cache-dir -r requirements.txt
COPY autoresponder.py data/*.session ./
RUN chown -R 1000. *
USER 1000
ENTRYPOINT [ "python", "-u", "autoresponder.py" ]