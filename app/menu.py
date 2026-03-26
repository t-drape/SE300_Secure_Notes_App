import datetime
import subprocess
import platform
import sys

print("Welcome to the Secure Notes Application")



class Menu():
    """This class implements the requirements defined in the SRD and the features defined in the SDD for the Menu Class"""
    def __init__(self):
        # password = self.get_password()
        # This line allows me to make a function call directly by using the returned user choice as an index (allows passing the file still)
        self.possible_actions = [self.new_note, self.display, self.append, self.summarize, self.delete]

    
    def save(self, file):
        pass

    def generate_filename(self):
        """Generate the filename for a new note based on the current date and current time (down to the second)"""
        # Use UTC for creating multiple files on the same day / no errors with timezone changes
        filename = datetime.datetime.now()
        # A file cannot be created in under 1 second, at least for humans
        filename = filename.strftime("%B_%d_%Y_%I_%M_%S_%p.txt")
        print(f"Filename: {filename}")
        return filename
    
    # Tests for generate_filename():
        # Does it create the correct date in UTC format?
        # Does it create an altered string for the filename?

    def choose_file(self):
        pass
        # print("What file would you like to perform this action on?")

    def confirm_delete(self, file):
        """Ensure user confirms desired deletion"""
        confirmation = False
        answer = input(f"Are you sure you want to delete {file}? This action cannot be reversed. [Y or y for yes]\nAnswer: ").lower()
        if (answer == "y"):
            confirmation = True
        return confirmation
    
        # Test Cases for confirm_delete():
            # Does it work with uppercase y (Y)?
            # Does it work with lowercase y (y)?
            # Do integer values break it?
            # Does it return boolean values?

    def new_note(self, file):
        with open(file, "w") as f:
            # Creates a file header
            # heading = f"Title: {file}"
            # f.write(heading)
            pass
            # Creates the file without a header
        self.open_and_wait(file)

        # Still need to save the file to the DB
        # Ensure the file is not empty
        # Save file
            

    def open_and_wait(self, filepath):
        """
        Opens a file with its default application and waits for the application to close.
        Code by Google AI, (Google AI Overview, 2026)
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

    def display(self, file):
        """
        Sources: Google AI overview of reading all lines from a file
        """
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                print(line)

    def append(self, file):
        self.open_and_wait(file)
        # Ensure the file is not empty
        # Save changes to the file

    def summarize(self, file):
        pass

    def delete(self, file):
        self.confirm_delete(file)
        print("Hello There")
    
    # Test cases for delete():
        # Does the function call confirm_delete before calling DB.delete()?

    def select(self):
        """Allow user to select their desired action, gracefully handling invalid input"""
        answer = input("""
    What action would you like to perform?
    (Input the number of the selected action)
        1. Create Note
        2. Display Note
        3. Change Note
        4. Summarize Note
        5. Delete Note
    Answer: """)
        try:
            answer = int(answer)
            if answer in range(1,6):
                return answer
            else:
                print("""
    Invalid Input. 
    Aborting action and returning to Menu.""")
                return -1
        except ValueError:
            print("""
    Invalid Input. 
    Aborting action and returning to Menu.""")
        return -1
    
    # Test Cases for select():
        # Does it work with valid input (1-5)?
        # Does it handle numeric values not in range (1-5)?
        # Does it handle non-numeric inputs?
        # Does it return an error value if an error occurs?
        # Does it return a useful value if the code runs properly?
    
    def get_password(self):
        password = input("What is your password? ")
        return password
    
    # Test cases for get_password():
        # Does it work with no user input?
        # Does it work with valid user input?

    def act(self, selected_action, filename=None):
        if filename is None:
            filename = self.generate_filename()
        self.possible_actions[selected_action-1](filename)
    # Test cases for act(selected_action, file):
        # Does the index match the correct chosen action?
        # Does the index pass a file correctly?
        # Does the index generate a filename if None is specified

m = Menu()
m.act(3, "March_26_2026_01_04_33_PM.txt")
# m.act(4)