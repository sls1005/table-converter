# Table Converter

This is a program, and also library, to convert CSV files into another form. However, it doesn't convert to `.xlsx`, nor to `.ods` files. These are not yet supported. It instead converts them into HTML or Markdown tables that you can immediately use in your webpages.

### Example

##### Input

`scores.csv`
```csv
Name,Score
Alice,70
Bob,70
Eve,70
Mallory,60
Trent,55
```

##### Command

```sh
$ python table_converter.py scores.csv
```

##### Output

```markdown
| Name | Score |
| - | - |
| Alice | 70 |
| Bob | 70 |
| Eve | 70 |
| Mallory | 60 |
| Trent | 55 |
```

##### Command

```sh
$ python table_converter.py scores.csv --to md-adj
```

##### Output

```markdown
| Name    | Score |
| ------- | ----- |
| Alice   |    70 |
| Bob     |    70 |
| Eve     |    70 |
| Mallory |    60 |
| Trent   |    55 |
```

##### Command

```sh
$ python table_converter.py scores.csv --to html
```

##### Output

```html
<!DOCTYPE html><html><head></head><body><table><tr><th>Name</th><th>Score</th></tr><tr><td>Alice</td><td>70</td></tr><tr><td>Bob</td><td>70</td></tr><tr><td>Eve</td><td>70</td></tr><tr><td>Mallory</td><td>60</td></tr><tr><td>Trent</td><td>55</td></tr></table></body></html>
```

##### Command

```sh
$ python table_converter.py scores.csv --to wiki
```

##### Output

```wiki
{|
!Name
!Score
|-
|Alice
|70
|-
|Bob
|70
|-
|Eve
|70
|-
|Mallory
|60
|-
|Trent
|55
|}
```

### Requirements

* Python 3 or later.

### Use cases

* On-terminal data-visualization.

* Web development.

* In early stages of data processing, converting a form of CSV files to a form that other programs can read.

### Supported input format

Currently, only CSV is supported. This program follows [RFC 4180](https://datatracker.ietf.org/doc/html/rfc4180) by default.

### Supported output format

* `html`: HTML. Performs character escaping.

* `markdown` or `md`: Markdown, GFM syntax. As of Apr. 2025, the table syntax is also considered compatible with the GLFM syntax. Special characters are not escaped.

* `markdown-adjusted` or `md-adj`: same as `markdown`, but formatted for better plain text readability on wide screens.

* `wiki`: wikitext as supported by MediaWiki. Special characters are not escaped.

* `csv`: CSV as defined in [RFC 4180](https://datatracker.ietf.org/doc/html/rfc4180). This is currently the same as the only supported input format, so it is only used for converting between encodings, adding byte-order marks, etc. (CSV are plain text files, and should be treated as plain text files. In many cases, when dealing with CSV files, these plain-text-file-specific details deserve your care even more than when dealing with normal plain text files.)

### How it works
The concept behind it is very simple. The output of this program, be it a Markdown table or HTML table, doesn't contain more information than a CSV file, just uses more characters to represent the information. I mean, a HTML table can indeed contain more information than a CSV file (such as the style), but this program's output doesn't contain.
