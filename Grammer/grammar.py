import spacy
from gingerit.gingerit import GingerIt
nlp = spacy.load("en_core_web_sm")

scoreForLengthySentences = "Good-60%"

def gingerItParse(speech):
    text1 = (speech)
    parser = GingerIt()
    result = parser.parse(text1)
    print(result)
    return {
        "message": result,
        "score": scoreForLengthySentences
    }

scoreForGrammerAccracy = "Good-60%"


def processGrammar(speech):
    retVal = []
    text = speech
    doc = nlp(text)

    Mcount = 0
    for token in doc:

        (token.text, token.dep_, token.head.text, token.head.pos_,
         [child for child in token.children])
        if token.dep_ == 'mark':
            Mcount = Mcount + 1

    # print(f"\n tagged as mark {Mcount}\n\n\n\n")

    for sent in doc.sents:
        word_count = 0
        (sent.text)
        print(f"\n SENTECNSENTENCE : {(sent.text)}.\n")

        for words in sent:
            # print(words.text)
            word_count = word_count + 1
        # print(word_count)

        if word_count < 20:
            print(f"\nGOOD SENTECNSENTENCE : This sentence contains efficient number of words\n")
            retVal.append(f"\nGOOD SENTECNSENTENCE : This sentence contains efficient number of words\n")
        if word_count >= 20:
            print(f"\n LENGTHY SENTECNSENTENCE: This sentence contains {word_count} WORDS.\n")
            retVal.append(f"\nLENGTHY SENTECNSENTENCE : This sentence contains {word_count} WORDS.\n")

        if word_count >= 20:
            transitionWordCount = 0
            for token in doc:
                if token.text == "also" or token.text == "although" or token.text == "so" or token.text == "however" or token.text == "then" or token.text == "because":
                    transitionWordCount = transitionWordCount + 1

                    a = token.text
                    print(f"\n {a.upper()}*")
                    retVal.append(f"\n {a.upper()}*")

            if word_count >= 20 and Mcount >= 1:
                print(
                    f"\nThis sentence contained mentioned {transitionWordCount} TRANSITION words in it, and {Mcount} CONJUNCTION words \n")
                retVal.append(f"\n This sentence contained mentioned {transitionWordCount} TRANSITION words in it, and {Mcount} CONJUNCTION words \n")
                print(" Sentence is too long! You shoud not use more than 20 words in a single sentence!\n")
                retVal.append("\n Sentence is too long! You shoud not use more than 20 words in a single sentence!\n")

            if word_count >= 20:
                print("\n This sentence contained mentioned {transitionWordCount} transition words in it.\n")
                retVal.append(f"\n This sentence contained mentioned {transitionWordCount} transition words in it.\n")
                print(" Sentence is too long! You should not use more than 20 words in a single sentence!\n")
                retVal.append("Sentence is too long! You shoud not use more than 20 words in a single sentence!\n")

        if transitionWordCount == 1 and word_count > 20:
            print("Try to split senetce to two sesentences from transition word!\n")
            retVal.append("Try to split senetce to two sesentences from transition word!\n")

        if transitionWordCount >= 2 and word_count > 20:
            print(
                " To make your English perfect make sure you don't use two transition words in a single sentence. Try to split senetce to two sesentences from transition words or conjunction!\n\n")
            retVal.append(" To make your English perfect make sure you don't use two transition words in a single sentence. Try to split senetce to two sesentences from transition words or conjunction!\n\n")
        return {
            "message": retVal,
            "score": scoreForLengthySentences
        }

print(processGrammar("I'll be there in time, but I also have to do my homhomework too,although I should finish them,so I may be late. And one more thing, can I use your car ?. Anyway after today I also need to work hard because my exam is in the next month."))