FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --default-timeout=100 -i https://pypi.org/simple/ -r requirements.txt
CMD ["python","manage.py","runserver","0.0.0.0:8000"]