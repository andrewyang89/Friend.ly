import speech_recognition as sr


def recognize_speech_record(prompt: str) -> str:
    """
    Recognizes spoken word using Google's speech recognition software

    Parameters
    ----------
    prompt the desired prompt displayed to the user

    Returns
    -------
    Spoken text separated by spaces
    """
    r = sr.Recognizer()
    text = ""
    with sr.Microphone() as source:
        print(prompt)
        audio_text = r.listen(source)
        print("Speech Recognition Started")

        try:
            # using google speech recognition
            text = r.recognize_google(audio_text)
            print("Text: " + r.recognize_google(audio_text))
        except:
            print("Speech Recognition Unsuccessful")

    return text

def recognize_speech_file(path: str) -> str:
    """
    Recognizes audio from a audio file using Google's speech recognition software

    Parameters
    -------
    path the path of the specified audio file
    Returns
    -------
    Spoken text separated by spaces
    """
    r = sr.Recognizer()
    text = ""

    with sr.AudioFile(path) as source:

        audio_text = r.listen(source)

        try:
            # using google speech recognition
            text = r.recognize_google(audio_text)
            print("Text: " + r.recognize_google(audio_text))
        except:
            print("Speech Recognition Unsuccessful")

    return text