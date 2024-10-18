import os
from tinytag import TinyTag


mp3s = [i for i in os.listdir('.') if i.lower().endswith(('mp3', 'flac'))]

for mp3 in mp3s:
	extension = mp3.split('.')[-1].lower()
	tag = TinyTag.get(mp3)
	# remane mp3 file to 'artist - title.mp3'
	new_name = tag.artist + ' - ' + tag.title + f'.{extension}'
	# replace invalid characters
	new_name = new_name.replace('/', '-').replace('\\', '-').replace(':', ' -').replace('*', '').replace('?', '').replace('"', "'").replace('<', '').replace('>', '').replace('|', '').replace('!', '')
	# check if file already exists
	if new_name[:-len(extension)-1] != mp3[:-len(extension)-1] and os.path.exists(new_name):
		i = 2
		valid_name = new_name[:-len(extension)-1] + f' ({i}).{extension}'
		while valid_name[:-len(extension)-1] != mp3[:-len(extension)-1] and os.path.exists(valid_name):
			i += 1
			valid_name = new_name[:-len(extension)-1] + f' ({i}).{extension}'
		new_name = valid_name
	if new_name != mp3:
		os.rename(mp3, new_name)
		print('Renamed:', mp3, '->', new_name)
		try:
			lrc = mp3[:-len(extension)] + 'lrc'
			new_lrc = new_name[:-len(extension)] + 'lrc'
			os.rename(lrc, new_lrc)
			print('  Renamed lyrics too')
		except:
			pass
print('Done!')
