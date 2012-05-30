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

from PyQt4.QtCore import QObject, Qt
from PyQt4.QtGui import QDockWidget
from views.pyioview import PyIoView


class PyIoController(QObject):
    def __init__(self, distributedObjects):
        QObject.__init__(self)
        self.distributedObjects = distributedObjects

        self.pyioView = PyIoView(self.distributedObjects.debugController)

        self.distributedObjects.signalProxy.insertDockWidgets.connect(self.insertDockWidgets)

    def insertDockWidgets(self):
        self.pyioDock = QDockWidget("Python Console")
        self.pyioDock.setObjectName("PyIoView")
        self.pyioDock.setWidget(self.pyioView)
        self.distributedObjects.signalProxy.emitAddDockWidget(Qt.BottomDockWidgetArea, self.pyioDock, True)
