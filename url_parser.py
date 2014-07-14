import re

string = ".. http://t.co/mAhZ18ljjN"
re.sub(r'[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', "", string)