#!/usr/bin/python3

import atpic.diff_match_patch



# wrapper on google 'diff_match_patch'
# bettwer than simplediff as it considers newlines
# and has a default HTML

def diff_xml(textA,textB):
    # create a diff_match_patch object
    dmp = atpic.diff_match_patch.diff_match_patch()

    # Depending on the kind of text you work with, in term of overall length
    # and complexity, you may want to extend (or here suppress) the
    # time_out feature
    dmp.Diff_Timeout = 0   # or some other value, default is 1.0 seconds
    
    # All 'diff' jobs start with invoking diff_main()
    diffs = dmp.diff_main(textA, textB)
  
    # diff_cleanupSemantic() is used to make the diffs array more "human" readable
    dmp.diff_cleanupSemantic(diffs)
    return diffs

def diff_html(textA,textB):
    # textA=textAb.decode('utf-8')
    # textB=textBb.decode('utf-8')

    # create a diff_match_patch object
    dmp = atpic.diff_match_patch.diff_match_patch()

    # Depending on the kind of text you work with, in term of overall length
    # and complexity, you may want to extend (or here suppress) the
    # time_out feature
    dmp.Diff_Timeout = 0   # or some other value, default is 1.0 seconds
    
    # All 'diff' jobs start with invoking diff_main()
    diffs = dmp.diff_main(textA, textB)
  
    # diff_cleanupSemantic() is used to make the diffs array more "human" readable
    dmp.diff_cleanupSemantic(diffs)

    # and if you want the results as some ready to display HMTL snippet
    htmlSnippet = dmp.diff_prettyHtml(diffs)
    return htmlSnippet


if __name__ == "__main__":
    textA = """the cat in the
red hat
some older line
"""
    textB = """the feline in the
blue hat
some new line
some older line
"""
    diff=diff_html(textA,textB)
    print(diff)
