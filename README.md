# Trix

Metadata parser/converter/encoder for Hunter's Trix.

*Scot Hacker, 05/15 - http://birdhouse.org/blog/contact/*

[Hunter's Trix](https://www.facebook.com/GratefulDeadTrix/info?tab=page_info) is an incredible (and very large) collection of "matrix" recordings of some of the best Grateful Dead shows.

> "The series is produced and mixed by Jubal Hunter Seamons and includes CD cover artwork for each volume/show." 

A matrix involves taking a high-quality soundboard recording and merging (matrixing) it with one or more audience recordings (Auds) of the same show. The resulting matrix brings you the maximum fidelity of the soundboard source and the ambience/electricity of being in the audience at the same time.

There are more than 100 Hunter matrixes being traded as legal torrents on [etree.org](http://bt.etree.org/). 

![HT30](http://img238.imageshack.us/img238/646/gd910408bookletcover.jpg)

Unfortunately, there are two problems: 1) They're all in FLAC format, instead of Apple Lossleess (ALAC). Since most people use iTunes, this means most people must go through a manual transcoding process; 2) The first 94 shows are missing embedded metadata and cover art (the cover art is beautiful). I'm obsessive about having perfect metadata and cover art in every single track in my collection, which meant manually copying and pasting metadata (including track and disc numbers, show dates and venues, track and album titles, etc.) from text files in the download directory into individual track files. It was taking 20+ minutes to process each album. So I decided to automate the process with this python script. 

I had originally planned to share the completed ALAC versions of the collection back to the community, but Hunter talked me out of it. So I'm doing the next best thing here and sharing the conversion script. With everything installed and working, I was able to cut the processing time down from ~20 minutes per recording to 1 minute. The final results are added to your iTunes collection automagically.

![HT58](http://fc07.deviantart.net/fs71/f/2013/292/6/4/ht_vol__58__booklet_cover_by_hseamons-d2z55zf.jpg)

### Installation

You will need some comfort working in the Terminal, installing command-line tools, and running Python scripts. I'm sorry I can't offer support for these techniques.

Copy `trix.py` into a folder somewhere on your python path. Try `/usr/local/bin` if in doubt. Then you'll need to make sure these three tools are installed and working:

- [metaflac](https://xiph.org/flac/documentation_tools_metaflac.html) CLI binary
- [MP4v2](https://mp4v2.googlecode.com/svn/doc/1.9.0/ToolGuide.html) for adding cover art (mp4art)
- [FFMpeg](https://www.ffmpeg.org/) to convert from .flac to .m4a

### Workflow

0. Create a directory to process files from, such as `process`

0. From the bittorrent download directory, copy all `*.flac` files, the cover image you want, and the main info file, which probably has a name like `gd74-06-22.mtx.seamons.txt` into the `process` directory.

0. Rename the info file to `data.txt`. Rename the cover art file to `cover.jpg`

0. In the terminal, cd to the "process" directory and run `python trix.py`

0. Enter the volume number (e.g. `67`) when prompted

0. When the crunching is complete, make sure everything ended up in iTunes OK.

0. Dig!

![HT17](http://img98.imageshack.us/img98/7313/gd801003bookletcover.jpg)
