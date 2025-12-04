FROM python:3.11-slim

WORKDIR /app

# Install Node.js (required for Reflex)
RUN apt-get update && apt-get install -y curl unzip && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Initialize the app (creates .web directory)
# RUN reflex init

# Expose ports
EXPOSE 3000
EXPOSE 8001

# Run the app
CMD ["reflex", "run", "--loglevel", "info"]
