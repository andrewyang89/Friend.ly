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

    lonely_person_answers : np.array - shape-(M, 50)
        The given user's answers' descriptor vectors, where M is the number of
        questions

    other_lonely_people_answers : dict
        Database of len-N, where N is the number of users (including our poor
        lonely user), that maps names to a set of descriptor vectors
        (shape-(M, 50) each)

    Returns
    -------
    kscores : List[tuple]
        List of k tuples of closest detected matches in descending order of
        strength, each formatted as follows: (name, match score)

    """

    del other_lonely_people_answers[lonely_person]

    print('(N) - Number of other users: '
          + (len(other_lonely_people_answers)))
    print('(N, M, 50) - Shape of answer database excluding user: '
          + np.array(list(other_lonely_people_answers.values())).shape)

    names = np.array(list(other_lonely_people_answers.keys()))
    print('names initialized')
    answers = np.array(list(other_lonely_people_answers.values()))
    print('answers initialized')

    #answers_transposed = np.swapaxes(answers, 0, 1)
    #print('(N, 50, M) - Shape of transposition: ' + answers_transposed.shape)

    #creating an ndarray of shape-(N, M)
    cos_distances = np.ndarray(shape=(answers.shape[0], answers.shape[1]))

    for name in range(len(names)):
        for answer in range(len(lonely_person_answers)):
            cos_distances[name, answer] = np.matmul(lonely_person_answers[answer],
                                            np.swapaxes(answers[answer], 0, 1)) /
                                            (lonely_person_answers[answer] *
                                            answers_transposed[answer])

    distances = np.sum(cos_distances, axis=1)

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
