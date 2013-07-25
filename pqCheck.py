# -*- coding: utf-8 -*-

# These imports move Python 2.x almost to Python 3.
# They must precede anything except #comments, including even the docstring
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

__version__ = "1.02.0" # refer to PEP-0008
__author__  = "David Cortesi"
__copyright__ = "Copyright 2011, 2012, 2013 David Cortesi"
__maintainer__ = "?"
__email__ = "tallforasmurf@yahoo.com"
__status__ = "first-draft"
__license__ = '''
 License (GPL-3.0) :
    This file is part of PPQT.
    PPQT is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You can find a copy of the GNU General Public License in the file
    extras/COPYING.TXT included in the distribution of this program, or see:
    <http://www.gnu.org/licenses/>.
'''

'''
todo
'''

from PyQt4.QtCore import (Qt, QAbstractTableModel, QString, QVariant, SIGNAL)
from PyQt4.QtGui import (QHBoxLayout, QPushButton, QSortFilterProxyModel,
                         QTableView, QVBoxLayout, QWidget, QTextCursor,
                         QHeaderView)

import pqMsgs

import unicodedata
from lxml import etree
from collections import defaultdict
from itertools import cycle


# Implement a concrete table model by subclassing Abstract Table Model.
# The data served is derived from the character census prepared as
# metadata in the editor.
class myTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(myTableModel, self).__init__(parent)
        # The header texts for the columns
        self.headerDict = { 0:"Tag", 1:"Language",
                            2:"Count", 3:"Content" }
        # the text alignments for the columns
        self.alignDict = { 0:Qt.AlignHCenter, 1: Qt.AlignHCenter,
                           2:Qt.AlignLeft, 3:Qt.AlignLeft }
        # The values for tool/status tips for data and headers
        self.tipDict = { 0: "HTML Tag", 1: "Language code",
                         2: "Number of occurences", 3: "Content of tag" }

    def columnCount(self,index):
        if index.isValid() : return 0 # we don't have a tree here
        return len(self.headerDict)

    def flags(self,index):
        return Qt.ItemIsEnabled

    def rowCount(self,index):
        if index.isValid() : return 0 # we don't have a tree here
        return len(IMC.xml_tags_lang)

    def headerData(self, col, axis, role):
        if (axis == Qt.Horizontal) and (col >= 0):
            if role == Qt.DisplayRole : # wants actual text
                return QString(self.headerDict[col])
            elif (role == Qt.ToolTipRole) or (role == Qt.StatusTipRole) :
                return QString(self.tipDict[col])
        return QVariant() # we don't do that

    def data(self, index, role ):
        if role == Qt.DisplayRole : # wants actual data
            row = index.row()
            if 0 == index.column():
                return IMC.xml_tags_lang[row][0]
            elif 1 == index.column():
                return IMC.xml_tags_lang[row][1]
            elif 2 == index.column():
                return len(IMC.xml_tags_lang[row][3])
            elif 3 == index.column():
                return IMC.xml_tags_lang[row][2]
        elif (role == Qt.TextAlignmentRole) :
            return self.alignDict[index.column()]
        elif (role == Qt.ToolTipRole) or (role == Qt.StatusTipRole) :
            return QString(self.tipDict[index.column()])
        # don't support other roles
        return QVariant()

class langPanel(QWidget):
    def __init__(self, parent=None):
        super(langPanel, self).__init__(parent)
        # Do the layout: refresh button with a table below.
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        topLayout = QHBoxLayout()
        mainLayout.addLayout(topLayout,0)
        self.refreshButton = QPushButton("Refresh")
        self.last_row = None
        self.row_cycle_it = None
        topLayout.addWidget(self.refreshButton,0)
        topLayout.addStretch(1)
        self.view = QTableView()
        self.view.setCornerButtonEnabled(False)
        self.view.setWordWrap(True)
        self.view.setAlternatingRowColors(True)
        mainLayout.addWidget(self.view,1)

        # Set up the table model/view. Interpose a sort filter proxy
        # between the view and the model.
        self.model = myTableModel()
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setDynamicSortFilter(True)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.view.setModel(self.proxy)

        # Hook up the refresh button clicked signal to refresh below
        self.connect(self.refreshButton, SIGNAL("clicked()"),self.refresh)

        # Connect doubleclicked from our table view to self.findThis
        self.connect(self.view, SIGNAL("doubleClicked(QModelIndex)"), self.findThis)


    # This slot receives a double-click on the table. Figure out which
    # character it is and get the Find panel set up to search for it.
    def findThis(self,qmi):
        rep = None

        # Get row in IMC.xml_tags_lang
        this_row = self.proxy.mapToSource(qmi).row()

        # Cycle through all the source lines
        if not self.last_row or self.last_row != this_row:
            self.row_cycle_it = cycle(IMC.xml_tags_lang[this_row][3])

        # Center edit view on line containing the tag (or more
        # exactly, the closing > of the opening tag), and select the
        # line.
        doc = IMC.editWidget.document()
        tc = QTextCursor(doc)
        textBlock = doc.findBlockByNumber(self.row_cycle_it.next() - 1)
        tc.setPosition(textBlock.position(), QTextCursor.MoveAnchor)
        tc.setPosition(textBlock.position()+textBlock.length(), QTextCursor.KeepAnchor)
        IMC.editWidget.setTextCursor(tc)

        # Remember this row in case we double click again, so we can
        # cycle through the occurences.
        self.last_row = this_row

    # This slot receives the main window's docWillChange signal.
    def docWillChange(self):
        #self.view.setSortingEnabled(True)
        IMC.xml_tags_lang = []
        self.last_row = None
        self.row_cycle_it = None
        self.model.beginResetModel()

    # Subroutine to reset the visual appearance of the table view,
    # invoked on table reset because on instantiation we have no table.
    # Bump up the width of column 0 because when it sets it to its contents
    # there isn't room for the header plus the sort triangle
    def setUpTableView(self):
        self.view.sortByColumn(3,Qt.AscendingOrder)
        self.view.resizeColumnsToContents()
        self.view.resizeRowsToContents()
        self.view.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.view.setSortingEnabled(True)

    # This slot receives the main window's docHasChanged signal.
    # Let the table view populate with all-new metadata (or empty
    # data if the command was File>New).
    def docHasChanged(self):
        self.model.endResetModel()
        self.setUpTableView()

    # This slot receives the click of the refresh button. Tell the
    # model we are resetting everything so the view will suck up new
    # data. Then call our editor to rebuild the metadata.
    def refresh(self):
        #self.view.setSortingEnabled(False)
        self.model.beginResetModel()
        self.find_tags()
        self.model.endResetModel()
        self.setUpTableView()


    def find_tags(self):

        IMC.xml_tags_lang = []

        for xparser in [ ('XML', etree.XMLParser(load_dtd=True)),
                         ('HTML', etree.HTMLParser()) ]:
            try:
                self.tree = etree.fromstring(unicode(IMC.editWidget.toPlainText()), xparser[1]).getroottree()
            except:
                continue
            break
        else:
            # Could not parse the file
            return

        # Add a space in </br> to space because normalize-space doesn't do it
        find = etree.XPath("//br")
        for element in find(self.tree):
            element.tail = ' ' + (element.tail or '')

        # XML namespace jugling
        XMLNS = "{http://www.w3.org/XML/1998/namespace}"
        attr = self.tree.getroot().attrib
        xmlns = attr.get('xmlns', None)
        if xmlns:
            xmlns = '{' + xmlns + '}'
        else:
            xmlns = ""
        document_lang = attr.get('lang', None)
        document_xmllang = attr.get(XMLNS+'lang', None)
        default_lang = (document_lang or document_xmllang)

        xml_tags_lang = []

        for element in self.tree.iter(tag=etree.Element):

            # Remove the namespace from the tags
            # (eg. {http://www.w3.org/1999/xhtml})
            tag = element.tag.replace(xmlns, "")

            if tag == 'html':
                continue

            if tag in [ 'i', 'cite', 'em', 'span' ]:

                # Find the language attribute, lang or xml:lang.
                lang = element.attrib.get('lang',
                                          element.attrib.get(XMLNS+'lang', None))

                if not lang:
                    # No language found
                    if tag == 'span':
                        # span with no lang tag, ignore.
                        continue

                    # Default to main language
                    lang = default_lang

                # Store as (tag, lang, content, sourceline)
                xml_tags_lang.append(( QString(tag), QString(lang),
                                       QString(etree.XPath("normalize-space()")(element)),
                                       element.sourceline))

        # Collapse identical entries (the first 3 elements), and keep
        # the line numbers where the tag is seen (4th element, in a
        # list).
        # The content of IMC.xml_tags_lang will be:
        #   [ (tag, lang, content, [sourceline, sourceline, ...] ), ...]
        d = defaultdict(list)
        for x in xml_tags_lang:
            d[(x[0:3])].append(x[3])

        IMC.xml_tags_lang = [ x + (y,) for x, y in d.iteritems() ]




if __name__ == "__main__":
    import sys
    from PyQt4.QtCore import (Qt,QFile,QIODevice,QTextStream)
    from PyQt4.QtGui import (QApplication,QFileDialog,QPlainTextEdit)
    import pqIMC
    import pqMsgs
    import pqLists

    IMC = pqIMC.tricorder() # create inter-module communicator
    app = QApplication(sys.argv) # create an app
    pqMsgs.IMC = IMC

    W = langPanel() # create the widget with the table view and model
    W.show()

    if len(sys.argv) < 2:
        utname = QFileDialog.getOpenFileName(W, "UNIT TEST DATA FOR LANGS", ".")
        utfile = QFile(utname)
    else:
        utfile = QFile(sys.argv[1])

    if not utfile.open(QIODevice.ReadOnly):
        raise IOError, unicode(utfile.errorString())

    W.docWillChange()

    utstream = QTextStream(utfile)
    utstream.setCodec("UTF-8")
    utqs = utstream.readAll()

    IMC.editWidget = QPlainTextEdit()
    IMC.editWidget.setPlainText(utqs)

    W.find_tags()

    W.docHasChanged()
    app.exec_()
