"""Spelling aliases for live material filenames.

Topic pages look a file up by its exact Resource title. Live files are
not renamed. A title that differs only by one of the three known
spellings still resolves to the file that is on disk.

New files do not use these aliases. They are named
``N-klass-kebab-type.ext`` and stored in ``apps/resources/bundled_files``.
See ``docs/naming.md``.
"""

from __future__ import annotations


def canonical_filename(name):
    """Preferred spelling of an existing filename. The bytes stay put."""
    if not name:
        return name
    name = name.replace('Labirinth', 'Labirint').replace('labirinth', 'labirint')
    name = name.replace('JoopTorchosu', 'Jooptor').replace('joopTorchosu', 'jooptor')
    name = name.replace('Ekvivalenettuuluk', 'Ekvivalenttuuluk').replace(
        'ekvivalenettuuluk', 'ekvivalenttuuluk',
    )
    return name


def filename_variants(name):
    """The live title and the other spelling of the same file."""
    if not name:
        return []
    found = [name]
    pairs = (
        ('Labirinth', 'Labirint'),
        ('labirinth', 'labirint'),
        ('JoopTorchosu', 'Jooptor'),
        ('joopTorchosu', 'jooptor'),
        ('Ekvivalenettuuluk', 'Ekvivalenttuuluk'),
        ('ekvivalenettuuluk', 'ekvivalenttuuluk'),
    )
    for wrong, right in pairs:
        if wrong in name and right not in name.replace(wrong, ''):
            found.append(name.replace(wrong, right))
        elif right in name and wrong not in name:
            found.append(name.replace(right, wrong))
    # unique, stable
    out = []
    for item in found:
        if item not in out:
            out.append(item)
    return out


def resource_for_title(resources, title):
    """The active resource for this title, or for its spelling alias."""
    if not title:
        return None
    found = resources.get(title)
    if found is not None:
        return found
    for other in filename_variants(title):
        found = resources.get(other)
        if found is not None:
            return found
    return None
