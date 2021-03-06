#  -*- Mode: python; coding: utf-8; indent-tabs-mode: nil -*- */
#
#  The original file is part of systemd. This one was modified for
#  update-checker.
#
#  Copyright 2012 Lennart Poettering
#  Copyright 2013 Zbigniew Jędrzejewski-Szmek
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
#
#  systemd is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with systemd; If not, see <http://www.gnu.org/licenses/>.

import collections
import sys
import re
from xml_helper import *

MDASH = ' — ' if sys.version_info.major >= 3 else ' -- '

TEMPLATE = '''\
<refentry id="update-checker.index" conditional="HAVE_PYTHON">

  <refentryinfo>
    <title>update-checker.index</title>
    <productname>update-checker</productname>
  </refentryinfo>

  <refmeta>
    <refentrytitle>update-checker.index</refentrytitle>
    <manvolnum>7</manvolnum>
  </refmeta>

  <refnamediv>
    <refname>update-checker.index</refname>
    <refpurpose>List all manpages from the update-checker project</refpurpose>
  </refnamediv>
</refentry>
'''

SUMMARY = '''\
  <refsect1>
    <para id='counts' />
  </refsect1>
'''

COUNTS = '\
This index contains {count} entries, referring to {pages} individual manual pages.'


def check_id(page, t):
    id = t.getroot().get('id')
    if not re.search('^' + id + '[.]', page):
        raise ValueError("id='{}' is not the same as page name '{}'".format(id, page))

def make_index(pages):
    index = collections.defaultdict(list)
    for p in pages:
        t = xml_parse(p)
        check_id(p, t)
        section = t.find('./refmeta/manvolnum').text
        refname = t.find('./refnamediv/refname').text
        purpose = ' '.join(t.find('./refnamediv/refpurpose').text.split())
        for f in t.findall('./refnamediv/refname'):
            infos = (f.text, section, purpose, refname)
            index[f.text[0].upper()].append(infos)
    return index

def add_letter(template, letter, pages):
    refsect1 = tree.SubElement(template, 'refsect1')
    title = tree.SubElement(refsect1, 'title')
    title.text = letter
    para = tree.SubElement(refsect1, 'para')
    for info in sorted(pages, key=lambda info: str.lower(info[0])):
        refname, section, purpose, realname = info

        b = tree.SubElement(para, 'citerefentry')
        c = tree.SubElement(b, 'refentrytitle')
        c.text = refname
        d = tree.SubElement(b, 'manvolnum')
        d.text = section

        b.tail = MDASH + purpose # + ' (' + p + ')'

        tree.SubElement(para, 'sbr')

def add_summary(template, indexpages):
    count = 0
    pages = set()
    for group in indexpages:
        count += len(group)
        for info in group:
            refname, section, purpose, realname = info
            pages.add((realname, section))

    refsect1 = tree.fromstring(SUMMARY)
    template.append(refsect1)

    para = template.find(".//para[@id='counts']")
    para.text = COUNTS.format(count=count, pages=len(pages))

def make_page(*xml_files):
    template = tree.fromstring(TEMPLATE)
    index = make_index(xml_files)

    for letter in sorted(index):
        add_letter(template, letter, index[letter])

    add_summary(template, index.values())

    return template

if __name__ == '__main__':
    with open(sys.argv[1], 'wb') as f:
        f.write(xml_print(make_page(*sys.argv[2:])))
