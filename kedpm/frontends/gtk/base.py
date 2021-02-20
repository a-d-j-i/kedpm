# Copyright (C) 2003  Andrey Lebedev <andrey@micro.lt>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id: base.py,v 1.5 2003/09/05 19:40:23 kedder Exp $

from gi.repository import Gtk


def processEvents():
    while Gtk.events_pending():
        Gtk.main_iteration_do(Gtk.FALSE)


class Window:
    '''Base class for all KedPM windows.
    
    methods, which names starts with "on_" gets automatically connected to
    respective glade signals.'''

    name = ""
    window = None
    signals = {}

    # menu_names=[]
    # menus = {}

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_objects_from_file("glade/kedpm.glade", [self.name])
        self.widgetTree = builder
        # pygtkcompat.glade.XML(globals.glade_file, self.name)
        # create signal table and connect it
        signals = {}
        for item in dir(self):
            if item.startswith('on_'):
                signals[item] = getattr(self, item)
        self.signals = signals
        # self.widgetTree.signal_autoconnect(self.signals)
        self.widgetTree.connect_signals(self.signals)
        self.window = self.widgetTree.get_object(self.name)
        # for menu in self.menu_names:
        #    print "Loading", menu
        #    menu_wt = Gtk.glade.XML(globals.glade_file, menu)
        #    menu_wt.signal_autoconnect(signals)
        #    self.menus[menu] = menu_wt.get_widget(menu)

    def __getitem__(self, name):
        # print("__getitem__", name)
        return self.widgetTree.get_object(name)

    def getGladeWidget(self, name):
        self.widgetTree.add_objects_from_file("glade/kedpm.glade", [name])
        # widgetTree = pygtkcompat.glade.XML(globals.glade_file, name)
        # widgetTree.signal_autoconnect(self.signals)
        self.widgetTree.connect_signals(self.signals)
        return self.widgetTree.get_object(name)


class Dialog(Window):
    def __init__(self, transient_for="main"):
        super(Dialog, self).__init__()
        # Window.__init__(self)
        ### if transient_for:
            ### if transient_for == "main":
            ###    transient_for = globals.app.wnd_main.window
            ### self.set_transient_for(transient_for)

    def run(self):
        response = self.window.run()
        if response == Gtk.ResponseType.OK:
            self.process()
        self.destroyDialog()
        return response

    def destroyDialog(self):
        self.window.destroy()

    def process(self):
        pass
