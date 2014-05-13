#!/usr/bin/python

from datetime import datetime
import MySQLdb
import sys

def Connect():
  return MySQLdb.connect(
    host="localhost",
    user="moor-mails",
    passwd="********",
    db="moor-mails")

def Disconnect(connection):
  connection.close()

def ReadEmail():
  return sys.stdin.read()

def AddEmail(connection, content, sender, recipient):
  cursor = connection.cursor()

  query = """INSERT INTO email_meta SET
    tstamp=%s,
    recipient=%s,
    sender=%s"""
  parameters = (datetime.now(), recipient, sender)
  cursor.execute(query, parameters)

  id = cursor.lastrowid
  query = """INSERT INTO email_data SET
    id=%s,
    data=%s"""
  parameters = (id, content)
  cursor.execute(query, parameters)

  connection.commit()

assert len(sys.argv) == 3
recipient = sys.argv[1]
sender = sys.argv[2]
assert recipient
assert sender

try:
  connection = Connect()
  AddEmail(connection, ReadEmail(), sender, recipient)
  Disconnect(connection)
except:
  sys.exit(75) # postfix temporary failure
