#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: lms
@file: gne.py
@time: 2020/2/27 21:50
@desc:
"""
from gne import GeneralNewsExtractor

# news_url: https://news.163.com/20/0222/19/F610K69R00019B3E.html
html = open('news.html', 'r+', encoding='utf-8').read()

extractor = GeneralNewsExtractor()
result = extractor.extract(html, with_body_html=True)
# res_json = json.dumps(result, ensure_ascii=False)
for k, v in result.items():
    print(k, v)
