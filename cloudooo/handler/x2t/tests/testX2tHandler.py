##############################################################################
#
# Copyright (c) 2009-2010 Nexedi SA and Contributors. All Rights Reserved.
#                    Gabriel M. Monnerat <gabriel@tiolive.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is free software: you can Use, Study, Modify and Redistribute
# it under the terms of the GNU General Public License version 3, or (at your
# option) any later version, as published by the Free Software Foundation.
#
# You can also Link and Combine this program with other software covered by
# the terms of any of the Free Software licenses or any of the Open Source
# Initiative approved licenses and Convey the resulting work. Corresponding
# source of such a combination shall include the source code for all other
# software used.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING file for full licensing terms.
# See https://www.nexedi.com/licensing for rationale and options.
#
##############################################################################


from zipfile import ZipFile
from cStringIO import StringIO
from cloudooo.handler.x2t.handler import Handler
from cloudooo.tests.handlerTestCase import HandlerTestCase

OPENOFFICE = True


class TestHandler(HandlerTestCase):

  def afterSetUp(self):
    self.kw = dict(env=dict(PATH=self.env_path))

  def testConvertXlsx(self):
    """Test conversion of xlsx to xlsy and back"""
    y_data = Handler(self.tmp_url, open("data/test.xlsx").read(), "xlsx", **self.kw).convert("xlsy")
    y_body_data = ZipFile(StringIO(y_data)).open("body.txt").read()
    self.assertTrue(y_body_data.startswith("XLSY;v10;0;"), "%r... does not start with 'XLSY;v10;0;'" % (y_body_data[:20],))

    x_data = Handler(self.tmp_url, y_data, "xlsy", **self.kw).convert("xlsx")
    # magic inspired by https://github.com/minad/mimemagic/pull/19/files
    self.assertIn("xl/", x_data[:2000])

  def testConvertXlsy(self):
    """Test conversion of xlsy to xlsx and back"""
    x_data = Handler(self.tmp_url, open("data/test_body.xlsy").read(), "xlsy", **self.kw).convert("xlsx")
    self.assertIn("xl/", x_data[:2000])
    x_data = Handler(self.tmp_url, open("data/test.xlsy").read(), "xlsy", **self.kw).convert("xlsx")
    self.assertIn("xl/", x_data[:2000])

    y_data = Handler(self.tmp_url, x_data, "xlsx", **self.kw).convert("xlsy")
    y_body_data = ZipFile(StringIO(y_data)).open("body.txt").read()
    self.assertTrue(y_body_data.startswith("XLSY;v10;0;"), "%r... does not start with 'XLSY;v10;0;'" % (y_body_data[:20],))

  def testConvertDocx(self):
    """Test conversion of docx to docy and back"""
    y_data = Handler(self.tmp_url, open("data/test_with_image.docx").read(), "docx", **self.kw).convert("docy")
    y_zip = ZipFile(StringIO(y_data))
    y_body_data = y_zip.open("body.txt").read()
    self.assertTrue(y_body_data.startswith("DOCY;v10;0;"), "%r... does not start with 'DOCY;v10;0;'" % (y_body_data[:20],))
    y_zip.open("media/image1.png")

    x_data = Handler(self.tmp_url, y_data, "docy", **self.kw).convert("docx")
    # magic inspired by https://github.com/minad/mimemagic/pull/19/files
    self.assertIn("word/", x_data[:2000])

  def testConvertDocy(self):
    """Test conversion of docy to docx and back"""
    x_data = Handler(self.tmp_url, open("data/test_with_image.docy").read(), "docy", **self.kw).convert("docx")
    self.assertIn("word/", x_data[:2000])

    y_data = Handler(self.tmp_url, x_data, "docx", **self.kw).convert("docy")
    y_zip = ZipFile(StringIO(y_data))
    y_body_data = y_zip.open("body.txt").read()
    self.assertTrue(y_body_data.startswith("DOCY;v10;0;"), "%r... does not start with 'DOCY;v10;0;'" % (y_body_data[:20],))
    y_zip.open("media/image1.png")

  def testgetMetadata(self):
    """Test getMetadata from yformats"""
    handler = Handler(self.tmp_url, "", "xlsy", **self.kw)
    self.assertEquals(handler.getMetadata(), {
	u'CreationDate': u'00/00/0000 00:00:00',
	u'ImplementationName': u'com.sun.star.comp.comphelper.OPropertyBag',
	u'MIMEType': u'text/plain',
	u'ModificationDate': u'00/00/0000 00:00:00',
	u'PrintDate': u'00/00/0000 00:00:00',
	u'TemplateDate': u'00/00/0000 00:00:00',
	})
    handler = Handler(self.tmp_url, open("data/test_with_metadata.xlsy").read(), "xlsy", **self.kw)
    self.assertEquals(handler.getMetadata(), {
        u'CreationDate': u'31/01/2018 21:09:10',
        u'Keywords': [u'\u0442\u0435\u0441\u0442', u'\u0441\u0430\u0431\u0436\u0435\u043a\u0442'],
        'MIMEType': 'application/x-asc-spreadsheet',
        u'ModificationDate': u'31/01/2018 21:22:36',
        u'PrintDate': u'00/00/0000 00:00:00',
        u'Subject': u'\u0432\u044b\u043a\u043b\u044e\u0447\u0438 \u0442\u0435\u043b\u0435\u0432\u0438\u0437\u043e\u0440',
        u'TemplateDate': u'00/00/0000 00:00:00',
        u'Title': u'kesha'})

  def testsetMetadata(self):
    """Test setMetadata for yformats"""
    handler = Handler(self.tmp_url, open("data/test_with_metadata.xlsy").read(), "xlsy", **self.kw)
    new_mime_data = handler.setMetadata({
            "Title": "test title",
            "Subject": "test subject",
            "Keywords": "test keywords",
           })
    handler = Handler(self.tmp_url, new_mime_data, "xlsy", **self.kw)
    self.assertEquals(handler.getMetadata(), {u'Keywords': u'test keywords', 'MIMEType': 'application/x-asc-spreadsheet', u'Title': u'test title', u'Subject': u'test subject'})

  def testGetAllowedConversionFormatList(self):
    """Test all combination of mimetype

    None of the types below define any mimetype parameter to not ignore so far.
    """
    get = Handler.getAllowedConversionFormatList
    self.assertEquals(get("application/x-asc-text;ignored=param"),
      [("application/vnd.openxmlformats-officedocument.wordprocessingml.document", "Word 2007 Document"),
       ('application/vnd.oasis.opendocument.text', 'ODF Text Document')])
    self.assertEquals(get("application/x-asc-spreadsheet;ignored=param"),
      [("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "Excel 2007 Spreadsheet"),
	('application/vnd.oasis.opendocument.spreadsheet', 'ODF Spreadsheet Document')])
    self.assertEquals(get("application/x-asc-presentation;ignored=param"),
      [("application/vnd.openxmlformats-officedocument.presentationml.presentation", "PowerPoint 2007 Presentation"),
	('application/vnd.oasis.opendocument.presentation', 'ODF Presentation Document')])

