from difflib import SequenceMatcher


def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def similarity(words,checker):
    words = words.split(' ')
    checker = checker.split(' ')
    for w in words:
        if not list(filter( lambda l: compWords(l,w),checker)):
            return False

    return True

def compWords(x,y):
    th = SequenceMatcher(None,x,y).ratio()
    if th > 0.75:
        return True
    else:
        return False


