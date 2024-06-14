FROM python:3.11
WORKDIR /app
ADD . .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8000", "flaskapp:app"]
