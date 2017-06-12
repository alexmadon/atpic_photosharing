# needs a vncserver (e.g tightvncserver)
# and khtml2png2 
# /usr/bin/khtml2png2


vncserver -localhost -geometry 800x800 -depth 24 -IdleTimeout 0



kill:

date +%T
echo killing epiphany.....
pkill -9 epiphany
echo killing vncserver.....
vncserver -kill :1
vncserver -kill :2
vncserver -kill :3
vncserver -kill :4
vncserver -kill :5
echo Cleaning vncserver..... 
rm -f /tmp/.X11-unix/X*
rm -f /tmp/.X*-lock
date +%T


khtml2png2 --display :1 http://atpic.com atpic.png
