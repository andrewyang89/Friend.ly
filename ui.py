from input_to_descriptors import new_person
from database import Database
from find_friends import find_friends
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
from recognize_speech import recognize_speech_record
from input_to_descriptors import compute_descriptors

class UI:

    def __init__(self):
        self.db = Database()
        self.db.load('loaded_10_people.pkl')
        self.logged_in = False

    def forgetful_new_person(self, db,new_name):
        names = self.db.names
        # contacts = self.db.contacts
        entries = self.db.biographies
        # connect to audio to text file
        new_entry = recognize_speech_record("Tell us a bit about yourself so that we can try to find your account: ")
        #actually do the comparison and find the most similar
        names.append(new_name)
        # contacts.append(new_contact)
        entries.append(new_entry)

        descriptors = compute_descriptors(entries)
        self.db.add_and_update_profiles(names, entries, descriptors)


    def user_prompt(self, demomode=False):

        if demomode:

            command = input("\n-----------\nDEMO ACTIVE\n-----------\n\nWhat would you like to demo?\n\n0: Sign In or Create a Profile\n1: Find a new best friend\n2: Have a practice conversation\n3: Find a group\n4: Quit\n\n(Please enter an integer from 0 to 4)\n\n")

            if command == '0':

                sign_in = input("\n----------------------------------------\nDo you have a preexisting profile? [y/n]\n----------------------------------------\n\n")

                if sign_in == "y" or sign_in == "yes":

                    self.name = input("\n------------------\nWhat is your name?\n------------------\n\n")

                    if self.name not in self.db.names:

                        confirm = input("\n-------------------------------------------------------------------------------------------------------\nThat name doesn't appear to be associated with an account. Are you sure you entered it correctly? [y/n]\n-------------------------------------------------------------------------------------------------\n\n")

                        if confirm == "y" or confirm == "yes":

                            self.forgetful_new_person(self.db, name)
                            print("\n----------------------------------------------------------------------------------------------------------------------\nFound you! And I definitely didn't just make a new profile using the information you gave because you are incompetent.\n----------------------------------------------------------------------------------------------------------------------\n")

                        elif confirm == "n" or confirm == "no":

                            print("\n----------------------------------\nRedirecting you to the homepage...\n----------------------------------\n")
                            self.user_prompt(True)

                        self.db.save('loaded_10_people.pkl')

                    else:
                        print("\n----------------\nLOGIN SUCCESSFUL\n----------------\n")

                elif sign_in == "n" or sign_in == "no":

                    new_person(self.db)
                    self.db.save('loaded_10_people.pkl')
                    self.name = self.db.names[-1]

                else:

                    print("\n------------------------------\nPlease input a valid response.\n------------------------------")

                self.user_prompt(True)

            elif command == '1':

                similar_name = str(find_friends(1, self.name, self.db)[0][0])
                print("\n" + "-" * (25 + len(similar_name)) + "\nYour most similar match: " + similar_name + "\n" + "-" * (25 + len(similar_name)) + "\n")
                rating = input("\n-------------------------------------------------------\nSo, how much of a stalker are you? (On a scale of 1-10)\n-------------------------------------------------------\n\n")

                """
                if type(int(rating)) is not int or type(float(rating)) is not float:

                    print("\n------------------------------\nPlease input a valid response.\n------------------------------")

                Let's just pretend that all answers will be valid casts.
                """

                if int(rating) <= 5:

                    print("\n--------------\nSuit yourself.\n--------------\n")

                elif int(rating) > 5 and int(rating) < 10:

                    stalkee = self.db.database[similar_name]
                    print("\n------------------\nHave at it, champ.\n------------------\n")
                    print("\nName: " + stalkee.name + "\nBiography: " + stalkee.biography + "\nContact: " + stalkee.contact + "\nPositivity Score: " + "0" + "\nPicture: \n")
                    #imgplot = plt.imshow(stalkee.picture)
                    #plt.show()

                else:

                    print("\n-----------------------------------------------\nI don't think you'll be needing our help then.\n-----------------------------------------------\n")

                self.user_prompt(True)

            elif command == '2':
                pass

            elif command == '3':

                k = int(input("\n------------------------------------------\nHow many people do you want in your group?\n------------------------------------------\n\n"))
                group = find_friends(k, self.name, self.db)
                group_names = ""
                for i in range(len(group)-1):
                    group_names += (group[i][0] + ", ")
                group_names += (group[len(group)-1][0])
                group_list = group_names.split(", ")
                print("\n---------------------------" + "-" * len(group_names) + "\nYour most similar matches: " + group_names + "\n---------------------------" + "-" * len(group_names) + "\n")
                rating = input("\n-------------------------------------------------------\nSo, how much of a stalker are you? (On a scale of 1-10)\n-------------------------------------------------------\n\n")

                """
                if type(int(rating)) is not int or type(float(rating)) is not float:

                    print("\n------------------------------\nPlease input a valid response.\n------------------------------")

                Let's just pretend that all answers will be valid casts.
                """

                if int(rating) <= 5:

                    print("\n--------------\nSuit yourself.\n--------------\n")

                elif int(rating) > 5 and int(rating) < 10:

                    print("\n------------------\nHave at it, champ.\n------------------\n")
                    for similar_name in group_list:
                        stalkee = self.db.database[similar_name]
                        print("\nName: " + stalkee.name + "\nBiography: " + stalkee.biography + "\nContact: " + stalkee.contact + "\nPositivity Score: " + "0" + "\nPicture: \n")
                        #imgplot = plt.imshow(stalkee.picture)
                        #plt.show()

                else:

                    print("\n-----------------------------------------------\nI don't think you'll be needing our help then.\n-----------------------------------------------\n")

                self.user_prompt(True)




            elif command == '4':

                print("\nGoodbye.")

            else:

                print("\n------------------------------\nPlease input a valid response.\n------------------------------")

            self.user_prompt(True)
