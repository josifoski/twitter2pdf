#! /usr/bin/env python3

# Getting tweets from lists script and creating txt and pdf from them
# using optional filter
# programmer: Josifoski Aleksandar about.me/josifsk

import sys
import os
import codecs
import re
import datetime
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj

# DEPENDANCIES DEPENDANCIES DEPENDANCIES
# program uses python3+
# program is dependant on installed console twitter client https://github.com/sferik/t
# dependant on thirdparty packages: reportlab pdfrw (this are used to implement footer and page numbering in exported pdf)
# on ubuntu they can be installed via pip3: pip3 install pdfrw reportlab
# also program is dependant on installed libreoffice to generate pdf, keep eye how is started via command line

# INPUT INPUT INPUT INPUT INPUT INPUT INPUT 
startdate = '2015-09-21' 
enddate = '2015-09-21'
printreff = True  #writing time, source, link
username = 'adam222up' #change here username
blist = True #for using lists, if false, then username tweets from timeline will be pulled
if blist:
    whichlist = 'news' #also change here specific list
filtering = True
numofpulledtweets = 200 #last tweets
##############################################

internalcount = 0

if blist:
    os.system("t list timeline -l -r -n %d %s/%s > tweets.txt" % (numofpulledtweets, username, whichlist))
    decision = whichlist
else:
    os.system("t timeline -l -r -n %d %s > tweets.txt" % (numofpulledtweets, username))
    decision = username

firstday = datetime.datetime.strptime(startdate, "%Y-%m-%d").timetuple().tm_yday
lastday = datetime.datetime.strptime(enddate, "%Y-%m-%d").timetuple().tm_yday
year = enddate[:4]
ddat1 = { 'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12' }

ftemp = codecs.open('tweets.txt', 'r', 'utf-8')

lstemp = ftemp.readlines()
for ind in range(len(lstemp)):
    lstemp[ind] = lstemp[ind].strip()

ftemp.close()

if startdate == enddate:
    fname = decision + '_' + startdate + 'd'
    title = (decision + ' ' + startdate).rjust(44)
else:
    fname = decision + '_' + startdate + '-' + enddate + 'd'
    title = (decision + ' ' + startdate + ':' + enddate).rjust(44)

out = codecs.open(fname + '.txt', 'w', 'utf-8')
out.write( title + '\n\n')

bejko = []
for twit in lstemp:
    concreteday = datetime.datetime.strptime(year + '-' + ddat1[twit.split()[1]] + '-' + '%02d' % int(twit.split()[2]), "%Y-%m-%d").timetuple().tm_yday
    if concreteday >= firstday and concreteday <= lastday: 
        bejko.append(' '.join(twit.split()[1:]))

# reject tweets where this words occures if filtering is True, feel free to adjust filter
lmyfilter = [ 'Ријана', 'Северина', 'Цеца', 'Роналдо', 'Кардашијан', 'Шаулиќ', 'Астон Вила',  'Спортклуб',  'НБА',
'Хајди Клум', 'SportMedia', 'СуперСпорт', 'СЕХА', 'Барса', 'Реал Мадрид', 'Суарез', 'секс', 'облини', 'задник', 'задници', 'градник', 'пенис', 'Мадона', 'Лопез',
'порно', 'Беквалац', 'Бундес', 'Примера', 'ВИДЕО 18+', 'ВИДЕО+18', '+18 ВИДЕО', 'манекенка', 'старлета', 'Мурињо', 'Лигата на шампиони',
'оргаз',  'Јувентус', 'Фиорентина', 'Сампдорија', 'Лацио', 'топлес', 'проститу', 'ФИФА', 'гаќи', 'премиер лига',
'деколте', 'зодијак', 'Automedia', 'Авто Магазин', 'Galaxy', 'Samsung', 'Џастин Бибер']

for twit in bejko:
        if filtering:
            letitpass = True
            for filteritem in lmyfilter:
                if filteritem.lower().strip('!"&\'()*,-./:;?<>[\]_{}«·»‑–—―‖‘’“”…′$#') in twit.lower():
                    letitpass = False
            if letitpass:
                if 'http:' in twit.split()[-1]:
                    out.write(' '.join(twit.split()[4:-1]) + '\n')
                else:
                    out.write(' '.join(twit.split()[4:]) + '\n')
                if printreff:
                    if 'http:' in twit.split()[-1]:
                        out.write('//' + '%04d' % internalcount + ' ' + ' '.join(twit.split()[:4]) + ' ' + twit.split()[-1] + '\n\n')
                        internalcount += 1
                    else:
                        out.write('//' + '%04d' % internalcount + ' ' +  ' '.join(twit.split()[:4]) + '\n\n')
                        internalcount += 1
                else:
                    out.write('\n')
                                      

        else:
            if 'http:' in twit.split()[-1]:
                out.write(' '.join(twit.split()[4:-1]) + '\n')
            else:
                out.write(' '.join(twit.split()[4:]) + '\n')
            if printreff:
                if 'http:' in twit.split()[-1]:
                    out.write('//' + '%04d' % internalcount + ' ' +  ' '.join(twit.split()[:4]) + ' ' + twit.split()[-1] + '\n\n')
                    internalcount += 1
                else:
                    out.write('//' + '%04d' % internalcount + ' ' +  ' '.join(twit.split()[:4]) + '\n\n')
                    internalcount += 1 
            else:
                out.write('\n')   


out.close()

# be careful if using libreoffice for generating pdf, in olderversions via command line
# it can start differently like loffice libreoffice or similar
os.system('libreoffice5.0 --writer --headless --convert-to pdf %s ' %  (fname + '.txt'))


# Tnx to this answer for implementing footer and page numbering http://stackoverflow.com/a/28283732/2397101
# this code follows

input_file = fname + '.pdf'
output_file = fname.rstrip('d') + '.pdf'

# Get pages
reader = PdfReader(input_file)
pages = [pagexobj(p) for p in reader.pages]


# Compose new pdf
canvas = Canvas(output_file)

for page_num, page in enumerate(pages, start=1):

    # Add page
    canvas.setPageSize((page.BBox[2], page.BBox[3]))
    canvas.doForm(makerl(canvas, page))

    # Draw footer
    footer_text = "Page %s of %s" % (page_num, len(pages))
    x = 128
    canvas.saveState()
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setLineWidth(0.5)

    canvas.line(66, 53, page.BBox[2] - 66, 53)
    canvas.setFont('Times-Roman', 10)
    canvas.drawString(page.BBox[2]-x, 40, footer_text)
    
    canvas.restoreState()

    canvas.showPage()

canvas.save()
os.remove(input_file)
os.rename(fname + '.txt', fname.rstrip('d') + '.txt')

print('Done.')

