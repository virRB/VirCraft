score = 0

wierd_stuff = ['!', '@', '.', '/', '%', '$', '#', '^', '*', '&']

def test(word):
    global score, wierd_stuff
    score += (len(word) * 2)
    for i in wierd_stuff:
        if i in word:
            score += word.count(i) * 2
    w = score
    score = 0
    return w