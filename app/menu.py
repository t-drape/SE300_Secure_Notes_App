"""
This file completes the requirements described in our SRD and SDD for the Menu class.
Trace Tag: [SDD_HLD_01_MENU]
"""

import datetime

from security_manager import SecurityManager
from db import DbConnect
from summarizer import Summarizer


# NOTE: NEED TO SWITCH TO USING TEMPFILES!
# FIX: Only use strings in the current terminal instance

# SDD_HLD_MENU_001
# o SDD_TT_3_002 o SDD_TT_3_003 o SDD_TT_3_006 o SDD_TT_3_010 o SDD_TT_3_014
# ▪ SRD::T_02 ▪ SRD::T_03 ▪ SRD::T_04 ▪ SRD::T_11 ▪ SRD::T_12 ▪ SRD::T_13 ▪ SRD::T_14 ▪ SRD::T_21 ▪ SRD::T_22 ▪ SRD::T_29 ▪ SRD::T_30 ▪ SRD::T_39 ▪ SRD::T_44 ▪ SRD::T_45

# • SDD_HLD_MENU_002
# SDD_TT_3_001 o SDD_TT_3_005 o SDD_TT_3_007 o SDD_TT_3_008 SDD_TT_3_009 o SDD_TT_3_012
# SRD::T_06 ▪ SRD::T_11 ▪ SRD::T_12 ▪ SRD::T_13 ▪ SRD::T_14 ▪ SRD::T_19 ▪ SRD::T_23 ▪ SRD::T_53 ▪ SRD::T_54

# • SDD_HLD_MENU_003
# o SDD_TT_3_003 o SDD_TT_3_004 o SDD_TT_3_010 o SDD_TT_3_011
# ▪ SRD::T_02 ▪ SRD::T_04 ▪ SRD::T_12 ▪ SRD::T_13 ▪ SRD::T_14 ▪ SRD::T_20 ▪ SRD::T_28 ▪ SRD::T_29 ▪ SRD::T_31 ▪ SRD::T_39 ▪ SRD::T_43


class Menu():
    """This class implements the requirements defined in the SRD and the features defined in the SDD for the Menu Class"""
    def __init__(self):
        self.DB_DIR_NAME = "Notes"
        self.security = SecurityManager()
        self.db = DbConnect()
        self.Ai = Summarizer()
        self.__password = self.__get_password()
        # This line allows me to make a function call directly by using the returned user choice as an index (allows passing the file still)
        self.possible___actions = [self.__new_note, self.__display_note, self.__append, self.__summarize, self.__delete]

    # Helper methods for encryption/decryption
    def __get_plaintext(self, encrypted_content : str):
        """Gets the encrypted note content passed as a string, then calls the appropriate SecurityManager function to 
        decrypt the content into plaintext.
        
        Trace Tags:
        """

        # get encrypted bytes from DB and decrypt it
        # encrypted_data = System.db.get_note(file)
        # with open(file, "rb") as f:
        #     encrypted_data = f.read()
        plaintext = self.security.decrypt_note(encrypted_content, self.__password)
        if plaintext is None:
            print("Error: could not decrypt note.")
        return plaintext

    def __encrypt_and_save(self, plaintext, file):
        """
        Receives the plaintext string of the note's content and the filename, encrypts the string, and then
        calls the appropriate DB function to save the note persistently.

        Trace Tags: SDD_TT_3_001
        """
        # encrypt and save to DB
        encrypted = self.security.encrypt_note(plaintext, self.__password)
        if encrypted is None:
            print("Error: could not encrypt note.")
            return
        
        self.db.create_note(self.DB_DIR_NAME, file, encrypted)
        
    # NOTE: Overlapping functionality with __encrypt_and_save
    # FIX: Having two functions does nothing to improve readability. This code is fine. 

    def __generate_filename(self):
        """Generate the filename for a new note based on the current date and current time (down to the second)

        Trace Tags: SDD_TT_3_002
        """
        # Use UTC for creating multiple files on the same day / no errors with timezone changes
        filename = datetime.datetime.now()
        # A file cannot be created in under 1 second, at least for humans
        filename = filename.strftime("%B_%d_%Y_%I_%M_%S_%p.txt")
        print(f"Filename: {filename}")
        return filename
    
    # Tests for __generate_filename():
        # Does it create the correct date in UTC format?
        # Does it create an altered string for the filename?

    # NOTE: Will call a DB function to show all files in the DB
    def __choose_file(self):
        """
        Allows a user to __select the file they wish to perform an __action on.

        Trace Tags: SDD_TT_3_003
        """

        files = self.db.list_in_directory(self.DB_DIR_NAME)
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
        # chosen_file = input("What file would you like to perform this __action on?: ")
        # if chosen_file in files:
        #     return chosen_file
        # else:
        #     print("I'm sorry, that file doesn't exist. Please __select a file from the ones shown.")
        #     file = self.__choose_file()
        #     print(file)

        # Test cases for __choose_file:
            # Disallows invalid files?
            # Correctly returns valid files?

    # NOTE: Must first check to see if the file is not already __deleted, a DB function
    def __confirm___delete(self, file):
        """Ensure user confirms desired deletion.

        Trace Tags: SDD_TT_3_004
        """
        if self.db.verify_integrity(self.DB_DIR_NAME, file):
            confirmation = False
            answer = input(f"Are you sure you want to __delete {file}? This __action cannot be reversed. [Y or y for yes]\nAnswer: ").lower()
            if (answer == "y"):
                confirmation = True
            return confirmation
    
        # Test Cases for __confirm___delete():
            # Does it work with uppercase y (Y)?
            # Does it work with lowercase y (y)?
            # Do integer values break it?
            # Does it return boolean values?

    def __new_note(self, file):
        """
        Allow a user to create a new note using the terminal

        Trace Tags: SDD_TT_3_005
        """
        note = input(f"{file}: ")
        self.__encrypt_and_save(note, file)

    def __get_encrypted_note_content_from_DB(self, file):
        """Return file content from the saved note in the DB.

        """
        encrypted_content = self.db.__display_note(self.DB_DIR_NAME, file)
        return encrypted_content

    def __display_note(self, file):
        """
        Receives encrypted note content, Calls the appropriate decrypt function, and then prints plaintext to the output window.

        Trace Tags: SDD_TT_3_006
        """
        # encrypted_content = self.db.__display_note("Notes", file)
        # decrypted_file_contents = self.__get_plaintext(encrypted_content)
        decrypted = self.__get_plaintext(self.__get_encrypted_note_content_from_DB(file))
        print(decrypted)

    def __append(self, file):
        """
        Receives an encrypted string from the DB. Then, it prompts the user to add to the given string. It then 
        re-encrypts the content, and saves it to the DB using the appropriate update function.

        Trace Tags: SDD_TT_3_007
        """
        encrypted_content = self.__get_encrypted_note_content_from_DB(file)
        decrypted_content = self.__get_plaintext(encrypted_content)
        new_content = input(f"{file}: {decrypted_content}\nYou cannot overwrite this data. However, you can add to it. Make sure to add a space if needed:\n")
        __appended_string = decrypted_content + new_content
        self.db.update_note(self.DB_DIR_NAME, file, self.security.encrypt_note(__appended_string, self.__password))
        # with open(f)
        # self.open_and_wait(file)
        # Ensure the file is not empty
        # Save changes to the file

    def __summarize(self, file):
        """
        Receives encrypted note content, Calls the appropriate decrypt function, passes the plaintext as
        a string to the AI class instance summary function, and then prints the returned string to the output window 

        Trace Tags: SDD_TT_3_008
        """
        decrypted_content = self.__get_plaintext(self.__get_encrypted_note_content_from_DB(file))
        if decrypted_content:
            print((self.Ai.summarize(decrypted_content)))
        else:
            print("Error: Could not __summarize note.")

    def __delete(self, file):
        """
        Calls __confirm___delete to ensure no mistaken hard __deletes occur, and then calls the associated
        DB function to permanently __delete the file from memory

        Trace Tags: SDD_TT_3_009
        """
        if self.__confirm___delete(file):
            self.db.delete_note(self.DB_DIR_NAME,file)
        else:
            print("Aborting Deletion.")
    
    # Test cases for __delete():
        # Does the function call __confirm___delete before calling DB.__delete()?

    def __select(self):
        """Allow user to __select their desired __action and file, gracefully handling invalid input. 
        Converts string input to an integer, and then returns that integer. Calls __choose_file for 
        non-creation __actions and calls __generate_filename for __new_note. It returns the filename and 
        integer together as a tuple.
        
        Trace Tags: SDD_TT_3_010
        SDD_HLD_MENU_001, SDD_HLD_MENU_002
        """
        answer = input("""
    Note: To exit the program press ^C, (CTRL key, then C key)
    What action would you like to perform?
    (Input the number of the __selected __action)
        1. Create Note
        2. Display Note
        3. Change Note
        4. Summarize Note
        5. Delete Note
        6. Exit Program
    Answer: """)
        try:
            answer = int(answer)
            if answer in range(1,6):
                if (answer == 1):
                    file = self.__generate_filename()
                else:
                    file = self.__choose_file()
                if file:
                    return (answer, file)
                else:
                    print("Error with file. Aborting and returning to Menu.")
            elif (answer == 6):
                return [answer, None]
            else:

                print("""
    Invalid Input. 
    Aborting __action and returning to Menu.""")
                
                return self.__select()
            
        except ValueError:

            print("""
    Invalid Input. 
    Aborting __action and returning to Menu.""")
            
        return self.__select()
    
    # Test Cases for __select():
        # Does it work with valid input (1-5)?
        # Does it handle numeric values not in range (1-5)?
        # Does it handle non-numeric inputs?
        # Does it return an error value if an error occurs?
        # Does it return a useful value if the code runs properly?
    
    def __get_password(self):
        """
        Queries the user for their password. Each file is associated with a password, and can only be decrypted
        with that ex__act password. This allows multiple users to have the same DB without exposing their private information.
        (Assuming all parties have a unique password)

        Trace Tags: SDD_TT_3_011
        SDD_HLD_MENU_003
        """
        password = input("What is your password? ")
        return password
    
    # Test cases for __get_password():
        # Does it work with no user input?
        # Does it work with valid user input?

    # NOTE: Must connect this with __choose_file, so that display cannot be called with "None"
    def __act(self, __selected___action, filename):
        """
        Calls the __select function to allow a user to pick their desired __action, maps the returned integer to the 
        associated function, and then calls that function. If a filename is not provided, then the program will generate
        a new file by calling the __generate_filename function.

        Trace Tags: SDD_TT_3_012
        SDD_HLD_MENU_001, SDD_HLD_MENU_002, SDD_HLD_MENU_003
        """

        if (__selected___action == 6):
            return False

        if __selected___action:
            self.possible___actions[__selected___action-1](filename)
            return True
        else:
            print("Invalid __action. Aborting all further __action and returning to Menu.")
    # Test cases for __act(__selected___action, file):
        # Does the index match the correct chosen __action?
        # Does the index pass a file correctly?
        # Does the index generate a filename if None is specified

    def run(self):
        """
        Main Loop that will run until the user exits the program. It will continually prompt the user
        with the menu, and then run the __selected __action. It then returns to the menu and repeats.

        Trace Tags: SDD_HLD_MENU_002
        """

        print("Welcome to the Secure Notes Application")
        run_flag = True
        while run_flag:
            [action, file] = self.__select()
            run_flag = self.__act(action, file)
