import os
import pykakasi
from mutagen.flac import FLAC
from mutagen.id3 import ID3, USLT
import argparse
import logging

parser = argparse.ArgumentParser(description='Romanise Japanese lyrics in mp3/flac files in a directory')
parser.add_argument('directory', nargs='?', default='.', help='Directory containing music files (default: current directory)')
parser.add_argument('-r', '--recursive', action='store_true', help='Recurse into subdirectories')
parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without saving changes')
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
		os.path.join(dirpath, i)
		for i in os.listdir(dirpath)
		if i.lower().endswith(('mp3', 'flac')) and os.path.isfile(os.path.join(dirpath, i))
	]

kks = pykakasi.kakasi()

# Logging setup
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def romanise_lyrics(text):
	if not any((ord('ぁ') <= ord(i) <= ord('ん') for i in text)):
		return text
	result = ''
	line_timestamp = ''
	for line in text.split('\n'):
		if ']' not in line:
			result += line + '\n'
			continue
		current_line_timestamp = line[:line.index(']') + 1]
		if line_timestamp == current_line_timestamp:
			result += line + '\n'
			continue
		line_timestamp = current_line_timestamp
		line_lyrics = line[line.index(']') + 1:]
		if not line_lyrics.strip():
			result += line + '\n'
			continue
		line_romanised = []
		for item in kks.convert(line_lyrics):
			line_romanised.append(item['hepburn'])
		result += line + '\n'
		result += line_timestamp + ' '.join(line_romanised) + '\n'
	return result

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
			tags.add(USLT(encoding=3, lang=uslt_tag_name.split('::')[-1], desc='', text=romanised_lyrics))
			tags.save(music)
			logger.info('Processed %s', music)
	else:
		logger.warning('Unsupported file format: %s', music)

logger.info('All done!')
