from input_to_descriptors import new_person
from database import Database
from find_friends import find_friends
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
from recognize_speech import recognize_speech_record
from input_to_descriptors import compute_descriptors
from Whispers_Friends import whispers
from ngram_model import story
import pickle

with open('fairytale.pkl', 'rb') as file:
    lm = pickle.load(file)

class UI:

    def __init__(self):
        self.db = Database()
        self.db.load('loaded_10_people.pkl')
        self.logged_in = False

    def forgetful_new_person(self, db,new_name):
        names = db.names
        # contacts = db.contacts
        entries = db.biographies
        # new_contact = input("Please enter your contact")
        # connect to audio to text file
        new_entry = recognize_speech_record("Tell us a bit about yourself: ")
        names.append(new_name)
        # contacts.append(new_contact)
        entries.append(new_entry)

        descriptors = compute_descriptors(entries)

        print ("Taking a picture. Smile!")
        pic, positivity_score = take_image_classify_emotion()
        db.add_and_update_profiles(names, entries, descriptors)
        db.update_one_profile(new_name,new_picture=pic,positivity_score=positivity_score, new_short_bio=summarize_doc(new_name, db))


    def user_prompt(self, demomode=False):

        if demomode:

            print("\n-----------")
            print("\nDEMO ACTIVE")
            print("\n-----------")
            print("\n\nWhat would you like to demo?\n")
            print("\n0: Sign In or Create a Profile")
            print("\n1: Find a New Best Friend")
            print("\n2: Tell Me a Story")
            print("\n3: Find a Group")
            print("\n4: View All Friend Groups")
            print("\n5: Quit")
            command = input("\n(Please enter an integer from 0 to 4)\n\n")

            if command == '0':

                print("\n----------------------------------------")
                print("\nDo you have a preexisting profile? [y/n]")
                sign_in = input("\n----------------------------------------\n\n")

                if sign_in == "y" or sign_in == "yes":

                    print("\n------------------")
                    print("\nWhat is your name?")
                    self.name = input("\n------------------\n\n")

                    if self.name not in self.db.names:

                        print("\n-------------------------------------------------------------------------------------------------------")
                        print("\nThat name doesn't appear to be associated with an account. Are you sure you entered it correctly? [y/n]")
                        confirm = input("\n-------------------------------------------------------------------------------------------------\n\n")

                        if confirm == "y" or confirm == "yes":

                            self.forgetful_new_person(self.db, name)
                            print("\n----------------------------------------------------------------------------------------------------------------------")
                            print("\nFound you! And I definitely didn't just make a new profile using the information you gave because you are incompetent.")
                            print("\n----------------------------------------------------------------------------------------------------------------------\n")

                        elif confirm == "n" or confirm == "no":

                            print("\n----------------------------------")
                            print("\nRedirecting you to the homepage...")
                            print("\n----------------------------------\n")
                            self.user_prompt(True)

                        self.db.save('loaded_10_people.pkl')

                    else:
                        print("\n----------------")
                        print("\nLOGIN SUCCESSFUL")
                        print("\n----------------\n")

                elif sign_in == "n" or sign_in == "no":

                    new_person(self.db)
                    self.db.save('loaded_10_people.pkl')
                    self.name = self.db.names[-1]

                else:

                    print("\n------------------------------")
                    print("\nPlease input a valid response.")
                    print("\n------------------------------\n")

                self.user_prompt(True)

            elif command == '1':

                similar_name = str(find_friends(1, self.name, self.db)[0][0])
                print("\n" + "-" * (25 + len(similar_name)))
                print("\nYour most similar match: " + similar_name)
                print("\n" + "-" * (25 + len(similar_name)) + "\n")

                """
                print("\n-------------------------------------------------------")
                print("\nSo, how much of a stalker are you? (On a scale of 1-10)")
                rating = input("\n-------------------------------------------------------\n\n")


                #if type(int(rating)) is not int or type(float(rating)) is not float:

                    #print("\n------------------------------\nPlease input a valid response.\n------------------------------")

                #Let's just pretend that all answers will be valid casts.


                if int(rating) <= 5:

                    print("\n--------------")
                    print("\nSuit yourself.")
                    print("\n--------------\n")

                elif int(rating) > 5 and int(rating) < 10:

                    stalkee = self.db.database[similar_name]
                    print("\n------------------")
                    print("\nHave at it, champ.")
                    print("\n------------------\n")
                    print("\nName: " + stalkee.name)
                    print("\nBiography: " + stalkee.biography)
                    print("\nContact: " + stalkee.contact)
                    print("\nPositivity Score: " + "0")
                    print("\nPicture: \n")
                    #imgplot = plt.imshow(stalkee.picture)
                    #plt.show()

                else:

                    print("\n----------------------------------------------")
                    print("\nI don't think you'll be needing our help then.")
                    print("\n-----------------------------------------------\n")
                """
                print("\n-----------------------------------")
                print("\nWould you like to learn more? [y/n]")
                resp = input("\n-----------------------------------\n\n")

                if confirm == "y" or confirm == "yes":

                    stalkee = self.db.database[similar_name]
                    print("\n------------------")
                    print("\nHave at it, champ.")
                    print("\n------------------")
                    print("\nName: " + stalkee.name)
                    print("\nBiography: " + stalkee.biography)
                    print("\nContact: " + stalkee.contact)
                    print("\nPositivity Score: " + stalkee.positivity_score)
                    print("\nPicture: \n")
                    imgplot = plt.imshow(stalkee.picture)
                    plt.show()

                elif confirm == "n" or confirm == "no":

                    print("\n--------------")
                    print("\nSuit yourself.")
                    print("\n--------------\n")

                else:

                    print("\n------------------------------")
                    print("\nPlease input a valid response.")
                    print("\n------------------------------\n")

                self.user_prompt(True)

            elif command == '2':

                print("\nLet me tell you a story:\n\n")
                print(story(lm))
                self.user_prompt(True)

            elif command == '3':

                print("\n------------------------------------------")
                print("\nHow many people do you want in your group?")
                k = int(input("\n------------------------------------------\n\n"))
                group = find_friends(k, self.name, self.db)
                group_names = ""
                for i in range(len(group)-1):
                    group_names += (group[i][0] + ", ")
                group_names += (group[len(group)-1][0])
                group_list = group_names.split(", ")
                print("\n---------------------------" + "-" * len(group_names))
                print("\nYour most similar matches: " + group_names)
                print("\n---------------------------" + "-" * len(group_names) + "\n")
                print("\n-------------------------------------------------------")
                print("\nSo, how much of a stalker are you? (On a scale of 1-10)")
                rating = input("\n-------------------------------------------------------\n\n")

                """
                if type(int(rating)) is not int or type(float(rating)) is not float:

                    print("\n------------------------------\nPlease input a valid response.\n------------------------------")

                Let's just pretend that all answers will be valid casts.
                """

                if int(rating) <= 5:

                    print("\n--------------")
                    print("\nSuit yourself.")
                    print("\n--------------\n")

                elif int(rating) > 5 and int(rating) < 10:

                    print("\n------------------")
                    print("\nHave at it, champ.")
                    print("\n------------------\n")
                    for similar_name in group_list:
                        stalkee = self.db.database[similar_name]
                        print("\nName: " + stalkee.name)
                        print("\nBiography: " + stalkee.biography)
                        print("\nContact: " + stalkee.contact)
                        print("\nPositivity Score: " + "0")
                        print("\nPicture: \n")
                        #imgplot = plt.imshow(stalkee.picture)
                        #plt.show()

                else:

                    print("\n----------------------------------------------")
                    print("\nI don't think you'll be needing our help then.")
                    print("\n----------------------------------------------\n")

                self.user_prompt(True)

            elif command == '4':
                print("\n\n--------")
                whispers(self.db.database)

            elif command == '5':

                print("\n--------")
                print("\nGoodbye.")
                print("\n--------")

            else:

                print("\n------------------------------")
                print("\nPlease input a valid response.")
                print("\n------------------------------")
                self.user_prompt(True)
