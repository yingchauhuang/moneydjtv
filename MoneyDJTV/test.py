# coding=utf-8
from django.template import Template,Context
from django.template.loader import get_template
#from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext, loader
import os
import sys
settings.configure(TEMPLATE_DIRS=('C:\\Develop\\moneydjtv\\moneydjtv\\templates',))
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
#t = loader.get_template('main_page.html')
#t = render_to_response('test.html')
#t = loader.get_template('test.html')
#t =  get_template('TVNews_section_industry.html')
t =  get_template('test.html')
paginator_context = {
        'News1Title': 'News1Title XXX',
        'News1Image': 'ctee.jpg',
        'News2Title': 'News2Title XXX',
        'News2Image': 'EDN.png',
        'News3Title': 'News3Title XXX',
        'News3Image': 'EDN.png',
        'News4Title': 'News4Title XXX',
        'News4Image': 'apple.jpg',
        'Slide1Title': unicode('News'),
        'IndustryName': 'ABC',
        'R1C1' : '$$$$',
        'R2C1' : '$$$$',
        'R3C1' : '$$$$',
        'R4C1' : '$$$$',
        'R1C2' : '$$$$',
        'R2C2' : '$$$$',
        'R3C2' : '$$$$',
        'R4C2' : '$$$$',
        'R1C3' : '$$$$',
        'R2C3' : '$$$$',
        'R3C3' : '$$$$',
        'R4C3' : '$$$$',
    }
c = Context(paginator_context)
result=t.render(c)

f = open('work.html', 'w')
f.write(result.encode('utf8'))
f.close()