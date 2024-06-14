FROM python:3.11
WORKDIR /
ADD . /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8000", "myapp:app"]
