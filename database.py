import pickle

class Profile():
    def __init__(self, name, biography=None, contact=None, descriptor_vector=None, picture=None, positivity_score=None):
        """
        Initialize Profile with initial descriptions
        
        Parameters
        ----------
        name : str
            name of the person
        
        biography : str
            raw text of the person when describing themselves
        
        contact : str
            contact information (email, phone, etc)
        
        descriptor_vector : numpy.ndarray
            associated descriptor vector for the raw text
        
        picture : ??
            photo of person
        
        positivity_score : float
            number that evaluate how "positive" or "negative" the person seems
        """
        self.name = name
        self.biography = biography
        self.contact = contact
        self.descriptor_vector = descriptor_vector
        self.picture = picture
        self.positivity_score = positivity_score


    def __repr__(self):
        return "Name: {}\nBiography: {}\nDescriptor Vector: {}".format(self.name, self.biography, self.descriptor_vector)

class Database():
    def __init__(self, names=[], biographies=[], descriptor_vectors=[]):
        """
        Initialize Database with initial entries
        
        Parameters
        ----------
        names : List
            list of names to go into database
        
        biographies : List
            list of raw text corresponding to person's biography
        
        descriptor_vectors : List[numpy.ndarray]
            list of descriptor_vectors for the associated raw text biography
        """

        self.database = dict(zip(names, [Profile(name, biography=bio, descriptor_vector=vec) for name, bio, vec in zip(names, biographies, descriptor_vectors)]))
        
    
    def add_and_update_profiles(self, names, biographies, descriptor_vectors):
        """
        Add and update Profiles in database
        
        Parameters
        ----------
        names : List
            names of person in database to be added/updated
        
        biographies : List
            biographies associated to names in raw text form
        
        descriptor_vectors : List[numpy.ndarray]
            descriptor vectors associated to names
        """
        for name, bio, vec in zip(names, biographies, descriptor_vectors):
            if name in self.database:
                self.database[name].name = name
                self.database[name].biography = bio
                self.database[name].descriptor_vector = vec
            else:
                self.database[name] = Profile(name, biography=bio, descriptor_vector=vec)
    
    
    def save(self, filename):
        """
        Save the database to a pickle file
        
        Parameters
        ----------
        filename : str
            path to store the pickle file in
        """
        with open(filename, mode='wb') as file:
            pickle.dump(self.database, file)
    
    
    def load(self, filename):
        """
        Load existing pickle database and add to current
        
        Parameters
        ----------
        filename : str
            path to load the pickle database from
        """
        with open(filename, mode='rb') as file:
            loaded_db = pickle.load(file)
        self.database.update(loaded_db)
    

    def remove_profile(self, name):
        """
        Remove person from database

        Parameters
        ----------
        name : str
            name of person to remove from database
        """
        del self.database[name]
    

    @property
    def names(self):
        return sorted(list(self.database.keys()))
    

    @property
    def biographies(self):
        return [self.database[name].biography for name in self.names]

"""
# Database Class usage
db = Database()  # First instantiate database (this instantiates empty database)
db = Database(['sally', 'bob', 'john'], ['i like cheese', 'i love food', 'i want a car'], [np.random.rand(3), np.random.rand(3), np.random.rand(3)])  # Or add preexisting entries

# Get all names and biographies
names = db.names
entries = db.biographies

# Say you have a new name and corresponding entry
new_name = "John"
new_entry = "I like biking"

names.append(new_name)  # Add name to list of names
entries.append(new_entry)  # Add entry to list of entries

descriptors = compute_descriptors(...)  # Make new descriptor vectors with updated vocab and whatnot

db.add_and_update_profiles(names, entries, descriptors)  # Update the database with the new list of names, entries, and descriptors
"""