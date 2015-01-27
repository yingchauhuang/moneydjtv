# -*- coding: utf8 -*-
import MySQLdb
import json
import collections
from telnetlib import theNULL

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

def gentaifex():
    sqlquery="SELECT * FROM future where  tDate>ADDDATE(now(),-14) and skid='FITX' and SKEXP='00' order by tDate desc  limit 5;"
    cursor.execute(sqlquery.decode("utf-8"))
    rowarrays_file = 'taifex.tw.json'
    rows = cursor.fetchall()
    # Convert query to row arrays
    rowarray_list = []
    for row in rows:
        t = (str(row[0]),float(row[5]),float(row[3]),float(row[6]),float(row[4]))
        rowarray_list.append(t)
    j = json.dumps(rowarray_list)
    f = open(data_directory+rowarrays_file,'w')
    print >> f, j
    f.close()
    cursor.nextset()


def genUnSettle(Institute='外資及陸資'):
#外資及陸資                    future_unsettle_foreign
#自營商                     future_unsettle_brokerage
#SKType='0' '交易人'         future_unsettle_0
#SKType='1' '特定法人'     future_unsettle_1
#SKType='2' '非特定法人'    future_unsettle_2
#future_unsettle
    sqlquery="call genUnSettle (\'%s\');"  % (Institute)
    cursor.execute(sqlquery.decode("utf-8"))
    for case in switch(Institute):
        if case('外資及陸資'):
            rowarrays_file = 'future_unsettle_foreign.tw.json'
            break
        if case('自營商'):
            rowarrays_file = 'future_unsettle_brokerage.tw.json'
            break
        if case('交易人'):
            rowarrays_file = 'future_unsettle_0.tw.json'
            break
        if case('特定法人'):
            rowarrays_file = 'future_unsettle_1.tw.json'
            break
        if case('非特定法人'): 
            rowarrays_file = 'future_unsettle_2.tw.json'
            break
    rows = cursor.fetchall()
    # Convert query to row arrays
    rowarray_list = []
    for row in rows:
        t = (str(row[1]),float(row[2]))
        rowarray_list.append(t)
    j = json.dumps(rowarray_list)
    f = open(data_directory+rowarrays_file,'w')
    print >> f, j
    f.close()
    cursor.nextset()

def genbuysell(SKName='臺股期貨',Institute='外資及陸資'):
#外資及陸資                    future_SKID_foreign
#自營商                     future_SKID_brokerage
#SKType='0' '交易人'         future_SKID_0
#SKType='1' '特定法人'     future_SKID_1
#SKType='2' '非特定法人'    future_SKID_2
    if (SKName=='臺股期貨') :
        for case in switch(Institute):
            if case('外資及陸資'):
                rowarrays_file = 'future_tx_foreign.tw.json'
                break
            if case('自營商'):
                rowarrays_file = 'future_tx_brokerage.tw.json'
                break
            if case('交易人'):
                rowarrays_file = 'future_tx_0.tw.json'
                break
            if case('特定法人'):
                rowarrays_file = 'future_tx_1.tw.json'
                break
            if case('非特定法人'): 
                rowarrays_file = 'future_tx_2.tw.json'
                break
    else :
        for case in switch(Institute):
            if case('外資及陸資'):
                rowarrays_file = 'future_%s_foreign.tw.json' % SKName[5:]
                break
            if case('自營商'):
                rowarrays_file = 'future_%s_brokerage.tw.json' % SKName[5:]
                break 
            if case('投信'):
                rowarrays_file = 'future_%s_fund.tw.json' % SKName[5:]
                break
            if case('交易人'):
                rowarrays_file = 'future_%s_0.tw.json' % SKName[5:]
                break
            if case('特定法人'):
                rowarrays_file = 'future_%s_1.tw.json' % SKName[5:]
                break
            if case('非特定法人'): 
                rowarrays_file = 'future_%s_2.tw.json' % SKName[5:]
                break

    sqlquery="call genbuysell (\'%s\',\'%s\');"  % (SKName,Institute)
    cursor.execute(sqlquery)
    rows = cursor.fetchall()
    # Convert query to row arrays
    rowarray_list = []
    for row in rows:
        t = (str(row[1]),float(row[2]),float(row[3]))
        rowarray_list.append(t)
    j = json.dumps(rowarray_list)
    f = open(data_directory+rowarrays_file,'w')
    print >> f, j
    f.close()
    cursor.nextset()
    
def genTSEbuysell(Institute='外資及陸資',cursor= mydb.cursor()):
#外資及陸資                    future_SKID_foreign
#自營商                     future_SKID_brokerage
#SKType='0' '交易人'         future_SKID_0
#SKType='1' '特定法人'     future_SKID_1
#SKType='2' '非特定法人'    future_SKID_2
    for case in switch(Institute):
        if case('外資及陸資'):
            rowarrays_file = 'future_foreign.tw.json' 
            break
        if case('自營商'):
            rowarrays_file = 'future_brokerage.tw.json'
            break
        if case('投信'):
            rowarrays_file = 'future_fund.tw.json'
            break
        if case('合計'):
            rowarrays_file = 'future_total.tw.json' 
            break
        if case('融資'): # default 
            rowarrays_file = 'future_margin_buy.tw.json' 
            break
        if case('融券'): # default 
            rowarrays_file = 'future_margin_sell.tw.json' 
            break
    sqlquery="call genTSEbuysell (\'%s\');"  % (Institute)
    cursor.execute(sqlquery)
    rows = cursor.fetchall()
    # Convert query to row arrays
    rowarray_list = []
    for row in rows:
        t = (str(row[1]),float(row[2]),float(row[3]))
        rowarray_list.append(t)
    j = json.dumps(rowarray_list)
    f = open(data_directory+rowarrays_file,'w')
    print >> f, j
    cursor.nextset()
data_directory='c:/develop/MoneyDJTV/Data/'
genUnSettle(Institute='外資及陸資')
genUnSettle(Institute='自營商')
genUnSettle(Institute='交易人')
genUnSettle(Institute='特定法人')
genUnSettle(Institute='非特定法人')
genbuysell(SKName='臺股期貨',Institute='外資及陸資')
genbuysell(SKName='臺股期貨',Institute='自營商')
genbuysell(SKName='臺股期貨',Institute='交易人')
genbuysell(SKName='臺股期貨',Institute='特定法人')
genbuysell(SKName='臺股期貨',Institute='非特定法人')
genTSEbuysell(Institute='外資及陸資')
genTSEbuysell(Institute='自營商')
genTSEbuysell(Institute='合計')
genTSEbuysell(Institute='融資')
genTSEbuysell(Institute='融券')
gentaifex()
cursor.close()