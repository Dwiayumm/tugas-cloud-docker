# Gunakan image Python versi ringan
FROM python:3.9-alpine

# Set direktori kerja di dalam kontainer
WORKDIR /code

# Set variabel untuk Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install dependensi dasar Alpine
RUN apk add --no-cache gcc musl-dev linux-headers

# Copy file requirements dan install
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Expose port 5000 agar bisa diakses
EXPOSE 5000

# Copy sisa kode aplikasi
COPY . .

# Perintah untuk menjalankan aplikasi
CMD ["flask", "run"]