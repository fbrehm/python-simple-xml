#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Frank Brehm
@contact: frank.brehm@profitbricks.com
@organization: Profitbricks GmbH
@copyright: © 2010 - 2015 by Profitbricks GmbH
@license: LGPL3+
@summary: a module for a simple xml solution.
"""


# Standard modules
import logging
import xml.etree.ElementTree as ET

# Third party modules

import six
from six import StringIO

__author__ = 'Frank Brehm <frank.brehm@profitbricks.com>'
__copyright__ = '(C) 2010 - 2015 by profitbricks.com'
__contact__ = 'frank.brehm@profitbricks.com'
__version__ = '0.2.3'
__license__ = 'LGPL3+'


DEFAULT_ENCODING = 'utf-8'
LOG = logging.getLogger(__name__)

#==============================================================================
class XMLNode(object):
    """
    Object representation of a single XML node without
    any children.
    """

    def __init__(self, node, encoding=DEFAULT_ENCODING):
        """
        Constructor.

        @param node: a node from a xml.etree.ElementTree
        @type node: xml.etree.ElementTree.Element
        @param encoding: the encoding used for encode from unicode or back
        @type encoding: str
        """

        self.node = node
        """
        @ivar: a xml.etree.ElementTree.node object for the attributes
               of the current XMLNode object
        @type: xml.etree.ElementTree.Element object
        """

        self.encoding = encoding
        """
        @ivar: the encoding used for encode from unicode or back
        @type: str
        """

    def __getitem__(self, key):
        return self.node.attrib.get(key)

    def __setitem__(self, key, value):
        self.node.attrib[key] = value

    def __unicode__(self):
        """Returns the text value of the node as unicode in Python2 and str in Python3"""
        t = self.node.text or ''
        if isinstance(t, six.binary_type):
            t = t.decode(self.encoding)
        return t

    def __str__(self):
        """Returns the text value of the node as str"""
        t = self.node.text or ''
        # LOG.debug("Text of XMLNode before coding: %r", t)
        if six.PY2:
            if isinstance(t, six.text_type):
                # LOG.debug("Encoding to %r ...", self.encoding)
                t = t.encode(self.encoding)
        else:
            if isinstance(t, six.binary_type):
                # LOG.debug("Decoding from %r ...", self.encoding)
                t = t.decode(self.encoding)
        # LOG.debug("Text of XMLNode after coding: %r", t)
        return t

    def __bytes__(self):
        """Returns the text value of the node as str in Python2 and bytes in Python3"""
        t = self.node.text or ''
        if isinstance(t, six.text_type):
            t = t.encode(self.encoding)
        return t

    def __repr__(self):
        return self.__unicode__()

    def __len__(self):
        return 1


#==============================================================================
class XMLTree(object):
    """
    Object representation of a XML tree.
    """

    def __init__(self, node, encoding=DEFAULT_ENCODING):
        """
        Constructor.

        @param node: an element from a xml.etree.ElementTree
        @type node: xml.etree.ElementTree.Element
        @param encoding: the encoding used for encode from unicode or back
        @type encoding: str
        """

        self.nodes = {}
        """
        @ivar: dict with all available tag names as keys and either
               a list of or a single XMLTree or XMLNode object.
        @type: dict
        """

        self.node = node
        """
        @ivar: a xml.etree.ElementTree.Element object for the attributes
               of the current XMLTree object
        @type: xml.etree.ElementTree.Element object
        """

        self.encoding = encoding
        """
        @ivar: the encoding used for encode from unicode or back
        @type: str
        """

        for n in node:
            if len(n.getchildren()):
                xmlnode = XMLTree(n, self.encoding)
            else:
                xmlnode = XMLNode(n, self.encoding)
            if n.tag in self.nodes:
                if isinstance(self.nodes[n.tag], (XMLTree, XMLNode)):
                    self.nodes[n.tag] = [self.nodes[n.tag], xmlnode]
                else:
                    self.nodes[n.tag].append(xmlnode)
            else:
                self.nodes[n.tag] = xmlnode

    def __unicode__(self):
        t = str(dict((k, str(v)) for k, v in six.iteritems(self.nodes)))
        if six.PY2:
            return t.decode(self.encoding)
        return t

    def to_dict(self):
        d = {}
        for key in self.nodes:
            value = self.nodes[key]
            if isinstance(value, XMLNode):
                value = str(value)
            elif isinstance(value, XMLTree):
                value = value.to_dict()
            else:
                l = []
                for v in value:
                    if isinstance(value, XMLNode):
                        val = str(v)
                    else:
                        val = v.to_dict()
                    l.append(val)
                value = l
            d[key] = value
        return d

    def __str__(self):
        return str(self.to_dict())

    def __bytes__(self):
        t = str(dict((k, str(v)) for k, v in six.iteritems(self.nodes)))
        if six.PY2:
            return t
        return t.encode(self.encoding)

    def __getattr__(self, attr):
        return self.nodes[attr]

    def __getitem__(self, key):
        return self.node.attrib.get(key)

    def __setitem__(self, key, value):
        self.node.attrib[key] = value

    def __len__(self):
        return len(self.nodes)


#==============================================================================
def parse_xml_file(file_object, encoding=DEFAULT_ENCODING):
    """
    Reads the given file object and returns a complete XMLTree object.

    @raise ParseError: on invalid XML given
    @return: a XMLTree object

    """
    tree = ET.parse(file_object)
    return XMLTree(tree.getroot(), encoding)


#==============================================================================
def parse_xml_string(string, encoding=DEFAULT_ENCODING):
    """
    Parses the given string and returns a complete XMLTree object.

    @raise ParseError: on invalid XML given
    @return: a XMLTree object

    """
    return parse_xml_file(StringIO(string), encoding)


#==============================================================================

if __name__ == "__main__":
    pass

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
