# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Blender
# Note: Update the Blender version and URL as needed
RUN apt-get update && apt-get install -y wget libfreetype6 libglu1-mesa libxi6 libxrender1 && \
    wget -q https://mirror.clarkson.edu/blender/release/Blender2.83/blender-2.83.0-linux64.tar.xz && \
    tar -xf blender-2.83.0-linux64.tar.xz -C /usr/local --strip-components=1 && \
    rm blender-2.83.0-linux64.tar.xz

# Optionally, if you need Blender's Python API to control Blender from an external Python script:
# Ensure Blender's Python version matches the container's Python version
# Install bpy or other modules as needed

# Install any additional dependencies
RUN apt-get install -y ffmpeg libsm6 libxext6

# Install Python dependencies
# Copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Set Blender's Python path (replace "2.83" with your version of Blender)
ENV BLENDER_PYTHON=/usr/local/2.83/python/bin/python3.7m

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME Poseify-Animation

CMD ["flask", "run", "--host=0.0.0.0"]