from difflib import SequenceMatcher
str1 = ' Hola'
str2 = 'Hola Hola'
matcher = SequenceMatcher(None, str1, str2)
match = matcher.find_longest_match(0, len(str1), 0, len(str2))
match

print('ey')