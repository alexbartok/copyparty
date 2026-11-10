#!/usr/bin/env python3
"""Show what an upstream update means for the boring fork. Changes nothing.

usage: scripts/boring/sync-check.py [UPSTREAM_REF] [--base REF]

UPSTREAM_REF  what to merge next (default: upstream/hovudstraum)
--base REF    compare from here (default: the merge base of HEAD and UPSTREAM_REF)

It lists:
  1. English texts that upstream added or changed (they need plain wording)
  2. emoji in lines that upstream added to the web files (they need an icon or a word)
  3. the upstream theme count (the plain theme uses the numbers 10 and 11)
  4. the files where a merge can conflict with this fork
"""
import re
import subprocess
import sys

WEB = "copyparty/web/"
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF☀-➿⬀-⯿←-⇿⌀-⏿■-◿]"
)


def git(*args):
    return subprocess.run(
        ("git",) + args, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout


def eng_table(ref):
    """key -> source text of the English table in browser.js at ref"""
    src = git("show", "%s:%sbrowser.js" % (ref, WEB))
    ret = {}
    inside = False
    for ln in src.split("\n"):
        if not inside:
            inside = "Ls.eng = {" in ln
            continue
        if ln.rstrip() == "\t};":
            break
        m = re.match(r'^\t\t"([A-Za-z0-9_]+)": (.*?),?\s*(//.*)?$', ln)
        if m:
            ret[m.group(1)] = m.group(2)
    return ret


def main():
    args = sys.argv[1:]
    base = None
    if "--base" in args:
        i = args.index("--base")
        base = args[i + 1]
        del args[i : i + 2]

    up = args[0] if args else "upstream/hovudstraum"
    if not base:
        base = git("merge-base", "HEAD", up).strip()

    n = git("rev-list", "--count", "%s..%s" % (base, up)).strip()
    print("upstream %s is %s commits ahead of %s\n" % (up, n, base[:10]))
    if n == "0":
        print("nothing to merge")
        return

    old, new, mine = eng_table(base), eng_table(up), eng_table("HEAD")
    added = [k for k in new if k not in old]
    changed = [k for k in new if k in old and new[k] != old[k]]
    gone = [k for k in old if k not in new]
    print("1. English texts: %d added, %d changed, %d removed" % (len(added), len(changed), len(gone)))
    for k in added:
        print("  + %s: %s" % (k, new[k][:160]))
    for k in changed:
        print("  ~ %s\n      upstream now: %s\n      this fork:    %s" % (k, new[k][:160], mine.get(k, "(missing)")[:160]))
    for k in gone:
        print("  - %s" % (k,))

    print("\n2. emoji in lines that upstream added to the web files")
    diff = git("diff", "-U0", base, up, "--", WEB + "*.js", WEB + "*.html", ":!" + WEB + "tl")
    fn = ""
    hits = 0
    for ln in diff.split("\n"):
        if ln.startswith("+++ "):
            fn = ln[6:]
        elif ln.startswith("+") and EMOJI.search(ln):
            hits += 1
            print("  %s: %s" % (fn, ln[1:].strip()[:150]))
    if not hits:
        print("  none")

    src = git("show", "%s:copyparty/__main__.py" % (up,))
    m = re.search(r"^\s+THEMES = (\d+)", src, re.M)
    themes = m.group(1) if m else "?"
    print("\n3. upstream theme count: %s" % (themes,))
    if themes != "10":
        print("  WARNING: upstream added a theme. The plain theme uses the numbers 10 and 11")
        print("  and the css class f; move it (docs/boring/MAINTAINING.md, section Themes).")

    print("\n4. files changed on both sides (a merge can conflict here)")
    theirs = set(git("diff", "--name-only", base, up).split("\n")) - {""}
    mb = git("merge-base", "HEAD", up).strip()
    ours = set(git("diff", "--name-only", mb, "HEAD").split("\n"))
    both = sorted(theirs & ours)
    for f in both:
        print("  " + f)
    if not both:
        print("  none")


if __name__ == "__main__":
    main()
