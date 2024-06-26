# Use the official Python image from the Docker Hub
FROM python:3

# Set the working directory in the container
WORKDIR /Dashboard


# Copy the requirements file into the container
COPY Requirements.txt .

# Install the Python dependencies
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r Requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run the preprocess and db_init scripts
RUN python preprocess.py

# Expose the port Streamlit uses
EXPOSE 8501

# Command to run the Streamlit app
CMD ["sh","entrypoint.sh"]
