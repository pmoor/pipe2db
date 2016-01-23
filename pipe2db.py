#!/usr/bin/python

import boto
import gcs_oauth2_boto_plugin
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
  bucket_name = "***"
  data = bz2.compress(sys.stdin.read())
  checksum = hashlib.md5(data).hexdigest()
  recipient = recipient.lower()
  sender = sender.lower()
  time = datetime.now()

  key_name = "%s/%s/%04d/%02d/%s-%s" % (bucket_name, recipient, time.year, time.month, time.isoformat(), checksum)

  uri = boto.storage_uri(key_name, "gs")
  key = uri.new_key()
  key.set_metadata("time", time.isoformat())
  key.set_metadata("recipient", recipient)
  key.set_metadata("sender", sender)
  key.set_contents_from_string(data, replace=False)
except:
  print(sys.exc_info())
  sys.exit(75) # postfix temporary failure
