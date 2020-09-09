"""
David Braun (github.com/DBraun)

-- INSTRUCTIONS:
Install Python 3.4 or higher

Download ffmpeg and move the folder so you have C:/ffmpeg/bin/ffmpeg.exe

Put "C:/ffmpeg/bin" in your "PATH" system environment variable.
Use a semicolon to separate it from other items already in PATH.

Use pip to install ffmpy:
pip install ffmpy

Use this script to learn about the script arguments:
python batch_encode_frames.py --help

-- TODO ROADMAP:
* Add GIF encoding support. Use palettegen and automatically delete palette.png when done
* Handle pre-multiplying RGB by alpha and other transparency-related issues. HAPQ with alpha?
* More flexibility for resolution scaling such as specifying a multiplier like "2x".
* Encode audio with the video. Might assume there's an audio file inside each directory.
* Parse argument for how to name output movies such as a dynamic datetime suffix.
* Better directory traversal/testing for directories that have irregular depths.
"""
from ffmpy import FFmpeg

import glob
import re

import os
import argparse

class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


parser = argparse.ArgumentParser(description='Batch convert directories of images to movies. \
	All command-line arguments are optional.')
parser.add_argument('--input', dest='input', default='', help='The directory that contains folders of images. \
	Use backslashes if necessary.')
parser.add_argument('--output', dest='output', action=readable_dir, default=None, help='The output directory. If not specified,\
		The output movies will be sibling to their inputs.')
parser.add_argument('--loglevel', dest='loglevel', default='quiet', choices=['quiet','info','verbose'])
parser.add_argument('--no-overwrite', dest='no_overwrite', default=False, action='store_true',
	help='Do you want to disable overwriting of existing movies.')
parser.add_argument('--extension', dest='extension', default='png', choices=['png','tif','tiff','jpeg','jpg'],
                    help='The file extension of the images that will be encoded.')
parser.add_argument('--fps', dest='fps', type=float, default=30,
                    help='The desired frame rate for the output movie.')
# mjpeg is photo/jpeg
parser.add_argument('--vcodec', dest='vcodec', default='hap_q', choices=['hap','hap_q','hap_alpha','libx264','libx265','mjpeg']) # 'gif' not implemented yet!
parser.add_argument('--width', dest='width', default=None, help="Width in pixels of the output. \
	Aspect ratio of the input will be preserved if height isn't specified.")
parser.add_argument('--height', dest='height', default=None, help="Height in pixels of the output. \
	Aspect ratio of the input will be preserved if width isn't specified.")
parser.add_argument('--vb', dest='vb', default=None, help='video variable bitrate: For example "20M" for 20 Mbps')
parser.add_argument('--bf', dest='bf', default=None, help='B-Frame interval. This is optional.')
parser.add_argument('--g', dest='g', default=None, help='Group of pictures interval. Maybe set to 1 when you set bf to 0.')
parser.add_argument('--crf', dest='crf', default=None, help="Constant Rate Factor. Use this if you care more about quality than filesize. \
	The range is 0-51 where 0 is lossless, 23 is the default, and 51 is high compression.")

args = parser.parse_args()

DIRECTORY = args.input
FPS = args.fps
LOGLEVEL = args.loglevel
NOOVERWRITE = args.no_overwrite
EXTENSION = args.extension
VCODEC = args.vcodec
WIDTH = args.width
HEIGHT = args.height
VARIABLEBITRATE = args.vb
BFRAMES = args.bf
CRF = args.crf
GOP = args.g

# format argument is necessary in case of hap_q and hap_alpha.
# codec must also change.
FORMAT = None
original_vcodec = VCODEC
if VCODEC == 'hap_q' or VCODEC == 'hap_alpha':
	FORMAT = VCODEC
	VCODEC = 'hap'

paths = glob.glob(DIRECTORY+'/*') if DIRECTORY != '' else glob.glob('*')
paths = [p for p in paths if os.path.isdir(p)] # keep only directories

pattern = re.compile('.*?(\d*)\D*\.'+EXTENSION) # for regex later
# The regex has 4 sections. The second section is grouped.
# The first section is any amount of text, non-greedy.
# The second section is any amount of digits, greedy, and captured in a group.
# The third section is any amount of non-digits, greedy.
# The fourth section is a period and then a file extension.

for p in paths:

	images = glob.glob(p+'/*.'+EXTENSION)
	if not images:
		# This directory doesn't have one of the files
		# with the requested image extension.
		# Continue on to the next directory.
		continue

	firstimage = images[0] # 'foo/bar_0001.png'
	
	m = re.match(pattern, firstimage)

	if m is None:
		# This directory didn't have the expected image.
		# Perhaps there's something irregular about the digit naming.
		# Continue on to the next directory.
		continue

	digit_string = m.group(1) # '0001' hopefully but might be '0100' etc.
	num_digits = len(digit_string) # len('0001') -> 4

	replace_string = '%0{0}d'.format(str(num_digits)) # '%04d' for 4 digit padding
	dotextension = firstimage[m.end(1):] # .png or _blah.png in the case of foo/bar_0001_blah.png

	if args.output is not None:
		head = args.output
	else:
		head = ''

	inputpath = firstimage[:m.start(1)] + replace_string + dotextension # 'foo/bar_%04d.png'
	if VCODEC == 'libx264':
		filename = p + '.mp4'  # 'foo.mp4'
	elif VCODEC != 'gif':
		filename = p + '_{0}.mov'.format(original_vcodec)  # 'foo_hapq.mov'
	else:
		filename = p + '.gif'

	output = os.path.join(head, filename)

	outputdir = os.path.dirname(output)
	if not os.path.isdir(outputdir):
		# make directory to contain movie
		os.makedirs(outputdir)

	scale = ''
	if WIDTH is not None and HEIGHT is not None:
		scale = '-vf scale={0}:{1}'.format(WIDTH, HEIGHT)
	if WIDTH is not None and HEIGHT is None:
		scale = '-vf scale={0}:-1'.format(WIDTH)
	elif HEIGHT is not None and WIDTH is None:
		scale = '-vf scale=-1:{0}'.format(HEIGHT)

	loglevel = '-loglevel ' + LOGLEVEL
	overwrite = '' if NOOVERWRITE else '-y'

	# ffmpeg stuff

	if VCODEC == 'gif':

		# if making a GIF, make the palette first.
		palette = p + "_palette.png"
		if scale == '':
			print("You must specify a width or height when making a GIF.")
			continue
		scalefilter = scale[4:] # 'scale=192:108' etc
		filters = 'fps={0},{1}:flags=lanczos'.format(str(FPS),scalefilter)

		ff = FFmpeg(global_options=[loglevel],
			inputs={inputpath: None},
			outputs={palette: '-y -vf "{filters},palettegen"'.format(filters=filters)}
			)
		print(ff.cmd)
		ff.run()

		# now make the gif
		from collections import OrderedDict
		inputs = OrderedDict([(inputpath, None), (palette, None)])
		ff = FFmpeg(global_options=[loglevel,overwrite],
			inputs=inputs,
			outputs={output: '-lavfi {filters} [x]; [x][1:v] paletteuse'.format(filters=filters)}
			)
		print(ff.cmd)
		ff.run()

	else:
		# not a gif encoding

		all_args = [
			scale,
			'-vb {0}'.format(VARIABLEBITRATE) if VARIABLEBITRATE is not None else '',
			'-bf '+str(BFRAMES) if BFRAMES is not None else '',
			'-g '+str(GOP) if GOP is not None else '',
			'-crf '+str(CRF) if CRF is not None else '',
			'-codec:v '+VCODEC,
			'-format ' +FORMAT if FORMAT is not None else '',
			'-vsync vfr', # this line makes the first frame not get duplicated.
			'-r ' + str(FPS)]

		all_args = filter(lambda a: a != '', all_args)

		ff = FFmpeg(global_options=[loglevel,overwrite, '-r ' + str(FPS)],
			inputs={inputpath: None},
			outputs={output: " ".join(all_args)}
			)
		print(ff.cmd)
		ff.run()
