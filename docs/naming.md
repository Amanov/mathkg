# Material file names

New files use one pattern and one folder.

- Folder: `apps/resources/bundled_files/`
- Name: `N-klass-kebab-type.ext`

`N` is the grade in the 12-year programme. `type` is the material kind
(`sabak`, `ish-barak`, `labirint`, `jooptor`, and so on). Example:
`6-klass-maalymat-diagramma-orto-maani-sabak.pptx`.

Do not put new files in `media/` or `static_cdn/`. Those trees are the
older copies. A topic page still finds a material by the exact
`Resource.title`, which is the filename.

## Live files stay under their current names

Do not rename or delete a file that is already on the site, and do not
replace one file with another because the bytes match. A spelling
difference is recorded in `docs/filename-aliases.csv` instead.

The only spelling fixes in that table are:

| Live spelling | Canonical spelling |
| --- | --- |
| `Labirinth` | `Labirint` |
| `JoopTorchosu` | `Jooptor` |
| `Ekvivalenettuuluk` | `Ekvivalenttuuluk` |

`apps/resources/filenames.py` applies those three pairs. A page that
asks for either spelling receives the resource that exists. The file
on disk is not moved.
