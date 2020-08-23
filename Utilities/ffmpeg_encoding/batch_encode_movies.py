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
python batch_encode_movies.py --help

-- TODO ROADMAP:
* Add GIF encoding support. Use palettegen and automatically delete palette.png when done
* Handle pre-multiplying RGB by alpha and other transparency-related issues. HAPQ with alpha?
* More flexibility for resolution scaling such as specifying a multiplier like "2x".
* Parse argument for how to name output movies such as a dynamic datetime suffix.
* Better directory traversal/testing for directories that have irregular depths.
"""
from ffmpy import FFmpeg

import glob
import re

import argparse
import os

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
		the output movies will be sibling to their inputs.')
parser.add_argument('--loglevel', dest='loglevel', default='quiet', choices=['quiet','info','verbose'])
parser.add_argument('--no-overwrite', dest='no_overwrite', default=False, action='store_true',
	help='Do you want to disable overwriting of existing movies.')
parser.add_argument('--fps', dest='fps', type=float, default=None,
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

paths = glob.glob(DIRECTORY+'/**', recursive=True) if DIRECTORY is not '' else glob.glob('*')
paths = [p for p in paths if os.path.isfile(p)] # keep only files
video_extensions = ['webm','mkv','flv','mov','gif','avi','wmv','mp4','mv4','mpg','mp2','mpeg','mpv','m4v']
paths = [p for p in paths if str(os.path.splitext(p)[1])[1:] in video_extensions]

for inputpath in paths:
	
	head, tail = os.path.split(inputpath)  # 'some_folder', 'foo.mp4'

	filename = os.path.splitext(tail)[0] # 'foo'

	if args.output is not None:
		head = args.output

	output = os.path.join(head, filename + '_{0}.mov'.format(original_vcodec))  # 'some_folder/foo_hapq.mov'

	scale = ''
	if WIDTH is not None and HEIGHT is not None:
		aspect = str(int(HEIGHT)) + '/' + str(int(WIDTH))
		crop = 'crop=in_h*{aspect}:in_h'.format(aspect=aspect)
		scale = '-vf {0},scale={1}:{2}'.format(crop, WIDTH, HEIGHT)
	if WIDTH is not None and HEIGHT is None:
		scale = '-vf scale={0}:-1'.format(WIDTH)
	elif HEIGHT is not None and WIDTH is None:
		scale = '-vf scale=-1:{0}'.format(HEIGHT)

	loglevel = '-loglevel ' + LOGLEVEL
	overwrite = '' if NOOVERWRITE else '-y'

	all_args = [
		'-r ' + FPS if FPS is not None else '',
		scale,
		'-vb {0}'.format(VARIABLEBITRATE) if VARIABLEBITRATE is not None else '',
		'-bf '+str(BFRAMES) if BFRAMES is not None else '',
		'-g '+str(GOP) if GOP is not None else '',
		'-crf '+str(CRF) if CRF is not None else '',
		'-codec:v '+VCODEC,
		'-format ' +FORMAT if FORMAT is not None else '']

	all_args = filter(lambda a: a != '', all_args)

	# ffmpeg stuff

	ff = FFmpeg(global_options=[loglevel,overwrite],
		inputs={inputpath: None},
		outputs={output: " ".join(all_args)}
		)
	print(ff.cmd)
	ff.run()
