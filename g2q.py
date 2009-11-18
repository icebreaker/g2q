####################################################################################
#
# Gedit To QtCreator Style Scheme Converter v0.1
#
# Copyright (c) 2009, Mihail Szabolcs
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
#   * 	Redistributions of source code must retain the above copyright
#		notice, this list of conditions and the following disclaimer.
#
#   * 	Redistributions in binary form must reproduce the above copyright
#		notice, this list of conditions and the following disclaimer in
#		the documentation and/or other materials provided with the
#		distribution.
#
#   * 	Neither the name of the G2Q nor the names of its contributors
#		may be used to endorse or promote products derived from this
#		software without specific prior written permission.
#
#	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#	ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#	LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#	OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#	SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#	INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#	THE POSSIBILITY OF SUCH DAMAGE.
#
####################################################################################
import sys
import xml.dom.minidom

# Converter Helper Class
class g2qElement:
	# Constructor
	def __init__(self,name):
		self.attr = {}
		self.setAttr('name',name)
	# Set an attribute (name=>value)
	def setAttr(self,name,value):
		self.attr[name] = value
	# Get an attribute by name
	def getAttr(self,name):
		if name in self.attr:
			return self.attr[name]
		return None
	# Bake xml as string
	def toXML(self):
		xml = '<style'
		for name,value in self.attr.iteritems():
			xml+=' '+name+'="'+value+'"'
		xml+= '/>\n'
		return xml

# Converter Class
class g2q:
	# Constructor
	def __init__(self,ifile):
		self.ifile 	= ifile
		self.name	= None
		self.elems	= []
		# Try to parse the Gedit Scheme
		self._parseXML()
	# Ready Status
	def ready(self):
		if self.name and len(self.elems):
			return True
		return False
	# Bake xml as string
	def toXML(self):
		xml = '<style-scheme version="1.0" name="'+self.name.replace("&","&amp;")+'">\n'
		for e in self.elems:
			xml+=e.toXML()
		xml+= '</style-scheme>\n'
		return xml
	# Parse XML
	def _parseXML(self):
		try:
			fin = xml.dom.minidom.parse(self.ifile)
		except:
			return 0
    	       
		root = None
		for n in fin.childNodes:
			if n.nodeType == n.ELEMENT_NODE:
				self.name = n.getAttribute('_name')
				root = n
				break

		if not self.name or not root:
			return -1
			
		e = g2qElement('DisabledCode')
		e.setAttr('foreground','#ffffff')
		self.elems.append(e)

		for n in root.childNodes:
			if n.nodeType != n.ELEMENT_NODE or n.localName != 'style':
				continue
    	
			name = n.getAttribute('name')
			if not name or not name in self.convMap:
				continue
    			
			name = self.convMap[ name ]	
			
			e = g2qElement(name)

			for a in self.attrList:
				attr = n.getAttribute(a)
				if len(attr):
					e.setAttr(a,attr)
    		
			self.elems.append(e)

		return 1
	############### Variables ######################
	# Gedit to QtCreator style map
	convMap={
		'text':'Text',
	 	'def:type':'Type',
	 	'def:string':'String',
	 	'current-line':'CurrentLine',
		'line-numbers':'LineNumber',
	 	'def:comment':'Comment',
	 	'selection':'Selection',
	 	'def:preprocessor':'Preprocessor',
	 	'def:operator':'Operator',
	 	'def:number':'Number',
		'def:keyword':'Keyword',
		'def:reserved':'Label',
		'def:statement':'Parentheses',
		'def:doc-comment':'Doxygen.Comment',
		'def:doc-comment-element':'Doxygen.Tag',
		'diff:added-line':'AddedLine',
		'diff:location':'DiffLocation',
		'diff:removed-line':'RemovedLine'
	}
	# List of attributes we are interested in
	# when parsing elements
	attrList=[
		'background',
		'foreground',
		'underline',
		'bold',
		'italic'
	]

#Link
#Occurrences
#Occurrences.Rename
#DiffFile
#SearchResult
#SearchScope

# Main Procedure
def main():
	print 'Gedit To QtCreator Style Scheme Converter v0.1'
	print 'Copyright (c) 2009, Mihail Szabolcs'
	print ''

	args = sys.argv[1:]

	if not args or len(args) != 2:
	    print "usage: g2q gedit-scheme.xml qt-creator-output-scheme.xml"
	    return
	
	print "Processing %s ..." % (args[0])
	conv = g2q(args[0])

	if not conv.ready():
		return

	xml = conv.toXML()
	if not xml or not len(xml):
		return
	
	try:
		file = open(args[1],"w")
		file.write(xml.encode("utf-8"))
		file.close()
	except:
		print 'An error occurred while saving the file.'
		return
	
	print 'Done!'
	
# Execute The Main Procedure
if __name__ == '__main__':
 	main()
