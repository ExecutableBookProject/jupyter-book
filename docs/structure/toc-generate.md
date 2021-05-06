---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Generate a Table of Contents file from your book's files

You can use `jupyter-book` to *generate* a table of contents file from your book
using the filenames of your book's content. To do so, run the following command

```bash
jupyter-book toc from-site path/to/book
```

Jupyter Book will search `mybookpath/` for any [content files](../file-types/index)
and create a `_toc.yml` file out of them. There are a few considerations to keep in mind:

* Each sub-folder must have at least one content file inside it
* The ordering of files in `_toc.yml` will depend on the alphanumeric order of
  the filenames (e.g., `folder_01` comes before `folder_02`, and `apage` comes
  before `b_page`)
* If there is a file called `index.md` in any folder, it will be listed first.

You may also **generate navigation bar *titles* from each file of your book**.
If you do so, note that if the file name begins with `<integer>_filename.md`, then
the `<integer>` part will be removed before it is inserted into `_toc.yml`.

In addition, you have a few extra options for controlling how the `_toc.yml` file is generated.

```{code-cell}
:tags: [remove-input]
!jupyter-book toc from-site -h
```
