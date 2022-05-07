FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /web_django
WORKDIR /web_django
COPY requirements.txt /web_django/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /web_django/
EXPOSE 8000
CMD ["run.sh"]
CMD python /web_django/manage.py migrate
CMD python /web_django/manage.py runserver
