# -*- coding: utf-8 -*-

import re
import hashlib
from urllib import urlencode

class Books():
    books = [
        {
            'Фантастика':
                [
                    {
                        'id': 2,
                        'name': 'Понедельник начинается в субботу',
                        'author': 'Братья Стругацкие',
                        'descr': 'советская фантастическая классика'
                    },
                    {
                        'id': 5,
                        'name': 'Корпорация "Бессмертие"',
                        'author': 'Робер Шекли',
                        'descr': 'зачетная книжень'
                    },
                ]
        },
        {
            'detective':
                [
                    {
                        'id': 4,
                        'name': 'Дуновение смерти',
                        'author': 'Айзек Азимов',
                        'descr': '''В детективном романе Айзека Азимова «Дуновение
    смерти» рассказывается о том, как Луис Брэйд, старший преподаватель химии Университета,
    обнаруживает как-то вечером в лаборатории мертвое тело своего аспиранта Ральфа Ньюфелда,
    который был отравлен цианидом. Было похоже на несчастный случай или на самоубийство.
    Лишь один Брэйд твердо стоял на своем. Это убийство! В результате своего дилетантского расследования
    он и сам чуть не стал жертвой...'''
                    },
                    {
                        'id': 8,
                        'name': 'Закон трех отрицаний',
                        'author': 'Александра Маринина',
                        'descr': '''Насте Каменской не повезло - она попала в аварию.
    Скоро ее выпишут из госпиталя, но сломанная нога все болит и болит, так что Настя
    передвигается с большим трудом. Она решает обратиться к специалисту, использующему
    нетрадиционные методы лечения. Но когда Настя звонит по нужному телефону, выясняется,
    что этот специалист убит. А тут еще одна неприятность. После госпиталя Насте негде жить:
    ее квартира занята неожиданно нагрянувшими родственниками. Так Настя оказывается на даче
    у знакомого, где совершает лечебные прогулки и развлекает себя обсуждением с коллегами
    подробностей очередного громкого убийства молодой кинозвезды. И вдруг она с ужасом
    обнаруживает, что за ней кто-то следит...'''
                    },
                ]
        },
    ]

    current_ver = '1.0.1'

    def __init__(self, ver, bid = 0, isfinal = 0, pid = -1):
        self.ver = ver
        self.bid = int(bid)
        self.isfinal = int(isfinal)
        self.pid = int(pid)

    def check_ver(self):
        '''validates version'''
        # version does not setted at all
        if not self.ver: raise Exception('ERROR: VER is empty')

        matches = re.compile('^([0-9]{1})\.([0-9]{1})\.([0-9]{1})$').findall(self.ver)

        # version does not match pattern N.N.N
        if matches == []: return 'ERROR: VER is invaild'

        if self.ver <> self.current_ver: raise Exception('ERROR: this VER is not supported')

        return True

    def book_by_id(self):
        '''returns book data as dictionary by book id'''
        res = ''
        b = []
        for book in self.books:
            b.extend([book[k] for k in book.keys()])

        for one_book in b[0]:
            if one_book['id'] == self.bid:
                res = one_book

        return res

    def get_category_books(self):
        # show books in category
        if self.pid == -1: raise Exception('ERROR: specify subcategory id (pid)')
        res = ''
        count = 0
        if self.pid>=0 and self.pid in range(len(self.books)):
            book = [self.books[self.pid][k] for k in self.books[self.pid].keys()]
            book = book[0]
            count = len(book)
            i = 0
            for b in book:
                res += urlencode({'NAME' + str(i): b['name'], 'ID' + str(i): b['id'], })
                i += 1
        return res, count

    def get_categories(self):
        #show categories
        i = 0
        categories = [k.keys() for k in self.books]
        count = len(categories)
        res = ''
        for category in categories:
            res += urlencode({'NAME' + str(i): category[0], 'ID' + str(i): i})
            i += 1
        return res, count

def index(cmd = '', ver = 0, new = 0, isfinal = 0, pid = -1, bid = 0):

    cmd = cmd.upper()
    count = 0

    books = Books(ver, bid, isfinal, pid)

    # >> LIST
    if cmd == 'LIST':
        
        ver_is_valid = books.check_ver()
        if ver_is_valid <> 1: return ver_is_valid

        # check isfinal
        if not isfinal: return 'ERROR: ISFINAL is empty'

        isfinal = int(isfinal)
        res = ''

        if isfinal == 1:
            res, count = books.get_category_books()

        elif isfinal == 0:
            res, count = books.get_categories()
        else:
            return 'ERROR: ISFINAL should be 1 or 0'
        

        return 'COUNT=%d%s' % (count, res)
    # <<

    # >> BOOK
    elif cmd == 'BOOK':
        ver_is_valid = books.check_ver()
        if ver_is_valid <> 1: return ver_is_valid

        if not bid: return 'ERROR: no book id (bid) found'
        bid = int(bid)
        res =  urlencode(books.book_by_id())
            
        return 'BID=' + str(bid) + '%s' % res
    # <<

    # >> GET
    elif cmd == 'GET':
        ver_is_valid = check_ver(ver)
        if ver_is_valid <> 1: return ver_is_valid

        if not bid: return 'ERROR: no book id (bid) found'
        bid = int(bid)

        res = urlencode(book_by_id(bid))

        if not len(res): return 'ERROR: no such book'

        bidded_link = hashlib.md5(res+'salt').hexdigest()

        return 'LINK=' + bidded_link
    # << 

    elif cmd == 'REG':
        ver_is_valid = check_ver(ver)
        if ver_is_valid <> 1: return ver_is_valid

        return 'LOGIN=footren&pass=v324jzrn'

        return 'REG'
    
    else:
        return 'ERROR'
    
