FROM python:3.11-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY bot/ ./bot/

# Create logs directory
RUN mkdir -p /workspace/logs

# Set environment variables
ENV PYTHONPATH=/workspace

# Run the bot
CMD ["python", "-m", "bot.main"]