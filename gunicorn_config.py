# gunicorn_config.py

# This is the address and port Gunicorn will listen on.
# 0.0.0.0 means it will listen on all available network interfaces.
# Render provides the port number via an environment variable.
bind = "0.0.0.0:7860"

# Number of worker processes to handle requests.
# For a free tier, 2 is a good starting point.
workers = 2

# CRITICAL: Set a long timeout.
# The default is 30 seconds. Loading a large ML model can take longer.
# This gives the worker 300 seconds (5 minutes) to start up before
# Render's health check assumes it has failed.
timeout = 300

# Set the log level for more detailed output during debugging.
loglevel = "info"
