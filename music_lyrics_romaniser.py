import os
from mutagen.flac import FLAC
from mutagen.id3 import ID3, USLT
import argparse
import logging

parser = argparse.ArgumentParser(
    description='Romanise Japanese lyrics in mp3/flac files in a directory')
parser.add_argument(
    'directory',
    nargs='?',
    default='.',
    help='Directory containing music files (default: current directory)')
parser.add_argument('-r',
                    '--recursive',
                    action='store_true',
                    help='Recurse into subdirectories')
parser.add_argument(
    '-s',
    '--style',
    dest='style',
    type=str.lower,
    choices=('salt', 'vanilla'),
    default='salt',
    help=
    'Set the style when translations are available: salt (Salt Player, placing romaji above translations) or vanilla (Vanilla Music, placing romaji in the same line with translations) (default: salt)'
)
parser.add_argument(
    '-b',
    '--backend',
    dest='backend',
    type=str.lower,
    choices=('cutlet', 'kakasi'),
    default='cutlet',
    help='Set the romanisation backend: cutlet or kakasi (default: cutlet)')
parser.add_argument(
    '-c',
    '--convert-only',
    action='store_true',
    help=
    'Convert existing romaji lines to the selected style instead of generating new ones'
)
parser.add_argument('--dry-run',
                    action='store_true',
                    help='Perform a dry run without saving changes')
args = parser.parse_args()

dirpath = os.path.abspath(args.directory)

if args.recursive:
	music_list = []
	for root, _, files in os.walk(dirpath):
		for fname in files:
			if fname.lower().endswith(('mp3', 'flac')):
				path = os.path.join(root, fname)
				if os.path.isfile(path):
					music_list.append(path)
else:
	music_list = [
	    os.path.join(dirpath, i) for i in os.listdir(dirpath)
	    if i.lower().endswith((
	        'mp3', 'flac')) and os.path.isfile(os.path.join(dirpath, i))
	]

if args.backend == 'cutlet':
	import cutlet
	katsu = cutlet.Cutlet()

	def convert_to_romaji(text):
		return katsu.romaji(text)
else:
	import pykakasi
	kks = pykakasi.kakasi()

	def convert_to_romaji(text):
		return ' '.join([item['hepburn'] for item in kks.convert(text)])


logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def dump_additional_lines(additional_lines, timestamp):
	result = ''
	if additional_lines:
		if args.style == 'salt':
			result += '\n'.join(
			    (timestamp + i) for i in additional_lines) + '\n'
		else:
			result += timestamp + '｜'.join(additional_lines) + '\n'
		additional_lines.clear()
	return result


def romanise_lyrics(text):
	if not args.convert_only and not any(
	    (ord('ぁ') <= ord(i) <= ord('ん') for i in text)):
		return text
	result = ''
	line_timestamp = ''
	additional_lines = []
	at_beginning = True
	for line in text.split('\n'):
		keep_line = False
		if ']' not in line:
			keep_line = True
		else:
			current_line_timestamp = line[:line.index(']') + 1]
			line_content = line[line.index(']') + 1:]
			if not line_content.strip() or at_beginning and (':' in line_content or '：' in line_content):
				keep_line = True
		if keep_line:
			result += dump_additional_lines(additional_lines, line_timestamp)
			result += line + '\n'
			continue
		at_beginning = False
		if line_timestamp == current_line_timestamp:
			if args.style == 'salt' and args.convert_only:
				additional_lines += line_content.split('｜')
			else:
				additional_lines.append(line_content)
			continue
		result += dump_additional_lines(additional_lines, line_timestamp)
		line_timestamp = current_line_timestamp
		if not args.convert_only:
			additional_lines.append(convert_to_romaji(line_content))
		result += line + '\n'
	result += dump_additional_lines(additional_lines, line_timestamp)
	return result


if __name__ == '__main__':
	for music in music_list:
		ext = music.split('.')[-1].lower()
		if ext == 'flac':
			tags = FLAC(music)
			if 'lyrics' not in tags:
				logger.warning('No lyrics found in %s', music)
				continue
			lyrics = tags['lyrics'][0]
			romanised_lyrics = romanise_lyrics(lyrics)
			if args.dry_run:
				logger.info('Should have processed %s', music)
				logger.info('\n%s', romanised_lyrics)
			else:
				tags['lyrics'] = romanised_lyrics
				tags.save()
				logger.info('Processed %s', music)
		elif ext == 'mp3':
			tags = ID3(music)
			uslt_tag_name = None
			for i in tags.keys():
				if i.startswith('USLT'):
					uslt_tag_name = i
					if uslt_tag_name == 'USLT::jpn':
						break
			else:
				if uslt_tag_name is None:
					logger.warning('No lyrics found in %s', music)
					continue
			lyrics = tags.getall(uslt_tag_name)[0].text
			romanised_lyrics = romanise_lyrics(lyrics)
			if args.dry_run:
				logger.info('Should have processed %s', music)
				logger.info('\n%s', romanised_lyrics)
			else:
				tags.delall(uslt_tag_name)
				tags.add(
				    USLT(encoding=3,
				         lang=uslt_tag_name.split('::')[-1],
				         desc='',
				         text=romanised_lyrics))
				tags.save(music)
				logger.info('Processed %s', music)
		else:
			logger.warning('Unsupported file format: %s', music)

	logger.info('All done!')
