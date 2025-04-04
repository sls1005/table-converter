# -*- coding: ASCII -*-
import os

def md_table_header_row(headers): # list[str|int|float] -> str
    n = 0
    code = '|'
    for header in headers:
        code += ' ' + str(header) + ' |'
        n += 1
    return code + '\n|' + (n * ' - |')

def md_table_data_row(data): # list[str|int|float] -> str
    result = '\n|'
    for d in data:
        result += ' ' + str(d) + ' |'
    return result

def matrix_to_md_table(headers_and_data): # list[list[str|int|float]] -> str
    if len(headers_and_data) < 1:
        raise ValueError
    headers = headers_and_data[0]
    result = md_table_header_row(headers)
    if len(headers_and_data) > 1:
        for row in headers_and_data[1:]:
            result += md_table_data_row(row)
    return result

def matrix_to_md_table_adjusted(headers_and_data): # list[list[str|int|float]] -> str
    if len(headers_and_data) < 1:
        raise ValueError
    ncol = 0
    col_widths = []
    result = '|'
    headers = headers_and_data[0]
    for header in headers:
        col_widths.append(len(str(header)))
        ncol += 1
    if len(headers_and_data) > 1:
        for row in headers_and_data[1:]:
            for i, d in enumerate(row):
                if i >= ncol:
                    raise ValueError
                else:
                    n = len(str(d))
                    if col_widths[i] < n:
                        col_widths[i] = n
    for i, header in enumerate(headers):
        s = str(header)
        result += ' ' + s + (' ' * (col_widths[i] - len(s))) + ' |'
    result += '\n|'
    for n in col_widths:
        result += ' ' + (n * '-') + ' |'
    if len(headers_and_data) > 1:
        for row in headers_and_data[1:]:
            result += '\n|'
            for i, d in enumerate(row):
                s = str(d)
                k = col_widths[i] - len(s)
                if (not isinstance(d, str)) or s.isdigit() or s.replace('.', '').isdigit():
                    result += (' ' * (k + 1)) + s
                else:
                    result += ' ' + s + (' ' * k)
                result += ' |'
    return result

def save_matrix_as_markdown_into(output_file, headers_and_data):
    output_file.write(matrix_to_md_table(headers_and_data))

def save_matrix_as_markdown(headers_and_data, filename, encoding = 'UTF-8', eol = os.linesep):
    with open(filename, 'w', encoding=encoding, newline=eol) as f:
        save_matrix_as_markdown_into(f, headers_and_data)

def save_matrix_as_adjusted_markdown_table_into(output_file, headers_and_data):
    output_file.write(matrix_to_md_table_adjusted(headers_and_data))
