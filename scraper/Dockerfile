FROM python:3.9-bullseye
RUN pip install git+https://github.com/kevinzg/facebook-scraper.git pydantic
WORKDIR /app
ADD . /app
CMD ["python", "main.py"]