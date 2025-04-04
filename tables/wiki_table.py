# -*- coding: ASCII -*-
import os

def wiki_table_header_row(headers): # list[str|int|float] -> str
    result = ''
    for header in headers:
        result += "\n!" + str(header)
    return result
    # Reference: https://m.mediawiki.org/wiki/Help:Tables

def wiki_table_data_row(data): # list[str|int|float] -> str
    result = '\n|-'
    for d in data:
        result += '\n|' + str(d)
    return result

def matrix_to_wiki_table(headers_and_data): # list[list[str|int|float]] -> str
    if len(headers_and_data) < 1:
        raise ValueError
    headers = headers_and_data[0]
    code = '{|' + wiki_table_header_row(headers)
    if len(headers_and_data) > 1:
        for row in headers_and_data[1:]:
            code += wiki_table_data_row(row)
    return code + '\n|}'

def save_matrix_as_wiki_into(output_file, headers_and_data):
    output_file.write(matrix_to_wiki_table(headers_and_data))

def save_matrix_as_wiki(headers_and_data, filename, encoding = 'UTF-8', eol = os.linesep):
    with open(filename, 'w', encoding=encoding, newline=eol) as f:
        save_matrix_as_wiki_into(f, headers_and_data)
