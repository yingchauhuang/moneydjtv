# -*- coding: utf8 -*-
import MySQLdb
import json
import collections
from telnetlib import theNULL
import csv
# MySQL database username
DB_USER='yhuang';

# MySQL database password
DB_PASSWORD='perlin1997';

# MySQL hostname
DB_HOST='twmodedb.cw7dmbpk8io1.us-east-1.rds.amazonaws.com';
DB_dbname='marketdata'
mydb = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_dbname,charset='utf8')
cursor = mydb.cursor()

## {{{ http://code.activestate.com/recipes/410692/ (r8)
# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False
 
    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
     
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def gentaifex(querydate=None):
    if querydate is None:
        sqlquery="call genTaifex(null);"
    else :
        sqlquery="call genTaifex(\'%s\');"  % (querydate)    
    cursor.execute(sqlquery.decode("utf-8"))
    rowarrays_file = 'taifex.tw.csv'
    rows = cursor.fetchall()
    # Convert query to row arrays
    rowarray_list = []
    f = open(data_directory+rowarrays_file,'wb')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow([i[0] for i in cursor.description])
    for row in rows:
        rowarray_list = []
        rowarray_list.append(str(row[0]))
        rowarray_list.append(str(row[1]))
        rowarray_list.append(str(row[2]))
        rowarray_list.append(float(row[3]))
        rowarray_list.append(float(row[4]))
        rowarray_list.append(float(row[5]))
        rowarray_list.append(float(row[6]))
        wr.writerow(rowarray_list)
    #j = json.dumps(rowarray_list)
    
    f.close()
    cursor.nextset()


def genUnSettle(Institute='外資及陸資',querydate=None):
#外資及陸資                    future_unsettle_foreign
#自營商                     future_unsettle_brokerage
#SKType='0' '交易人'         future_unsettle_0
#SKType='1' '特定法人'     future_unsettle_1
#SKType='2' '非特定法人'    future_unsettle_2
#future_unsettle
    if querydate is None:
        sqlquery="call genUnSettle (\'%s\');"  % (Institute)
    else :
        sqlquery="call genUnSettle(\'%s\',\'%s\');"  % (Institute,querydate)
    cursor.execute("SET NAMES utf8;")
    cursor.execute(sqlquery.decode("utf-8"))
    for case in switch(Institute):
        if case('外資及陸資'):
            rowarrays_file = 'future_unsettle_foreign.tw.csv'
            break
        if case('自營商'):
            rowarrays_file = 'future_unsettle_brokerage.tw.csv'
            break
        if case('交易人'):
            rowarrays_file = 'future_unsettle_0.tw.csv'
            break
        if case('特定法人'):
            rowarrays_file = 'future_unsettle_1.tw.csv'
            break
        if case('非特定法人'): 
            rowarrays_file = 'future_unsettle_2.tw.csv'
            break
    rows = cursor.fetchall()
    rowarray_list = []
    f = open(data_directory+rowarrays_file,'wb')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow([i[0] for i in cursor.description])
    for row in rows:
        rowarray_list = []
        rowarray_list.append(row[0].encode('utf8'))
        rowarray_list.append(str(row[1]))
        rowarray_list.append(float(row[2]))
        rowarray_list.append(float(row[3]))
        wr.writerow(rowarray_list)
    #j = json.dumps(rowarray_list)
    cursor.nextset()

def genbuysell(SKName='臺股期貨',Institute='外資及陸資',querydate=None):
#外資及陸資                    future_SKID_foreign
#自營商                     future_SKID_brokerage
#SKType='0' '交易人'         future_SKID_0
#SKType='1' '特定法人'     future_SKID_1
#SKType='2' '非特定法人'    future_SKID_2
    if (SKName=='臺股期貨') :
        for case in switch(Institute):
            if case('外資及陸資'):
                rowarrays_file = 'future_tx_foreign.tw.csv'
                break
            if case('自營商'):
                rowarrays_file = 'future_tx_brokerage.tw.csv'
                break
            if case('交易人'):
                rowarrays_file = 'future_tx_0.tw.csv'
                break
            if case('特定法人'):
                rowarrays_file = 'future_tx_1.tw.csv'
                break
            if case('非特定法人'): 
                rowarrays_file = 'future_tx_2.tw.csv'
                break
    else :
        for case in switch(Institute):
            if case('外資及陸資'):
                rowarrays_file = 'future_%s_foreign.tw.csv' % SKName[5:]
                break
            if case('自營商'):
                rowarrays_file = 'future_%s_brokerage.tw.csv' % SKName[5:]
                break 
            if case('投信'):
                rowarrays_file = 'future_%s_fund.tw.csv' % SKName[5:]
                break
            if case('交易人'):
                rowarrays_file = 'future_%s_0.tw.csv' % SKName[5:]
                break
            if case('特定法人'):
                rowarrays_file = 'future_%s_1.tw.csv' % SKName[5:]
                break
            if case('非特定法人'): 
                rowarrays_file = 'future_%s_2.tw.csv' % SKName[5:]
                break

    if querydate is None:
        sqlquery="call genbuysell (\'%s\',\'%s\');"  % (SKName,Institute)
    else :
        sqlquery="call genbuysell (\'%s\',\'%s\',\'%s\');"  % (SKName,Institute,querydate)
    cursor.execute("SET NAMES utf8;")
    cursor.execute(sqlquery)
    rows = cursor.fetchall()
    rowarray_list = []
    f = open(data_directory+rowarrays_file,'wb')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow([i[0] for i in cursor.description])
    for row in rows:
        rowarray_list = []
        rowarray_list.append(row[0].encode('utf8'))
        rowarray_list.append(str(row[1]))
        rowarray_list.append(float(row[2]))
        rowarray_list.append(float(row[3]))
        wr.writerow(rowarray_list)

    cursor.nextset()
    
def genTSEbuysell(Institute='外資及陸資',querydate=None):
#外資及陸資                    future_SKID_foreign
#自營商                     future_SKID_brokerage
#SKType='0' '交易人'         future_SKID_0
#SKType='1' '特定法人'     future_SKID_1
#SKType='2' '非特定法人'    future_SKID_2
    for case in switch(Institute):
        if case('外資及陸資'):
            rowarrays_file = 'future_foreign.tw.csv' 
            break
        if case('自營商'):
            rowarrays_file = 'future_brokerage.tw.csv'
            break
        if case('投信'):
            rowarrays_file = 'future_fund.tw.csv'
            break
        if case('合計'):
            rowarrays_file = 'future_total.tw.csv' 
            break
        if case('融資'): # default 
            rowarrays_file = 'future_margin_buy.tw.csv' 
            break
        if case('融券'): # default 
            rowarrays_file = 'future_margin_sell.tw.csv' 
            break
    if querydate is None:
        sqlquery="call genTSEbuysell (\'%s\');"  % (Institute)
    else :
        sqlquery="call genfuture_buysell(\'%s\',\'%s\');"  % (Institute,querydate)
    cursor.execute("SET NAMES utf8;")
    cursor.execute(sqlquery)
    rows = cursor.fetchall()
    rowarray_list = []
    f = open(data_directory+rowarrays_file,'wb')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow([i[0] for i in cursor.description])
    for row in rows:
        rowarray_list = []
        rowarray_list.append(row[0].encode('utf8'))
        rowarray_list.append(str(row[1]))
        rowarray_list.append(float(row[2]))
        rowarray_list.append(float(row[3]))
        wr.writerow(rowarray_list)

    cursor.nextset()
       
def genfuture_buysell(querydate=None):
    rowarrays_file = 'future_buysell.tw.csv' 
    if querydate is None:
        sqlquery="call genfuture_buysell(null);"
    else :
        sqlquery="call genfuture_buysell(\'%s\');"  % (querydate)
    cursor.execute("SET NAMES utf8;")
    cursor.execute(sqlquery)
    rows = cursor.fetchall()
    rowarray_list = []
    f = open(data_directory+rowarrays_file,'wb')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow([i[0] for i in cursor.description])
    for row in rows:
        rowarray_list = []
        rowarray_list.append(row[0].encode('utf8'))
        rowarray_list.append(str(row[1]))
        rowarray_list.append(row[2].encode('utf8'))
        rowarray_list.append(row[3].encode('utf8'))
        rowarray_list.append(float(row[4]))
        wr.writerow(rowarray_list)
    cursor.nextset()
    
def genfuture_UnSettle(querydate=None):
    rowarrays_file = 'future_UnSettle.tw.csv'
    if querydate is None:
        sqlquery="call genfuture_UnSettle(null);"
    else :
        sqlquery="call genfuture_UnSettle(\'%s\');"  % (querydate)
    cursor.execute("SET NAMES utf8;")
    cursor.execute(sqlquery)
    rows = cursor.fetchall()
    rowarray_list = []
    f = open(data_directory+rowarrays_file,'wb')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow([i[0] for i in cursor.description])
    for row in rows:
        rowarray_list = []
        rowarray_list.append(row[0].encode('utf8'))
        rowarray_list.append(str(row[1]))
        rowarray_list.append(row[2].encode('utf8'))
        rowarray_list.append(float(row[3]))
        rowarray_list.append(float(row[4]))
        wr.writerow(rowarray_list)
    cursor.nextset()

def genTSE_buysell(querydate=None):
    rowarrays_file = 'TSE_buysell.tw.csv' 
    if querydate is None:
        sqlquery="call genTSE_buysell(null);"
    else :
        sqlquery="call genTSE_buysell(\'%s\');"  % (querydate)
    cursor.execute("SET NAMES utf8;")
    cursor.execute(sqlquery)
    rows = cursor.fetchall()
    rowarray_list = []
    f = open(data_directory+rowarrays_file,'wb')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow([i[0] for i in cursor.description])
    for row in rows:
        rowarray_list = []
        rowarray_list.append(row[0].encode('utf8'))
        rowarray_list.append(str(row[1]))
        rowarray_list.append(row[2].encode('utf8'))
        rowarray_list.append(float(row[3]))
        wr.writerow(rowarray_list)
    cursor.nextset()
    
def genALL_buysell(querydate=None):
    rowarrays_file = 'ALL_buysell.tw.csv' 
    if querydate is None:
        sqlquery="call genALL_buysell(null);"
    else :
        sqlquery="call genALL_buysell(\'%s\');"  % (querydate)
    cursor.execute("SET NAMES utf8;")
    cursor.execute(sqlquery)
    rows = cursor.fetchall()
    rowarray_list = []
    f = open(data_directory+rowarrays_file,'wb')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow([i[0] for i in cursor.description])
    for row in rows:
        rowarray_list = []
        rowarray_list.append(row[0].encode('utf8'))
        rowarray_list.append(str(row[1]))
        rowarray_list.append(row[2].encode('utf8'))
        rowarray_list.append(row[3].encode('utf8'))
        rowarray_list.append(float(row[4]))
        wr.writerow(rowarray_list)
    cursor.nextset()
def genTSE_Lending(querydate=None):
    rowarrays_file = 'tse_lending.tw.csv' 
    if querydate is None:
        sqlquery="call genTSE_Lending(null);"
    else :
        sqlquery="call genTSE_Lending(\'%s\');"  % (querydate)
    cursor.execute("SET NAMES utf8;") 
    cursor.execute(sqlquery)
    rows = cursor.fetchall()
    rowarray_list = []
    f = open(data_directory+rowarrays_file,'wb')
    f.truncate()
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow([i[0] for i in cursor.description])
    for row in rows:
        rowarray_list = []
        rowarray_list.append(str(row[0]))
        rowarray_list.append(float(row[1]))
        rowarray_list.append(float(row[2]))
        rowarray_list.append(float(row[3]))
        rowarray_list.append(float(row[4]))
        wr.writerow(rowarray_list)
    cursor.nextset()
data_directory='c:/develop/MoneyDJTV/Data/'
gentaifex()
# genUnSettle(Institute='外資及陸資')
# genUnSettle(Institute='自營商')
# genUnSettle(Institute='交易人')
# genUnSettle(Institute='特定法人')
# genUnSettle(Institute='非特定法人')
# genbuysell(SKName='臺股期貨',Institute='外資及陸資')
# genbuysell(SKName='臺股期貨',Institute='自營商')
# genbuysell(SKName='臺股期貨',Institute='交易人')
# genbuysell(SKName='臺股期貨',Institute='特定法人')
# genbuysell(SKName='臺股期貨',Institute='非特定法人')
# genTSEbuysell(Institute='外資及陸資')
# genTSEbuysell(Institute='自營商')
# genTSEbuysell(Institute='合計')
# genTSEbuysell(Institute='融資')
# genTSEbuysell(Institute='融券')
genfuture_buysell(None)
genfuture_UnSettle(None)
genTSE_buysell(None)
genALL_buysell(None)
genTSE_Lending(None)
cursor.close()