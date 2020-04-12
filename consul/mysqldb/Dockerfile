FROM mariadb
RUN  apt-get update -y
RUN  apt-get install -y python3-pip python3-dev build-essential
COPY . /mysql_config
WORKDIR /mysql_config
RUN pip3 install -r requirements.txt
RUN chmod 777 -R /mysql_config
ENTRYPOINT ["python3"]
CMD ["config.py"]