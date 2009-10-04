# -*- coding: utf-8 -*-

from urllib import urlencode
import os

book_links = {  '1e5d528b84713b7f737829899a498e12': 'books/heminguyei_yernest_starik_i_more.fb2',
                '5e9eb55610983db061a3fce0d427f7be': 'books/heminguyei_yernest_starik_i_more.fb2',
                'd0bf269b17c21b2e3424e77aec6660fa': 'books/heminguyei_yernest_starik_i_more.fb2',
                '62aaec9fae8e547ebbade8726604e8a7': 'books/heminguyei_yernest_starik_i_more.fb2',
                '85bef13f60ed429c97718bf77fdc8dcb': 'books/heminguyei_yernest_starik_i_more.fb2'}

def index(fname = ''):
    path = os.path.dirname(os.path.abspath(__file__))

    if fname == '':
        return urlencode({'MESSAGE': 'get is empty', 'CODE': 10})
        
    if fname in book_links:
        with open(path + '/' + book_links[fname]) as file:
            content = file.readlines()
        return ''.join(content)
        
    else:
        return urlencode({'MESSAGE': 'no such book', 'CODE': 11})
