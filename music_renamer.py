import os
from tinytag import TinyTag

mp3s = []

# get all mp3 filenames in current path
for filename in os.listdir('.'):
	if filename.endswith(('mp3', 'MP3', 'flac', 'FLAC')):
		mp3s.append(filename)

for mp3 in mp3s:
	extension = mp3.split('.')[-1].lower()
	tag = TinyTag.get(mp3)
	# remane mp3 file to 'artist - title.mp3'
	new_name = tag.artist + ' - ' + tag.title + f'.{extension}'
	# replace invalid characters
	new_name = new_name.replace('/', '-').replace('\\', '-').replace(':', ' -').replace('*', '').replace('?', '').replace('"', "'").replace('<', '').replace('>', '').replace('|', '').replace('!', '')
	# check if file already exists
	if new_name != mp3.lower() and os.path.exists(new_name):
		i = 2
		valid_name = new_name[:-len(extension)-1] + f' ({i}).{extension}'
		while new_name != mp3 and os.path.exists(valid_name):
			i += 1
			valid_name = new_name[:-len(extension)-1] + f' ({i}).{extension}'
		new_name = valid_name
	os.rename(mp3, new_name)
	# lrc file
	try:
		lrc = mp3[:-len(extension)] + 'lrc'
		new_lrc = new_name[:-len(extension)] + 'lrc'
		os.rename(lrc, new_lrc)
	except:
		pass
	print('Renamed:', mp3, '->', new_name)
print('Done!')
