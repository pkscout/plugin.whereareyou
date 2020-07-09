from kodi_six import xbmc, xbmcaddon, xbmcgui
from kodi_six.utils import py2_decode
import json, os, sys
from resources.lib.waysettings import loadSettings
from resources.lib.xlogger import Logger
try:
    from urllib.parse import unquote_plus as _unquote_plus
    from urllib.parse import quote_plus as _quote_plus
except ImportError:
    from urllib import unquote_plus as _unquote_plus
    from urllib import quote_plus as _quote_plus


class Main:

    def __init__( self ):
        self._init_vars()
        self.LW = Logger( preamble='[Where Are You]', logdebug=self.SETTINGS['debug'] )
        self.LW.log( ['script version %s started' % self.SETTINGS['ADDONVERSION']], xbmc.LOGINFO )
        self._parse_argv()
        if self.TITLE and self.MESSAGE:
            self._display_dialog()
        else:
            self._mappings_options()
        self.LW.log( ['script stopped'], xbmc.LOGINFO )


    def _display_dialog( self ):
        use_extended_dialog = False
        addon = ''
        mapping_args = ''
        try:
            json_mappings = json.loads( self.SETTINGS['mappings'] )
        except ValueError:
            json_mappings = {}
        if json_mappings:
            for item in json_mappings:
                thematch = json_mappings.get( item, {} ).get( 'match', '' )
                self.LW.log( ['checking for %s in %s' % (thematch, self.TITLE)] )
                self.LW.log( ['checking for %s in %s' % (thematch, self.MESSAGE)] )
                if thematch.lower() in self.TITLE.lower() or thematch.lower() in self.MESSAGE.lower():
                    self.LW.log( ['found match'] )
                    addon = json_mappings.get( item, {} ).get( 'addon', '' )
                    mapping_args = json_mappings.get( item, {} ).get( 'args', '' )
                    self.MESSAGE = '%s %s' % (self.MESSAGE, self.SETTINGS['ADDONLANGUAGE']( 32303 ))
                    use_extended_dialog = True
                    break
        if use_extended_dialog:
            if self.DIALOG.yesno( self.TITLE, self.MESSAGE ):
                args = addon
                if mapping_args:
                    args = '%s,%s' % (args, mapping_args)
                xbmc.executebuiltin( 'RunScript(plugin.whereareyou.broker,%s)' % args )
        else:
            self.DIALOG.ok( self.TITLE, self.MESSAGE )
        xbmc.Player().play( os.path.join( self.SETTINGS['ADDONPATH'], 'resources', 'blank.mp4' ) )


    def _get_addonlist( self ):
        res = xbmc.executeJSONRPC (
            '{ "jsonrpc": "2.0", "method": "Addons.GetAddons","params":{"type":"xbmc.addon.video"}, "id": "1"}' )
        json_res = json.loads( res )
        addons = json_res.get( 'result', {} ).get( 'addons', [] )
        self.LW.log( ['the addons are:', addons] )
        addonlist = []
        for item in addons:
            addon = item.get( 'addonid', '' )
            if addon:
                addonlist.append( addon )
        addonlist.sort()
        return addonlist


    def _init_vars( self ):
        self.SETTINGS = loadSettings()
        self.DIALOG = xbmcgui.Dialog()


    def _mappings_options( self ):
        options = [ self.SETTINGS['ADDONLANGUAGE']( 32300 ) ]
        if self.SETTINGS['mappings']:
            options.append( self.SETTINGS['ADDONLANGUAGE']( 32301 ) )
            options.append( self.SETTINGS['ADDONLANGUAGE']( 32302 ) )
        ret = self.DIALOG.select( self.SETTINGS['ADDONLANGUAGE']( 32200 ), options )
        self.LW.log( ['got back %s from the dialog box' % str( ret )] )
        if ret == -1:
            return
        if ret == 0:
            self._option_add()
        elif ret == 1:
            self._option_edit()
        elif ret == 2:
            self._option_edit( dodelete=True )


    def _option_add( self, default_match='', default_addon='', default_args='' ):
        thematch = self.DIALOG.input( self.SETTINGS['ADDONLANGUAGE']( 32201 ), defaultt=default_match )
        if not thematch:
            return
        addonlist = self._get_addonlist()
        default_addon_loc = None
        if default_addon:
            x = 0
            for addon in addonlist:
                self.LW.log( ['checking %s against %s' % (addon, default_addon)] )
                if addon == default_addon:
                    default_addon_loc = x
                    self.LW.log( ['found match, the default location is %s' % str( default_addon_loc )] )
                    break
                x = x + 1
        if default_addon_loc:
            self.LW.log( ['using dialog with preselect'] )
            ret = self.DIALOG.select( self.SETTINGS['ADDONLANGUAGE']( 32202 ), addonlist, preselect=default_addon_loc )
        else:
            self.LW.log( ['using dialog with no preselect'] )
            ret = self.DIALOG.select( self.SETTINGS['ADDONLANGUAGE']( 32202 ), addonlist )
        if ret == -1:
            return
        addon = addonlist[ret]
        args = self.DIALOG.input( self.SETTINGS['ADDONLANGUAGE']( 32203 ), defaultt=default_args )
        try:
            json_mappings = json.loads( self.SETTINGS['mappings'] )
        except ValueError:
            json_mappings = {}
        json_mappings[thematch] = {'match':thematch, 'addon':addon, 'args':args}
        self.SETTINGS['ADDON'].setSetting( 'mappings', json.dumps( json_mappings ) )


    def _option_edit( self, dodelete=False ):
        self.LW.log( [self.SETTINGS['mappings']] )
        try:
            json_mappings = json.loads( self.SETTINGS['mappings'] )
        except ValueError:
            self._option_add()
            return
        saved_mappings = []
        for item in json_mappings:
            mapping_name = json_mappings.get( item, {} ).get( 'match', '' )
            if mapping_name:
                saved_mappings.append( mapping_name )
        saved_mappings.sort()
        ret = self.DIALOG.select( self.SETTINGS['ADDONLANGUAGE']( 32204 ), saved_mappings )
        if ret == -1:
            return
        if dodelete:
            del json_mappings[saved_mappings[ret]]
            self.SETTINGS['ADDON'].setSetting( 'mappings', json.dumps( json_mappings ) )
        else:
            thematch = json_mappings.get( saved_mappings[ret], {} ).get( 'match', '' )
            addon = json_mappings.get( saved_mappings[ret], {} ).get( 'addon', '' )
            args = json_mappings.get( saved_mappings[ret], {} ).get( 'args', '' )
            self._option_add( default_match=thematch, default_addon=addon, default_args=args )

    def _parse_argv( self ):
        try:
            params = dict( arg.split( "=" ) for arg in sys.argv[2].split( "&" ) )
        except IndexError:
            params = {}
        except Exception as e:
            self.LW.log( ['unexpected error while parsing arguments %s' % e] )
            params = {}
        self.TITLE = py2_decode( _unquote_plus( params.get( 'title', '') ) )
        self.MESSAGE = py2_decode( _unquote_plus( params.get( 'message', '') ) )


