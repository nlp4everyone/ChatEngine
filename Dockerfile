FROM python:3.9-slim

# Set workdir
WORKDIR /workspace
COPY requirements.txt /workspace
# Install
RUN pip install -r requirements.txt
# Copy the rest
COPY . /workspace

EXPOSE 8005