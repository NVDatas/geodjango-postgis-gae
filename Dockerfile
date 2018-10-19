FROM asia.gcr.io/google_appengine/python

# Install dependencies library
RUN apt-get update -y && \
    apt-get install --no-install-recommends -y -q \
        binutils \
        gdal-bin \
        python-gdal && \
    apt-get clean && \
    rm /var/lib/apt/lists/*_*

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
RUN virtualenv /env -p python3.6

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Add the application source code.
ADD . /app

# Run a WSGI server to serve the application. gunicorn must be declared as
# a dependency in requirements.txt.
CMD bash -c "sh ./config/startup.sh && gunicorn --chdir ./app/ -b :$PORT wsgi"
