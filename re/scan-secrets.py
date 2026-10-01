#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/scan-secrets.py
推送前凭据与 PII 扫描：只读本地待推送文件，不改任何文件。
"""
import os, re, sys, json, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 待扫描：git 未跟踪文件 + 本轮新增
def untracked():
    out = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT,
                         capture_output=True, text=True, encoding='utf-8')
    files = []
    for line in out.stdout.splitlines():
        if line.startswith('??'):
            p = line[3:].strip().strip('"')
            files.append(p)
    return files

RULES = [
    ('高德/地图 key(32位hex)', re.compile(r'\b[0-9a-f]{32}\b', re.I)),
    ('securityJsCode', re.compile(r'securityJsCode\s*[:=]\s*["\']?[0-9a-f]{16,}', re.I)),
    ('Bearer/token 字面量', re.compile(r'(Bearer\s+[A-Za-z0-9\-_\.]{20,})', re.I)),
    ('token/password/secret 赋值',
     re.compile(r'(?i)(token|password|passwd|secret|apiKey|api_key|accessKey)\s*[:=]\s*["\'][^"\']{8,}["\']')),
    ('微信 appid/secret', re.compile(r'(?i)(wx[a-f0-9]{16}|corpsecret\s*[:=])')),
    ('手机号', re.compile(r'(?<!\d)1[3-9]\d{9}(?!\d)')),
    ('身份证号', re.compile(r'(?<!\d)\d{17}[\dXx](?!\d)')),
    ('私钥块', re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),
]

# 人名清单属机构内部信息，不随仓库分发；需要复扫时在此临时填入
PII_NAME = re.compile(r'(?!x)x')  # 空匹配，不做姓名检测


def main():
    files = untracked()
    print('待扫描未跟踪文件: %d' % len(files))
    hits = {}
    pii = {}

    for rel in files:
        full = os.path.join(ROOT, rel)
        paths = []
        if os.path.isdir(full):
            for dp, _, fns in os.walk(full):
                for fn in fns:
                    paths.append(os.path.join(dp, fn))
        else:
            paths.append(full)
        for p in paths:
            try:
                with open(p, encoding='utf-8', errors='replace') as f:
                    s = f.read()
            except Exception:
                continue
            relp = os.path.relpath(p, ROOT)
            for name, rx in RULES:
                for m in rx.finditer(s):
                    hits.setdefault(name, []).append((relp, m.group(0)[:60]))
            for m in PII_NAME.finditer(s):
                pii.setdefault(relp, set()).add(m.group(0))

    print('\n== 凭据扫描 ==')
    if not hits:
        print('  未命中任何凭据规则  ✅')
    for k, v in sorted(hits.items()):
        print('  [%s] %d 处' % (k, len(v)))
        for f, t in v[:6]:
            print('      %s :: %s' % (f, t))

    print('\n== PII 人名扫描 ==')
    if not pii:
        print('  未命中  ✅')
    for f, names in sorted(pii.items()):
        print('  %-50s %s' % (f, sorted(names)))

    out = {'files': len(files),
           'secretHits': {k: v for k, v in hits.items()},
           'piiHits': {k: sorted(v) for k, v in pii.items()}}
    dest = os.path.join(ROOT, 're', 'secret-scan.json')
    with open(dest, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print('\nWrote: re/secret-scan.json')


if __name__ == '__main__':
    main()
