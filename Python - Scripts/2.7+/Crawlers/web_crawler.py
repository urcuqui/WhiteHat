# Web crawler
# Author: Christian Urcuqui
# Date: 17 August 2016

import webbrowser
import csv


def open_url_csv(path, delimiter, column_url):


    file = open(path, "rt", encoding='utf-8')
    rd = csv.reader(file, delimiter=delimiter)
    next(rd, None)
    for row in rd:
        url = (''.join(row))
        print(url.split(";")[column_url])
        webbrowser.open_new_tab(url.split(";")[column_url])

open_url_csv('../Datasets/url_short_set.csv', ' ', 0)