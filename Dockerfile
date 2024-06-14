FROM python:3.11
WORKDIR /
ADD . /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "flaskapp.py" ]
