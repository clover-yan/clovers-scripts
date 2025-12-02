# clovers-scripts

Clover's Scripts. Contains small but useful scripts.

Clover 的脚本。包括微小但好用的脚本。

## folder_breaker（仅 Windows）

`folder_breaker.bat` 用于「粉碎」文件夹，可以把某个文件夹下所有的文件移动到该目录下。

把脚本复制到要粉碎的目录，运行即可。

## music_renamer

`music_renamer.py` 用于将某个文件夹下的所有音乐文件按照`歌手 - 歌曲名`格式重命名。

支持同时重命名 `lrc` 文件。

> **注意：**请确保音乐文件的标签（元数据）信息是正确的，否则可能会导致重命名结果不符合预期。

符合先决条件之后，在终端中运行即可。

### 先决条件

- Python 3
- 安装了 TinyTag 库（`pip install tinytag`）

## music_lyrics_romaniser

`music_lyrics_romaniser.py` 用于将某个文件夹下的所有音乐文件的歌词标签（元数据）进行罗马字化处理。

支持 `mp3` 和 `flac` 格式的音乐文件。

支持两种风格，用 `-s` 参数指定：
- `salt`：适用于椒盐音乐、Myune Music 等播放器，罗马字歌词会被放在原歌词的下方一行、翻译歌词的上方一行。
- `vanilla`：适用于香草音乐，罗马字歌词会和翻译歌词同处于原歌词的下方一行，中间用竖线 `｜` 分隔。

支持对这个脚本生成的带罗马音歌词进行风格互转，用 `-c` 参数指定。

符合先决条件之后，在终端中运行即可。

### 先决条件

- Python 3
- 拥有使用如下 LRC 歌词格式的音乐库：
  ```
  [00:10.00]歌词
  [00:10.00]译文
  [00:20.00]歌词
  [00:20.00]译文
  ...
  ```
- 安装了 mutagen 库（`pip install mutagen`）
- 安装了 pykakasi 库（`pip install pykakasi`）

## photo_merger（仅 Windows）

`photo_merger.py` 用于将某个文件夹下的所有图片全部尾接头相连拼接。

符合先决条件之后，在终端中运行即可。

### 先决条件

- Python 3
- 安装了 PIL 库（`pip install pillow`）
