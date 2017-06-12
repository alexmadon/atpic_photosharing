# compatibility checks:

# a servershort should not be 4 digits
# to make the diff between
# http://atpic.com/alex
# http://atpic.com/2009

# servershort should not be in a reserved word: pic, user, gallery, tag, phrase, dav, and two letters: fr, en, 
# http://alex.atpic.com
# http://fr.atpic.com
# TOO BAD:
# do not do lang based on hostname but on IP (geoIP), Cookie or Header or &lang=

# not underscore, not dots, only [a-z0-9\-]
