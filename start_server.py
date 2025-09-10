import os
import subprocess
import sys

# Start the FastAPI server with Socket.IO support from root
# Note: Using app_sio which includes Socket.IO ASGI app
subprocess.run([sys.executable, '-m', 'uvicorn', 'backend.app.main_new:app_sio', '--host', '0.0.0.0', '--port', '8000', '--reload'])
