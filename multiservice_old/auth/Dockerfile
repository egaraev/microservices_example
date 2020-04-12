FROM centos:latest
RUN yum install -y gcc python3-devel 
COPY . /auth
WORKDIR /auth
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["auth.py"]
