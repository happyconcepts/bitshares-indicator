#!/usr/bin/env python

# bitshares-indicator
# copyright 2018 ben bird
# https://github.com/happyconcepts/bitshares-indicator

VERSION 	= '0.3'
APPID 		= 'bitshares-indicator'

import os
import requests 
import gi
import signal

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Pixbuf

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as AppIndicator

from datetime import datetime

class buyBTSindicator(object):
    # constructor
    def __init__(self):
	self.ind = AppIndicator.Indicator.new(APPID,
	os.path.dirname(os.path.realpath(__file__)) +
	"/icons/bts.png",AppIndicator.IndicatorCategory.SYSTEM_SERVICES
        )
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)
	self.test = False
	# update interval (minutes):
	self.interval = 5  
        self.symbol = 'BTS'
	self.base = 'USDT' # usd, eur, cny
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

	item_base = Gtk.MenuItem()
        item_base.set_label("Settings")
	item_base.connect("activate", self.set_base)
        item_base.show()
        self.menu.append(item_base)

	item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.handler_menu_exit)
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.ind.set_menu(self.menu)

    def set_base (self, source):
	win = SetBaseWindow()
	#win.connect("destroy", Gtk.main_quit)
	win.show_all()

    @staticmethod
    def handler_menu_exit(evt):
        Gtk.main_quit()
	print APPID +" has quit"

    def handler_menu_reload(self, evt):
        self.price_update()

    def about(source, evt):
        dialog = Gtk.AboutDialog()
	dialog.set_border_width(10)
        dialog.set_program_name('bitshares-indicator')
        dialog.set_version(VERSION)
        dialog.set_license('MIT License\n\n' + ' A copy of the license is available at https://github.com/happyconcepts/bitshares-indicator/blob/master/LICENSE' )
        dialog.set_wrap_license(True)
	dialog.set_copyright('Copyright 2018 Ben Bird.')
	dialog.set_comments('Linux app indicator tracks bitshares price (BTS)\n\n'+'Donations appreciated!\n\n' + 'BTS: buy-bitcoin\n' +'BitUSD: buy-bitcoin\n'+'Bitcoin: 1FZhqidv4oMRoiry9mGASFL7JSgdB27Mmn')
	dialog.set_website('http://www.buybts.com')   
	pixbuf = Pixbuf.new_from_file_at_size("icons/bitshares.png", 40, 40)
	dialog.set_logo(pixbuf)
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
            return "Error: binance (api): " + json['msg']
        else:
	    return u'\u0E3F' + str(json['price'])

class SetBaseWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Settings")
        self.set_border_width(15)
	self.set_default_size(300, 60)
	self.set_position(Gtk.WindowPosition.CENTER)
        hbox = Gtk.Box(spacing=6)
        self.add(hbox);

	label = Gtk.Label("Choose your base:")
        hbox.pack_start(label, False, False, 0)
        button1 = Gtk.RadioButton.new_with_label_from_widget(None, "$ USD")
        button1.connect("clicked", self.change_base, "USDT")
	if ind.base == 'USDT':
	    button1.set_active(True)
	hbox.pack_start(button1, False, False, 0)

        button2 = Gtk.RadioButton.new_from_widget(button1)
        button2.set_label(u'\u20AC' + " Euro")
        button2.connect("clicked", self.change_base, "EUR")
	if ind.base == 'EUR':
	    button2.set_active(True)
        hbox.pack_start(button2, False, False, 0)

    def change_base(self, button, name):
	if button.get_active():
	    ind.base = name
            print("base set: " +ind.base)

  
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    print "starting "+APPID +" v. "+VERSION
    ind = buyBTSindicator()
    ind.main()

