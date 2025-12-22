# # Use slim python image
# FROM python:3.11-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# # Install system deps
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     default-libmysqlclient-dev \
#     gcc \
#  && rm -rf /var/lib/apt/lists/*

# # Copy requirements
# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# # Copy backend code ONLY
# COPY . .

# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app    

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    wget \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:$PORT app:app"]





# FROM python:3.11-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt  # Try this first
# COPY backend/ .
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
