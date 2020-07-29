from input_to_descriptors import new_person
from database import Database
from find_friends import find_friends
class UI:
    db = Database()
    db.load('loaded_10_people.pkl')
    logged_in = False

    def forgetful_new_person(db,new_name):
        names = db.names
        # contacts = db.contacts
        entries = db.biographies
        # connect to audio to text file
        new_entry = recognize_speech_record("Tell us a bit about yourself so that we can try to find your account: ")
        #actually do the comparison and find the most similar
        names.append(new_name)
        # contacts.append(new_contact)
        entries.append(new_entry)

        descriptors = compute_descriptors(entries)
        db.add_and_update_profiles(names, entries, descriptors)


    def user_prompt(demomode=False):
        command = int(input("\nWhat would you like to do?\n\n0: Sign In or Create a Profile\n1: Find a new best friend\n2: Have a practice conversation\n3: Find a group\n4: Quit\n\n(Please enter an integer from 0 to 4)\n\n"))

        if demomode:
            if command == 0:
                sign_in = input("\n----------------------------------------\nDo you have a preexisting profile? [y/n]\n----------------------------------------\n\n")
                if sign_in == "y" or sign_in == "yes":
                    name = input("------------------\nWhat is your name?\n------------------\n")
                    if name not in db.names:
                        confirm = input("\n-------------------------------------------------------------------------------------------------------That name doesn't appear to be associated with an account. Are you sure you entered it correctly? [y/n]\n-------------------------------------------------------------------------------------------------\n")
                        if confirm == "y" or confirm == "yes":
                            forgetful_new_person(db, name)
                            print("\n----------------------------------------------------------------------------------------------------------------------\nFound you! And I definitely didn't just make a new profile using the information you gave because you are incompetent.\n----------------------------------------------------------------------------------------------------------------------\n")
                        elif confirm == "n" or confirm == "no":
                            print("\nRedirecting you to the homepage...\n")
                            user_prompt(True)
                        new_person(db)
                        db.save('loaded_10_people.pkl')
                elif sign_in == "n" or sign_in == "no":
                    new_person(db)
                    db.save('loaded_10_people.pkl')
                    name = db.names[-1]
                else:
                    print("\n------------------------------\nPlease input a valid response.\n------------------------------")
                UI.user_prompt()

            elif command == 1:
                print("\nYour most similar match: " + str(find_friends(1, name, db)[0][0]))
                UI.user_prompt()

            elif command == 2:
                """Insert once it exists"""
                UI.user_prompt()

            elif command == 3:
                k = int(input("How many people do you want in your group?"))
                group = find_friends(k, name, db)
                group_names = ""
                for i in range(len(group)-1):
                    group_names += (group[i][0] + ", ")
                group_names += (group[len(group)-1][0])
                print("Your most similar matches: " + group_names)
                UI.user_prompt()




            elif command == 4:
                print("\nGoodbye.")

            else:
                print("\n------------------------------\nPlease input a valid response.\n------------------------------")
            UI.user_prompt()

        else:
            if command == 0:
                sign_in = input("\n----------------------------------------\nDo you have a preexisting profile? [y/n]\n----------------------------------------\n\n")
                if sign_in == "y" or sign_in == "yes":
                    name = input("------------------\nWhat is your name?\n------------------\n")
                    if name not in db.names:
                        confirm = input("\n-------------------------------------------------------------------------------------------------------That name doesn't appear to be associated with an account. Are you sure you entered it correctly? [y/n]\n-------------------------------------------------------------------------------------------------\n")
                        if confirm == "y" or confirm == "yes":
                            forgetful_new_person(db, name)
                            print("\n----------------------------------------------------------------------------------------------------------------------\nFound you! And I definitely didn't just make a new profile using the information you gave because you are incompetent.\n----------------------------------------------------------------------------------------------------------------------\n")
                        elif confirm == "n" or confirm == "no":
                            print("\nRedirecting you to the homepage...\n")
                            user_prompt(True)
                        new_person(db)
                        db.save('loaded_10_people.pkl')
                elif sign_in == "n" or sign_in == "no":
                    new_person(db)
                    db.save('loaded_10_people.pkl')
                    name = db.names[-1]
                else:
                    print("\n------------------------------\nPlease input a valid response.\n------------------------------")
                UI.user_prompt()

            elif command == 1:
                similar_name = str(find_friends(1, name, db)[0][0])
                print("\n" + "-" * (25 + len(similar_name)) + "\nYour most similar match: " + similar_name + "-" * (25 + len(similar_name)))
                UI.user_prompt()

            elif command == 2:
                """Insert once it exists"""
                UI.user_prompt()

            elif command == 3:
                k = int(input("How many people do you want in your group?"))
                group = find_friends(k, name, db)
                group_names = ""
                for i in range(len(group)-1):
                    group_names += (group[i][0] + ", ")
                group_names += (group[len(group)-1][0])
                print("Your most similar matches: " + group_names)
                UI.user_prompt()

            elif command == 4:
                print("\nGoodbye.")

            else:
                print("\n------------------------------\nPlease input a valid response.\n------------------------------")
            UI.user_prompt()
