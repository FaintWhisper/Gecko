# Gecko: An automatic tagger for your music
This tool helps you tag your music automatically in a standard and coherent way using the iTunes Store API.

The matching efficency is somewhere between 75~80%, higher than most of the tools currently available out there (although it was designed in the begining to work especially well with EDM songs).

**Important**: Currently, **only FLAC Format is supported**, please, feel free to submit a pull request to add compatibiliy with other formats.

## Prerequisites
You must have Python 3.5+ installed in your computer to make use of this tool.

## Installation
1. Download the latest version of the program from the releases tab.
2. Extract the contents inside a folder.
3. Open a terminal windows and type the following command:
```
python -m pip install -r requirements.txt
```

## Use
1. Place your songs inside the root directory of the project, alonside the script named 'tag.bat'.
2. Run the script by double clicking it and wait for it to finish.

*Tip*: You can also drag and drop the songs you want to tag over the script.

Once finished, all the songs that have been processed succesfully will be fully tagged, although, you may experience a bit of delay if you are trying to tag many songs at once, the script may sleep occasionally to avoid exceeding the requests stablished in the iTunes Store API service policy.

## Authors

* **Amit Karamchandani Batra** - [RYSKZ](https://github.com/RYSKZ)

## Contributing
If you want to contribute to this project you're more than welcome, just send a pull request and you are done!

## Acknowledgments

Thanks to the team behind the library 'itunespy': https://github.com/sleepyfran/itunespy

## License

This project is licensed under the GNU v3.0 License.
