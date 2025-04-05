#!/usr/bin/env python
# -*- coding: ASCII -*-
# Python 3 is recommended for interpreting this. Python 2 is not supported.
import csv
import os
import sys
from sys import stdin, stdout, argv
from tables.html_table import save_matrix_as_html_into
from tables.markdown_table import save_matrix_as_markdown_into, save_matrix_as_adjusted_markdown_table_into
from tables.wiki_table import save_matrix_as_wiki_into

usage = '''Usage: table_converter.py [options] [file]

Arguments:

    [file]                                    The name of the input file (optional). Can also be specified with the '-i' option. If it is not given, this program reads from stdin. If both this and '-i <file>' are given, or any of them is specified more than once, this program will report an error and exit.

Options:

    -h, --help                                Show this help message and exit.

    -i, --input <file>                        The name of the input file (optional). If not specified, the first argument not recognized as an option will be used.

    -o, --output <file>                       The name of the output file. If it is not given, this program writes to stdout. If a file of this name exists, this program will report and error and exit.

    -e1, --input-encoding <encoding>          The encoding of the input file. Default: UTF-8. This will be ignored when there is no input file or when reading from stdin. Hint: You must specify this if your file uses an early Asian variable-length encoding.

    -e2, --output-encoding <encoding>         The encoding of the output file. Default: UTF-8. This will be ignored when there is no output file or when writing to stdout.

    -e, --encoding <encoding>                 Specifying the default encoding for encoding the output file and decoding the input file when their encodings are not specified.

    -f2, --to <format>                        The expected format of the OUTPUT file. Possible values: html (HTML), csv (CSV as defined in RFC 4180), wiki (wikitext as supported by MediaWiki), markdown (Markdown, GFM syntax), markdown-adjusted (similar to 'markdown'; the generated table will be formatted for plain text readability. This assumes infinite screen width with a monospaced font), md (alias for 'markdown'), md-adj (alias for markdown-adjusted), md-gfm (currently an alias for 'markdown'), md-glfm (currently an alias for 'markdown'). Default: markdown. Other formats are not supported.

    -s1, --input-separator <separator>        The character that separates two values in a CSV input file. Defaults to a comma (','). This is ignored if the input file is not a CSV file.

    -s2, --output-separator <separator>       The character that separates two values in a CSV output file. Defaults to a comma (','). This is ignored if the output file is not a CSV file.

    -s, --separator <separator>               Specifying the default character to separate two values in a CSV input or output file when their separators are not specified.

    --output-line-end < CR | LF | CRLF >      The name of the end-of-line character(s) of the output file. This will be ignored when writing to stdout. Default: system default.

    --use-byte-order-mark                     Enable the byte-order-mark-aware mode for UTF-8. Default: off. If enabled, this program is supposed to write a byte-order mark to the start of a file when writing and skip it when reading if the encoding is UTF-8. This will be ignored when reading from stdin or writing to stdout. Hint: You should try this flag if the normal output seems incorrect for you. This is a flag; it doesn't accept any additional value.

    --bom (or '-bom')                         An alias for '--use-byte-order-mark'.

    --use-byte-order-mark-for-input           Indicate that the byte-order-mark-aware mode for UTF-8 should be enabled for the input, but not the output unless otherwise specified.

    --bom1 (or '-bom1')                       An alias for '--use-byte-order-mark-for-input'.

    --use-byte-order-mark-for-output          Indicate that the byte-order-mark-aware mode for UTF-8 should be enabled for the output, but not the input unless otherwise specified.

    --bom2 (or '-bom2')                       An alias for '--use-byte-order-mark-for-output'.

If no argument is provided, this program reads CSV from stdin and writes a Markdown table (GFM syntax) to stdout.

Example: python3 table_converter.py -i input-file.csv -s1 ',' -e1 UTF-16 -o output-file.md -f2 md -e2 UTF-8

Note: The 'markdown-adjusted' mode is optimized for wide screens, not for small screens. It is recommeded that you use `-f2 wiki` (which uses a lot of linebreaks) for the purpose of information-visualizing if you are on a terminal with a small screen.
'''

csv.register_dialect("rfc4180", delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_MINIMAL, quotechar='"', doublequote=True, skipinitialspace=False, strict=False)
# Reference: https://datatracker.ietf.org/doc/html/rfc4180

def csv_file_to_matrix(filename, separator = ',', encoding='UTF-8'): # str, str, str -> list[list[str]]
    result = [] #: list[list[str]]
    with open(filename, 'r', newline='', encoding=encoding) as f:
        for row in csv.reader(f, dialect="rfc4180", delimiter=separator):
            result.append(row)
    return result

def save_matrix_as_csv_into(output_file, headers_and_data, separator = ',', eol = os.linesep):
    csv.writer(output_file, dialect="rfc4180", delimiter=separator, lineterminator=eol).writerows(headers_and_data)

def save_matrix_as_csv(headers_and_data, filename, separator = ',', eol = os.linesep, encoding = 'UTF-8'):
    with open(filename, 'w', newline='', encoding=encoding) as f:
        save_matrix_as_csv_into(f, headers_and_data, separator=separator, eol=eol)

def main():
    supported_output_formats = ['html', 'csv', 'wiki', 'markdown', 'markdown-adjusted', 'md-gfm', 'md-glfm', 'md', 'md-adj']
    default_encoding = 'UTF-8' # UTF-8, no BOM
    input_encoding = None
    output_encoding = None
    default_separator = ','
    input_separator = None
    output_separator = None
    output_file_format = 'markdown'
    output_line_end = os.linesep
    input_file_name = None
    output_file_name = None
    default_use_utf8_bom = False
    use_utf8_bom_for_input = False
    use_utf8_bom_for_output = False
    argc = len(argv)
    i = 1
    while i < argc:
        a = argv[i]
        if a in ('-h', '--help'):
            print(usage)
            return
        elif a in ('-i', '--input'):
            if input_file_name is not None:
                exit("[Error] The input file name is specified more than once. ('%s' and '%s')" % (input_file_name, a))
            elif i == argc - 1:
                exit("[Error] No value after '%s'" % a)
            else:
                input_file_name = argv[i+1]
                i += 2
                continue
        elif a in ('-o', '--output'):
            if i == argc - 1:
                exit("[Error] No value after '%s'" % a)
            else:
                output_file_name = argv[i+1]
                i += 2
                continue
        elif a in ('-e', '--encoding'):
            if i == argc - 1:
                exit("[Error] No value after '%s'" % a)
            else:
                default_encoding = argv[i+1]
                i += 2
                continue
        elif a in ('-e1', '--input-encoding'):
            if i == argc - 1:
                exit(-1)
            else:
                input_encoding = argv[i+1]
                i += 2
                continue
        elif a in ('-e2', '--output-encoding'):
            if i == argc - 1:
                exit("[Error] No value after '%s'" % a)
            else:
                output_encoding = argv[i+1]
                i += 2
                continue
        elif a in ('-s', '--separator'):
            if i == argc - 1:
                exit("[Error] No value after '%s'" % a)
            else:
                default_separator = argv[i+1] # needs extra check
                i += 2
                continue
        elif a in ('-s1', '--input-separator'):
            if i == argc - 1:
                exit("[Error] No value after '%s'" % a)
            else:
                input_separator = argv[i+1]
                i += 2
                continue
        elif a in ('-s2', '--output-separator'):
            if i == argc - 1:
                exit("[Error] No value after '%s'" % a)
            else:
                output_separator = argv[i+1]
                i += 2
                continue
        elif a in ('-f2', '--to'):
            if i == argc - 1:
                exit("[Error] No value after '%s'" % a)
            else:
                a2 = argv[i+1]
                output_file_format = a2.lower()
                if output_file_format not in supported_output_formats:
                    exit("[Error] Unknown output format: '%s'" % a2)
                i += 2
                continue
        elif a in ('--output-line-end'):
            if i == argc - 1:
                exit("[Error] No value after '%s'" % a)
            else:
                a2 = argv[i+1]
                s = a2.upper()
                eol_chars = {
                    'CR': '\r',
                    'LF': '\n',
                    'CRLF': '\r\n'
                }
                if s in eol_chars.keys():
                    output_line_end = eol_chars[s]
                else:
                    exit("[Error] Unknown character name: '%s'" % a2)
                i += 2
                continue
        elif a in ('-bom', '--bom', '--use-byte-order-mark'):
            default_use_utf8_bom = True
        elif a in ('-bom1', '--bom1', '--use-byte-order-mark-for-input'):
            use_utf8_bom_for_input = True
        elif a in ('-bom2', '--bom2', '--use-byte-order-mark-for-output'):
            use_utf8_bom_for_output = True
        elif input_file_name is None:
            input_file_name = a
        else:
            exit("[Error] Extra argument given: '%s'" % a)
        i += 1
    if input_encoding is None:
        input_encoding = default_encoding
    if output_encoding is None:
        output_encoding = default_encoding
    if input_separator is None:
        input_separator = default_separator
    if output_separator is None:
        output_separator = default_separator
    if use_utf8_bom_for_input or default_use_utf8_bom:
        if input_encoding in ('UTF-8', 'utf-8', 'UTF_8', 'utf_8', 'UTF8', 'utf8'):
            input_encoding = 'utf-8-sig' # It seems that this encoding variant is supported since very early days. No need for version check.
    if use_utf8_bom_for_output or default_use_utf8_bom:
        if output_encoding in ('UTF-8', 'utf-8', 'UTF_8', 'utf_8', 'UTF8', 'utf8'):
            output_encoding = 'utf-8-sig'
    if sys.version_info.major < 3:
        exit("[Error] This version of interpreter ('%d') is not supported. Please use a newer interpreter to run this." % sys.version_info.major)
    matrix = []
    if input_file_name is None:
        for row in csv.reader(stdin.readlines(), dialect="rfc4180", delimiter=input_separator):
            matrix.append(row)
    else:
        matrix = csv_file_to_matrix(input_file_name, separator=input_separator, encoding=input_encoding)
    alias = {
        'markdown': 'md',
        'md-gfm': 'md',
        'md-glfm': 'md',
        'markdown-adjusted': 'md-adj'
    }
    output_function = {
        'html': save_matrix_as_html_into,
        'md': save_matrix_as_markdown_into,
        'md-adj': save_matrix_as_adjusted_markdown_table_into,
        'wiki': save_matrix_as_wiki_into
    }
    if output_file_format in alias.keys():
        output_file_format = alias[output_file_format]
    if output_file_name is None:
        if output_file_format == 'csv':
            save_matrix_as_csv_into(stdout, matrix, separator=output_separator, eol='\n') # '\n' here. The file object, not the CSV writer, is expected to translate this '\n' into system default. This is not ideal but can be proved to be correct. It prevents worst case ("\r\r\n").
        else:
            output_function[output_file_format](stdout, matrix)
        print('') # for newline
    elif output_file_format == 'csv':
        save_matrix_as_csv(matrix, output_file_name, separator=output_separator, eol=output_line_end, encoding=output_encoding)
    else:
        with open(output_file_name, 'w', encoding=output_encoding, newline=output_line_end) as output_file:
            output_function[output_file_format](output_file, matrix)

if __name__ == '__main__':
    main()
