def grade(key):
    if "helloworld" in key:
        return 100, "Correct!"
    elif "goodbyeworld" in key:
        return 50, ":("
    else:
        return 0, "Sorry, not this time."