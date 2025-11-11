FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# install requirements
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY /src/. /app/

# Run the app in port 80
EXPOSE 80

CMD ["fastapi", "run", "app.py", "--port", "80"]