# Example 19-2. Unix socket echo client

# ***** cat also test using *****
# socat - /tmp/socketname
# *******************************
import socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('localhost', 8881))
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/socketname")


print "Connected to server"
data = """A few lines of data
to test the operation
of both server and client."""
for line in data.splitlines(  ):
    sock.sendall(line+'\n')
    print "Sent:", line
    response = sock.recv(8192)
    print "Received:", response
sock.close(  )
