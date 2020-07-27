import numpy as np

def find_friends(k, lonely_person, lonely_person_answers, other_lonely_people_answers):
    """Computes the cosine distance between the given lonely user's answers'
    descriptor vectors and all all other users' answers' descriptor vectors

    Parameters
    ----------
    k : int
        Number of closest matches to be retrieved

    lonely_person : str?
        ID/name of the given lonely person

    lonely_person_answers : np.array - shape-(D,)
        The given user's answers' descriptor vectors, where D is the size of the
        vocabulary

    other_lonely_people_answers : dict
        Database of len-N, where N is the number of users (including our poor
        lonely user), that maps names to a set of descriptor vectors
        (shape-(D,) each)

    Returns
    -------
    kscores : List[tuple]
        List of k tuples of closest detected matches in descending order of
        strength, each formatted as follows: (name, match score)

    """

#You make me very sad.

#Very sad indeed.

    del other_lonely_people_answers[lonely_person]

    print('(N) - Number of other users: '
          + (len(other_lonely_people_answers)))
    print('(N, D) - Shape of answer database excluding user: '
          + np.array(list(other_lonely_people_answers.values())).shape)

    names = np.array(list(other_lonely_people_answers.keys()))
    print('names initialized')
    answers = np.array(list(other_lonely_people_answers.values()))
    print('answers initialized')

    print('(D, N) - Shape of transposition: ' + answers.T.shape)

    cos = np.matmul(lonely_person_answers, answers.T)

    zip_dists = []
    top_k = []
    for count_to_k in range(k):
        i = np.argmax(distances)
        name = names[np.argmax(distances)]
        top_k.append(name)
        zip_dists.append(distances[i])
        distances = np.delete(distances, i)
        names = np.delete(names, i)

    kscores = list(zip(top_k, zip_dists))

    return kscores
