---
substitutions:
  key1: "I'm a **substitution**"
  key2: |
    ```{note}
    {{ key1 }}
    ```
  fishy: |
    ```{image} /images/fun-fish.png
    :alt: fishy
    :width: 200px
    ```
  jinja: "[Jinja templates](https://jinja.palletsprojects.com/en/2.11.x/)"
  repo_name: "jupyter-book"
  repo_url: "[my repo url](https://github.com/executablebooks/jupyter-book)"
---

# Special content blocks

A common use of directives and roles is to designate "special blocks" of your content.
This allows you to include more complex information such as warnings and notes, citations, and figures.
This section covers a few common ones.

(content-blocks:myst-extensions)=
## MyST syntax extensions

{term}`MyST Markdown` has a base syntax that it supports, and additional syntax can be enabled to add extra functionality.
By default, Jupyter Book enables a few extra syntax pieces for MyST in order to more closely resemble the Markdown experience in Jupyter Notebooks and interfaces.
These extensions are:

`dollarmath`
: To support `$$` and `$` syntax for math blocks. See [](./math.md).

`linkify`
: To auto-detect HTML-like links in your markdown and convert them to hyperlinks.

`substitution`
: To allow you to define markdown "variables" and substitute text in using them. See [](content:substitutions).

`colon_fence`
: To allow you to use `:::` fences for admonitions, in order to make them easier to render in interfaces that do not support MyST. See [](admonitions:colons).

To enable your own syntax extensions, use the following configuration pattern:

```yaml
parse:
  myst_enable_extensions:
    - extension-1
    - extension-2
```

Note that this will **override** the default Jupyter Book extension list.
You should include all of the extensions that you want to be enabled.

:::{seealso}
For a list of syntax extensions in MyST, see [the MyST documentation](https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html).
:::

(content:admonitions)=
## Notes, warnings, and other admonitions

Let's say you wish to highlight a particular block of text that exists slightly apart from the narrative of your page.
You can use the **`{note}`** directive for this.

For example, the following text:

````md
```{note}
Here is a note!
```
````

Results in the following output:

```{note}
Here is a note!
```

````{margin} A note on nesting
You can nest admonitions (and other content blocks) inside one another. For example:

:::{note}
Here's a note block inside a margin block
:::

See {ref}`markdown/nesting` for instructions to do this.
````

There are a number of similarly-styled blocks of text. For example, here is a `{warning}`
block:

`````{warning}
Here's a warning! It was created with:
````
```{warning}
```
````
`````

For a complete list of options, see [the `sphinx-book-theme` documentation](https://sphinx-book-theme.readthedocs.io/en/latest/reference/demo.html#admonitions).

### Blocks of text with custom titles

You can also choose the title of your message box by using the
**`{admonition}`** directive. For example, the following text:

````md
```{admonition} Here's your admonition
Here's the admonition content
```
````

Results in the following output:

```{admonition} Here's your admonition
Here's the admonition content
```

If you'd like to **style these blocks**, then use the `:class:` option. For
example:

`````{admonition} This admonition was styled...
:class: tip
Using the following pattern:
````
```{admonition} My title
:class: tip
My content
```
````
`````

(admonitions:colons)=
### Markdown-friendly directives with `:::`

The admonition syntax above utilises the general [directives syntax](content:myst/directives).
However, if you're using an interface that does not support {term}`MyST Markdown`, it will render as a raw literal block.
Many directives contain markdown inside, and if you'd like this markdown to render "normally", you may also use `:::` fences rather than ` ``` ` fences to define the directive. As a result, the contents of the directive will be rendered as markdown.


For example:

```md
:::{note}
This text is **standard** _Markdown_
:::
```

:::{note}
This text is **standard** _Markdown_
:::

Similar to normal directives, these admonitions can also be nested:

```md
::::{important}
:::{note}
This text is **standard** _Markdown_
:::
::::
```

::::{important}
:::{note}
This text is **standard** _Markdown_
:::
::::

:::{note}
You can use this syntax for any kind of directive, though it is generally recommended to use only with directives that contain pure markdown in their content.
:::


### Insert code cell outputs into admonitions

If you'd like to insert the outputs of running code *inside* admonition
blocks, we recommend using [`glue` functionality](content:code-outputs:glue).
For example, we'll insert one of the outputs that was glued into the book from the [code outputs page](./code-outputs.md).

The code below:

````md
```{note}
Here's my figure:
{glue:figure}`sorted_means_fig`
```
````

generates:

```{note}
Here's my figure:
{glue:}`sorted_means_fig`
```

See [](content:code-outputs:glue) for more information on how to use `glue` to insert your outputs directly into your content.

:::{tip}
To hide code input and output that generated the variable you are inserting, use the `remove_cell` tag.
See [](../interactive/hiding.md) for more information and other tag options.
:::

(content-blocks:html-admonitions)=
### HTML admonitions

A drawback of admonition syntax is that it will not render in interfaces that do not support this syntax (e.g., GitHub). If you'd like to use admonitions that are defined *purely with HTML*, MyST can parse them via the `html_admonitions` extension. To use it, first enable it with the following configuration:

```yaml
parse:
  myst_enable_extensions:
    # don't forget to list any other extensions you want enabled,
    # including those that are enabled by default!
    - html_admonition
```

Then, you may define admonitions in your book like so:

:::{tabbed} Markdown Input
```html
<div class="admonition note" name="html-admonition" style="background: lightgreen; padding: 10px">
<p class="title">This is the **title**</p>
This is the *content*
</div>
```
:::

:::{tabbed} Rendered Output
<div class="admonition note" name="html-admonition" style="background: lightgreen; padding: 10px">
<p class="title">This is the **title**</p>
This is the *content*
</div>
:::

See [](myst-parser:syntax/html-admonition) for more information about HTML admonitions.

(content/panels)=
## Panels

Panels provide an easy way for you to organize chunks of content into flexible containers on your page.
They are useful for creating card-like layouts, flexible columns, and grids.
Panels are based off of [Bootstrap CSS](https://getbootstrap.com/docs/4.5/components/card/), and utilize Bootstrap's classes to control the look and feel of panels.

Here is an example that creates two panels:

`````
````{panels}
Panel header 1
^^^
Panel body 1
+++
Panel footer 1
---

Panel header 2
^^^
Panel body 2
+++
Panel footer 2
````
`````

- `---` separates each panel
- `^^^` defines the panel header
- `+++` defines the panel footer

```{note}
Panel headers and footers are optional.
If you don't include `^^^` or `+++` in your panel, they will not show up.
```

You can embed all kinds of content inside of panels. For example, the following panels:

````{panels}
Content of the left panel.

{badge}`example-badge,badge-primary`

---

```{link-button} content/panels
:text: Clickable right panel
:type: ref
:classes: stretched-link
```
````

were created with:


`````md
````{panels}
Content of the left panel.

{badge}`example-badge,badge-primary`

---

```{link-button} content/panels
:text: Clickable right panel
:type: ref
:classes: stretched-link
```

````
`````

```{seealso}
See the [Sphinx Panels card layout documentation](https://sphinx-panels.readthedocs.io/en/latest/#card-layout) for more information.
```

### Controlling the look and feel of panels

You can control the look and feel of panels by passing attaching bootstrap classes to panel headers/body/footers.
You do this by passing configuration options to your  `{panels}` directive.

For example:


```{seealso}
See the [Panels card styling documentation](https://sphinx-panels.readthedocs.io/en/latest/#card-styling) for more information.
```

For example, you can control how many columns are in your panels by using [Bootstrap column classes](https://getbootstrap.com/docs/4.0/layout/grid/). These panels:

````{panels}
:column: col-4
:card: border-2
Header A
^^^
Body A
---
Header B
^^^
Body B
---
Header C
^^^
Body C
````

Were created by this code:

`````
````{panels}
:column: col-4
:card: border-2
Header A
^^^
Body A
---
Header B
^^^
Body B
---
Header C
^^^
Body C
````
`````


```{warning} 
Directives for styling a card must begin on the line **immediately** after the initial directive (for the first panel) and the `---` line denoting the start of a new panel.
```

These panels:

```{panels}
:column: w-75 text-justified
Lorem ipsum and other stuff. Just keep typing. Shouldn't I copy the formal lorem ipsum? Meh. Nah. Too much work.
---
:column: w-25 text-center
See: This works!
```

are created with:

````
```{panels}
:column: w-75 text-justified
Lorem ipsum and other stuff. Just keep typing. Shouldn't I copy the formal lorem ipsum? Meh. Nah. Too much work.
---
:column: w-25 text-center
See: This works!
```
````

But a slight change:

````
```{panels}
:column: w-75 text-justified
Lorem ipsum and other stuff. Just keep typing. Shouldn't I copy the formal lorem ipsum? Meh. Nah. Too much work.
---

:column: w-25 text-center
See: This breaks!!
```
````

Produces this:

```{panels}
:column: w-75 text-justified
Lorem ipsum and other stuff. Just keep typing. Shouldn't I copy the formal lorem ipsum? Meh. Nah. Too much work.
---

:column: w-25 text-center
See: This breaks!!
```

## Dropdowns

Dropdowns allows you to hide content behind a title and a button.
There are two kinds of dropdowns in Jupyter Book:

### The `{dropdown}` directive

Use the `{dropdown}` directive to create a clickable dropdown with a title.

For example:

`````{panels}
source
^^^
````
```{dropdown} Here's my dropdown
And here's my dropdown content
```
````
---
result
^^^
```{dropdown} Here's my dropdown
And here's my dropdown content
```
`````

(content/toggle-admonitions)=
### Dropdown admonitions

You can also hide the body of your admonition blocks so that users must click a button to reveal their content.
This is helpful if you'd like to include some text that isn't immediately visible to the user.

To turn an admonition into a dropdown, add the `dropdown` class to them. For example:

`````{panels}
source
^^^
````md
```{note}
:class: dropdown
The note body will be hidden!
```
````
---
result
^^^
```{note}
:class: dropdown
The note body will be hidden!
```
`````

You can use this in conjunction with `{admonition}` directives to include your
own titles and stylings. For example:

`````{panels}
source
^^^
````md
:::{admonition} Click here!
:class: tip, dropdown
Here's what's inside!
:::
````
---
result
^^^
:::{admonition} Click here!
:class: tip, dropdown
Here's what's inside!
:::
`````

:::{important}
Admonition dropdowns require JavaScript to be enabled on the browser which they are viewed.
By contrast, the [dropdown directive](content/panels) below works purely *via* HTML+CSS.
:::


(content/definition-lists)=

## Definition lists

Definition lists are enabled by defining the following setting in your `_config.yml`:

```yaml
parse:
  myst_enable_extensions:
    # don't forget to list any other extensions you want enabled,
    # including those that are enabled by default!
    - deflist
```

Definition lists utilise the [markdown-it-py deflist plugin](https://markdown-it-py.readthedocs.io/en/latest/plugins.html), which itself is based on the [Pandoc definition list specification](http://johnmacfarlane.net/pandoc/README.html#definition-lists).

Here's an example:

````{panels}
source
^^^
```md
Term 1
: Definition

Term 2
: Definition
```
---
result
^^^
Term 1
: Definition

Term 2
: Definition
````

From the [Pandoc documentation](https://pandoc.org/MANUAL.html#definition-lists):

> Each term must fit on one line, which may optionally be followed by a blank line, and must be followed by one or more definitions.
> A definition begins with a colon or tilde, which may be indented one or two spaces.
>
> A term may have multiple definitions, and each definition may consist of one or more block elements (paragraphs, code blocks, lists, etc.)

Here is a more complex example, demonstrating some of these features:

Term *with Markdown*
: Definition [with reference](content/definition-lists)

  A second paragraph
: A second definition

Term 2
  ~ Definition 2a
  ~ Definition 2b

Term 3
:     A code block
: > A quote
: A final definition, that can even include images:

  <img src="../images/fun-fish.png" alt="fishy" width="200px">

This was created with the following Markdown:

```md
Term *with Markdown*
: Definition [with reference](ontent/definition-lists)

  A second paragraph

Term 2
  ~ Definition 2a
  ~ Definition 2b

Term 3
:     A code block

: > A quote

: A final definition, that can even include images:

  <img src="../images/fun-fish.png" alt="fishy" width="200px">
```

## Quotations and epigraphs

Quotations and epigraphs provide ways to highlight information given by others.

### Quotations

**Regular quotations** are controlled with standard Markdown syntax, i.e., by
inserting a caret (`>`) symbol in front of one or more lines of text. For example:

````{panels}
source
^^^
```md
> Here is a cool quotation.
>
> From me, Jo the Jovyan
```
---
result
^^^
> Here is a cool quotation.
>
> From me, Jo the Jovyan
````

### Epigraphs

**Epigraphs** draw more attention to a quote and highlight its author. You should
keep these relatively short so that they don't take up too much vertical space. Here's
how an epigraph looks:

`````{panels}
source
^^^
````md
```{epigraph}
Here is a cool quotation.

From me, Jo the Jovyan
```
````
---
result
^^^
```{epigraph}
Here is a cool quotation.

From me, Jo the Jovyan
```
`````

You can provide an **attribution** to an epigraph by adding `--` to the final line, followed by the quote author. For example:

`````{panels}
source
^^^
````md
```{epigraph}
Here is a cool quotation.

-- Jo the Jovyan
```
````
---
result
^^^
```{epigraph}
Here is a cool quotation.

-- Jo the Jovyan
```
`````

## Glossaries

Glossaries allow you to define terms in a glossary so you can then link back to it
throughout your content. You can create a glossary with the following
syntax:

````md
```{glossary}
Term one
  An indented explanation of term 1

A second term
  An indented explanation of term2
```
````

which creates:

```{glossary}
Term one
  An indented explanation of term 1

A second term
  An indented explanation of term2
```

To reference terms in your glossary, use the `{term}` role. For example,
`` {term}`Term one` `` becomes {term}`Term one` and `` {term}`A second term` ``
becomes {term}`A second term`.

(content:tabs)=
## Tabbed content

You can also use [`sphinx-panels`](sphinx-panels:panels/usage) to produce [**tabbed content**](sphinx-panels:components-tabbed).
This allows you to display a variety of tabbed content blocks that users can click on.

For example, here's a group of tabs showing off code in a few different languages:

````{tabbed} c++

```{code-block} c++

int main(const int argc, const char **argv) {
  return 0;
}
```
````

````{tabbed} python

```{code-block} python

def main():
    return
```
````

````{tabbed} java

```{code-block} java

class Main {
    public static void main(String[] args) {
    }
}
```
````

````{tabbed} julia

```{code-block} julia

function main()
end
```
````

````{tabbed} fortran

```{code-block} fortran

PROGRAM main
END PROGRAM main
```
````

You can use this functionality with the `{tabbed}` directive. You can provide a sequence of `{tabbed}` directives, and each one will be used to generate a new tab (unless the `:new-group:` option is added to a `{tabbed}` directive.)

For example, the following code:

````
```{tabbed} Tab 1 title
My first tab
```

```{tabbed} Tab 2 title
My second tab with `some code`!
```
````

produces

```{tabbed} Tab 1 title
My first tab
```

```{tabbed} Tab 2 title
My second tab with `some code`!
```

**Insert code outputs in your tabs** with the [`glue` functionality](glue/gluing).

For example, the following tabs use this functionality to glue images and tables generated somewhere else in these docs:

````{tabbed} A histogram
```{glue:figure} boot_fig
:figwidth: 300px
:name: "fig-boot-tab"

This is a **caption**, with an embedded `{glue:text}` element: {glue:text}`boot_mean:.2f`!
```
````
````{tabbed} A table
```{glue:figure} df_tbl
:figwidth: 300px
:name: "tbl:df-tab"

A caption for a pandas table.
```
````
``````{tabbed} Code to generate this
`````
````{tabbed} A histogram
```{glue:figure} boot_fig
:figwidth: 300px
:name: "fig-boot-tab"

This is a **caption**, with an embedded `{glue:text}` element: {glue:text}`boot_mean:.2f`!
```
````

````{tabbed} A table
```{glue:figure} df_tbl
:figwidth: 300px
:name: "tbl:df-tab"

A caption for a pandas table.
```
````

````{tabbed} Code to generate this
`{ code block here }`
````
`````
``````

See the [`sphinx-panels` tabbed](sphinx-panels:components-tabbed) documentation for more information on how to use this.

(content:substitutions)=
## Substitutions and variables in markdown

Substitutions allow you to define **variables** in the front-matter of your page, and then **insert** those variables into your content throughout.

To use a substitution, first add front-matter content to the top of a page like so:

````yaml
---
substitutions:
  key1: "I'm a **substitution**"
  key2: |
    ```{note}
    {{ key1 }}
    ```
  fishy: |
    ```{image} img/fun-fish.png
    :alt: fishy
    :width: 200px
    ```
---
````

You can use these substitutions inline or as blocks, and you can even nest substitutions in other substitutions (but circular references are prohibited):

:::{tabbed} Markdown Input

```md
Inline: {{ key1 }}

Block level:

{{ key2 }}

```
:::

:::{tabbed} Rendered Output
Inline: {{ key1 }}

Block level:

{{ key2 }}
:::

You can also insert substitutions inside of other markdown structures like tables:

:::{tabbed} Markdown Input

```md
| col1     | col2      |
| -------- | --------- |
| {{key2}} | {{fishy}} |
```
:::

:::{tabbed} Rendered Output
| col1     | col2      |
| -------- | --------- |
| {{key2}} | {{fishy}} |
:::

:::{seealso}
For more information about Substitutions, see [](myst-parser:syntax/substitutions).
:::

### Define substitutions for your whole book

You can also define book-level substitution variables with the following configuration:

```yaml
parse:
  myst_substitutions:
    key: value
```

These substitutions will be available throughout your book. For example, the global substitution key `my-global-substitution` is defined in this book's `_config.yml` file, and it produces: {{ sub3 }}.

### Formatting substitutions

MyST substitutions use {{ jinja }} in order to substite in key / values. This means that you can apply any standard Jinja formatting to your substitutions. For example, you can **replace text in your substitutions** like so:

:::{tabbed} Markdown Input

```md
The original key1: {{ key1 }}

{{ key1 | replace("a substitution", "the best substitution")}}
```
:::

:::{tabbed} Rendered Output
The original key1: {{ key1 }}

{{ key1 | replace("a **substitution**", "**the best substitution**")}}
:::

### Using substitutions in links

If you'd like to use substitutions to insert and modify **links** in your book, here are two options to explore:

1. **Define the entire markdown link as a variable**. For example:

   :::{tabbed} Markdown Input

   ```yaml
   substitutions:
     repo_url: [my repo url](https://github.com/executablebooks/jupyter-book)
   ```
   ```md
   Here's my link: {{ repo_url }}
   ```
   :::

   :::{tabbed} Rendered Output
   Here's my link: {{ repo_url }}
   :::
2. Use Jinja features to insert the variable.
   Because substitutions use {{ jinja }}, you also have access to **Python formatting** operations in your substitution.
   For example:

   :::{tabbed} Markdown Input

   ```yaml
   substitutions:
     repo_name: jupyter-book
   ```
   ```md
   Here's my link: {{ '[my repo: `{repo}`](https://github.com/executablebooks/{repo})'.format(repo=repo_name) }}
   ```
   :::

   :::{tabbed} Rendered Output
   Here's my link: {{ '[my repo: `{repo}`](https://github.com/executablebooks/{repo})'.format(repo=repo_name) }}
   :::

## Citations and cross-references

You can add citations and cross-references to your book. See
{doc}`citations` for more information on how to do this.

## Figures

You can thoroughly customise the look of figures in your book. See {doc}`figures` for
more information.

## Page layout and sidebar content

You can also use MyST to control various aspects of the page layout. For more
information on this, see {doc}`layout`.

## Footnotes

You can include footnotes in your book using standard Markdown syntax.
This will include a numbered reference to the footnote in-line, and append the footnote
to a list of footnotes at the bottom of the page.

To create a footnote, first insert a reference in-line with this syntax: `[^mylabel]`.
Then, define the text for that label like so:

```md
[^mylabel]: My footnote text.
```

You can define `[^mylabel]` anywhere in the page, though its definition will always
be placed at the bottom of your built page. For example, here's a footnote [^mynote]
and here's another one [^mynote2]. You can click either of them to see the footnotes
at the bottom of this page.

[^mynote]: Here's the text of my first note.
[^mynote2]: And the text of my second note.
            Note that
            [you can include Markdown footnote definitions](https://executablebooks.org).

(custom-div-blocks)=
## Custom `<div>` blocks

You can add custom `div` blocks along with whatever classes you'd like using
the `{div}` directive. The `{div}` directive will wrap everything inside in a single `<div>` with the classes you provide. For example:

````md
```{div} my-class
**Some content.**
```
````

Will result in the following HTML when your book is built:

```html
<div class="my-class">
  <strong>Some content.</strong>
</div>
```

This can be useful if you'd like to style your book with [custom CSS or JavaScript](custom-assets).
