FROM python:3.7
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
EXPOSE  80
CMD ["python", "/app/main2.py"]