import os
import sys

# Ensure the source directory is in the system path for module resolution
# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

if __name__ == "__main__":
    from src import app
