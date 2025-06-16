# Use an official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy your app files
COPY main.py pokedex_(Update_05.20).csv ./

# Install dependencies
RUN pip install --no-cache-dir bokeh pandas

# Expose the default Bokeh port
EXPOSE 5006

# Run the Bokeh server
CMD ["bokeh", "serve", "--show", "--allow-websocket-origin=*", "main.py"]