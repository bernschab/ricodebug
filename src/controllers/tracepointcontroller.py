# ricodebug - A GDB frontend which focuses on visually supported
# debugging using data structure graphs and SystemC features.
#
# Copyright (C) 2011  The ricodebug project team at the
# Upper Austrian University Of Applied Sciences Hagenberg,
# Department Embedded Systems Design
#
# This file is part of ricodebug.
#
# ricodebug is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further information see <http://syscdbg.hagenberg.servus.at/>.

"""@package tracepointcontroller
    the tracepoint controller 
"""

from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4.QtGui import QDockWidget
from tracepointmodel import TracepointModel
from tracepointview import TracepointView

class TracepointController(QObject):
    def __init__(self, distributed_objects):
        """ init tracepoint controller and members.
        @param distributed_objects: passing distributed objects
        @note There are following signals: \n
            * insertDockWidgets() : necessary for plugin system\n
            * clicked(QModelIndex): if a row in tracepointView is clicked\n
            * cleanupModels(): clear Tracepoints\n
			* runClicked((): clear Tracepoint Data on every click on run button\n
        """
        
        QObject.__init__(self)
        self.distributed_objects = distributed_objects
        
        """@var self._model: (TracepointModel), this class provides the model for tracepointView"""
        self._model = TracepointModel(self.distributed_objects)
        """@var self.tracepointView: (TracepointView), this class presents data from _model"""
        self.tracepointView = TracepointView()        
        self.tracepointView.tracepointView.setModel(self._model)
        
        #register with session manager to save Tracepoints
        self.distributed_objects.signal_proxy.emitRegisterWithSessionManager(self, "Tracepoints")
        
        QObject.connect(self.distributed_objects.signal_proxy, SIGNAL('insertDockWidgets()'), self.insertDockWidgets)
        QObject.connect(self.tracepointView.tracepointView, SIGNAL('clicked(QModelIndex)'), self.updateWaveforms)  
        QObject.connect(self.distributed_objects.signal_proxy, SIGNAL('inferiorStoppedNormally(PyQt_PyObject)'), self.updateWaveforms)
        QObject.connect(self.distributed_objects.signal_proxy, SIGNAL('cleanupModels()'), self._model.clearTracepoints)
        QObject.connect(self.distributed_objects.signal_proxy, SIGNAL('runClicked()'), self._model.clearTracepointData)
        
    def updateWaveforms(self):
        '''update tracepoint waveforms'''
        index = self.tracepointView.getSelectedRow()
        if index != None:
            self._model.selectionMade(index)
        
    def insertDockWidgets(self):
        """needed for plugin system"""
        self.tracepointDock = QDockWidget("Tracepoints")
        self.tracepointDock.setObjectName("TracepointView")
        self.tracepointDock.setWidget(self.tracepointView)
        self.distributed_objects.signal_proxy.addDockWidget(Qt.BottomDockWidgetArea, self.tracepointDock, True)

    def toggleTracepoint(self, file_, line):
        """ toggles the breakpoint in file file_ with linenumber line
        @param file_: (string), fullname of file
        @param line: (int), linenumber where the breakpoint should be toggled
        """
        return self._model.toggleTracepoint(file_, line)

    def getTracepointsFromModel(self):
        """returns a list of tracepoints
        @return tracepoints: a list of tracepoints
        """
        return self._model.getTracepoints()

    def saveSession(self, xmlHandler):
        """Insert session info to xml file"""
        tpparent = xmlHandler.createNode("Tracepoints")
        for tp in self._model.getTracepoints():
            tpnode = xmlHandler.createNode("Tracepoint", tpparent, { "file": tp.file, "line": tp.line })
            for var in tp.wave:
                xmlHandler.createNode("TracepointVariable", tpnode, { "name": var.name })
           
    def loadSession(self, xmlHandler): 
        """load session info to xml file""" 
        tpparent = xmlHandler.getNode("Tracepoints")
        if tpparent != None:
            childnodes = tpparent.childNodes()
            for i in range(childnodes.size()):
                attr = xmlHandler.getAttributes(childnodes.at(i))
                self._model.insertTracepoint(attr["file"], attr["line"])
                
                vars = childnodes.at(i).childNodes()
                for j in range(vars.size()):
                    attr = xmlHandler.getAttributes(vars.at(j))
                    self._model.getTracepoints()[i].addVar(attr["name"])
    
    def model(self):
        return self._model