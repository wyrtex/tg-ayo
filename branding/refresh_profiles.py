#!/usr/bin/env python3
"""Re-wrap the bundled fake provisioning profiles with a far-future ExpirationDate.

The fake .mobileprovision files shipped with Telegram-iOS carry a fixed expiry;
once it passes, rules_apple's plisttool refuses to build. These profiles only
stamp entitlements into an UNSIGNED build (we re-sign in ESign anyway), and the
extraction tools ("security cms -D", "openssl smime -verify -noverify") do not
check the signer, so re-signing with a throwaway cert is fine.

Usage: refresh_profiles.py <telegram-ios-dir>
"""
import datetime
import glob
import os
import plistlib
import subprocess
import sys
import tempfile


def find_openssl():
    candidates = [
        '/opt/homebrew/opt/openssl@3/bin/openssl',
        '/usr/local/opt/openssl@3/bin/openssl',
        '/opt/homebrew/bin/openssl',
        'openssl',
    ]
    for c in candidates:
        try:
            subprocess.run([c, 'version'], check=True, capture_output=True)
            return c
        except Exception:
            continue
    raise RuntimeError('no usable openssl found')


def main():
    root = sys.argv[1]
    profiles_dir = os.path.join(root, 'build-system/fake-codesigning/profiles')
    openssl = find_openssl()
    print('using openssl:', openssl)

    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    expiry = now + datetime.timedelta(days=3650)

    work = tempfile.mkdtemp()
    key_path = os.path.join(work, 'key.pem')
    cert_path = os.path.join(work, 'cert.pem')
    subprocess.run([
        openssl, 'req', '-x509', '-newkey', 'rsa:2048', '-nodes',
        '-keyout', key_path, '-out', cert_path, '-days', '3650',
        '-subj', '/CN=AyoGram Fake Profile Signer'
    ], check=True, capture_output=True)

    count = 0
    for path in sorted(glob.glob(os.path.join(profiles_dir, '*.mobileprovision'))):
        data = open(path, 'rb').read()
        start = data.find(b'<?xml')
        end = data.find(b'</plist>')
        if start == -1 or end == -1:
            print('skip (no plist):', os.path.basename(path))
            continue
        end += len(b'</plist>')
        plist = plistlib.loads(data[start:end])
        plist['ExpirationDate'] = expiry
        plist['CreationDate'] = now
        plist['TimeToLive'] = 3650
        xml_path = os.path.join(work, 'profile.plist')
        open(xml_path, 'wb').write(plistlib.dumps(plist, fmt=plistlib.FMT_XML))
        subprocess.run([
            openssl, 'smime', '-sign', '-nodetach', '-binary',
            '-signer', cert_path, '-inkey', key_path,
            '-in', xml_path, '-outform', 'der', '-out', path
        ], check=True, capture_output=True)
        count += 1
        print('refreshed:', os.path.basename(path), '->', expiry.date().isoformat())

    if count == 0:
        raise RuntimeError('no profiles refreshed at %s' % profiles_dir)
    print('done, %d profiles' % count)


if __name__ == '__main__':
    main()
