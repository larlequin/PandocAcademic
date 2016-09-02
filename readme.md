# Pandoc Academic Plugin for Sublime Text 2/3 #

A [Sublime Text 2/3](http://www.sublimetext.com/2) plugin to handle [Pandoc](http://johnmacfarlane.net/pandoc/).
The plugin proposes:

- a syntax highlighting tool associated with two dark color themes,
- different snippets to quickly add Pandoc functions
- a conversion tool to transform a Pandoc file to HTML, DocX, PDF and Beamer documents.

Based on the [Pandoc Render plugin](https://github.com/jclement/SublimePandoc).


## Version ##

Plugin version: v1.1 -- Automatically launch the file-associated program after the compilation.

Plugin version: v1.2 -- Add the grid table module and the LaTeX class option.

Plugin version: v1.3 -- Convert the script to run on Python 3 / Sublime Text 3


## Installation ##

The easiest way to install the package is to use the [package control manager](http://wbond.net/sublime_packages/package_control).
Go to Preferences > Package Control > Install Package and search for "Pandoc Academic".

You can also install the plugin manually. Download the latest version from Github and copy the folder into your Sublime Text 2 Packages folder.
(for instance in Linux: ~/.config/sublime-text-2/Packages).

~~~~~~~~~~~~~ {#mycode .sh}
$ git clone git://github.com/larlequin/Pandoc-Academic-Plugin.git
~~~~~~~~~~~~~~~~~~~~~~


## Dependencies ##

You need to have a working installation of [Pandoc](http://johnmacfarlane.net/pandoc/), version 1.9.4.2 or higher.


## Available Commands ##

### Syntax and color scheme ###

You can select the syntax for a markdown file (Pandoc) in the Menu: View > Syntax > Pandoc.
This syntax should be selected to make the conversion menu available.

The compatible color schemes are available in the Menu: Preferences > Color Scheme > Pandoc Academic > ColorScheme.

### Conversion ###

Conversions are available in the Menu: Tools > Pandoc Academic > Pandoc Convert (only if Pandoc is defined as syntax).
You can convert a Pandoc file to:

- HTML
- DocX
- PDF (via LaTeX, see Pandoc documentation)
- Beamer (via LaTeX, see Pandoc documentation)

You can also use key shortcuts to launch the conversions:

- HTML    >   *CTL+ALT+h*
- DocX    >   *CTL+ALT+d*
- Beamer  >   *CTL+ALT+b*
- PDF     >   *CTL+SHIFT+ALT+p*

### Snippets ###

*Generic snippets:*

- co + tabulation  = snippet to add a comment (HTML format)
- bo + tabulation  = snippet to add bold text in Pandoc/Markdown (**)
- it + tabulation  = snippet to add italic text in Pandoc/Markdown (*)
- link + tabulation= snippet to add a web link in Pandoc/Markdown

*Figures and Tables:*

- img + tabulation = snippet to add a picture in Pandoc
- tab + tabulation = snippet to add a table from a file and its title (as for an article)

*Citation/bibliography snippets:*

- ci + tabulation  = snippet to add a citation in brackets [text? @citationkey]
- bib + tabulation = add the \[\[BIB]] option to the current file

*Mathematic snippets:*

- mat + tabulation = snippet to add mathematics based on LaTeX style
- pow + tabulation = snippet to add the eta squared symbol

*Other snippets:*

- not + tabulation = add a footnote
- toc + tabulation = add the \[\[TOC]] option to the current file
- temp + tabulation = add the \[\[DOCSYTLE=name]] option to the current file
- class + tabulation= add the \[\[CLASS=name]] option to the current file
- head + tabulation = add the \[\[HEADER]] option to the current file
- rend + tabulation = add the \[\[NORENDER]] option to the current


## Pandoc Options ##

The following hints can be added in your document to flip on additional features in Pandoc:

- **\<!-- \[\[TOC]] -->**: Add a Table of Contents to the top of your output document.
- **\<!-- \[\[NUM]] -->**: Turn on numbering of sections.
- **\<!-- \[\[BIB]] -->**: Add the bibliography option to handle citation and reference (@citationkey). The bibliography file should have the same name as the Pandoc file.
- **\<!-- \[\[BIBSTYLE=name]] -->**: Specify a csl bibliography style.
- **\<!-- \[\[DOCSTYLE=name]] -->**: Specify a template for the convertion to HTML or DOCX or theme in Beamer.
- **\<!-- \[\[CLASS=name]] -->**: Specify a class type to use for a PDF, LaTeX or Beamer document.
- **\<!-- \[\[HEADER]] -->**: Add the option to add a custom header for the convertion to Beamer (the file should be in the same directory as the Pandoc file).
- **\<!-- \[\[NORENDER]] -->**: Option to not automatically start the associated program.


*Note:* these hints are processed by the plugin and are NOT part of Pandoc itself.


## Templates ##

The Templates could be found in the "Styles" folder in the Pandoc plugin folder (in the package folder of Sublime Text).
The version comes with a standard html and docx template (from the Pandoc Render plugin) and with an APA guideline DOCX template.

You can use your custom templates by specifying the path in addition of the template name in the option BIBSTYLE, DOCSTYLE, CLASS and HEADER.


## Tables ##

Create a grid table in Pandoc is a laborious task.
With Pandoc Academic you can create or extend existing grid tables easily.

The module will automatically add filling dashed and cross.
The module will also automatically resize the columns widths based on the longest cell of each column.
You can handle empty cells and extend an existing grid table.

### Create a new table ###

To create a new table, just type your data with at least 2 spaces to separate the columns.

Example:

    Conditions  Col1  Col2  Col3
    Line 1  data1  data2  data3
    Line 2  data4  data5  data6

Then select the data with your mouse and go to Tools > Pandoc Academic > Pandoc Table or use the shortcut CTL+SHIFT+ALT+t.
You should see:

    +------------+-------+-------+-------+
    | Conditions | Col1  | Col2  | Col3  |
    +============+=======+=======+=======+
    | Line 1     | data1 | data2 | data3 |
    +------------+-------+-------+-------+
    | Line 2     | data4 | data5 | data6 |
    +------------+-------+-------+-------+

The module will always consider the first line as the title line.
If one or more cells should be empty just type NA in.

### Extend an existing table ###

The module allows to extend an existing table.
Just add the new data or modify the current one, and use the module:

    +------------+-------+-------+-------+
    | Conditions | Col1  | Col2  | Col3  | Col4
    +============+=======+=======+=======+
    | Line 1     | rename | data2 | data3 | data7
    +------------+-------+-------+-------+
    | Line 2     | data4 | long long data | data6 | data8
    +------------+-------+-------+-------+

will become:

    +------------+--------+----------------+-------+-------+
    | Conditions | Col1   | Col2           | Col3  | Col4  |
    +============+========+================+=======+=======+
    | Line 1     | rename | data2          | data3 | data7 |
    +------------+--------+----------------+-------+-------+
    | Line 2     | data4  | long long data | data6 | data8 |
    +------------+--------+----------------+-------+-------+


## Path option ##

If Pandoc is not in the path of Sublime Text, you can specify a custom path in your file with the following command: **[[PATH=path_name]]**.

If you want to change the path used by the plugin, you can edit the plugin file "PandocConvertor.py".
Change the line 146:

    cmd = ['pandoc']

with:

    cmd = ['your_path']


## Disclosure ##

I am an academic guy, not a software programmer or a computer guru.
This plugin is therefore missing some features and could be improved.
I try to do my best, but I need your feedbacks to help me to do so: [larlequin@gmail.com](mailto:larlequin@gmail.com).
In the same vein, if you're willing to help or to be involved in this project, your participation is more than welcome.

Thanks!

Guillaume
