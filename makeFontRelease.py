#!/usr/bin/python
# (c) 2020~2026 David SPORN
# SPDX : GPL3.0-or-later
#
# Arguments
# ---
# * $1 : path to sfdir folder, without the ".sfdir" extension, e.g. to process 'src/whatever.sfdir', give 'src/whatever'
# ---

from sys import argv
import os
import fontforge

#
# --- argument checking ---
#
if len(argv) < 2:
    raise RuntimeError(f"must.be.called.with.one.argument:{argv[0]}")

SOURCE_FONT = f"{argv[1]}.sfdir"
if not os.path.exists(SOURCE_FONT):
    raise RuntimeError(f"must.exist:{SOURCE_FONT}")
if not os.path.isdir(SOURCE_FONT) and not os.path.isfile(SOURCE_FONT):
    raise RuntimeError(f"must.be.an.existing.file.or.folder:{SOURCE_FONT}")

#
# --- build parameters ---
#
BASE_DIR = os.path.abspath(os.path.dirname(argv[0]))
(_, FILE_NAME) = os.path.split(argv[1])

TARGET_DIR = os.path.join(BASE_DIR,"build")
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)
if not os.path.isdir(TARGET_DIR):
    raise RuntimeError(f"must.be.a.folder:{TARGET_DIR}")

TARGET_NAME = os.path.join(TARGET_DIR, FILE_NAME)

#
# === START PROCESSING ===
#

curfnt = fontforge.open(SOURCE_FONT)

#
# Required so that the generated fonts are rendered correctly
#
curfnt.selection.all()
curfnt.removeOverlap()
curfnt.correctDirection()
curfnt.addExtrema()

#
# Correct generation flags
#
genflags = ("opentype", "dummy-dsig")

for f in ["otf", "woff"]:
    target_font = f"{TARGET_NAME}.{f}"
    print(f"Generating '{target_font}' ...")
    curfnt.generate(target_font, flags=genflags)

#
# Required for TTF fonts
#
for layer in curfnt.layers:
    curfnt.layers[layer].is_quadratic = True

for f in ["ttf"]:
    target_font = f"{TARGET_NAME}.{f}"
    print(f"Generating '{target_font}' ...")
    curfnt.generate(target_font, flags=genflags)

#
# Required to avoid accidental mutation of the source files
# (better safe than sorry)
#
curfnt.revert()

