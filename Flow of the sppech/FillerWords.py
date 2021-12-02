ScoreforFillerwords = 60/100

def wordcount(filename, listwords):
    try:
        read = filename.split("\n")
        for word in listwords:
            lower = word.lower()

            count = 0

            for sentance in read:
                line = sentance.split()
                for each in line:
                    line2 = each.lower()
                    line2 = line2.strip("!@#$%^&*(()_+=")

                    if lower == line2:
                        count += 1

            print(lower, ":", count)
            return {
                "message": str(lower) + ":" + str(count),
                "score": ScoreforFillerwords
            }
    except FileExistsError:
        print("Have not filler word")
        return "Have not filler word"

