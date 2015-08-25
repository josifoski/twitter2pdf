# twitter2pdf
Generate pdf from twitter streams, user timelines or lists

Getting tweets from lists or user timelines python script and creating pdf from them
using optional filter
programmer: Josifoski Aleksandar twitter.com/adam222up


Dependencies
program uses python3+
program is dependant on installed console twitter client https://github.com/sferik/t
dependant on thirdparty packages: reportlab pdfrw (this are used to implement footer and page numbering in exported pdf)
on ubuntu they can be installed via pip3: pip3 install pdfrw reportlab
also program is dependant on installed libreoffice to generate pdf, keep eye how is started via command line

# Usage
just before starting script change this details (in script):

# INPUT
startdate = '2015-08-01' 
enddate = '2015-08-24'
printreff = True  #writing time, source, link
username = 'adam222up' #change here username
blist = True #for using lists, if false, then username tweets from timeline will be pulled
if blist:
    whichlist = 'news' #also change here specific list
filtering = True
numofpulledtweets = 200 #last tweets
