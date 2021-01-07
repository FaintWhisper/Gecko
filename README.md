# SongCat: An automatic tagger for your music
This tool helps you tag your music automatically in a standard and coherent way using the iTunes API.

The matching efficency is about 75~80%, higher than most of the tools currently available out there (although it was designed in the begining to work especially well with EDM songs).

Currently, **only FLAC Format is supported**, please, feel free to submit a pull request to add compatibiliy with more formats.

## Prerequisites
You must have Python 2.7 installed in your computer to make use of this tool.

## Installation
1. Download the latest version of the program from the releases tab.
2. Extract the contents inside a folder.
3. Open a terminal windows and type the following command:
```
py -2 -m pip install -r requirements.txt
```

##Use
1. Place your songs inside the root directory of the project, alonside the script named 'Tag.bat'.
2. Run the script by double clicking it and wait for it to finish.

Once finished, all the songs that have been processed succesfully will be fully tagged.

*Tip*: You can also drag and drop the songs you want to tag into the script.

**Note**: You may experience a bit of delay if you are trying to tag many songs at once, this may occur to avoid exceeding the limit set by the iTunes API service policy.

## Contributing
If you didn't downloaded the packed version from the releases tab and instead you cloned the repo you will need to download the following binaries of my other projects and place them inside the '/bin' folder:
- ArtworkDownloader - https://github.com/RYSKZ/Artwork-Downloader/releases/tag/1.0.0
- Get a song genre from Beatport - https://github.com/RYSKZ/Get-a-song-genre-from-Beatport/releases/tag/1.0.0

If you want to contribute to this project you're more than welcome, just send a pull request and you are done!

## Authors

* **Amit Karamchandani Batra** - [RYSKZ](https://github.com/RYSKZ)

## License

This project is licensed under the GNU v3.0 License.

## Acknowledgments

Thanks to the team behind the library 'pyhton-itunes': https://github.com/ocelma/python-itunes
