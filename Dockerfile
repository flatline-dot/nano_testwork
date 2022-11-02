FROM python:3.8
RUN mkdir /nano_testwork
COPY . /nano_testwork
WORKDIR /nano_testwork
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3", "app/db.py"]