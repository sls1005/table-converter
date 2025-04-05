# -*- coding: ASCII -*-
import html
import os

def html_table_header_row(headers): # list[str|int|float] -> str
    code = '<tr>'
    for header in headers:
        code += '<th>' + html.escape(str(header)) + '</th>'
    return code + '</tr>'

def html_table_data_row(data): # list[str|int|float] -> str
    code = '<tr>'
    for d in data:
        code += '<td>' + html.escape(str(d)) + '</td>'
    return code + '</tr>'

def matrix_to_html_table(headers_and_data): # list[list[str|int|float]] -> str
    if len(headers_and_data) == 0:
        return ''
    headers = headers_and_data[0]
    code = '<table>' + html_table_header_row(headers)
    if len(headers_and_data) > 1:
        for row in headers_and_data[1:]:
            code += html_table_data_row(row)
    return code + '</table>'

def save_matrix_as_html_into(output_file, headers_and_data):
    output_file.write('<!DOCTYPE html><html><head></head><body>' + matrix_to_html_table(headers_and_data) + '</body></html>')

def save_matrix_as_html(headers_and_data, filename, encoding = 'UTF-8', eol = os.linesep):
    with open(filename, 'w', encoding=encoding, newline=eol) as f:
        save_matrix_as_html_into(f, headers_and_data)
