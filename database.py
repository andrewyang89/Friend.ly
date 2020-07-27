import pickle

class Database():
    def __init__(self, names=[], raw_text=[], descriptor_vectors=[]):
        """
        Initialize Database with initial entries
        
        Parameters
        ----------
        names : List
            list of names to go into database
        
        raw_text : List
            list of raw text corresponding to person's biography
        
        descriptor_vectors : List[numpy.ndarray]
            list of descriptor_vectors for the associated raw text biography
        """
        self.database = dict(zip(names, zip(raw_text, descriptor_vectors)))
        self.biographies = raw_text
        
    
    def add_profile(self, name, raw_text, descriptor_vector):
        """
        Add new profile to database
        
        Parameters
        ----------
        name : str
            new profile's name to be added into database
        
        raw_text : str
            raw text biography of profile
        
        descriptor_vector : numpy.ndarray
            associated descriptor vector
        
        """
        self.database[name] = (raw_text, descriptor_vector)
        self.biographies.append(raw_text)
    
    
    def update_profile(self, name, new_descriptor_vector):
        """
        Update particular person's descriptor vector
        
        Parameters
        ----------
        name : str
            name of person in database to be updated
        
        new_descriptor_vector : numpy.ndarray
            updated descriptor vector for the person
        """
        self.database[name] = (self.database[name][0], new_descriptor_vector)
    
    
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