from input_to_descriptors import new_person
from database import Database
from find_friends import find_friends

db = Database()
db.load('loaded_10_people.pkl')
profile_created = False

def user_prompt():
    command = int(input("\nWhat would you like to do?\n\n0: Create a profile (and switch to it)\n1: Find a new best friend\n2: Have a practice conversation\n3: Find a group\n4: Quit\n\n(Please enter an integer from 0 to 4)\n\n"))

    if command == 0:
        new_person(db)
        db.save('loaded_10_people.pkl')
        profile_created = True
        user_prompt()

    #profile_created and
    elif command == 1:
        print("\nYour most similar match: " + str(find_friends(1, db.names[-1], db)[0][0]))
        user_prompt()

    elif command == 2:
        """Insert once it exists"""
        user_prompt()

    #profile_created and
    elif command == 3:
        k = int(input("\nHow many people do you want in your group?"))
        group = find_friends(k, db.names[-1], db)
        group_names = ""
        for i in range(len(group)-1):
            group_names += (group[i][0] + ", ")
        group_names += (group[len(group)-1][0])
        print("Your most similar matches: " + group_names)
        user_prompt()

    elif command == 4:
        print("\nGoodbye.")
