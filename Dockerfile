# Dockerfile

FROM python:3.12-slim

# set a working directory
WORKDIR /app

# install OS-level deps if you need any (e.g. ffmpeg), otherwise skip
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     ffmpeg \
#   && rm -rf /var/lib/apt/lists/*

# copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy your application code
COPY . .

# expose the port we’ll bind Gunicorn to
EXPOSE 13131

# run Gunicorn with 3 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:13131", "--workers", "3", "main:app"]
