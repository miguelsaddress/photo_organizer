import argparse
import os

def DepthValues(value):
	CHOICES = ['y', 'ym', 'ymd']
	if value not in CHOICES:
		raise argparse.ArgumentTypeError("Value must be one of the following: %s" % CHOICES)
	else:
		return value

def ValidDirectory(directory):
	if directory[-1] == "/":
		directory = directory[:-1]

	if os.path.isdir(directory):
		return os.path.abspath(directory)
	else:
		raise argparse.ArgumentTypeError("Input folder must be a valid existing directory")

parser = argparse.ArgumentParser(description='Parsers')
parser.add_argument('--input', '-i', action='store', default=None, dest='input_folder', required=True, type=ValidDirectory, help='The input folder to read')
parser.add_argument('--output', '-o', action='store', default=None, dest='output_folder', type=ValidDirectory, help='The output folder to read')
parser.add_argument('--depth', '-d', action='store', default='ymd', dest='depth', type=DepthValues, help='Level of folder depth. It can be one of the following: y, ym, ymd. Defaults to ymd')
parser.add_argument('--move','-m', action='store_true', default=False, dest='must_move', help='Files must be moved instead of copied. If not given, files are copied')
parser.add_argument('--recursive', '-r', action='store_true', default=False, dest='recursive', help='Should read subfolders recursively.')
parser.add_argument('--verbose', '-v', action='store_true', default=False, dest='verbose', help='Should show information of progress.')

args = parser.parse_args()

print('--depth = %s' % args.depth)
print('--move = %s' % args.must_move)
print('--recursive = %s' % args.recursive)
print('--input = %s' % args.input_folder)
print('--output = %s' % args.output_folder)
print('--verbose = %s' % args.verbose)
print('')


