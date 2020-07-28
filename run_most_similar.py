from input_to_descriptors import compute_descriptors, new_person
from database import Database
from find_friends import find_friends


db = Database()
db.load('loaded_10_people.pkl')
new_person(db)
print(db.names)
print("Your most similar match: " + str(find_friends(1, db.names[-1], db)[0][0]))
# print("Contact: ")
db.save('loaded_10_people.pkl')