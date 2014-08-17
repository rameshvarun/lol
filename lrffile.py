import struct
import json
from cStringIO import StringIO
import os
import logging

'''
The code for this module was strongly based on the following ruby
script by https://github.com/robertabcd
Script Link: https://github.com/robertabcd/lol-ob/blob/master/lrf.rb
'''

class LRFFile:
  """Class that can be used to parse the information in a .lrf replay file"""

  def __init__(self, filename):
    # Open file in read-binary mode
    self.file = open(filename, "rb")

    '''For portability concerns, all the binary data is stored in
    little endian format'''

    # First four bytes are version number, second four bytes are meta data size
    self.version, self.meta_size = struct.unpack("<LL", self.file.read(8))

    # Meta data is a large json
    self.metadata = json.loads(self.file.read(self.meta_size))

    # Store the current position as where the data section starts
    data_offset = self.file.tell()

    # Iterate through all of the "parts" in the data
    self.parts = {}
    for index in self.metadata["dataIndex"]:
      key = index['Key']
      offset = index['Value']['offset']
      size = index['Value']['size']

      self.file.seek(data_offset + offset)
      if key == "stream":
        self.parts[key] = LRFStream(self.file)
      else:
        raise Exception("Unkown key %s in dataIndex list." % key)

class LRFStream:
  def __init__(self, file):

    self.type = file.read(1).encode("hex")
    self.size = struct.unpack("<L", file.read(4))[0]

    if self.type != '4e':
      raise Exception("Unkown stream type 0x%s" % self.type)

    print type
    print self.size

    stream_end = file.tell() + self.size - 5

    payload_size = struct.unpack("<L", file.read(4))[0]
    print payload_size
    assert (payload_size + 4) == (self.size - 5)

    i = 0
    while file.tell() < stream_end:
      unk0, uri_size = struct.unpack("<LL", file.read(8))
      #print unk0
      #print uri_size
      obj = file.read(uri_size)
      magic = file.read(1).encode("hex")

      if magic != '0a':
        raise Exception("Magic error: expected 0x0a got 0x%s" % magic)

      i = i + 1
      if i % 2 == 1:
        print obj
      #quit()'''



LRFFile("test.lrf")
