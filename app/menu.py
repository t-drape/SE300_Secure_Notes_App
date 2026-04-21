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
    """
    This class implements the requirements defined in the SRD and the features defined in the SDD for the Menu Class
    """
    def __init__(self):
        """
        Initialize Feature classes and class variables

        Trace Tags: SDD_HLD_MENU_002
                        SRD_T_30
                        SRD_T_31
                        SRD_T_39
        """
        self.DB_DIR_NAME = "Notes"
        self.security = SecurityManager()
        self.db = DbConnect()
        self.Ai = Summarizer()
        self.__password = self.__get_password()
        # This line allows me to make a function call directly by using the returned user choice as an index (allows passing the file still)
<<<<<<< HEAD
        self.possible___actions = [self.__new_note, self.__display_note, self.__append, self.__summarize, self.__delete]

    # Helper methods for encryption/decryption
    def __get_plaintext(self, encrypted_content : str):
        """Gets the encrypted note content passed as a string, then calls the appropriate SecurityManager function to 
        decrypt the content into plaintext.
        
        Trace Tags:
=======
        self.possible_actions = [self.new_note, self.display_note, self.append, self.summarize, self.delete]
        self.possible_actions_as_strings_for_display = ["Create Note", "Display Note", "Change Note", "Summarize Note", "Delete Note"]

    # Helper methods for encryption/decryption
    def get_plaintext(self, encrypted_content : str):
        """
        Get encrypted file content as a string, call the appropriate feature function to decrypt,
        and return a decrypt4ed string

        Trace Tags: SDD_HLD_MENU_002
                        SRD_T_21
                        SRD_T_44
                        SRD_T_45
>>>>>>> trace_tags
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

<<<<<<< HEAD
        Trace Tags: SDD_TT_3_001
=======
        Trace Tags: SDD_HLD_MENU_002
                        SDD_TT_3_001
                            SRD_T_05
                            SRD_T_19
                            SRD_T_21
                            SRD_T_44
                            SRD_T_45

>>>>>>> trace_tags
        """
        # encrypt and save to DB
        encrypted = self.security.encrypt_note(plaintext, self.__password)
        if encrypted is None:
            print("Error: could not encrypt note.")
            return
        
        self.db.create_note(self.DB_DIR_NAME, file, encrypted)
        
    # NOTE: Overlapping functionality with __encrypt_and_save
    # FIX: Having two functions does nothing to improve readability. This code is fine. 

<<<<<<< HEAD
    def __generate_filename(self):
        """Generate the filename for a new note based on the current date and current time (down to the second)

        Trace Tags: SDD_TT_3_002
=======
    def generate_filename(self):
        """
        Generate the filename for a new note based on the current date and current time (down to the second)
        
        Trace Tags: SDD_HLD_MENU_001
                        SDD_TT_3_002
>>>>>>> trace_tags
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
<<<<<<< HEAD
        Allows a user to __select the file they wish to perform an __action on.

        Trace Tags: SDD_TT_3_003
=======
        Allows a user to select the file they wish to perform an action on

        Trace Tags: SDD_HLD_MENU_002, SDD_HLD_MENU_003
                        SDD_TT_3_003
                            SRD_T_21
                            SRD_T_44
                            SRD_T_45
>>>>>>> trace_tags
        """

        files = self.db.list_in_directory(self.DB_DIR_NAME)
        if files:
            print("All available files: ")
            print(files)
            chosen_file = input("What file? Type it here: ")
            if chosen_file in files:
                return chosen_file
            else:
                print("Error: No such file exists. Are you sure you typed the filename correctly?")
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

<<<<<<< HEAD
    # NOTE: Must first check to see if the file is not already __deleted, a DB function
    def __confirm___delete(self, file):
        """Ensure user confirms desired deletion.

        Trace Tags: SDD_TT_3_004
=======
    # NOTE: Must first check to see if the file is not already deleted, a DB function
    def confirm_delete(self, file):
        """
        Ensure user confirms desired deletion
        
        Trace Tags: SDD_HLD_MENU_001, SDD_HLD_MENU_003
                        SDD_TT_3_004
                            SRD_T_20
                            SRD_T_21
                            SRD_T_43
                            SRD_T_44
>>>>>>> trace_tags
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

<<<<<<< HEAD
        Trace Tags: SDD_TT_3_005
        """
        note = input(f"{file}: ")
        self.__encrypt_and_save(note, file)

    def __get_encrypted_note_content_from_DB(self, file):
        """Return file content from the saved note in the DB.

        """
        encrypted_content = self.db.__display_note(self.DB_DIR_NAME, file)
=======
        Trace Tags: SDD_HLD_MENU_003
                        SDD_TT_3_005
                            SRD_T_05
                            SRD_T_06
                            SRD_T_11
                            SRD_T_21
                            SRD_T_44
                            SRD_T_45
        """
        note = input(f"{file}: ")
        if note:
            self.encrypt_and_save(note, file)
        else:
            print("Error: Please write something in the note for it to save.")

    def get_encrypted_note_content_from_DB(self, file):
        """
        Return file content from the saved note in the DB

        Trace Tags: SDD_HLD_MENU_002
                        SRD_T_05
        """
        encrypted_content = self.db.display_note(self.DB_DIR_NAME, file)
>>>>>>> trace_tags
        return encrypted_content

    def __display_note(self, file):
        """
<<<<<<< HEAD
        Receives encrypted note content, Calls the appropriate decrypt function, and then prints plaintext to the output window.

        Trace Tags: SDD_TT_3_006
=======
        Receives encrypted note content, Calls the appropriate decrypt function, and then prints plaintext to the output window

        Trace Tags: SDD_HLD_MENU_003
                        SDD_TT_3_006
                            SRD_T_14
                            SRD_T_05
>>>>>>> trace_tags
        """
        # encrypted_content = self.db.__display_note("Notes", file)
        # decrypted_file_contents = self.__get_plaintext(encrypted_content)
        decrypted = self.__get_plaintext(self.__get_encrypted_note_content_from_DB(file))
        print(decrypted)

    def __append(self, file):
        """
        Receives an encrypted string from the DB. Then, it prompts the user to add to the given string. It then 
        re-encrypts the content, and saves it to the DB using the appropriate update function.

<<<<<<< HEAD
        Trace Tags: SDD_TT_3_007
        """
        encrypted_content = self.__get_encrypted_note_content_from_DB(file)
        decrypted_content = self.__get_plaintext(encrypted_content)
        new_content = input(f"{file}: {decrypted_content}\nYou cannot overwrite this data. However, you can add to it. Make sure to add a space if needed:\n")
        __appended_string = decrypted_content + new_content
        self.db.update_note(self.DB_DIR_NAME, file, self.security.encrypt_note(__appended_string, self.__password))
=======
        Trace Tags: SDD_HLD_MENU_OO2, SDD_HLD_MENU_003
                        SDD_TT_3_007
                            SRD_T_13
                            SRD_T_43
        """
        encrypted_content = self.get_encrypted_note_content_from_DB(file)
        decrypted_content = self.get_plaintext(encrypted_content)
        new_content = input(f"{file}: {decrypted_content}\nYou cannot overwrite this data. However, you can add to it. To make no changes, simply press Enter. Make sure to add a space if needed:\n")
        appended_string = decrypted_content + new_content
        self.db.update_note(self.DB_DIR_NAME, file, self.security.encrypt_note(appended_string, self.__password))
>>>>>>> trace_tags
        # with open(f)
        # self.open_and_wait(file)
        # Ensure the file is not empty
        # Save changes to the file

    def __summarize(self, file):
        """
        Receives encrypted note content, Calls the appropriate decrypt function, passes the plaintext as
        a string to the AI class instance summary function, and then prints the returned string to the output window 

<<<<<<< HEAD
        Trace Tags: SDD_TT_3_008
=======
        Trace Tags: SDD_HLD_MENU_002, SDD_HLD_MENU_003
                        SDD_TT_3_008
                            SRD_T_12
                            SRD_T_45
>>>>>>> trace_tags
        """
        decrypted_content = self.__get_plaintext(self.__get_encrypted_note_content_from_DB(file))
        if decrypted_content:
            print((self.Ai.summarize(decrypted_content)))
        else:
            print("Error: Could not __summarize note.")

    def __delete(self, file):
        """
<<<<<<< HEAD
        Calls __confirm___delete to ensure no mistaken hard __deletes occur, and then calls the associated
        DB function to permanently __delete the file from memory

        Trace Tags: SDD_TT_3_009
=======
        Calls confirm_delete to ensure no mistaken hard deletes occur, and then calls the associated
        DB function to permanently delete the file from memory

        Trace Tags: SDD_HLD_MENU_002, SDD_HLD_MENU_003
                        SDD_TT_3_09
                            SRD_T_23
                            SRD_T_44
                            SRD_T_45
>>>>>>> trace_tags
        """
        if self.__confirm___delete(file):
            self.db.delete_note(self.DB_DIR_NAME,file)
        else:
            print("Aborting Deletion.")
    
    # Test cases for __delete():
        # Does the function call __confirm___delete before calling DB.__delete()?

<<<<<<< HEAD
    def __select(self):
        """Allow user to __select their desired __action and file, gracefully handling invalid input. 
        Converts string input to an integer, and then returns that integer. Calls __choose_file for 
        non-creation __actions and calls __generate_filename for __new_note. It returns the filename and 
        integer together as a tuple.
        
        Trace Tags: SDD_TT_3_010
        SDD_HLD_MENU_001, SDD_HLD_MENU_002
=======
    def select(self):
        """
        Allow user to select their desired action and file, gracefully handling invalid input. 
        Converts string input to an integer, and then returns that integer. Calls choose_file for 
        non-creation actions and calls generate_filename for new_note. It returns the filename and 
        integer together as a tuple.
        
        Trace Tags: SDD_HLD_MENU_001, SDD_HLD_MENU_003
                        SDD_TT_3_010
                            SRD_T_03
                            SRD_T_21
                            SRD_T_22
                            SRD_T_29
                            SRD_T_30
                            SRD_T_44
                            SRD_T_45
>>>>>>> trace_tags
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
                print(f"Selected Action: {self.possible_actions_as_strings_for_display[answer-1]}")
                if (answer == 1):
                    file = self.__generate_filename()
                else:
                    file = self.__choose_file()
                if file:
                    return (answer, file)
                else:
                    print("Error with file. Aborting and returning to Menu.")
            elif (answer == 6):
                print("Exiting the Secure Notes Application")
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

<<<<<<< HEAD
        Trace Tags: SDD_TT_3_011
        SDD_HLD_MENU_003
=======
        Trace Tags: SDD_HLD_MENU_003
                        SDD_TT_3_011
                            SRD_T_28
                            SRD_T_31
>>>>>>> trace_tags
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
<<<<<<< HEAD
        a new file by calling the __generate_filename function.

        Trace Tags: SDD_TT_3_012
        SDD_HLD_MENU_001, SDD_HLD_MENU_002, SDD_HLD_MENU_003
=======
        a new file by calling the generate_filename function.

        Trace Tags: SDD_HLD_MENU_002, SDD_HLD_MENU_003
                        SDD_TT_3_012
                            SRD_T_02
                            SRD_T_04
                            SRD_T_21
                            SRD_T_44
                            SRD_T_45
>>>>>>> trace_tags
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
<<<<<<< HEAD
        Main Loop that will run until the user exits the program. It will continually prompt the user
        with the menu, and then run the __selected __action. It then returns to the menu and repeats.

        Trace Tags: SDD_HLD_MENU_002
        """

        print("Welcome to the Secure Notes Application")
        run_flag = True
        while run_flag:
            [action, file] = self.__select()
            run_flag = self.__act(action, file)
=======
        Control SUD runtime flow, exit controls, and loop functionality

        Trace Tags: SDD_HLD_MENU_001, SDD_HLD_MENU_003
                        SRD_T_04
        """
        self.db.create_directory(self.DB_DIR_NAME)
        print("Welcome to the Secure Notes Application")
        run_flag = True
        while run_flag:
            [action, file] = self.select()
            run_flag = self.act(action, file)
        print("Thank you for using our software.")
>>>>>>> trace_tags
