# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Move into the frontend directory to run the Streamlit app
WORKDIR /app/frontend

# Run Streamlit
CMD ["streamlit", "run", "app.py"]
