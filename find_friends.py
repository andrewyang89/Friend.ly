import numpy as np
from database import Database as db
from database import Profile

def find_friends(k, lonely_person_name, lonely_people):
    """Computes the cosine distance between the given lonely user's answers'
    descriptor vectors and all all other users' answers' descriptor vectors

    Parameters
    ----------
    k : int
        Number of closest matches to be retrieved

    lonely_person : str?
        ID/name of the given lonely person

    lonely_people : Database
        Database of len-N, where N is the number of users (including our poor
        lonely user), that maps names to a Profile instance, each of which has
        respective descriptor vectors

    Returns
    -------
    kscores : List[tuple]
        List of k tuples of closest detected matches in descending order of
        strength, each formatted as follows: (name, match score)

    """

#You make me very sad.

#Very sad indeed.

    lonely_person = lonely_people.database[lonely_person_name]

    del lonely_people.database[lonely_person_name]

    """
    print('(N) - Number of other users: '
          + (len(lonely_people.database)))
    print('(N, D) - Shape of answer database excluding user: '
          + np.array(list(lonely_people.database.values().descriptor_vector)).shape)
    """

    names = np.array(list(lonely_people.database.keys()))
    print('names initialized')
    profiles = np.array(list(lonely_people.database.values()))
    print('profiles initialized')
    answers = np.ndarray(shape=(len(names), len(lonely_person.descriptor_vector)))
    print('answers initialized')
    for i in range(len(answers)):
        answers[i] = profiles[i].descriptor_vector
    print('answers filled')

    print('(D, N) - Shape of transposition: ' + answers.T.shape)

    cos = np.matmul(lonely_person.descriptor_vector, answers.T)

    zip_dists = []
    top_k = []
    for count_to_k in range(k):
        i = np.argmax(cos)
        name = names[np.argmax(cos)]
        top_k.append(name)
        zip_dists.append(cos[i])
        cos = np.delete(cos, i)
        names = np.delete(names, i)

    kscores = list(zip(top_k, zip_dists))

    return kscores
