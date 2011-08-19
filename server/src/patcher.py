#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
#
# Copyright (C) 2005-2009 University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals, 
# listed below:
#
# Author: Pablo Orduña <pablo@ordunya.com>
#

import sys

##########################################################
# 
#            R A T I O N A L E 
# 
# There is a set of issues with external libraries
# that have an impact in the project. Some of these
# might be considered bugs, other just version issues.
# 
# Since we can fix all these issues dynamically, we
# do it. This is easier to manage than changing the 
# code of the libraries.
# 

patches = []

def patch(func):
    patches.append(func)

def apply():
    for patch in patches:
        patch()

#########################################################
#
#     ZSI and PyExpat
#
# Description:
# 
#   ZSI used to use PyXML for parsing XML. This library
#   is really old, deprecated and doesn't count with 
#   compilations for many platforms. However, its 
#   functionality comes with the default Python Library,
#   so it should actually try to use this one instead of
#   PyXML. Actually, in the SVN they have started to use
#   it, but this change is not available in most
#   distributions. Due to this, we make ZSI use this
#   implementation.
# 

@patch
def patchZsiPyExpat():

    try:
        import ZSI
    except ImportError:
        print >> sys.stderr, "patchZsiPyExpat skipped; ZSI not installed"
        return

    # 
    # The new builder
    # 
    from xml.dom import expatbuilder

    class DefaultReader:
        """ExpatReaderClass"""
        fromString = staticmethod(expatbuilder.parseString)
        fromStream = staticmethod(expatbuilder.parse)

    # 
    # ZSI modules using PyExpat
    # 
    import ZSI.parse
    import ZSI.TC

    # 
    # We just change their default parsers:
    ZSI.parse.ParsedSoap.defaultReaderClass = DefaultReader

    class PatchedXMLString(ZSI.TC.XMLString):
        def parse(self, *args):
            self.readerclass = DefaultReader
            ZSI.TC.XMLString.parse(self, *args)

    ZSI.TC.XMLString = PatchedXMLString

#########################################################

