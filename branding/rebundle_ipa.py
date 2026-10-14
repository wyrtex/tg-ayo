#!/usr/bin/env python3
"""Change the bundle id prefix of every bundle inside an IPA so it can be
installed next to the official Telegram. The IPA is re-signed afterwards anyway.

Usage: rebundle_ipa.py <in.ipa> <out.ipa> <old-prefix> <new-prefix>
"""
import plistlib, sys, zipfile

src, dst, old, new = sys.argv[1:5]

def fix(v):
    if isinstance(v, str):
        if v == old or v.startswith(old + '.'):
            return new + v[len(old):]
        return v
    if isinstance(v, list):
        return [fix(x) for x in v]
    if isinstance(v, dict):
        return {k: fix(x) for k, x in v.items()}
    return v

count = 0
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename.startswith('Payload/') and info.filename.endswith('/Info.plist'):
            try:
                plist = plistlib.loads(data)
            except Exception:
                plist = None
            if isinstance(plist, dict):
                fixed = fix(plist)
                if fixed != plist:
                    fmt = plistlib.FMT_BINARY if data.startswith(b'bplist') else plistlib.FMT_XML
                    data = plistlib.dumps(fixed, fmt=fmt)
                    count += 1
                    print('rebundled', info.filename, '->', fixed.get('CFBundleIdentifier'))
        zout.writestr(info, data)

if count == 0:
    sys.exit('no Info.plist with bundle id %s found' % old)
