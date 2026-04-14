import datetime
import subprocess
import platform
import os

from security_manager import SecurityManager
from db import DbConnect, _DbConnectError
from summarizer import Summarizer


# NOTE: NEED TO SWITCH TO USING TEMPFILES!
# FIX: Only use strings in the current terminal instance


DB_DIR_NAME = "Notes"



class Menu():
    """This class implements the requirements defined in the SRD and the features defined in the SDD for the Menu Class"""
    def __init__(self):
        self.security = SecurityManager()
        self.db = DbConnect()
        self.Ai = Summarizer()
        self.__password = self.get_password()
        # This line allows me to make a function call directly by using the returned user choice as an index (allows passing the file still)
        self.possible_actions = [self.new_note, self.display_note, self.append, self.summarize, self.delete]

    # Helper methods for encryption/decryption
    def get_plaintext(self, encrypted_content : str):
        # get encrypted bytes from DB and decrypt it
        # encrypted_data = System.db.get_note(file)
        # with open(file, "rb") as f:
        #     encrypted_data = f.read()
        plaintext = self.security.decrypt_note(encrypted_content, self.__password)
        if plaintext is None:
            print("Error: could not decrypt note.")
        return plaintext

    def encrypt_and_save(self, plaintext, file):
        """
        Receives the plaintext string of the note's content and the filename, encrypts the string, and then
        calls the appropriate DB function to save the note persistently.
        """
        # encrypt and save to DB
        encrypted = self.security.encrypt_note(plaintext, self.__password)
        if encrypted is None:
            print("Error: could not encrypt note.")
            return
        
        self.db.create_note(DB_DIR_NAME, file, encrypted)
        
    # NOTE: Overlapping functionality with encrypt_and_save
    # FIX: Having two functions does nothing to improve readability. This code is fine. 

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

    # NOTE: Will call a DB function to show all files in the DB
    def choose_file(self):
        """
        Allows a user to select the file they wish to perform an action on
        """

        files = self.db.list_in_directory(DB_DIR_NAME)
        if files:
            print("All available files: ")
            print(files)
            chosen_file = input("What file? Type it here: ")
            if chosen_file in files:
                return chosen_file
        return None
        
        # files = [item for item in os.listdir() if os.path.isfile(item)]
        # # Change to showing all files on the DB
        # print(files)
        # chosen_file = input("What file would you like to perform this action on?: ")
        # if chosen_file in files:
        #     return chosen_file
        # else:
        #     print("I'm sorry, that file doesn't exist. Please select a file from the ones shown.")
        #     file = self.choose_file()
        #     print(file)

        # Test cases for choose_file:
            # Disallows invalid files?
            # Correctly returns valid files?

    # NOTE: Must first check to see if the file is not already deleted, a DB function
    def confirm_delete(self, file):
        """Ensure user confirms desired deletion"""
        if self.db.verify_integrity(DB_DIR_NAME, file):
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
        """
        Allow a user to create a new note using the terminal
        """
        note = input(f"{file}: ")
        self.encrypt_and_save(note, file)

    def get_encrypted_note_content_from_DB(self, file):
        """Return file content from the saved note in the DB"""
        encrypted_content = self.db.display_note(DB_DIR_NAME, file)
        return encrypted_content

    def display_note(self, file):
        """
        Receives encrypted note content, Calls the appropriate decrypt function, and then prints plaintext to the output window
        """
        # encrypted_content = self.db.display_note("Notes", file)
        # decrypted_file_contents = self.get_plaintext(encrypted_content)
        decrypted = self.get_plaintext(self.get_encrypted_note_content_from_DB(file))
        print(decrypted)

    def append(self, file):
        """
        Receives an encrypted string from the DB. Then, it prompts the user to add to the given string. It then 
        re-encrypts the content, and saves it to the DB using the appropriate update function.
        """
        encrypted_content = self.get_encrypted_note_content_from_DB(file)
        decrypted_content = self.get_plaintext(encrypted_content)
        new_content = input(f"{file}: {decrypted_content}\nYou cannot overwrite this data. However, you can add to it. A space is already added:\n")
        appended_string = decrypted_content + " " + new_content
        self.db.update_note(DB_DIR_NAME, file, self.security.encrypt_note(appended_string, self.__password))
        # with open(f)
        # self.open_and_wait(file)
        # Ensure the file is not empty
        # Save changes to the file

    def summarize(self, file):
        """
        Receives encrypted note content, Calls the appropriate decrypt function, passes the plaintext as
        a string to the AI class instance summary function, and then prints the returned string to the output window 
        """
        decrypted_content = self.get_plaintext(self.get_encrypted_note_content_from_DB(file))
        if decrypted_content:
            print((self.Ai.summarize(decrypted_content)))
        else:
            print("Error: Could not summarize note.")

    def delete(self, file):
        """
        Calls confirm_delete to ensure no mistaken hard deletes occur, and then calls the associated
        DB function to permanently delete the file from memory
        """
        if self.confirm_delete(file):
            self.db.delete_note(DB_DIR_NAME,file)
        else:
            print("Aborting Deletion.")
    
    # Test cases for delete():
        # Does the function call confirm_delete before calling DB.delete()?

    def select(self):
        """Allow user to select their desired action and file, gracefully handling invalid input. 
        Converts string input to an integer, and then returns that integer. Calls choose_file for 
        non-creation actions and calls generate_filename for new_note. It returns the filename and 
        integer together as a tuple."""
        answer = input("""
    Note: To exit the program press ^C, (CTRL key, then C key)
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
                if (answer == 1):
                    file = self.generate_filename()
                else:
                    file = self.choose_file()
                if file:
                    return (answer, file)
                else:
                    print("Error with file. Aborting and returning to Menu.")
            else:

                print("""
    Invalid Input. 
    Aborting action and returning to Menu.""")
                
                return self.select()
            
        except ValueError:

            print("""
    Invalid Input. 
    Aborting action and returning to Menu.""")
            
        return self.select()
    
    # Test Cases for select():
        # Does it work with valid input (1-5)?
        # Does it handle numeric values not in range (1-5)?
        # Does it handle non-numeric inputs?
        # Does it return an error value if an error occurs?
        # Does it return a useful value if the code runs properly?
    
    def get_password(self):
        """
        Queries the user for their password. Each file is associated with a password, and can only be decrypted
        with that exact password. This allows multiple users to have the same DB without exposing their private information.
        (Assuming all parties have a unique password)
        """
        password = input("What is your password? ")
        return password
    
    # Test cases for get_password():
        # Does it work with no user input?
        # Does it work with valid user input?

    # NOTE: Must connect this with choose_file, so that display cannot be called with "None"
    def act(self, selected_action, filename):
        """
        Calls the select function to allow a user to pick their desired action, maps the returned integer to the 
        associated function, and then calls that function. If a filename is not provided, then the program will generate
        a new file by calling the generate_filename function.
        """

        if selected_action:
            self.possible_actions[selected_action-1](filename)
        else:
            print("Invalid action. Aborting all further action and returning to Menu.")
    # Test cases for act(selected_action, file):
        # Does the index match the correct chosen action?
        # Does the index pass a file correctly?
        # Does the index generate a filename if None is specified

    def run(self):
        print("Welcome to the Secure Notes Application")
        while True:
            [action, file] = self.select()
            self.act(action, file)


m = Menu()
m.db.create_directory(DB_DIR_NAME)
m.run()
