#!/usr/bin/env python
#
# This file is part of the LibreOffice project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import fnmatch
import os
from subprocess import call

# Logic:
# Find all *.*odp recursively and see if there are corresponding .pngs
# if not call convert_deck.sh

matches = []
for root, dirnames, filenames in os.walk('filestore'):
    for filename in fnmatch.filter(filenames, 'deck*.*odp'):
        if len(fnmatch.filter(filenames, 'deck*.png')) <= 0:
            call(['./convert_deck.sh', root, '128x128'])
