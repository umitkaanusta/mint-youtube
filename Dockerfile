FROM python:3

WORKDIR /app

COPY . /app

RUN pip install Cython
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python run.py