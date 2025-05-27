# Etap 1: budowanie zależności
FROM python:3.12-slim AS builder
 
LABEL org.opencontainers.image.authors="Jan Kowalski"
 
WORKDIR /app
 
COPY requirements.txt .
 
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt
 
# Etap 2: końcowy obraz
FROM python:3.12-slim
 
WORKDIR /app
 
COPY --from=builder /install /usr/local
COPY . .
 
EXPOSE 5000
 
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
CMD curl -f http://localhost:5000 || exit 1
 
CMD ["python", "app.py"]