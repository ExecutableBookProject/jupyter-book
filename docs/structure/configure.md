(structure/configure)=
# Configuration options for the table of contents

This page covers some of the options you have available to control your book's behavior via the Table of Contents.

:::{seealso}
For an overview of the configuration structure for the Table of Contents, see [](toc/configuration-structure)
:::

## Add captions to parts

To add a caption to a Part (so that it shows up in the sidebar, for example) use the `caption:` option like so:

```
- caption: My part name
  chapters:
  - file: chapter1
  ...
```

## Specify alternate titles

If you'd like to specify an alternate title from the one defined within a file,
you may do so with the `title:` key. For example:

```yaml
- file: path/to/myfile
  title: My alternate page title
```

Note that this only applies to the sidebar
in the table of contents, it does not change the actual chapter/section title.

(toc/numbering)=
## Number your chapters and sections

You can automatically add numbers to each chapter of your book.
To add numbers to **all chapters of your book**, add the `numbered: true` flag to your book's defaults, like so:

```yaml
format: jb-book
root: intro
defaults:
  numbered: true
chapters:
  - file: chapter1
  - file: chapter2
```

Numbers will follow a hierarchy according to the structure defined in your `_toc.yml` file.

:::{admonition} Limit the depth of numbering
If you'd like to limit the depth of numbering, use an **integer** for the `numbered` flag.
This will be the depth of sub-sections to continue numbering.
For example, `numbered: 3`.
:::

If you'd like to number **subsets of chapters**, group them into parts and
apply the `numbered: true` flag to the parts whose chapters you wish to be numbered.

For example:

```yaml
format: jb-book
root: intro
parts:
- caption: Part 1
  numbered: true  # Only part 1 will be numbered
  chapters:
  - file: part1/chapter1
- caption: Part 2
  chapters:
  - file: part2/chapter1
```

:::{admonition} A few caveats about numbering
Jupyter Book relies on {term}`Sphinx` to apply section numbering, and this has a
few quirks to it. Here are a few gotchas:

* **Numbering applies to _sections_ of your page**.
  Note that when you add numbering to a section, it will add numbers to *each header
  in a file*. This means that if you have headers in a top-level section, then its
  headers will become numbered as sub-sections, and any other _files_ underneath it
  will begin as third-level children. See [](toc/structure) for more information.
* **Numbering resets across parts**.
  If you specify groups of sections via `- part:` entries, then numbering will restart between
  them. That means if you have two `- part:` entries with 2 pages each, you will
  have two sets of `1.` and `2.` sections, one for each part.
:::

## Add a table of contents to a page's content

If you'd like to add a table of contents for the sub-sections of a page
*within the page content* (in-line with the content on the page), you
may do so by using the `{tableofcontents}` directive. You can use it like so:

````md
```{tableofcontents}
```
````

See the source of [the content types page](../file-types/index.md) for an example.

### Control the depth of the displayed Table of Contents

To control the maximum depth of the Table of Contents that you insert, use the `maxdepth:` option in your `_toc.yml` file. For example:

```
- caption: My part name
  maxdepth: 2  # The displayed Table of Contents will only have two levels
  chapters:
  - file: chapter1
  ...
```
