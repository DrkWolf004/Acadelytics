#!/usr/bin/env python3
"""
Remove single-line comments starting with
Heuristics:
- Preserve shebang lines starting with
- Do not remove
- Track string quoting to avoid removing comment markers inside strings.
- Operates on a safe set of text file extensions to avoid corrupting binaries.

Run from project root. Backups are created with .bak extension before modification.
"""
from pathlib import Path
import sys
import shutil

TEXT_EXTS = {
    '.py', '.ts', '.js', '.tsx', '.jsx', '.html', '.htm', '.css', '.md', '.json', '.txt'
}

EXCLUDE_DIRS = {'.git', 'node_modules', 'venv', '.venv', 'dist', 'build', 'frontend/node_modules'}

root = Path(__file__).resolve().parents[1]
print('Project root:', root)

def should_process(path: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return False
    if path.is_dir():
        return False
    ext = path.suffix.lower()
    return ext in TEXT_EXTS


def remove_comments_from_line(line: str):

    if line.startswith('#!'):
        return line

    res = []
    i = 0
    n = len(line)
    in_single = False
    in_double = False
    in_back = False
    while i < n:
        ch = line[i]

        if ch == "'" and not in_double and not in_back:
            in_single = not in_single
            res.append(ch)
            i += 1
            continue
        if ch == '"' and not in_single and not in_back:
            in_double = not in_double
            res.append(ch)
            i += 1
            continue
        if ch == '`' and not in_single and not in_double:
            in_back = not in_back
            res.append(ch)
            i += 1
            continue


        if ch == '/' and not in_single and not in_double and not in_back and i+1 < n and line[i+1] == '/':

            prev = line[max(0, i-6):i]
            if 'http:' in prev or 'https:' in prev:

                res.append('//')
                i += 2
                continue

            break


        if ch == '#' and not in_single and not in_double and not in_back:

            break

        res.append(ch)
        i += 1

    out = ''.join(res).rstrip()

    if line.endswith('\n'):
        out += '\n'
    else:
        out = out
    return out


changed_files = []
for path in root.rglob('*'):
    try:
        if not should_process(path):
            continue
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    lines = text.splitlines(keepends=True)
    new_lines = []
    changed = False
    for line in lines:
        new_line = remove_comments_from_line(line)
        if new_line != line:
            changed = True
        new_lines.append(new_line)
    if changed:
        bak = path.with_suffix(path.suffix + '.bak')
        try:
            shutil.copy2(path, bak)
        except Exception:
            pass
        path.write_text(''.join(new_lines), encoding='utf-8')
        changed_files.append(str(path.relative_to(root)))

print('Modified files count:', len(changed_files))
for f in changed_files[:200]:
    print(f)

if len(changed_files) == 0:
    print('No files changed.')
else:
    print('Backups created with .bak extension for modified files.')
