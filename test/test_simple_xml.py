#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Frank Brehm
@contact: frank.brehm@profitbricks.com
@organization: Profitbricks GmbH
@copyright: © 2010 - 2015 by Profitbricks GmbH
@license: GPL3
@summary: test script (and module) for unit tests on the simple_xml module
'''

import os
import sys
import random
import glob
import logging
import tempfile
import shutil

try:
    import unittest2 as unittest
except ImportError:
    import unittest

libdir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', 'lib'))
sys.path.insert(0, libdir)

from general import SimpleXmlTestcase, get_arg_verbose, init_root_logger

from pb_base.common import to_utf8_or_bust

LOG = logging.getLogger('test_simple_xml')

SAMPLE_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<verzeichnis bla="blub">
    <titel>Wikipedia Städteverzeichnis</titel>
    <author>&lt;frank@brehm-online.com&gt;</author>
    <eintrag land="CH">
        <stichwort>Genf</stichwort>
        <eintragstext>Genf ist der Sitz von ...</eintragstext>
    </eintrag>
    <eintrag land="DE">
        <stichwort>Köln</stichwort>
        <eintragstext>Köln ist eine Stadt, die ...</eintragstext>
    </eintrag>
</verzeichnis>
"""

BROKEN_XML = """<uhu><banane</uhu>"""

# =============================================================================
class TestSimpleXml(SimpleXmlTestcase):

    # -------------------------------------------------------------------------
    def setUp(self):

        pass

    # -------------------------------------------------------------------------
    def test_import(self):

        LOG.info("Test importing simple_xml ...")

        import simple_xml       # noqa

    # -------------------------------------------------------------------------
    def test_parse_string(self):

        LOG.info("Test parsing a XML string into a XMLTree object and its string representation.")

        import simple_xml       # noqa
        from simple_xml import parse_xml_string

        if self.verbose > 2:
            LOG.debug("Source XML:\n%s", SAMPLE_XML)

        tree = parse_xml_string(SAMPLE_XML)
        LOG.debug("XMLTree object as a dict: %r", tree.to_dict())
        LOG.debug("Str of XMLTree object: %s", str(tree))

    # -------------------------------------------------------------------------
    def test_broken_xml(self):

        LOG.info("Test trying to parse a broken XML string.")

        import simple_xml       # noqa
        from simple_xml import parse_xml_string
        from xml.etree.ElementTree import ParseError

        if self.verbose > 2:
            LOG.debug("Broken source XML: %r", BROKEN_XML)

        with self.assertRaises(ParseError) as cm:
            tree = parse_xml_string(BROKEN_XML)
        e = cm.exception
        LOG.debug(
            "%s raised as expected on trying to parse broken XML: %s.",
            'ParseError', e)


# =============================================================================

if __name__ == '__main__':

    verbose = get_arg_verbose()
    if verbose is None:
        verbose = 0
    init_root_logger(verbose)

    LOG.info("Starting tests ...")

    suite = unittest.TestSuite()

    suite.addTest(TestSimpleXml('test_import', verbose))
    suite.addTest(TestSimpleXml('test_parse_string', verbose))
    suite.addTest(TestSimpleXml('test_broken_xml', verbose))

    runner = unittest.TextTestRunner(verbosity=verbose)

    result = runner.run(suite)

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
