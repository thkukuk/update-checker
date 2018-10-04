#
# Copyright (c) 2018 Thorsten Kukuk, Germany
#
# Author: Thorsten Kukuk <kukuk@suse.de>
#

CLEANFILES = $(MANS) $(DATA) update-checker.index.xml xml_helper.pyc

EXTRA_DIST = $(MANS) $(XMLS) $(DATA) custom-html.xsl \
	make-man-index.py xml_helper.py update-checker.index.xml

man_MANS = update-checker-migration.8 update-checker.conf.5 \
	   update-checker-migration.service.8 \
	   update-checker-migration.timer.8 update-checker.8 \
	   update-checker.service.8 update-checker.timer.8
noinst_DATA = update-checker-migration.8.html update-checker.conf.5.html \
	      update-checker.index.html update-checker.8.html \
	      update-checker-migration.service.8.html \
	      update-checker-migration.timer.8.html \
	      update-checker.service.8.html update-checker.timer.8.html
XMLS = update-checker.8.xml \
       update-checker-migration.8.xml \
       update-checker.conf.5.xml

XSLTPROC_FLAGS_HTML = \
	--nonet \
	--xinclude \
	--stringparam man.authors.section.enabled 0 \
	--stringparam man.copyright.section.enabled 0 \
	--stringparam package.name $(PACKAGE) \
	--stringparam package.version $(VERSION) \
	--stringparam chunker.output.encoding UTF-8 \
	--stringparam sysconfdir $(sysconfdir) \
	--stringparam prefix $(prefix) \
	$(srcdir)/custom-html.xsl

XSLTPROC_FLAGS_MAN = \
	--nonet \
	--xinclude \
	--stringparam sysconfdir $(sysconfdir) \
	--stringparam prefix $(prefix) \
	$(srcdir)/custom-man.xsl

if ENABLE_REGENERATE_MAN

define html-alias
	$(LN_S) -f $(notdir $<) $@
endef

update-checker.index.xml: make-man-index.py $(XMLS)
	python3 $(srcdir)/make-man-index.py $(srcdir)/$@ $(XMLS)

update-checker.index.html: update-checker.index.xml custom-html.xsl
	$(XSLTPROC) -o $(srcdir)/$@ --path $(srcdir) $(XSLTPROC_FLAGS_HTML) $<

update-checker.conf.5: update-checker.conf.5.xml custom-man.xsl
	$(XSLTPROC) -o $(srcdir)/$@ --path $(srcdir) --xinclude --nonet http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl $<

update-checker.conf.5.html: update-checker.conf.5.xml custom-html.xsl
	$(XSLTPROC) -o $(srcdir)/$@ --path $(srcdir) $(XSLTPROC_FLAGS_HTML) $<

update-checker.8: update-checker.8.xml
	$(XSLTPROC) -o $(srcdir)/$@ --path $(srcdir) --xinclude --nonet http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl $<

update-checker.service.8: update-checker.8

update-checker.timer.8: update-checker.8

update-checker.8.html: update-checker.8.xml custom-html.xsl
	$(XSLTPROC) -o $(srcdir)/$@ --path $(srcdir) $(XSLTPROC_FLAGS_HTML) $<

update-checker.service.8.html: update-checker.8.html
	$(html-alias)

update-checker.timer.8.html: update-checker.8.html
	$(html-alias)

update-checker-migration.8: update-checker-migration.8.xml
	$(XSLTPROC) -o $(srcdir)/$@ --path $(srcdir) --xinclude --nonet http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl $<

update-checker-migration.service.8: update-checker-migration.8

update-checker-migration.timer.8: update-checker-migration.8

update-checker-migration.8.html: update-checker-migration.8.xml custom-html.xsl
	$(XSLTPROC) -o $(srcdir)/$@ --path $(srcdir) $(XSLTPROC_FLAGS_HTML) $<

update-checker-migration.service.8.html: update-checker-migration.8.html
	$(html-alias)

update-checker-migration.timer.8.html: update-checker-migration.8.html
	$(html-alias)

endif
