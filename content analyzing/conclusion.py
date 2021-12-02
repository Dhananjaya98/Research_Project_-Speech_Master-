import spacy

scoreForConclusion = 60/100
nlp = spacy.load("en_core_web_sm")
#Count the total number of characters in the speech


def identify_conclusion(speech):
    totalCharacterCount = len(speech)
    conclusionCharacterCount = (85/100)*totalCharacterCount
    conclusion = (speech[int(conclusionCharacterCount):int(totalCharacterCount)])
    return {
        "message": conclusion,
        "score": scoreForConclusion
    }


def conclusion_best_practices(speech):
    conclusion = identify_conclusion(speech)["message"]
    final_words = []

    with open('content analyzing/bestPracticesForConclusion.txt', 'r') as file:
        for line in file:
            clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
            word, emotion = clear_line.split(':')

            if word in conclusion:
                final_words.append(word)

    return {
        "message": final_words,
        "score": scoreForConclusion
    }


def conclusion_questions(speech):
    retVal = []
    doc = nlp(identify_conclusion(speech)["message"])

    tokens = [token for token in doc]

    for i in range(len(tokens)):
        if (tokens[i].pos_ == 'ADV' and tokens[i + 1].pos_ == 'AUX' and tokens[i + 2].pos_ == 'PRON'):
            retVal.append(f"{tokens[i]} {tokens[i + 1]} {tokens[i + 2]}")

    return {
        "message": retVal,
        "score": scoreForConclusion
    }

