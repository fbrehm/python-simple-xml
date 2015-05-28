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

import xml.etree.ElementTree as ET

# Third party modules

import six
from six import StringIO

__author__ = 'Frank Brehm <frank.brehm@profitbricks.com>'
__copyright__ = '(C) 2010 - 2015 by profitbricks.com'
__contact__ = 'frank.brehm@profitbricks.com'
__version__ = '0.2.0'
__license__ = 'LGPL3+'


DEFAULT_ENCODING = 'utf-8'

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
        if six.PY2:
            if isinstance(t, text_type):
                t = t.encode(self.encoding)
        else:
            if isinstance(t, six.binary_type):
                t = t.decode(self.encoding)
        return t

    def __bytes__(self):
        """Returns the text value of the node as str in Python2 and bytes in Python3"""
        t = self.node.text or ''
        if isinstance(t, text_type):
            t = t.encode(self.encoding)
        return t

    def __repr__(self):
        return self.__unicode__()

    def __len__(self):
        return 1



#==============================================================================

if __name__ == "__main__":
    pass

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
