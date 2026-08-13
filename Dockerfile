# Use Playwright official Python image which includes browsers + OS deps
FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app

# Copy only requirements first to leverage cache
COPY requirements.txt .

# Install python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the repo
COPY . .

# Expose the port Railway uses (Railway sets $PORT at runtime)
ENV PORT=8000

# Start command (Railway will override with its own start if configured)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
