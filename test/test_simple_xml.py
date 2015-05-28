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

# =============================================================================
class TestSimpleXml(SimpleXmlTestcase):

    # -------------------------------------------------------------------------
    def setUp(self):

        pass

    # -------------------------------------------------------------------------
    def test_import(self):

        LOG.info("Test importing simple_xml ...")

        import simple_xml


# =============================================================================

if __name__ == '__main__':

    verbose = get_arg_verbose()
    if verbose is None:
        verbose = 0
    init_root_logger(verbose)

    LOG.info("Starting tests ...")

    suite = unittest.TestSuite()

    suite.addTest(TestSimpleXml('test_import', verbose))

    runner = unittest.TextTestRunner(verbosity=verbose)

    result = runner.run(suite)

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
