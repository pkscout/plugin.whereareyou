# *  Credits:
# *
# *  original Where Are You code by pkscout

from kodi_six import xbmc, xbmcaddon, xbmcgui, xbmcplugin
from kodi_six.utils import py2_decode
import os, sys
try:
    from urllib.parse import unquote_plus as _unquote_plus
except ImportError:
    from urllib import unquote_plus as _unquote_plus
from resources.common.xlogger import Logger

addon        = xbmcaddon.Addon()
addonname    = addon.getAddonInfo('id')
addonversion = addon.getAddonInfo('version')
addonpath    = addon.getAddonInfo('path')
addonicon    = xbmc.translatePath('%s/icon.png' % addonpath )
language     = addon.getLocalizedString
preamble     = '[Where Are You]'

lw = Logger( preamble=preamble, logdebug='True' )

class Main:

    def __init__( self ):
        self._parse_argv()
        if self.TITLE and self.MESSAGE:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok( self.TITLE, self.MESSAGE )
            self.play_video( os.path.join( addonpath, 'resources', 'blank.mp4' ) )
        else:
            lw.log( ['One or both of title ("%s") and message ("%s") not set.' % (self.TITLE, self.MESSAGE)] )


    def _parse_argv( self ):
        try:
            params = dict( arg.split( "=" ) for arg in sys.argv[2].split( "&" ) )
        except IndexError:
            params = {}        
        except Exception as e:
            lw.log( ['unexpected error while parsing arguments', e] )
            params = {}
        self.TITLE = py2_decode( _unquote_plus( params.get( 'title', '') ) )
        self.MESSAGE = py2_decode( _unquote_plus( params.get( 'message', '') ) )


    def play_video( self, path ):
        play_item = xbmcgui.ListItem( path=path )
        try:
            xbmcplugin.setResolvedUrl( int( sys.argv[1] ), True, listitem=play_item )
        except IndexError:
            return


if ( __name__ == "__main__" ):
    lw.log( ['script version %s started' % addonversion], xbmc.LOGNOTICE )
    action = Main()
lw.log( ['script stopped'], xbmc.LOGNOTICE )
