print("Welcome to the Secure Notes Application")

class Menu():
    """This class implements the requirements defined in the SRD and the features defined in the SDD for the Menu Class"""
    def __init__(self):
        password = self.get_password()

    
    # def save(file=generate_filename()): 
    #     if (file):
    #         print("Hello World")
    #     else:
    #         print("No Hello")

    def generate_filename():
        return "hello_world.txt"

    def choose_file():
        print("What file would you like to perform this action on?")

    def confirm_delete():
        confirmation = False
        answer = input("Are you sure? This action cannot be reversed. [Y or y for yes]\nAnswer: ").lower()
        if (answer == "y"):
            confirmation = True
        return confirmation
    
    """
    Test Cases for confirm_delete():
        Does it work with uppercase y (Y)?
        Does it work with lowercase y (y)?
        Do integer values break it?
        Does it return boolean values?
    """

    def new_note(file):
        pass

    def display(file):
        pass

    def append(file):
        pass

    def summarize(file):
        pass

    def delete(file):
        pass

    def select():
        answer = input("""
What action would you like to perform?
(Input the number of the selected action)
    1. Create Note
    2. Display Note
    3. Change Note
    4. Summarize Note
    5. Delete Note
                       """)
        try:
            answer = int(answer)
        except ValueError:
            print("""
                  Invalid Input. 
                  Aborting action and returning to Menu.
                  """)

    def get_password():
        return 0

    def act(selected_action):
        pass


def select():
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
        return answer
    except ValueError:
        print("""
Invalid Input. 
Aborting action and returning to Menu.""")
    return -1

c = select()
print(c)
