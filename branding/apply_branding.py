#!/usr/bin/env python3
"""Rename the app and swap the icon in an upstream Telegram-iOS checkout.

Usage: apply_branding.py <telegram-ios-dir> <display-name>
"""
import glob, os, re, shutil, sys

root, name = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))

# Display name: Info.plist fragments in Telegram/BUILD and localized InfoPlist.strings
build_path = os.path.join(root, 'Telegram/BUILD')
s = open(build_path).read()
s, n = re.subn(r'(<key>CFBundleDisplayName</key>\s*<string>)Telegram(</string>)', r'\g<1>' + name + r'\g<2>', s)
if n == 0:
    sys.exit('CFBundleDisplayName not found in Telegram/BUILD')
open(build_path, 'w').write(s)
print('BUILD: replaced %d display names' % n)

for p in glob.glob(os.path.join(root, 'Telegram/Telegram-iOS/*.lproj/InfoPlist.strings')):
    t = open(p, encoding='utf-8').read()
    t2 = re.sub(r'"CFBundleDisplayName"\s*=\s*"[^"]*";', '"CFBundleDisplayName" = "%s";' % name, t)
    if t2 != t:
        open(p, 'w', encoding='utf-8').write(t2)
        print('strings:', p)

# Icon: replace the glyph and recolor the circle (Icon Composer bundle)
icon_dir = os.path.join(root, 'Telegram/Telegram-iOS/Telegram.icon')
shutil.copy(os.path.join(here, 'Plane.svg'), os.path.join(icon_dir, 'Assets/Plane.svg'))
icon_json = os.path.join(icon_dir, 'icon.json')
j = open(icon_json).read()
replacements = {
    'display-p3:0.21569,0.68627,0.89020,1.00000': 'display-p3:0.66275,0.45490,1.00000,1.00000',
    'srgb:0.11373,0.57647,0.82353,1.00000': 'srgb:0.41569,0.23137,0.87843,1.00000',
    'srgb:0.00000,0.47843,1.00000,1.00000': 'srgb:0.50196,0.29804,1.00000,1.00000',
}
for old, new in replacements.items():
    if old not in j:
        print('warning: icon color %s not found' % old)
    j = j.replace(old, new)
open(icon_json, 'w').write(j)
print('icon updated')
