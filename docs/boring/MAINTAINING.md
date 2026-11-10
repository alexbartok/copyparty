# Maintaining the fork

The fork changes the interface only. Keeping it current means merging upstream and giving new upstream texts and icons the plain treatment.

## Update from upstream

One-time setup:

```
git remote add upstream https://github.com/9001/copyparty
```

Each update:

1. `git fetch upstream`
2. `scripts/boring/sync-check.py` lists what the update brings: new or changed English texts, new emoji in the web files, the upstream theme count, and the files where a merge can conflict. It changes nothing.
3. `git merge upstream/hovudstraum` (or a release tag such as `v1.20.27`).
4. Resolve conflicts. In the English table of `copyparty/web/browser.js`, keep the wording of this fork unless upstream changed what the text means.
5. Reword the texts that step 2 listed. Replace the emoji that step 2 listed with an icon or a word.
6. Run the tests: `python3 -m unittest discover -s tests` (needs Jinja2).
7. Start the server and look at the file list, the grid view, the settings and one upload, in plain dark and plain light.
8. Update the version in the "Upstream" section of `README.md`.

## Where the changes are

| Change | Place |
|---|---|
| Plain theme | Blocks between `/* theme f begin */` and `/* theme f end */` at the end of `browser.css`, `ui.css`, `splash.css`, `md.css`, `md2.css`, `mde.css`, `shares.css` and `rups.css` in `copyparty/web/` |
| Theme list and default | `THEMES` and `--theme` in `copyparty/__main__.py`; the names and the order in `settheme` in `browser.js` |
| English texts | The `Ls.eng` table at the top of `browser.js`; the page templates (`*.html`); replies to the browser in `copyparty/httpcli.py` and `copyparty/authsrv.py` |
| Tabs in the panels | `optabs()` at the end of `browser.js` |
| Placeholder thumbnails | `_plain()` in `copyparty/ico.py`; the URL parameter `ico` in `httpcli.py` and `browser.js` |

The other languages (`copyparty/web/tl/`) are not changed. A text that exists only in English has a fallback in the markup, for example `(L.tab_view || 'View')`.

## Rules for texts

- Say what the control does. No jokes, no slang, no emoji as words.
- Labels in sentence case.
- Tooltips: first what the control does, then `$NHotkey: X` as the last line if there is a hotkey.
- Keep every placeholder (`{0}`, `%s`), every `$N`, the HTML, and the form `tooltip">label`.

## Icons

Icons are [Lucide](https://lucide.dev) line icons, stored as CSS variables (`--i-NAME`) and drawn as a mask in the text color.

To add one, get the SVG file from Lucide and run:

```
scripts/boring/icon.py path/to/NAME.svg
```

Put the printed line into the `html.f {` block of the stylesheet. Then give the element the icon with `--i: var(--i-NAME)`, the way `html.f #opa_srch` does in `browser.css`.

## Themes

Upstream has ten themes, numbers 0 to 9, CSS classes `a` to `e`. The plain theme is number 10 (dark) and 11 (light), CSS class `f`.

If upstream adds a theme, it takes the numbers 10 and 11 and the class `f`. `sync-check.py` warns about that. Then move the plain theme up by one: rename `html.f`, `html.fz` and `html.fy` to the next letter in the eight stylesheets and in `msg.html`, raise `THEMES` by two more, and change the default of `--theme`, the names in `settheme`, and the checks for `'f'` in `browser.js`.
