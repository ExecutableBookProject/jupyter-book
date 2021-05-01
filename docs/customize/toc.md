# Structure your book with the Table of Contents

There are many ways in which you can control the table of contents for
your book. Most of them involve adding syntax to your `_toc.yml` file.

This page covers a few common options.

```{note}
The {download}`_toc.yml file for this site <../_toc.yml>` has an entry for each
of the features described below for reference.
```

## General TOC structure

The table of contents is broadly organized like so:

* The first entry of your `_toc.yml` file is the *introduction* to your book.
  It is the landing page for the HTML of your book.
* Subsequent entries define either **parts** or **chapters** in your book.
  These make up the main structure of your book. See [](toc/chapters-parts)
  for more information.
* Each chapter can optionally have **sections** that are defined by separate
  files. These are nested underneath the top page of the chapter. See [](toc/structure)
  for more information.
* Throughout the `_toc.yml` file, `- file:` entries point to text files that make up
  your book's content. Their paths are relative to the book's root.

```{note}
By default, the landing page of your book will appear in the navbar, but this can be disabled in your `_config.yml` file by setting the `home_page_in_navbar` option to `false` (under the [html section](https://jupyterbook.org/customize/config.html#configuration-reference)).
```

```{note}
Currently, it is not possible to add nested sections to your landing page (see [#844](https://github.com/executablebooks/jupyter-book/issues/844))
```

For reference, here is an example similar to this book's `_toc.yml` file:

```yaml
- file: myintro
  numbered: true

- part: Get started
  chapters:
  - file: start/overview
  - file: start/build

- part: Reference and test pages
  chapters:
  - file: test_pages/test
    sections:
      - file: test_pages/layout_elements
      - file: test_pages/equations
```

The sections below cover this information in more depth.

(toc/chapters-parts)=
## Defining chapters and parts in `_toc.yml`

The top layer of entries in your table of contents allows you to define
**chapters** and (optionally) **parts** of your book.

The first entry (`- file: myintro` above) defines the introductory page for your book.
It is also where you can control some behavior for the entire book (in the example
above, we set `numbered: true` to number *all* sections of the book).

Below the first entry you have two options for defining the structure of your book:

1. **A list of chapters.** You can specify each chapter with a `- file:` entry.
   Below is an example `_toc.yml` file with this structure:

   ```yaml
   - file: myintro

   - file: firstchapter
   - file: secondchapter
   ```

2. **A list of parts with chapters.** If you'd like to separate chapters into groups,
   do so by using `- part:` entries in the top level of `_toc.yml`. Each part should have
   a `chapters:` section that contains a list of `- file:` entries, each one pointing
   to the file for a chapter. Below is an example `_toc.yml` file with
   this structure:

   ```yaml
   - file: myintro

   - part: My first part
     chapters:
     - file: part1_firstchapter
     - file: part1_secondchapter
   - part: My second part
     chapters:
     - file: part2_firstchapter
   ```

   Note that **chapters do not continue between parts**. Think of each part as
   a self-contained collection of chapters (e.g., for the purposes of numbering).

:::{admonition} Don't mix these two structures!
:class: warning
When designing the top-level sections of your `_toc.yml` file, you must
pick *either* a list of chapters via `- file:` entries, or a list of parts
via `- part:` entries with chapters inside of them. You cannot intermix them both.
:::

(toc/files)=
### Files

**Files** point to a single file of content in your book's folder. If these files
are at the top level of your `_toc.yml` file, they will denote **chapters**. If they
are nested within another file (via the `sections:` key) then they will denote
**sections** within a chapter.

Here is an example file entry:

```yaml
- file: path/to/myfile
```

Additionally, **files can have nested sections in other files**. These subsections allow you
to define hierarchical structure in your book. For example, you may wish for the top-level
file to serve as an "introduction" for a collection of files underneath, like so:

```yaml
- file: my_intro
  sections:
    - file: my_first_page
    - file: my_second_page
      sections:
        - file: my_second_page_subsection
```

We recommend nesting your sections no more than 3 layers deep (as shown above).

#### Specifying alternate titles

If you'd like to specify an alternate title from the one defined within a file,
you may do so with the `title:` key. For example:

```yaml
- file: path/to/myfile
  title: My alternate page title
```

Note that this only applies to the sidebar
in the table of contents, it does not change the actual chapter/section title.

(toc/numbering)=
## Number your book's chapters and sections

You can automatically add numbers to each chapter of your book. To add numbers
to **all chapters of your book**, add the `numbered: true` flag to
your introduction page entry (the first entry in `_toc.yml`). For example:

```yaml
- file: intro
  numbered: true

- file: chapter1
- file: chapter2
- file: chapter3
```

This will cause all chapters of the book to be
numbered. They will follow a hierarchy according to the sub-sections structure
defined in your `_toc.yml` file.
You can also **limit the TOC numbering depth** by setting the `numbered` flag to an integer instead of `true`, e.g., `numbered: 3`.

By default, chapter numbering between parts will continue (it will not re-start at `1.` each time) using an extension called [sphinx-multitoc-numbering](https://github.com/executablebooks/sphinx-multitoc-numbering). To **restart chapter numbering between parts**, use the following setting in your `_config.yml` file:

```yaml
use_multitoc_numbering: false
```

If you'd like to number **subsets of chapters**, group them into parts and
apply the `numbered: true` flag to the parts whose chapters you wish to be numbered.
For example:

```yaml
- file: home

# Chapters in this part will not be numbered
- part: Introduction
  chapters:
  - file: page2

# Chapters in this part will be numbered
- part: Part 1
  numbered: true
  chapters:
  - file: chapter1
  - file: chapter2
```

### Numbering caveats and notes

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

(toc/structure)=
## How headers and sections map onto to book structure

Jupyter Book uses the {term}`Sphinx` documentation engine under the hood, which
represents the structure of your book in a particular way. Different choices
for the structure of `_toc.yml` and the header structures within your pages will
result in different outcomes for your overall book structure. Here are some general
tips and best-practices.

```{note}
This is particularly important when you [number your book's sections](toc/numbering)
or when you [build a PDF of your book through Latex](pdf:latex).
```

**Chapters are at the top of your book hierarchy**. The top level of your `_toc.yml` contains
a list of chapters. The title of each file will be the chapter's title.

**Headers map onto sections**. Jupyter Book interprets your book as a collection of sections,
and decides how those sections should be nested according to the hierarchy of
`_toc.yml` and the hierarchy of headers in a page. Within a file, the first
`## ` header it discovers will define the top-most section in the file, and any subsequent
`### ` headers underneath will become sub-sections (until another `## ` section
is encountered). This behavior is a bit different if the page is *nested* under
another (see below).

**Nested files define sections _underneath_ the last section of their parent**.
If you specify sections that are *nested* under a file (with the `sections:` key)
then those sections will begin *underneath* the last headers of the parent page.

For example, if your `_toc.yml` file looks like this:

```yaml
- file: myintro

- file: chapter1
  sections:
  - file: chapter1section
```

Then the sections of `chapter1section` will begin **under** the sections of `chapter1`.
Any headers in `chapter1section` will be treated as a "next-header-deeper" section in
`chapter1`.

In other words, if `chapter1` and `chapter1section` look like this:

````{panels}
`chapter1.md`
^^^^^^^^^^^^^
```md
# Chapter 1 title

## Chapter 1 second header
```
---
`chapter1section.md`
^^^^^^^^^^^^^^^^^^^^

```md
# Chapter 1 section title

## Chapter 1 section second header
```
````
Then your book will treat them like so:

```md
# Chapter 1 title

## Chapter 1 second header

### Chapter 1 section title

#### Chapter 1 section second header
```

However, if `chapter1.md` had an extra third-level header, like so:

````{panels}
`chapter1.md`
^^^^^^^^^^^^^
```md
# Chapter 1 title

## Chapter 1 second header

### Chapter 1 third header
```
---
`chapter1section.md`
^^^^^^^^^^^^^^^^^^^^

```md
# Chapter 1 section title

## Chapter 1 section second header
```
````

Then your book would treat them like so:

```md
# Chapter 1 title

## Chapter 1 second header

### Chapter 1 third header

#### Chapter 1 section title

##### Chapter 1 section second header
```

Keep this in mind when you design the structure of your files.

```{tip}
A good rule of thumb is to take one of these two approaches:

1. **don't put headers in your introduction pages**. This is
   true for both the book's introduction, as well as for any chapter introductions.
   Instead, leave the headers to pages that have more content in them, and use
   **bolded text** where you would otherwise use headers.
2. **Use a flat list of files instead of nested files**. This way the section
   hierarchy is defined only in a single file within each section. However, this
   means you will have longer files in general.
```

## Exclude some pages from your book's build

By default, Jupyter Book will build all content files that are found in your book's
folder, even if they are not specified in `_toc.yml` (and will raise a warning if
it finds a file that isn't listed there).

If you'd like Jupyter Book to skip a file entirely, you can do so with the following
configuration in `_config.yml`:

```yaml
exclude_patterns: [pattern1/*, path/to/myfile.ipynb]
```

Any files that match the patterns described there will be excluded from the build.
If you'd like to exclude files from being *executed* but still wish for them to be
built by Jupyter Book, see [](execute/exclude).

## Web-based navigation bar functionality

The following sections apply to controlling the left navigation bar in
HTML books built with Jupyter Book.

### Add external links

You can also add external links to websites that are outside of your book.
To do so, use the following pattern:

```yaml
- url: https://yoururl.com
```

The URL will be placed alongside the links to other pages above and below the
entry.

### Add a table of contents to a page's content

If you'd like to add a table of contents for the sub-sections of a page
*within the page content* (in-line with the content on the page), you
may do so by using the `{tableofcontents}` directive. You can use it like so:

````md
```{tableofcontents}
```
````

See the source of [the content types page](../file-types/index.md) for an example.

## Automatically generate your `_toc.yml` file

You can use `jupyter-book` to *generate* a table of contents file from your book
using the filenames of your book's content. To do so, run the following command

```bash
jupyter-book toc mybookpath/
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
