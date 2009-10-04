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
        {
            'single':
                [
                    {
                        'id': 11,
                        'name': 'Аксиология личностного бытия',
                        'author': 'В. П. Барышков',
                        'descr': '''В монографии исследуются онтологические основания ценностного отношения.
                        Предмет исследования — личностное бытие как область формирования и функционирования
                        ценностных смыслов. Рассматриваются субстациональная и коммуникативная концепции
                        ценностного мира человека. Для научных работников, преподавателей философии
                        и студентов вузов'''
                    },
                ]
        }
    ]

    current_ver = '1.0.2'

    def __init__(self, ver, bid = 0, isfinal = 0, pid = -1):
        self.ver = ver
        self.bid = int(bid)
        self.isfinal = int(isfinal)
        self.pid = int(pid)

    def check_ver(self):
        '''validates version'''
        # version does not setted at all
        if not self.ver: raise Exception('VER is empty', 1)

        matches = re.compile('^([0-9]{1})\.([0-9]{1})\.([0-9]{1})$').findall(self.ver)

        # version does not match pattern N.N.N
        if matches == []: raise Exception('VER is invaild', 2)

        if self.ver <> self.current_ver: raise Exception('this VER is not supported', 3)

        return True

    def book_by_id(self):
        '''returns book data as dictionary by book id'''
        res = ''
        b = []
        for book in self.books:
            b.extend([book[k] for k in book.keys()])

        for book_shelf in b:
            for one_book in book_shelf:
                if one_book['id'] == self.bid:
                    res = one_book

        if (not isinstance(res, dict)): raise Exception('Book information error, dosen\'t exisits?', 4)

        return res

    def get_category_books(self):
        # show books in category
        if self.pid == -1: raise Exception('specify subcategory id (pid)', 5)
        res = ''
        count = 0

        if self.pid>=0 and self.pid in range(len(self.books)):
            book = [self.books[self.pid][k] for k in self.books[self.pid].keys()]
            book = book[0]
            count = len(book)
            i = 0
            for b in book:
                res += '&' + urlencode({'NAME' + str(i): b['name'], 'ID' + str(i): b['id'], })
                i += 1
        return res, count

    def get_categories(self):
        #show categories
        i = 0
        categories = [k.keys() for k in self.books]

        #directories + books
        elcount = len(categories)

        # directoies
        count = elcount
        
        res = ''
        for category in categories:
            if (category[0] == 'single'):
            # we have single books
                count -= 1

            else:
                res += '&' + urlencode({'NAME' + str(i): category[0], 'ID' + str(i): i})
            i += 1

        res += '&' + urlencode({'NAME' + str(i): 'Аксиология личностного бытия', 'ID' + str(i): 11})

        return res, count, elcount

def index(cmd = '', ver = 0, new = 0, isfinal = 0, pid = -1, bid = 0):

    cmd = cmd.upper()
    bid = int(bid)
    count = 0

    books = Books(ver, bid, isfinal, pid)

    try:
        books.check_ver()
    except Exception, (error, code):
        return urlencode({'MESSAGE': error, 'CODE': code})

    # >> LIST
    if cmd == 'LIST':
        
        # check isfinal
        if not isfinal: return urlencode({'MESSAGE': 'ISFINAL is empty', 'CODE': 6})

        isfinal = int(isfinal)
        res = ''

        if isfinal == 1:
            res, count = books.get_category_books()
            return 'COUNT=%d%s' % (count, res)

        elif isfinal == 0:
            res, count, elcount = books.get_categories()
            return 'ELCOUNT=%d&COUNT=%d%s' % (elcount, count, res)
        else:
            return urlencode({'MESSAGE': 'ISFINAL should be 1 or 0', 'CODE': 7})
    # <<

    # >> BOOK
    elif cmd == 'BOOK':

        if not bid: return urlencode({'MESSAGE': 'no book id (bid) found', 'CODE': 8})
        
        try:
            res = urlencode(books.book_by_id())
        except Exception, (error, code):
            return urlencode({'MESSAGE': error, 'CODE': code})

        return 'BID=' + str(bid) + '&%s' % res
    # <<

    # >> GET
    elif cmd == 'GET':
        if not bid: return urlencode({'MESSAGE': 'no book id (bid) found', 'CODE': 8})

        try:
            res = urlencode(books.book_by_id())
        except Exception, (error, code):
            return urlencode({'MESSAGE': error, 'CODE': code})

        bidded_link = hashlib.md5(res+'salt').hexdigest()

        return urlencode({'http://wwww.bugtest.ru/get.py?fname=': bidded_link})
    # << 

    elif cmd == 'REG':
        return 'LOGIN=footren&PASS=v324jzrn'

    else:
        return urlencode({'MESSAGE': 'unknown command', 'CODE': 9})
    
