import spacy

scoreForIntroduction = 40/100
nlp = spacy.load("en_core_web_sm")


def identify_introduction(speech):
    total_character_count = len(speech)

    introduction_character_count = (15 / 100) * total_character_count
    introduction = (speech[0:int(introduction_character_count)])

    return {
        "message": introduction,
        "score": scoreForIntroduction
    }


def introduction_best_practices(speech):

    introduction = nlp(identify_introduction(speech)["message"])
    final_words = []

    with open('content analyzing/bestPracticesForIntroduction.txt', 'r') as file:
        for line in file:
            clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
            word, emotion = clear_line.split(':')

            if word in introduction:
                final_words.append(word)
    return {
        "message": final_words,
        "score": scoreForIntroduction
    }


def introduction_questions(speech):
    doc = nlp(identify_introduction(speech)["message"])

    tokens = [token for token in doc]
    identified_questions = []

    for i in range(len(tokens)):
        if (tokens[i].pos_ == 'ADV' and tokens[i + 1].pos_ == 'AUX' and tokens[i + 2].pos_ == 'PRON'):
            identified_questions.append(f"{tokens[i]} {tokens[i + 1]} {tokens[i + 2]}")

    return {
        "message": identified_questions,
        "score": scoreForIntroduction
    }

