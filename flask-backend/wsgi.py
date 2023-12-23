import os
import sys

from app import app


# Add the project directory to the sys.path
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))))

if __name__ == "__main__":
    app.run()

