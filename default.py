# *  Credits:
# *
# *  original Where Are You code by pkscout

import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os, sys, urllib
from resources.common.fix_utf8 import smartUTF8
from resources.common.xlogger import Logger

addon        = xbmcaddon.Addon()
addonname    = addon.getAddonInfo('id')
addonversion = addon.getAddonInfo('version')
addonpath    = addon.getAddonInfo('path').decode('utf-8')
addonicon    = xbmc.translatePath('%s/icon.png' % addonpath )
language     = addon.getLocalizedString
preamble     = '[Where Are You]'

lw      = Logger( preamble=preamble, logdebug='True' )

class Main:

    def __init__( self ):
        self._parse_argv()
        dialog = xbmcgui.Dialog()
        ok = dialog.ok( self.TITLE, self.MESSAGE )
        self.play_video( os.path.join( addonpath, 'resources', 'blank.mp4' ) )


    def _parse_argv( self ):
        try:
            params = dict( arg.split( "=" ) for arg in sys.argv[ 2 ].split( "&" ) )
        except IndexError:
            params = {}        
        except Exception as e:
            lw.log( ['unexpected error while parsing arguments', e] )
            params = {}
        self.TITLE = urllib.unquote_plus( params.get( 'title', '') ).decode( 'utf8' )
        self.MESSAGE = urllib.unquote_plus( params.get( 'message', '') ).decode( 'utf8' )


    def play_video( self, path ):
        play_item = xbmcgui.ListItem( path=path )
        xbmcplugin.setResolvedUrl( int(sys.argv[1]), True, listitem=play_item )


if ( __name__ == "__main__" ):
    lw.log( ['script version %s started' % addonversion], xbmc.LOGNOTICE )
    slideshow = Main()
lw.log( ['script stopped'], xbmc.LOGNOTICE )
