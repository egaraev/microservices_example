FROM egaraev/basecentos:latest
COPY . /usr/local/bin/
WORKDIR /usr/local/bin
RUN mkdir static/images
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "/usr/local/bin/server.py"]
