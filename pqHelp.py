# These imports move Python 2.x almost to Python 3.
# They must precede anything except #comments, including even the docstring
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

'''
The help consists of a QTextEdit in read-only mode, whose document
is a huge triple-quote text string. The contents of that string are
an HTML document edited elsewhere (BBEdit), saved as pqHelp.html
in the source folder, but simply pasted in here.
'''

__version__ = "0.1.0" # refer to PEP-0008
__author__  = "David Cortesi"
__copyright__ = "Copyright 2011, David Cortesi"
__maintainer__ = "?"
__email__ = "nobody@pgdp.net"
__status__ = "first-draft"
__license__ = '''
Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)
http://creativecommons.org/licenses/by-nc-sa/3.0/
'''
from PyQt4.QtCore import ( Qt, QString )
from PyQt4.QtGui import (QTextEdit,QTextCursor)
import pqMsgs

class helpDisplay(QTextEdit):
    def __init__(self, parent=None ):
        super(helpDisplay, self).__init__(parent)
        self.setHtml(QString(TheHelpText))
        self.setReadOnly(True)
    
    # Re-implement the parent's keyPressEvent in order to provide a simple
    # find function only.
    def keyPressEvent(self, event):
	kkey = int(event.modifiers())+int(event.key())
	if kkey == IMC.ctl_F: # ctl/cmd f
	    event.accept()
	    self.doFind()
	else: # not ctl/cmd f so,
	    event.ignore()
        # ignored or accepted, pass the event along.
        super(helpDisplay, self).keyPressEvent(event)

    # Do a simple find. getFindMsg returns (ok,find-text). This is a VERY
    # simple find from the present cursor position downward, case-insensitive.
    # If we get no hit we try once more from the top, thus in effect wrapping.    
    def doFind(self):
	(ok, findText) = pqMsgs.getFindMsg(self)
	if ok and (not findText.isNull()) :
	    if not self.find(findText): # no hits going down
		self.moveCursor(QTextCursor.Start) # go to top
		if not self.find(findText): # still no hit
		    pqMsgs.beep()

TheHelpText = '''<html>
<head>
</head>
<body>
<h1>PPQT Information</h1>
<p>PPQT is a tool for post-processing books for Project Gutenberg Distributed Proofreaders. PPQT is based on Qt by Nokia (qt.nokia.com). It is coded in Python using PQt4 (riverbankcomputing.co.uk). It is packaged for release using pyinstaller (pyinstaller.org).</p>
<h3>Licenses</h3>
<p>Qt is licensed for noncommercial use under the LGPL.
PyQt4 is licensed for noncommercial use under the GPL v2 and the GPL v3.
The source code of PPQT is released under the Creative Commons
Attribution-NonCommercial-ShareAlike license.</p>
<h3>Acknowledgements</h3>
<p>First a deep bow of respect to Steve Shulz (Thundergnat) who created and maintained Guiguts, the program from which PPQT takes inspiration and lots of ideas. Second, a genuflection  to Mark Summerfield for the book <i>Rapid GUI Developement with PyQt</i>.</p>
<h3>Mac Users Note</h3><p> Throughout this Help, when you read <b>ctl-</b>
you think <b>cmd-</b>. And when you read <b>alt-</b>, you think <b>opt-</b>.
Qt is quite consistent in these mappings. However, when you see <b>control-</b>, that really means, the Control key.</p>
<p>Try it now: key ctl-f for a simple Find dialog for searching in this help text.</p>
<h2>Files and Folders</h2>
<p>PPQT edits one book text at a time, for example <tt>afinebook.txt</tt>.
<h3>File Encodings and Suffixes</h3>
<p>PPQT is entirely Unicode internally. The text file is converted to Unicode
on input, and back to some byte code on output, based on the file suffix. Rename a new file as needed to get these encodings:</p>
<table border='1'>
<tr><td><tt>.txt</tt></td><td>Latin-1 or 7-bit Ascii (PPQT cannot distinguish between these)</td></tr>
<tr><td><tt>.utf</tt></td><td>UTF-8 encoding of Unicode, preferred for text with non-latin characters</td></tr>
<tr><td><tt>.win</tt></td><td>Windows code page 1252, the US and European Windows alphabet.</td></tr>
<tr><td><tt>.mac</tt></td><td>Mac Roman, the Apple alphabet.</td></tr>
<tr><td><tt>.isr</tt></td><td>Windows code page 1255, Windows Hebrew</td></tr> <tr><td><tt>.cyr</tt></td><td>Windows code page 1251, Windows Cyrillic alphabet.</td></tr>
<tr><td><tt>.kir</tt></td><td>KOI8-R, Cyrillic-Russian.</td></tr>
<tr><td><tt>.kiu</tt></td><td>KOI8-U, Cyrillic-Ukranian.</td></tr>
</table>
<p>When saving, prefer <tt>.utf</tt> if there is any chance the text contains non-Latin-1 characters; prefer <tt>.txt</tt> when you are sure it is pure Latin-1 or ASCII. However, PPQT will save to any of the above encodings based on the file suffix of the output file.</p>
<h3>Metadata</h3>
When opening  <tt>afinebook.txt</tt>, PPQT looks for a file named  <tt>afinebook.txt.meta</tt> in the same location (i.e. the full book name
plus <tt>.meta</tt>). If the meta file
is not found, PPQT assumes this is the first time it has opened this book.
It scans the text gathering information including the location of page separator lines, and counting words and characters. These metadata will be stored in the <tt>.meta</tt> file when the file is saved. When the <tt>.meta</tt> file does
exist, PPQT loads the metadata items from it.</p>
<p>Feel free to examine or edit the metadata file, but be aware that it is written in UTF-8 format. If strange characters appear, your editor app did not use the utf-encoding to load it. Do not save the metadata file unless you are sure you are loading and saving it in UTF-8 format.</p>
<h3>Page Images</h3>
<p>PPQT expects to find a folder named <tt>pngs</tt> in the same location as
the text file, containing the scan images for the book. These are displayed in 
the Pngs panel.</p>
<h2>The Main Window</h2>
<p>When launched, PPQT displays a single window divided in two by a vertical bar. The left side is the Edit Panel where you edit the document. The right side
is a tabbed set of panels for different functions. All these panels are described below.</p>
<p>You can adjust the size and location of the main window and you can drag
the vertical "splitter" left and right. These adjustments are remembered from
session to session.</p>
<h2>The Edit Panel</h2>
<p>The left-side panel is a typical modern plain text line-editor.
It uses a monospaced font, defaulting to Deja Vu Mono (dejavu-fonts.org)
or to Courier New, either of which is legible and has a full range
of Unicode characters. Select View>Font... to select another font, which will be remembered from session to session. (It would be a bad idea to use anything but a monospaced font.)</p>
<p>Below the edit panel is a status area where activity messages appear
from time to time. Bottom center is a line-number field displaying the
line number of the edit cursor. Type a new number in
that field and press Return to jump to a different line. Further to the
right is a progress bar that shows the status of some long-running operations.</p>
<h3>Selecting Text</h3>
<p>Select text
by dragging, or by click then shift-click, or by doubleclick (word) or 
tripleclick (line). Extend a selection by holding the shift key and
using an arrow key. Move text by dragging the selection,
or copy text by alt-dragging. PPQT does not support rectangular selections or discontinuous selections.</p>
<h3>Edit Keys</h3>
<ul>
<li>up/dn/left/right: move cursor</li>
<li>Home, also ctl-up: Top of text</li>
<li>End, also ctl-dn: Bottom of text</li>
<li>PgUp/PgDn: move cursor one editor screen up/dn</li>
<li>ctl-left and ctl-right: beginning and end of line</li>
<li>alt-left and alt-right: word-left, word-right</li>
<li>Add shift key to any of the above: extends selection</li>
<li>ctl-c/ctl-x/ctl-v: copy/cut/paste</li>
<li>ctl-z: undo</li>
<li>ctl-y, also shift-ctl-z: redo</li>
<li>ctl-hyphen: display text 1pt smaller</li>
<li>ctl-+: display text 1pt larger</li>
<li>ctl-f: display Find panel and put focus there</li>
<li>shift-ctl-f: copy selection to Find panel</li>
<li>ctl-g: repeat the last search forward (same as Find Next)</li>
<li>shift-ctl-g: repeat last search backward (same as Find Prior)</li>
<li>ctl-=: replace selection (same as Find panel replace #1)</li>
<li>ctl-t: replace selection and repeat find forward</li>
<li>shift-ctl-t: replace selection and repeat find backward</li>
<li>ctl-u, ctl-l, ctl-i: change selection to uppercase, lowercase, titlecase (Unicode compliant)</li>
<li>ctl-1 through ctl-9: jump to bookmark 1-9</li>
<li>shift-ctl-1 through shift-ctl-9: set bookmark 1-9 to cursor (bookmarks
are saved in the metadata file)</li>
</ul>
<h3>Scanno Highlighting</h3>
<p>Use File > Scannos to load a file of scannos: a text file with one word per line (e.g <tt>en-common</tt> from guiguts). May be a UTF file. The same file will be re-loaded each time PPQT is restarted, if it is found.</p>
<p>Use the View > Scannos menu to turn on scanno highlighting, putting
a plum-colored background on any word that appears in the scannos file. (Be patient, this may take several seconds to appear in a large book.)</p>
<h3>Spellcheck</h3>
<p>PPQT looks for a file <tt>good_words.</tt> (<tt>txt</tt> or <tt>utf</tt>) when it opens the text for the first time, and loads its contents. It looks for a file <tt>bad_words.</tt> (<tt>txt</tt> or <tt>utf</tt>)  also. The lists of "good" and "bad" words are saved in the metadata file thereafter. More "good" words can be added from the Words panel.</p>
<p>When building or refreshing its metadata, PPQT checks all words for spelling. A "bad" word is assumed to be misspelt; a "good" word is assumed to be correct. Any word not in those lists is presented to the spell-checker and noted as correct or misspelt based on the current dictionary.</p>
<p>Select View&nbsp;>&nbsp;Spelling to turn on red-underlining of misspelt words (may take some seconds in a large book). Use View&nbsp;>&nbsp;Dictionary to select a dictionary for the main language of the book. Use the Refresh button of the Words panel to spellcheck with the new dictionary. Dictionaries for several languages are included; more can be added by a procedure documented elsewhere.</p>
<p>You can mark any word, phrase or section for
spell-check with an alternate dictionary with the nonstandard tag <b><tt>&lt;sd</tt></b>&nbsp;<i>dictag</i><b>&gt;</b>...<b><tt>&lt;/sd></tt></b>, for example <tt>He whispered &lt;sd fr_FR>&lt;i>Je t'aime&lt;/i>&lt;/sd></tt>. During spellcheck, switching to and from the alternate dictionary may introduce a noticeable pause.</tt>
<h2>Pngs Panel</h2>
<p>Click the Pngs tab. This panel displays the scan image from the <tt>pngs</tt> folder that corresponds to the present edit cursor position. When the focus is in the Pngs panel (click in it) ctl-hyphen zooms out and ctl-plus zooms in. The current zoom setting is remembered from session to session.</p>
<p>You can use the PgUp and PgDn keys in the Pngs panel to see preceding and following scan images. However as soon as you move the text edit cursor,
the Pngs panel snaps back to the image corresponding to the cursor.</p>
<h2>Notes Panel</h2>
<p>Click the Notes tab. This panel is a simple plain-text editor to hold notes on the book in progress. Whatever contents you type here are saved
in the <tt>.meta</tt> file and reloaded with the book.</p>
<p>When the focus is in the Notes panel, the alt-ctl-L key causes the
current line number of the Edit panel cursor position to be entered, in curly braces: <tt>{1475}</tt>. (Note: under Ubuntu, alt-ctl-L may be the keyboard shortcut for Lock Screen. Use Ubuntu's Preferences &gt; Keyboard Shortcuts to change this to, e.g., shift-alt-ctl-L.)</p><p>The alt-ctl-P key causes the current book page
number to be entered in square brackets: <tt>[214]</tt>. Use these keys
to relate your notes to locations in the book, for example <tt>oe lig near {1475}; big table on [214]</tt>.
</p><p>
Place the cursor in or to the right of a {nnn} line number in the notes and key ctl-L. The Edit panel cursor jumps to that line. Place the cursor in or to the right of a [ppp] page number and key ctl-p. The Edit panel cursor jumps to the top of that page's text.</p>
<p>Key ctl-f for a simple Find dialog for searching in the notes.
If text is selected, it is pre-loaded in the find-text field. The search
starts at the cursor and wraps around at the end of the notes.</p>
<h2>Find Panel</h2>
<p>The Find panel has controls for search and replace, including saved searches.
Search/replace is done within top and bottom boundaries which are initially
the beginning and end of the document.
Upon doing any search, keyboard focus returns to the Edit panel.</p>
<h3>Find Controls</h3>
<p>The top row of five checkboxes affect the search.</p>
<table border='1'>
<tr><td style='width:6em;'>Respect Case</td><td>When checked, search is case-sensitive.</td></tr>
<tr><td>Whole Word</td><td>When checked, normal searches only match whole words.
Does not apply to regex (use <tt>\\b</tt> in the expression)</td></tr>
<tr><td>In Sel'n</td><td>When checked, search and replace occur in bounds
set when you click the First or Last button.</td></tr>
<tr><td>Regex</td><td>When checked, the Find string is treated as a regular expression.</td></tr>
<tr><td>Greedy</td><td>When checked, a regular expression matches all it can;
otherwise as little as it can.</td></tr>
</table>
<p>The Find text field is below the checkboxes. Here enter the text pattern
to look for. At the left is a popup menu
containing the last 10 find values you explicitly typed in the field.
(These are remembered from session to session.)
The Find text field turns pink when Regex is checked and the syntax is not valid.</p>
<p>Below the text field are four buttons that perform searches:</p>
<table border='1'>
<tr><td style='width:4em;'>Next</td><td>Search for the Find text beginning at the edit cursor and going toward the bottom boundary. Pressing Return in the Find text field is the same as clicking Next.</td></tr>
<tr><td>Prior</td><td>Search for the Find text beginning at the edit cursor and going back toward the top boundary.</td></tr>
<tr><td>First</td><td>If In Sel'n is checked, set the top and bottom of the
current selection as the search boundaries; otherwise set to the whole document.
Search for the Find text beginning at the top boundary and going forward.</td></tr>
<tr><td>Last</td><td>If In Sel'n is checked, set the top and bottom of the
current selection as the search boundaries; otherwise set to the whole document.
Search for the Find text beginning at the bottom boundary and going backward.</td></tr>
</table>
<h3>Replace Controls</h3>
<p>There are three Replace fields. They are identical in use. Each is a text
field to enter the replacement text. On the left is a popup menu with the
last 10 replacement strings you used out of that field.
(These are remembered from session to session.)
On the right is a Repl button that causes the current edit selection to be
replaced with the field contents.</p>
<p>Further right are three checkboxes. 
When &amp;Next is checked, use of any Repl button is followed by
the effect of the Next button. When &amp;Prior is checked, use
of any Repl button is followed by the effect of the Prior button.</p>
<p>When the focus is in the Edit panel, ctl-= has the effect of clicking
Repl on the first replace field; ctl-t is like clicking Repl and then Next; 
and shift-ctl-t is like clicking Repl and then Prior.</p>
<p>When ALL! is checked, clicking any Repl button
causes all instances of the Find text within the search boundaries
to be looked up and replaced.
Before the replacement is done, a message is shown: "Replace <i>nn</i>
occurrences of <i>find-text</i> with <i>repl-text</i>?" and you
have the option of cancelling the operation. The replace-all 
operation is a single undo/redo step.</p>
<h3>User-defined Buttons</h3>
<p>Below the Replace controls is an array of 24 pushbuttons. 
Use these to store find/replace operations for re-use.
To store an operation, right-click (Mac users: <b>control</b>-click)
a button. A message pops up asking you to give a short label for the button.
When you do so and click OK, that label is assigned to the button,
and the state of all the find/replace controls&mdash;all checkboxes
and entry fields&mdash;is stored in that button. Whenever you want to
repeat that search, click the button. All the find/replace
controls are returned to the stored settings.
The button contents are remembered from session to session.</p>
<p>To clear the contents of a button, right-click it, clear the label field to empty, and click OK.</p>
<p>To save the button settings to a file select File>Save Find Buttons. Provide the name and location for the saved file, which will be saved with UTF-8 encoding (so a suffix of .utf is a good idea). In the saved file each non-empty button is represented on a single line.</p>
<p>To load button settings from a file, select File>Load Find Buttons.
Any button definitions in the file are assigned to the buttons.
The intent of saving and loading buttons is to be able to save
and re-use complex search operations, and exchange them with other
users. The file syntax is documented elsewhere.</p>
<p></p>
<h3>Regex Syntax</h3>
<p>The Qt regex support is similar to but has fewer features than the Perl regexes used in guiguts. The following forms are used to match text.</p>
<table border='1'>
<tr><td style='width:3em;'>non-special characters</td><td>match themselves</td></tr>
<tr><td><b>\\</b><i>x</i></td><td>Escape for special characters: except as below, matches <i>x</i>. Use <b>\\\\</b> to match a slash.</td></tr>
<tr><td><b>\\n</b> </td><td>Matches between lines. <tt>\\n\\n</tt> matches an empty line</td></tr>
<tr><td><b>\\x</b><i>xxxx</i></td><td>matches Unicode character valued <i>xxxx</i>       </td></tr>
<tr><td><b>.</b> (dot)</td><td>Matches any one character <i>including newline</i>  </td></tr>
<tr><td><b>\\d</b> </td><td>  matches a decimal digit</td></tr>
<tr><td><b>\\D</b> </td><td> matches a non-digit  </td></tr>
<tr><td><b>\\s</b></td><td> matches a whitespace character <i>including newline</i></td></tr>
<tr><td><b>\\S</b></td><td> matches a non-whitespace character </td></tr>
<tr><td><b>\\w</b></td><td> matches a word character (any Unicode letter, number, or Mark) </td></tr>
<tr><td><b>\\W</b></td><td>matches a non-word character</td></tr>
<tr><td><b>\\</b><i>n</i> </td><td> matches the <i>n</i>-th captured text (same as perl/guiguts <b>$</b><i>n</i>)</td></tr>
<tr><td><b>[</b><i>chars</i><b>]</b></td><td> matches any one of the <i>chars</i>; may use ranges e.g. <tt>[A-Z1-9]</tt>    </td></tr>
<tr><td><b>[^</b><i>chars</i><b>]</td><td>  matches any character except <i>chars</i></td></tr>
<tr><td> <b>\\b</b></td><td>matches the zero-width boundary between a
word and non-word character. <tt>\\bon\\b</tt> matches only the word "on".</td></tr>
<tr><td><b>\\B</b></td><td> matches what <b>\\b</b> doesn't. <tt>\\Bon\\B</tt> will not match the word "on" but will match inside "tone". </td></tr>
</table><p>Any of the above expressions
can be or'd with stiles: <tt>alpha|beta</tt> means alpha or beta.
Any of those expressions may be put in parentheses to capture
the matching text for use in replacements. Any expression <i>E</i> can be quantified with these suffixes:</p>
<table border='1'>
<tr><td style='width:5em;'>  <i>E</i><b>?</b></td><td>  zero or one of <i>E</i> </td></tr>
<tr><td><i>E</i><b>+</b></td><td> one or more of <i>E</i>  </td></tr>
<tr><td> <i>E</i><b>*</b>   </td><td> zero or more of <i>E</i> </td></tr>
<tr><td> <i>E</i><b>{</b><i>n</i><b>,</b><i>m</i><b>}</b>  </td><td>from <i>n</i> to <i>m</i> of <i>E</i>, and <i>n</i> or <i>m</i> can be omitted:
<i>E</i><b>{</b><i>n</i><b>,}</b> at least <i>n</i> of <i>E</i>; <i>E</i><b>{,</b><i>m</i><b>}</b> at most <i>m</i> of <i>E</i></td></tr>
</table>
<p>Non-capturing parentheses force a match but do not capture the matching
text: <tt>(?:The color is)\s(red|green|blue)</tt> can only match a string
that begins "The color is" but the first capture, <b>\\1</b>, is what 
matched <tt>(red|green|blue)</tt>.</p>
<p>Lookahead tests with <b>(?=</b><i>E</i><b>)</b> and <b>(?!</b><i>E</i><b>)</b> are supported: <tt>Fred(?=\\n)</tt> 
matches "Fred" only at the end of a line; <tt>Fred(?!\\n)</tt> only when
not at end of line. However the lookbehind tests of Perl regexes are not supported.</p>
<p>Note: owing to some tricks PPQT plays with the Qt regex support, 
the caret and dollar codes, which usually match at beginning and end
of a line, only match at top and bottom search boundary respectively.
Use \\n to match at beginning and end of line.</p>
<p>Replacement text for a regex match may contain <b>\\</b><i>n</i> to refer
to the <i>n</i>th captured (parenthesized) text. None of the special
replacements supported by guiguts (such as <tt>\\U...\\E</tt> to uppercase
the text) are available.</p>
<h2>The Characters Panel</h2>
<p>Click the Char tab to show the Characters panel.
This panel displays a table of all characters seen in the document,
in four columns:</p>
<ul>
<li>Glyph: the character symbol</li>
<li>Value: the hex value of the unicode character</li>
<li>Count: the number of times the character appears</li>
<li>Unicode category</li>
</ul>
<p>Click on the heading of any column to sort on that column.
After you have edited the document, the table is out of date.
Click the Refresh button
to rebuild all metadata and make the counts accurate.</p>
<p>In the upper right is a popup menu with three choices:<p>
<ul>
<li>All: show all characters</li>
<li> &#172; 7-bit: show only characters not in 7-bit ASCII</li>
<li> &#172; Latin-1: show only characters not in the Latin-1 set</li>
</ul>
<p>Doubleclick a row to copy that character into the Find text and
display the Find panel.</p>
<h2>The Words Panel</h2>
<p>Click the Word tab to see the Words panel.
This is a table of all words in the document, in three columns:</p>
<ul>
<li>Word: text of the word</li>
<li>Count: the number of times the word appears</li>
<li>Features: a string of letters showing information about the word,
for example <tt>Aa---X</tt>, meaning from left to right:
<ul>
<li>A if the word contains an uppercase letter, else hyphen</li>
<li>a if the word contains a lowercase letter, else hyphen</li>
<li>9 if the word contains a digit, else hyphen</li>
<li>h if the word contains a hyphen, else hyphen</li>
<li>p if the word contains an apostrophe, else hyphen</li>
<li>X if the word is in bad_words or fails spellcheck, else hyphen</li>
</ul>
</ul>
Click on any column to sort on that column. Set the Respect Case
checkbox to decide if the Word column sort is case-sensitive.
After the text is edited the table is out of date.
Click Refresh to rebuild all metadata
and make the table current. Use the popup menu in the upper right
to filter the table to these categories:</p>
<ul>
<li>ALL: show all words</li>
<li>UPPERCASE: show only all-cap words</li>
<li>lowercase: show only lowercase words</li>
<li>mIxEdcase: show words having both upper and lowercase letters</li>
<li>Numbers: show only all-numeric words</li>
<li>Alnumeric: show words having both letters and digits</li>
<li>Hyphenated: show words containing a hyphen</li>
<li>Apostrophes: show words containing an apostrophe</li>
<li>Misspelt: show words that fail spellcheck</li>
</ul>
<p>Doubleclick a word to load that word in the Find text and display
the Find panel.</p>
<p>You can select one or more words by clicking, dragging, shift-clicking or
ctl-clicking in the first column.
Right-click (Mac users: <b>control</b>-click) on a word in the first
column to open a context menu with these options:</p>
<ul>
<li>Add to goodwords: Add all selected words to the good-words list
and show them as correctly spelled.</li>
<li>Similar words: Filter the word list to show only words that match the
clicked word when letter case, hyphens, and apostrophes are ignored.</li>
<li>First harmonic: Filter the word list to show only words that are
within one edit of difference from the clicked word.</li>
<li>Second harmonic: Show only words that are within one or two edits
of the clicked word.</li>
</ul>
<p>Use Similar words to find inconsistent use of hyphens. Use
First and Second Harmonic to find likely misspellings of a word.
After viewing Similar or First or Second Harmonic, select
All from the popup menu above the table to see all words again.</p>
<h2>The Pages Panel</h2>
<p>Click the Page tab to display the Pages panel. 
The lower part displays a table showing the page separator information extracted from the original file. The information is retained in the metadata even after the page separator lines are deleted. Use this table is to set the correct values for the folios, the visible page numbers that are displayed in an HTML etext. The columns are:</p>
<ul>
<li>Scan#: the number of the scanned image, usually three digits; this
is the filename of the .png image in the pngs folder.</li>
<li>Format: the display format for a visible folio: arabic or roman numerals.</li>
<li>Action: how to compute and display the folio for this page</li>
<li>Folio: the folio (book page number) for this scanned page</li>
<li>Proofers: the userids who proofed this page at its various stages</li>
</ul>
<p>The table is always in scan image order. Double-click a cell in the Scan# column to make the
editor jump to the top of that page's text.</p>
<p>
Double-click a cell in the Action column to set the folio action to one of:</p>
<ul>
<li>Add 1: this page's folio is +1 over the preceding page's</li>
<li>Set @: set this page's folio to the number in column 4</li>
<li>Skip folio: no visible page number for this image</li>
</ul>
<p>Double-click a number in the folio column to set a specific
numeric value to go with the Set @ action.
Double-click a cell in the Format column to set the format to
one of Arabic, roman (lowercase) or ROMAN (uppercase).
After making one or more of these changes, click the Update
button to update the table to reflect the changes. Using these
controls you can get the folios of the file to exactly match
the folios in the original book.</p>
<h3>Inserting Folio Text</h3>
<p>At the top of the panel is a text-entry field and an Insert button.
Use these to insert a text pattern at the start of every page (except
pages for which the Action is Skip folio). The text pattern may contain <tt>\\n</tt> to insert a line-break, and it may contain <tt>%f</tt> to insert the
folio number for that page. Insert
any unique pattern that you can extend later with regular expression
replacements, for example <tt>[=%f=]</tt>. The full-on pattern for
HTML folios in the side margin is:</p><blockquote>
<tt>\n&lt;span class='pgnum'>&lt;a id='Page_%f' name='Page_%f'>&lt;/a>[Pg&amp;nbsp;%f]&lt;/span>\n</tt>
</blockquote>
<p>Inserting folio text is a single undo/redo operation.</p>
<p>TBS: some way to open a proofer's profile page at pgdp.net 
by clicking in the proofer column.</p>
<h2>The Reflow Panel</h2>
<p>Click the Flow tab to display the Reflow panel.
This panel has controls related to reflowing paragraphs and marked-up
sections in the ASCII etext, and for HTML conversion.
</p>
<h3>Markup Codes</h3>
<p>Use the following codes to mark sections for special treatment in the
reflow of ASCII etext and during HTML conversion. During reflow, normal paragraphs are flowed in a 75-character line. Other markup sections are
supported as follows:</p>
<table border='1'>
<tr><th>Markup</th><th>Usage</th></tr>
<tr><td><b>/Q..Q/</b></td><td>Block Quote: paragraphs are reflowed
within left and right indents as set in the top row of controls.</td></tr>
<tr><td><b>/U..U/</b></td><td>Unsigned list: text is reflowed by paragraphs
with the first line of each paragraph indented 2 and others indented 4.</td></tr>
<tr><td><b>/P..P/</b></td><td>Poetry:single lines are indented as given
in the second row of controls.</td></tr>
<tr><td><b>/R..R/</b></td><td>Each line is aligned right, for the
heading of a letter, a signature or the source of a quote.
<tr><td><b>/*..*/</b></td><td>No-flow: the entire section may be indented
by an amount specified in the third control, otherwise no change.</td></tr>
<tr><td><b>/C..C/</b></td><td>Centering: single lines are indented so
as to center on the 75-char line, with at least a 2-space indent.</td></tr>
<tr><td><b>/T..T/</b><br /><b>/TM../T</b></td>
<td>Table formatting, see discussion below</td>
<tr><td><b>/X..X/</b></td><td>Left entirely alone.</td></tr>
</table>
<h3>ASCII Reflow</h3>
<p>Select a portion of text and click Reflow Now: Selection, or 
click Document to reflow the whole document. Reflow is a single
undo/redo operation. Before doing it you can
set the switches on the left center to skip over special sections. For example set the skip-Tables checkbox and /T markup is treated the same as /X and  left alone. During reflow, the markup codes are retained and you can
apply reflow multiple times without harm.</p>
<p>For Centered text, setting the "longest line+2" button adjusts
a centered section as far to the left as possible leaving a 2-space indent.
If the button is not set, each line is centered on 75 spaces, which
may produce a deep left margin.</p>
<p>Normally you reflow after removing &lt;i>, &lt;b>, and &lt;sc> markup.
However you can preview reflow while these are still in place by setting
the controls on the right center. For example if &lt;sc> markup will
be converted to uppercase, set the control to treat this markup as 0 length.</p>
<h4>Indents</h4>
<p>The top row of controls set the default indents for block quotes.
The <i>First</i> indent applies to the first line of a paragraph;
<i>Left</i> to the other lines. The <i>Right</i> indent causes lines to
be shorter than 75 by this amount.</p>
<p>The second row of controls set the indents for poetry, in which the <i>First</i>
indent applies to every line; the <i>Left</i> indent is used only if a line
is too long to fit in 75 chars and is folded.</p>
<p>You can specify the First, Left and/or Right indent for any section
by writing <b>F:</b><i>nn</i> <b>L:</b><i>nn</i> <b>R:</b><i>nn</i> following
the start of the markup. For example <tt>/Q F:8 L:6</tt> starts a 
block-quote markup with those margins, overriding the <i>First</i> and <i>Left</i> margins set with the visible controls, but using the <i>Right</i> from the control.</p>
<p>You can write these explicit indent values on Quote, Poetry and List markups. You can also use them on Right markup but only the <b>R:</b><i>nn</i> is used.
You can use them on no-reflow (/*) markup but only the <b>L:</b><i>nn</i> is used.</p>
<h4>Nesting Markups</h4>
<p>To a limited degree you can nest the markups. For example you can nest
a /P poetry section within a /Q block quote section or a /U list section.
You can nest a /R right align section in poetry or a quote. Multiple
levels of nesting (/R within /P within /Q) are possible. The F/L/R indents
for a nested section are taken relative to the indents for its containing section.</p>
<h4>ASCII Tables</h4>
PPQT treats tables as a special kind of reflow. You mark off the data lines
of the table with <b>/T..T/</b>. The logical columns within a row are separated
in one of two ways: by strings of two or more spaces, or with stiles (|).</p>
<p>A single-line table has one table row per text line. Here is a simple table with two rows and two columns.</p>
<pre>/T
column 1    755.00
another row  2000.00
T/</pre><p>A multi-line table has one or more text lines per logical row,
and the rows are separated by blank lines. The markup starts with <b>/TM</b>.
Here is a multiline table, a typical table of contents:</p>
<pre>/TM
Introduction.--The Present Need   xiii

Chapter I. Applied Art    1

Chapter IV. The Nature and
Properties of Clay   29
T/
</pre>
<p>By default PPQT makes a table 75 characters wide (less
if it is nested in another markup), aligns the column text left, and divides the
columns roughly in proportion to their contents. You can specify detailed
controls on the opening markup line.
Specify table properties with <b>T(</b><i>properties</i><b>)</b> where the
<i>properties</i> can be:</p>
<ul><li><b>W:</b><i>nn</i> for the width of the table.</li>
<li><b>S:'|'</b> (a stile in single quotes) to have the right side of the finished table be a column of
stile characters.</li>
<li><b>T:'-'</b> to have the top line of the table be a row of hyphens.</li>
</ul>
<p>For example <tt>/TM T(W:50)</tt> specifies a multi-line table with a
width of 50.</p>
<p>Set the defaults for all columns with <b>C(</b><i>properties</i><b>)</b>, where
the <i>properties</i> can be:</p>
<ul><li><b>W:</b><i>nn</i> for the minimum width of every column.</li>
<li><b>A:R/L/C</b> for align text left, right or center in the cell.</li>
<li><b>B:'-'</b> to have each cell have a line of hyphens under it.</li>
<li><b>S:'|'</b> to have the left side of each column be a column of stiles.</li>
</ul>
<p>You can set the width and alignment properties (only) of a specific
column <i>n</i> by writing <i>n</i><b>(</b><i>properties</i><b>)</b>.
Here is a fully-specified table before reflow:</p>
<pre>/TM TABLE(TOP:'-' WIDTH:40 SIDE:'|') COL(B:'-' S:'|') 2(A:R W:12)
cell  cell   now is the time for all 
one   two    good parties to end     

row 2 cell  @  some more exciting     
                prose 
T/</pre>
<p>and after reflow:</p>
<pre>/TM TABLE(TOP:'-' WIDTH:40 SIDE:'|') COL(B:'-' S:'|') 2(A:R W:12)
----------------------------------------
|cell one |    cell two|now is the time|
|         |            |for all good   |
|         |            |parties to end |
----------------------------------------
|row 2    |           @|some more      |
|cell     |            |exciting       |
|prose    |            |               |
----------------------------------------
T/</pre>
<p>You can omit the contents of empty cells on the right end of a row. However, you cannot leave blank a cell or cells on any line within a row, or PPQT will assign
text to the wrong column (as in the example above where "prose" fell
from column 3 to column 1 because column 1 & 2 were left blank).
To fill in for a cell that is logically empty,
use a single @ character on every line, as in the above example.</p>
<p>PPQT assigns horizontal space to columns using some brain-dead heuristics.
To get exactly the spacing you want, specify the width of the table and
of each column individually.</p>
<p>As suggested by the example, you can spell out the names of properties,
for example <tt>WIDTH:50</tt> instead of <tt>W:50</tt>. But actually, only
the initial letter is checked, so <tt>WATERMELON:50</tt> works, too.</p>
<h3>HTML Conversion</h3>
<p>ASCII reflow is designed so you can do it repeatedly. HTML conversion
is a one-shot deal, it wipes out the reflow markup lines and the spacing
of tables. Select a range of text and click HTML Convert: Selection, or
click Document to do the whole thing. HTML conversion is a single
undo/redo operation. During conversion the following changes are made
for the different markup types.</p>
<table border='1' style='width:100%;'>
<tr><th style='width:25%;'>Markup</th><th>Converted to:</th></tr>
<tr><td>text paragraphs</td><td><tt>&lt;p></tt><i>para text</i><tt>&lt;/p></tt></td></tr>
<tr><td><b>/Q</b></td><td><tt>&lt;div class="blockquote"></tt></tr>
<tr><td>text in /Q..Q/</td><td><tt>&lt;p></tt><i>para text</i><tt>&lt;/p></tt></td></tr>
<tr><td><b>Q/</b></td><td><tt>&lt;/div></tt></tr>
<tr><td><b>/U</b></td><td><tt>&lt;ul></tt></tr>
<tr><td>text in /U..U/</td><td><tt>&lt;li></tt><i>para text</i><tt>&lt;/li></tt></td></tr>
<tr><td><b>U/</b></td><td><tt>&lt;/ul></tt></tr>
<tr><td><b>/R</b></td><td><tt>&lt;div class="ralign"></tt></tr>
<tr><td>text in /R..R/</td><td><tt>&lt;p></tt><i>each line of text</i><tt>&lt;/p></tt></td></tr>
<tr><td><b>R/</b></td><td><tt>&lt;/div></tt></tr>
<tr><td><b>/X</b>, <b>/C</b>, <b>/*</b></td><td><tt>&lt;pre></tt></td></tr>
<tr><td>text in these</td><td>not touched</td></tr>
<tr><td><b>X/</b>, <b>C/</b>, <b>*/</b></td><td><tt>&lt;/pre></tt></td></tr>
<tr><td><b>/T</b>, <b>/TM</b></td><td><tt>&lt;table></tt> or <tt>&lt;table style="width:<i>pp</i>%;"></tt> where <i>pp</i> is the specified table width/75</tt></td></tr>
<tr><td><b>T/</b></td><td><tt>&lt;/table></tt></td>
</table>
<p>Within a table, the cell values are enclosed appropriately in <tt>&lt;tr></tt> and <tt>&lt;td></tt> codes. Where a specific width was given for a column, the first row of that column is coded <tt>&lt;td style="width:<i>pp</i>%;"></tt> where
<i>pp</i> is based on the specified width divided into the table width.
When a column has right alignment or center alignment, every cell in it is 
coded with <tt>class="r"</tt> or <tt>class="c"</tt> respectively.
This assumes CSS of<pre>td.r {text-align:right}
td.c {text-align:center}</pre>

<p>TBS: controls for removing line separators interactively.</p>
<h2>The Preview Panel</h2>
<p>Click the Pvw tab to display the HTML Preview panel. Whenever
you click the Refresh button on this panel, the complete contents of the
Edit document are copied into this panel and displayed as HTML.
The HTML rendering is done by the open-source WebKit (www.webkit.org), the same HTML engine used by Apple's Safari and by KDE. It fully supports CSS and
standard HTML code.</p>
<p>The base URL for image references is the base path of the book text file,
so the <tt>images</tt> folder should be located at the same place as the book text.</p>
<h2>The Footnote Panel</h2>
<p>TBS Mucho! Controls for validating and formatting footnotes.</p>
</body>
</html>'''


if __name__ == "__main__":
    import sys
    from PyQt4.QtCore import (Qt)
    from PyQt4.QtGui import (QApplication)
    app = QApplication(sys.argv) # create an app
    W = helpDisplay()
    W.show()
    app.exec_()

