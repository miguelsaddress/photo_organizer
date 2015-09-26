# Adapted from 
# http://stackoverflow.com/questions/21355316/getting-metadata-for-mov-video/21395803#21395803
import datetime
import struct


class VideoDater(object):

  ATOM_HEADER_SIZE = 8
  # difference between Unix epoch and QuickTime epoch, in seconds
  EPOCH_ADJUSTER = 2082844800

  def __init__(self, path):    
    # open file and search for moov item
    f = open(path, "rb")
    while 1:
      atom_header = f.read(self.ATOM_HEADER_SIZE)
      if atom_header[4:8] == 'moov':
        break
      else:
        atom_size = struct.unpack(">I", atom_header[0:4])[0]
        f.seek(atom_size - 8, 1)

    # found 'moov', look for 'mvhd' and timestamps
    atom_header = f.read(self.ATOM_HEADER_SIZE)

    if atom_header[4:8] == 'cmov':
      raise VideoFormatError("moov atom is compressed")
    elif atom_header[4:8] != 'mvhd':
      raise VideoFormatError("expected to find 'mvhd' header")
    else:
      f.seek(4, 1)
      cr_date = struct.unpack(">I", f.read(4))[0]
      mod_date = struct.unpack(">I", f.read(4))[0]
        
      self.creation_date = self.__set_formatted_date(cr_date)
      self.modification_date = self.__set_formatted_date(mod_date)

  def __set_formatted_date(self, date_ts):
    return datetime.datetime.utcfromtimestamp(date_ts - self.EPOCH_ADJUSTER)


class VideoFormatError(Exception):
  pass