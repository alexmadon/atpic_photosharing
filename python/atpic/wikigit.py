#!/usr/bin/python3
# cf ikiwiki git
# /usr/share/perl5/IkiWiki/Plugin/git.pm
# http://ikiwiki.info/tips/Hosting_Ikiwiki_and_master_git_repository_on_different_machines/
# By default, when creating a wiki, Ikiwiki creates and uses two repositories: a bare repository, and a « slave » repository, used as the source to render the wiki. All of these are on the same machine.


import subprocess

import atpic.mybytes

def send_git(command):
    # command is a list like: ['git','log']
    # repo directory with a slash at the end
    wikidir='/home/madon/public_html/perso/entreprise/sql_current/site/atpicwiki/'
    pr = subprocess.Popen(
        command,
        cwd=wikidir,
        stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE )
    (out, error) = pr.communicate()
    return(out,error)

def git_show(filename):
    (out, error)=send_git([b'git',b'show',b'HEAD:'+filename])
    return (out, error)

def git_log(command):
    # http://blog.lost-theory.org/post/how-to-parse-git-log-output/
    GIT_COMMIT_FIELDS = [b'id', b'author_name', b'author_email', b'date', b'message']
    GIT_LOG_FORMAT = [b'%H', b'%an', b'%ae', b'%ad', b'%s']
    abegin=b'%x1f'
    aend=b'%x1e'
    abegin=b'^^^___~~~'
    aend=b'^^^===~~~'
    GIT_LOG_FORMAT = abegin.join(GIT_LOG_FORMAT) + aend
    (log,err)=send_git([b'git',b'log',b'--format='+GIT_LOG_FORMAT]+command)
    log = log.strip(b'\n'+aend).split(aend)
    log = [row.strip().split(abegin) for row in log]
    log = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in log]
    return (log,err)


if __name__=='__main__':

    print(send_git([b'git',b'log']))

    print(send_git([b'git',b'log',b'--pretty=format:<A>%h%x09%an%x09%ad%x09%s</A>']))

    print(send_git([b'git',b'log',b'Index']))
    print(send_git([b'git',b'log',b'--',b'Index']))

    print(send_git([b'git',b'show',b'HEAD:Index']))
    print(send_git([b'git',b'show',b'HEAD~1:Index']))
    print(send_git([b'git',b'show',b'HEAD~0:Index']))
    print(send_git([b'git',b'show',b'HEAD~2:Index']))
    print(send_git([b'git',b'show',b'HEAD~8:Index']))
    print(git_show(b'Index'))
    print(send_git([b'git',b'diff',b'HEAD~1:Index',b'HEAD~0:Index']))
