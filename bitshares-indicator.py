#!/usr/bin/env python

# bitshares-indicator

import os
import requests 
import gi
import signal

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as AppIndicator
from datetime import datetime

VERSION 	= '0.1'
APPID 		= 'bitshares-indicator'
print "starting "+APPID +" v. " +VERSION

class buyBTSindicator(object):
    
    def __init__(self):
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	self.ind = AppIndicator.Indicator.new(APPID,os.path.dirname(os.path.realpath(__file__)) +"/icons/bts.png",AppIndicator.IndicatorCategory.SYSTEM_SERVICES
        )
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)
	self.test = False
	# update interval (minutes):
	self.interval = 5  
        self.symbol = 'BTS'
	self.base = 'USDT'
	self.menu = Gtk.Menu()
	self.build_menu()
        self.price_update()
        GLib.timeout_add_seconds(60 * self.interval, self.price_update)

    def build_menu(self):
        item_refresh = Gtk.MenuItem()
        item_refresh.set_label("Update Prices")
        item_refresh.connect("activate", self.handler_menu_reload)
        item_refresh.show()
        self.menu.append(item_refresh)

	item_about = Gtk.MenuItem()
        item_about.set_label("About")
        item_about.connect("activate", self.about)
        item_about.show()
        self.menu.append(item_about)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.handler_menu_exit)
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.ind.set_menu(self.menu)

    @staticmethod
    def handler_menu_exit(evt):
        Gtk.main_quit()
	print  APPID +" has quit"

    def handler_menu_reload(self, evt):
        self.price_update()

    def about(source, evt):
        dialog = Gtk.AboutDialog()
        dialog.set_program_name('Bitshares Indicator')
        dialog.set_version('0.1')
        dialog.set_license('MIT License\n\n' + 'Copy of the license available upon request' )
        dialog.set_wrap_license(True)
	dialog.set_copyright('Copyright 2018 Ben Bird.')
	dialog.set_comments('This AppIndicator is for Linux systems using Unity.\n\n'+'The indicator tracks the price of Bitshares crypto.\n\n')
	dialog.set_website('http://www.buybts.com')
        dialog.run()
        dialog.destroy()

    def price_update(self):
        timestamp = datetime.now().strftime('%m/%d %H:%M:%S')
	try:
	    if not self.test:
		self.b = binance(self.symbol)
		self.g = gate(self.symbol, self.base)
                self.ind.set_label(self.g.run() + " /BTC: " + self.b.run() , "")
		self.ind.set_icon(os.path.dirname(os.path.realpath(__file__)) +"/icons/bts.png")
		print timestamp + " BTS priced at " + self.g.log()
	    else:
		self.ind.set_label("Now in test mode.","")
		print timestamp + " prices not updated (test mode)"
        except Exception as e:
            print(str(e))
            self.ind.set_label("price update failed!","")
	    self.ind.set_icon(os.path.dirname(os.path.realpath(__file__)) +"/icons/bt_s.png")
	    print timestamp + " prices not updated (check connection)"
        return True

    def main(self):
        Gtk.main()

class gate:
    def __init__(self, coin='bts', base='usdt'):
        self.pair = coin +"_"+ base
        self.pair.lower()

    def run(self):
        url = 'http://data.gate.io/api2/1/ticker/'+self.pair
        response = requests.get(url)
        json = response.json()
        if not json['result']:
            return "Gate says: " + json['message']
        else:
	    chg = str(round(json['percentChange'],1))
	    self.last = round(json['last'],4)
            if chg[:1] != '-':
                chg = "+"+ chg
	    #return 'L: $'+str(round(json['last'],4)) +" 24h Ch: "+ chg +"% "
	    return 'L: $'+str(self.last) +" 24h Ch: "+ chg +"% "

    	
    def log(self):
	return "$" +str(self.last)
	

class binance:
    def __init__(self, coin='BTS', base='BTC'):
        self.pair = coin+base
        self.pair.upper()

    def run(self):
        url = 'https://api.binance.com/api/v3/ticker/price?symbol='+self.pair
        response = requests.get(url)
        json = response.json()
        if not json['price']:
            return "ERR: binance (api): " + json['msg']
        else:
	    return u'\u0E3F' + str(json['price'])

if __name__ == "__main__":
    ind = buyBTSindicator()
    ind.main()

