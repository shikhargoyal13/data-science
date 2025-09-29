# Use the official TensorFlow GPU image as the base image
FROM tensorflow/tensorflow:2.14.0-gpu

# Set the working directory inside the container
WORKDIR /tf/code

# Copy the current directory (project directory) to the container's working directory
COPY . /tf/code

# Install any necessary dependencies (like matplotlib)
RUN pip install --no-cache-dir -r /tf/code/requirements.txt

# Install any additional system dependencies if necessary
# RUN apt-get update && apt-get install -y <required-packages>

# Set environment variables if necessary (e.g., GPU usage)
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# Run the Python script (cnn_train.py) when the container starts
CMD ["python", "/tf/code/cnn_train_DA_Drop.py"]
