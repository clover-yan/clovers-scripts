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

## photo_merger（仅 Windows）

`photo_merger.py` 用于将某个文件夹下的所有图片全部尾接头相连拼接。

符合先决条件之后，在终端中运行即可。

### 先决条件

- Python 3
- 安装了 PIL 库（`pip install pillow`）
