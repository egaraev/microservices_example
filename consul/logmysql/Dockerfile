FROM egaraev/basecentos:latest
RUN yum install -y python-pip
COPY . /logmysql
WORKDIR /logmysql
RUN pip install -r requirements.txt
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Europe/Warsaw /etc/localtime
RUN chmod +x /logmysql/start.sh
#ENTRYPOINT ["python"]
#CMD ["app.py"]
ENTRYPOINT ["/logmysql/start.sh"]