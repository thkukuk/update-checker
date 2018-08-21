#
# Copyright (c) 2018 Ignaz Forster <iforster@suse.com>
#

EXTRA_DIST = update-checker.conf

install-data-local:
	$(mkinstalldirs) $(DESTDIR)$(sysconfdir)
	$(INSTALL_DATA) $(srcdir)/$(EXTRA_DIST) $(DESTDIR)$(sysconfdir)

uninstall-local:
	-rm $(DESTDIR)$(sysconfdir)/$(EXTRA_DIST)
