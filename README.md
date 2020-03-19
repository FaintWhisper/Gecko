# SongCat: An automatic tagger for your music
This tool helps you tag your music automatically and in a standard and coherent way using the iTunes API. The matching efficency is about 75~80%, higher that most of the tools currently available out there, although it was designed in the begining to work especially well with EDM songs.

**IMPORTANT NOTE**: For now this tools only supports songs in FLAC format. Please, feel free to submit a pull request to add compatibiliy with more types.

## Prerequisites
You must have installed Python 2.7 in your computer to make use of this tool.

## Use
After downloading the app from the releases tab, you should follow this steps to make use of the tool.

1. First, you need to place your songs inside the root directory of the project, alonside the script named 'Tag.bat'.
2. After that, run the script aforementioned (Tag.bat) and wait until it finishes.
3. Once finished, all the songs processed succesfully will be fully tagged.

You can also drag the songs you want to tag to the mentioned script.

Note: You may experience a bit of delay if you are trying to tag many songs at once, this may occur to avoid exceeding the limit set by the iTunes API service policy.

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
