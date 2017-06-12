#!/usr/bin/python3
# this is a py3k wrapper for exiftool which has json, xml and htmldump capability
# exiftool is written in perl
# but xml, jsonc make it useful from other languages

# exiftool -X file.raw
# exif can also do XML but on less formats
# exif --xml-output RAW_FUJI_S5000.RAF 


# exiftool -stay_open True -@ exifpipe > exifresults 2>&1 &

import subprocess
import atpic.log
import os

xx=atpic.log.setmod("INFO","exiftool3k")



def process_file(filename):
    # thexml=subprocess.check_output(["exiftool", "-X","-fast2",filename])
    thexml=subprocess.check_output(["exiftool", "-X","-l",filename])
    # thexml=subprocess.check_output(["exiftool", "-X", "-createdate", "-aperture", "-shutterspeed",filename])
    # thexml=subprocess.check_output(["echo", "Hello World!"])
    return thexml

def process(infile,outfile):
    # same as above but save result to file
    yy=atpic.log.setname(xx,'proccess')
    atpic.log.debug(yy,"input=",(infile,outfile))
    thexml=process_file(infile)
    f=open(outfile,'wb')
    f.write(thexml)
    f.close()


def process_file_withpipe(filename):
    yy=atpic.log.setname(xx,'process_file_withpipe')

    # -stay_open open could be used to make a service
    # as batch processing is much faster!!!


    # mkfifo exifpipe
    # exiftool -stay_open True -@ exifpipe &


    # I start exiftool as a "daemon" with

    # exiftool -stay_open True -@ /tmp/TestArgs > /tmp/TestArgs.log 2>&1 &

    # Then I pipe commands into the TestArgs file (I piped the complete, attached 12 MB TestArgs into /tmp/TestArgs AT ONCE (cat TestArgs >> /tmp/TestArgs)). 

    # for file in fixture/raw/*.*
    # do
    # echo "-X" >> /tmp/TestArgs
    # echo $file >> /tmp/TestArgs
    # echo "-execute" >> /tmp/TestArgs
    # done

    # for file in fixture/raw/*.*
    # do
    # echo -ne "-X\n$file\n-execute\n"  >> /tmp/TestArgs
    # done
    # echo -ne "-X\nfixture/raw/RAW_SONY_A100.ARW\n-execute\n"  > exifpipe

    # mkfifo exifpipe
    # mkfifo exifresults
    # exiftool -stay_open True -@ exifpipe > exifresults 2>&1 &
    # echo -ne "-X\nfixture/raw/RAW_SONY_A100.ARW\n-execute\n"  > exifpipe
    # cat exifresults 


    # write to the named pipe:
    atpic.log.debug(yy,'opening write pipe')
    # write_pipe=os.open("/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/tests/exifpipe",os.O_RDWR)
    # we force an exception if fifo is not writeable
    write_pipe=os.open("/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/tests/exifpipe",os.O_WRONLY|os.O_NONBLOCK)
    # write_pipe=os.open("/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/tests/exifpipe",os.O_WRONLY)

    # http://stackoverflow.com/questions/5782279/python-why-does-a-read-only-open-of-a-named-pipe-block

    # http://www.qnx.com/developers/docs/6.3.0SP3/neutrino/lib_ref/o/open.html
    """
    O_NONBLOCK
    
        When opening a FIFO with O_RDONLY or O_WRONLY set:

        If O_NONBLOCK is set:
            Calling open() for reading-only returns without delay. Calling open() for writing-only returns an error if no process currently has the FIFO open for reading. 
        If O_NONBLOCK is clear:
            Calling open() for reading-only blocks until a process opens the file for writing. Calling open() for writing-only blocks until a process opens the file for reading. 

        When opening a block special or character special file that supports nonblocking opens:

        If O_NONBLOCK is set:
            The open() function returns without waiting for the device to be ready or available. Subsequent behavior of the device is device-specific. 
        If O_NONBLOCK is clear:
            The open() function waits until the device is ready or available before returning. The definition of when a device is ready is device-specific. 

        Otherwise, the behavior of O_NONBLOCK is unspecified.
        """


    # write
    atpic.log.debug(yy,'start writing to pipe')

    os.write(write_pipe,"-X\n".encode("utf8"))
    command="%s\n" % filename
    os.write(write_pipe,command.encode("utf8"))
    os.write(write_pipe,"-execute\n".encode("utf8"))
    os.close(write_pipe)

    # write_pipe=open("/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/tests/exifpipe","w")
    # write_pipe.write("-X\n")
    # write_pipe.write("%s\n" % filename)
    # write_pipe.write("-execute\n")
    # atpic.log.debug(yy,'closing write pipe')
    # write_pipe.close()
    
    # read
    read_pipe=open("/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/tests/exifresults",'r')
    lines=[]
    line = read_pipe.readline()
    atpic.log.debug(yy,'first line=%s' % line)
    lines.append(line)
    while line:
        line = read_pipe.readline()
        atpic.log.debug(yy,'next line=%s' % line)
        if line=="{ready}\n":
            atpic.log.debug(yy,'GOT END')
            break
        else:
            lines.append(line)
    # close both pipes:
    read_pipe.close()
    thexml=''.join(lines)
    return thexml



if __name__=="__main__":
    filename=b'/home/madon/jpg/866475.jpg'
    thexml=process_file(filename)
    print(thexml)
