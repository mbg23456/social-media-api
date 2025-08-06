FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY environment.yml ./

# Install dependencies
RUN conda env create -f environment.yml

# Copy the rest of the application code into the container
# Current directory (.) -> working directory (. on a relative basis, ./usr/src/app in full)
# Use the cached result -- only this step will be re-run if source code changes
COPY . .

# Make RUN commands use the new environment:
#SHELL ["conda", "run", "-n", "webdev", "/bin/bash", "-c"]

# Spaces are split into different strings
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# ...existing code...
CMD ["conda", "run", "--no-capture-output", "-n", "webdev", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


