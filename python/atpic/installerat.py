"""Tools to install/check the Atpic installation"""


def check_file_match_re(strToFind,file):
    try:
        fileObject = open(file)
    except:
        print "Unable to open file " + fileName + "."
        sys.exit(1)
    occurances = 0
    try:
        for line in fileObject:
            occurances += line.count(strToFind)
    finally:
        fileObject.close()
        print "The string " + strToFind + " occurs " + str(occurances) + " times in the file "+ file + "."
