(toc/structure)=
# How headers and sections map onto to book structure

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
format: jb-book
root: myintro
chapters:
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

:::{tip}
A good rule of thumb is to take one of these two approaches:

1. **don't put headers in your introduction pages**. This is
   true for both the book's introduction, as well as for any chapter introductions.
   Instead, leave the headers to pages that have more content in them, and use
   **bolded text** where you would otherwise use headers.
2. **Use a flat list of files instead of nested files**. This way the section
   hierarchy is defined only in a single file within each section. However, this
   means you will have longer files in general.
:::
