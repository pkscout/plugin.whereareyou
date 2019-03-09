Where Are You is a hacky addon for Kodi that accepts a URL from a stream file and then displays a dialog box with the title and message from the stream file URL.  After the dialog is dismissed a black video plays for 2 seconds.  This is basically to do what the media stub file *should* do, which is display a title and a message for a given file, but the media stub only works if you have an optical drive attached to the device running Kodi.

The format of the URL is:

plugin://plugin.whereareyou?empty=pad&title=Available+streaming&message=This+is+available+via+the+Netflix+app+on+the+TV

I also wrote a little python3 command line tool to generate either media stub or stream files for things that you want in your library but are available on other devices (for me this is stuff like Netflix that I get by using an app on my TV rather than using Kodi).  That command line tool is available at:

https://github.com/pkscout/create.kodi.mediastubs

The icon is Compass by Diane from the Noun Project.