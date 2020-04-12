FROM egaraev/basecentos:latest
RUN yum install -y python-pip
COPY . /usr/local/bin/
WORKDIR /usr/local/bin
RUN pip install -r requirements.txt
RUN chmod +x *.sh
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Europe/Warsaw /etc/localtime
ENTRYPOINT ["/usr/local/bin/start.sh"]
