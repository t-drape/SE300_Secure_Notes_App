print("Welcome to the Secure Notes Application")

class Menu():
    """This class implements the requirements defined in the SRD and the features defined in the SDD for the Menu Class"""
    def __init__(self):
        # password = self.get_password()
        print("Hello")
        # This line allows me to make a function call directly by using the returned user choice as an index (allows passing the file still)
        self.possible_actions = [self.new_note, self.display, self.append, self.summarize, self.delete]

    
    def save(self, file):
        pass

    def generate_filename(self):
        pass
        # return "hello_world.txt"

    def choose_file(self):
        pass
        # print("What file would you like to perform this action on?")

    def confirm_delete(self):
        """Ensure user confirms desired deletion"""
        confirmation = False
        answer = input("Are you sure? This action cannot be reversed. [Y or y for yes]\nAnswer: ").lower()
        if (answer == "y"):
            confirmation = True
        return confirmation
    
        # Test Cases for confirm_delete():
            # Does it work with uppercase y (Y)?
            # Does it work with lowercase y (y)?
            # Do integer values break it?
            # Does it return boolean values?

    def new_note(self, file):
        pass

    def display(self, file):
        pass

    def append(self, file):
        pass

    def summarize(self, file):
        pass

    def delete(self, file):
        self.confirm_delete()
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

    def act(self, selected_action, file="None"):
        self.possible_actions[selected_action](file)
    
    # Test cases for act(selected_action, file):
        # Does the index match the correct chosen action?
        # Does the index pass a file correctly?

# m = Menu()
# m.act(4)