#!/usr/bin/python

import os
import shutil

from PIL import Image
from datetime import datetime
from video_dater import VideoDater
from video_dater import VideoFormatError

class Organizer(object):

  EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
  VIDEO_EXTENSIONS = ['.mp4', '.mov']
  DATE_TAKEN_ID = 36867
  DATE_TAKEN_FMT = "%Y:%m:%d %H:%M:%S"
  UNKNOWN_FOLDER = "unknown_date_taken"

  def __init__(self, args):

    self.UNKNOWN_DATE_TIME_FILES = []
    #from args
    self.VERBOSE = args.verbose
    self.DEPTH = args.depth
    self.MUST_MOVE = args.must_move
    self.RECURSIVE = args.recursive

    if args.output_folder[-1] == "/":
      self.OUTPUT_FOLDER = args.output_folder[:-1]
    else:
      self.OUTPUT_FOLDER = args.output_folder

    if args.input_folder[-1] == "/":
      self.INPUT_FOLDER = args.input_folder[:-1]
    else:
      self.INPUT_FOLDER = args.input_folder

    self.OUTPUT_UNKNOWN_FOLDER = self.OUTPUT_FOLDER + "/" + self.UNKNOWN_FOLDER;


  def run(self):
    self.traverse_folder(self.INPUT_FOLDER)
    self._deal_with_unknown_date_taken_files()

  def traverse_folder(self, folder):
    files = os.listdir(folder)
    self.debug("Files in input folder(%s): %s\n" % (folder, files))

    for current_file in files:
      full_path = folder + "/" + current_file
      if os.path.isfile(full_path):
        date_taken = self._try_get_date_taken(full_path)
        if date_taken is None:
          self.UNKNOWN_DATE_TIME_FILES.append(full_path)
          continue

        dst_folder = self._prepare_and_get_destination(date_taken)
        output_file = dst_folder + "/" + current_file
        self._handle_file(full_path, output_file)
      else:
        if self.RECURSIVE and os.path.isdir(full_path):
          self.traverse_folder(full_path)

  def _has_valid_photo_extension(self, full_path):
    filename, file_extension = os.path.splitext(full_path)
    if file_extension.lower() in self.EXTENSIONS:
      return True
    else:
      return False

  def _has_valid_video_extension(self, full_path):
    filename, file_extension = os.path.splitext(full_path)
    if file_extension.lower() in self.VIDEO_EXTENSIONS:
      return True
    else:
      return False

  def _try_get_date_taken(self, full_path):
    date_taken = None
    try:
      if self._has_valid_photo_extension(full_path):
        date_taken = self._get_date_taken_from_exif_data(full_path)
      elif self._has_valid_video_extension(full_path):
        date_taken = self._get_date_taken_from_video_data(full_path)
    except (AttributeError, VideoFormatError) as e:
      print "Error procesando %s\n" % full_path
      print "e = %s\n" % e

    return date_taken

  def _get_date_taken_from_exif_data(self, src_full_path):
    img = Image.open(src_full_path)   
    exif_data = img._getexif()
    date_taken = None

    if exif_data is not None:
      date_taken = exif_data.get(self.DATE_TAKEN_ID, None)
      if date_taken is not None:
        date = datetime.strptime(date_taken, self.DATE_TAKEN_FMT)
        return date

    return None

  def _prepare_and_get_destination(self, date):
    if date is None: return

    dst = self.OUTPUT_FOLDER

    if 'y' in self.DEPTH: 
        year = str(date.year)
        dst += "/%s" % year
    if 'm' in self.DEPTH: 
        month = datetime.strftime(date, "%B")
        dst += "/%s" % month
    if 'd' in self.DEPTH:
        day = str(date.day)
        dst += "/%s" % day

    if not os.path.exists(dst):
      os.makedirs(dst)

    return dst

  def _handle_file(self, src_path, dst_path):
    self.debug("\tFrom [%s]\n\tto [%s]\n" % (src_path, dst_path))
    if self.MUST_MOVE:
      os.rename(src_path, dst_path)
    else:
      shutil.copy(src_path, dst_path)
    
  def _deal_with_unknown_date_taken_files(self):
    if not os.path.exists(self.OUTPUT_UNKNOWN_FOLDER):
        os.makedirs(self.OUTPUT_UNKNOWN_FOLDER)

    for src in self.UNKNOWN_DATE_TIME_FILES:
        dst = self.OUTPUT_UNKNOWN_FOLDER + "/" + os.path.basename(src)
        self._handle_file(src, dst)


  def _get_date_taken_from_video_data(self, full_path):
    video_dater = VideoDater(full_path)
    date_taken = video_dater.creation_date
    if date_taken.year > 2000:
      return date_taken
    else:
     return None

  def debug(self, msg):
    if self.VERBOSE:
      print(msg)


if __name__ == "__main__":
  from argsparser import args

  org = Organizer(args)
  org.run()