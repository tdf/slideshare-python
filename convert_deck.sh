#!/usr/bin/env bash
#
# This file is part of the LibreOffice project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

soffice --headless --convert-to pdf --outdir $1 $1/deck.odp
convert -resize $2 $1/deck.pdf $1/deck.png
rm $1/deck.pdf
for i in $1/deck-*.png; do
    rev1=${i/*deck-/}
    rev2=${rev1/.png/}
    mkdir -p $1/$rev2
    mv $i $1/$rev2/thumbnail.png
done

