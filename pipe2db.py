#!/usr/bin/python

from boto.s3.connection import S3Connection, Location
from boto.s3.key import Key
import bz2
import hashlib
import sys
from datetime import datetime

assert len(sys.argv) == 3
recipient = sys.argv[1]
sender = sys.argv[2]
assert recipient
assert sender

try:
  connection = S3Connection("***", "***", host="s3-us-west-2.amazonaws.com")
  bucket = connection.get_bucket("moor-email")

  data = bz2.compress(sys.stdin.read())
  checksum = hashlib.md5(data).hexdigest()
  recipient = recipient.lower()
  sender = sender.lower()
  time = datetime.now()

  key_name = "%s/%04d/%02d/%s-%s" % (recipient, time.year, time.month, time.isoformat(), checksum)

  key = Key(bucket, key_name)
  key.set_metadata("time", time.isoformat())
  key.set_metadata("recipient", recipient)
  key.set_metadata("sender", sender)
  key.set_contents_from_string(data, replace=False, encrypt_key=True)
  connection.close()
except:
  print(sys.exc_info())
  sys.exit(75) # postfix temporary failure
