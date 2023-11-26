FROM python:3.10

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy main files
COPY . .

# Set working directory
WORKDIR /main

# Run the main
EXPOSE 5000
CMD ["python", "run.py"]