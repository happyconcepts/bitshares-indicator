#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bitshares-indicator
# copyright 2018 ben bird
# https://github.com/happyconcepts/bitshares-indicator
VERSION = '0.4 dev'
APPID 	= 'bitshares-indicator'

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

	self.base = 'USD'

	self.menu = Gtk.Menu()

	self.build_menu()

        self.price_update()

        self.testid = GLib.timeout_add_seconds(60 * self.interval, self.price_update)

	print ("timeout set with id#"+str(self.testid))

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


	item_settings = Gtk.MenuItem()
        item_settings.set_label("Settings")
	item_settings.connect("activate", self.set_list)
        item_settings.show()
        self.menu.append(item_settings)

	item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.handler_menu_exit)
        item.show()
        self.menu.append(item)

        self.menu.show()

        self.ind.set_menu(self.menu)


    def set_list (self, source):

	win = ListBoxWindow()

	win.set_keep_above(True)

	win.connect("destroy", self.handler_menu_reload)

	win.show_all()

    @staticmethod
    def handler_menu_exit(evt):

        Gtk.main_quit()

	print APPID +" has quit."

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
 
	pixbuf = Pixbuf.new_from_file_at_size("icons/bitshares.png", 45, 45)

	dialog.set_logo(pixbuf)

	dialog.run()

        dialog.destroy()

    def price_update(self):

        timestamp = datetime.now().strftime('%m/%d %H:%M:%S')

	try:

	    if not self.test:

		self.b = binance(self.symbol)
		
		if self.base =='EUR':

		    self.c = coinmktcap(self.symbol, self.base)

	     	    self.ind.set_label(self.c.run() + " ~BTC: "+ self.b.run() , "")

		    self.ind.set_icon(os.path.dirname(os.path.realpath(__file__)) +"/icons/bts.png")

		    print timestamp + " BTS price: "+ self.c.price()
		    #print timestamp + " BTS price: "+ self.c.price() + " and interval: " + str(self.interval)

                else :

		    self.g = gate(self.symbol, self.base)

		    self.ind.set_label(self.g.run() + " ~BTC: "+ self.b.run() , "")

		    self.ind.set_icon(os.path.dirname(os.path.realpath(__file__)) +"/icons/bts.png")

		    print timestamp + " BTS price: "+ self.g.price()
		    #print timestamp + " BTS price: "+ self.g.price() + " and interval: " + str(self.interval)
	    else:

		self.ind.set_label("Now in test mode.","")

		print timestamp + " prices not updated (test mode)"

		print "update interval is " + str(self.interval) + " min"

        except Exception as e:

            self.ind.set_label("price update failed!","")

	    self.ind.set_icon(os.path.dirname(os.path.realpath(__file__)) +"/icons/bt_s.png")

	    print timestamp + " prices not updated (check connection)"

	    print(str(e))

        return True

    def main(self):

        Gtk.main()



class gate:

    def __init__(self, coin='bts', base='usdt'):

	if base == 'USD':

	    base = 'USDT'    
    
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

	    return 'Last: $'+str(self.last) + " " +chg +"% (24h)"

    def price(self):

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

            return "Error: binance (api): "+ json['msg']

        else:

	    return u'\u0E3F'+str(json['price'])

class coinmktcap:

    def __init__(self, coin='bitshares', base='EUR'):

	if coin == 'BTS':

	    coin = 'bitshares'  
      
	self.pair = coin +"/?convert="+base

	self.base = base

    def run(self):

        url = 'https://api.coinmarketcap.com/v1/ticker/'+self.pair
	# https://api.coinmarketcap.com/v1/ticker/bitshares/?convert=EUR

        response = requests.get(url)

        json = response.json()

	self.cmcfield = 'price_'+self.base.lower() # price_eur

	if not json[0][self.cmcfield]:

            return "Error: coinmarketcap (api): " + json[0]['error']

        else:

	    self.last = round(float(json[0][self.cmcfield]),4)

	    self.chg = round(float(json[0]['percent_change_24h']),1)

	    self.chg = str(self.chg)

	    if self.chg[:1] != '-':

                self.chg = "+"+ self.chg

	    return 'Last: '+ u'\u20AC' + str(self.last) + " "+ self.chg +"% (24h)"

    def price(self):

	return  u'\u20AC'+str(self.last)


class ListBoxWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Settings")

	self.set_default_size(300, 200)

        self.set_position(Gtk.WindowPosition.CENTER)

	self.set_border_width(10)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.add(box_outer)

        listbox = Gtk.ListBox()

        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        box_outer.pack_start(listbox, True, True, 0)

        
	row = Gtk.ListBoxRow()

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

        row.add(hbox)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)

        hbox.pack_start(vbox, True, True, 0)

        label1 = Gtk.Label("Automatic Updates", xalign=0)

        label2 = Gtk.Label("PRICE SETTINGS", xalign=0)

        vbox.pack_start(label1, True, True, 0)

        vbox.pack_start(label2, True, True, 0)

        switch = Gtk.Switch()

        switch.props.valign = Gtk.Align.CENTER

        hbox.pack_start(switch, False, True, 0)

        listbox.add(row)


	row = Gtk.ListBoxRow()
        
	hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

        row.add(hbox)

	label = Gtk.Label("Base currency:", xalign=0)

        button1 = Gtk.RadioButton.new_with_label_from_widget(None, "$ USD")
        
	if ind.base == 'USD':

	    button1.set_active(True)

	button1.connect("clicked", self.change_base, "USD")

	hbox.pack_start(label, False, False, 0)

	hbox.pack_start(button1, False, False, 0)

	button2 = Gtk.RadioButton.new_from_widget(button1)

        button2.set_label(u'\u20AC' +" Euro")
        
	if ind.base == 'EUR':

	    button2.set_active(True)

        button2.connect("clicked", self.change_base, "EUR")

	hbox.pack_start(button2, False, False, 0)

	listbox.add(row)



        row = Gtk.ListBoxRow()

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

        row.add(hbox)

        label = Gtk.Label("Update interval, minutes", xalign=0)

        combo = Gtk.ComboBoxText()

	combo.connect("changed", self.change_interval)
        combo.insert(0, "5", "5")
        combo.insert(1, "10", "10")
	combo.insert(2, "15", "15")
	combo.insert(3, "60", "60")
	combo.insert(4, "1", "1")
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)

        listbox.add(row)








        listbox_2 = Gtk.ListBox()
        
        #listbox_2.connect('row-activated', lambda widget, row: print (row.data))
        
        box_outer.pack_start(listbox_2, True, True, 0)
        listbox_2.show_all()

    def change_base(self, button, name):

	if button.get_active():

	    ind.base = name

            print("base is set to " +ind.base)

    def change_interval(self, combo):

	self.interval_current = str(ind.interval)

	self.interval_new = combo.get_active_text()

        if self.interval_new is not None:

            print ("interval was " +str(ind.interval))

	    try:
	    #if GLib.source_remove(ind.testid):
		GLib.source_remove(ind.testid)
		print ("old timeout removed")
		ind.interval = self.interval_new
		ind.testid = GLib.timeout_add_seconds(60 * int(ind.interval), ind.price_update)
	        print ("new timeout id# " +str(ind.testid))
		print ("interval now is " +str(ind.interval))
	    except Exception as e:
		print e
  
if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    print "starting "+APPID +" v. "+VERSION

    ind = buyBTSindicator()

    ind.main()

