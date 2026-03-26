import subprocess
import platform
import sys

def open_and_wait(filepath):
    """
    Opens a file with its default application and waits for the application to close.
    """
    if platform.system() == "Windows":
        # 'start' command on Windows opens the file using its associated application
        # and requires shell=True to work correctly.
        subprocess.run(['start', filepath], shell=True, check=True)
    elif platform.system() == "Darwin": # macOS
        subprocess.run(['open', filepath], check=True)
    else: # Linux/other POSIX
        # xdg-open is a common utility for this purpose
        subprocess.run(['xdg-open', filepath], check=True)

# --- Main program flow ---
file_to_open = 'your_file.txt' # Replace with your file's path
# You can create a dummy file for testing if needed:
with open(file_to_open, 'w') as f:
    f.write("Hello, world!")

print(f"Opening {file_to_open}...")
try:
    open_and_wait(file_to_open)
    print(f"'{file_to_open}' has been closed. Resuming Python program.")
    # Your program continues here after the file/application is closed
    print("Program finished.")
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
except FileNotFoundError:
    print(f"Error: The file '{file_to_open}' was not found.")

