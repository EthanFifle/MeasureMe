# Use a slim version of Python image to reduce size
FROM python:3.7.7-slim

# Set the working directory
WORKDIR /SMPL-Anthropometry

# Copy only the requirements.txt file to leverage Docker cache
COPY requirements.txt .

# Install dependencies in a single RUN command and clean up after installation
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        # Add only necessary packages here, e.g., libgomp1 for PyTorch
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of your application's code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
