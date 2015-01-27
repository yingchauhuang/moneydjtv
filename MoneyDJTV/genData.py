
import MySQLdb
import json
import collections

# MySQL database username
DB_USER='yhuang';

# MySQL database password
DB_PASSWORD='perlin1997';

# MySQL hostname
DB_HOST='twmodedb.cw7dmbpk8io1.us-east-1.rds.amazonaws.com';
DB_dbname='marketdata'
mydb = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_dbname)
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

def genUnSettle(Institute='外資及陸資'):
#外資及陸資					future_unsettle_foreign
#自營商 					future_unsettle_brokerage
#SKType='0' '交易人' 		future_unsettle_0
#SKType='1' '特定法人' 	future_unsettle_1
#SKType='2' '非特定法人'	future_unsettle_2
#future_unsettle
    for case in switch(Institute):
    if case('外資及陸資'):
		cursor.execute("""
						SELECT Institute,tDate,Net_US,D_Net_US FROM marketdata.institute_future_contract where tDate>ADDDATE(now(),-14) and SKNAME='臺股期貨' and Institute='外資及陸資';
			""")
		rowarrays_file = 'future_unsettle_foreign.tw.json'
        break
    if case('自營商'):
		cursor.execute("""
					 SELECT Institute,tDate,Net_US,D_Net_US FROM marketdata.institute_future_contract where tDate>ADDDATE(now(),-14) and SKNAME='臺股期貨' and Institute='自營商';
		""")
		rowarrays_file = 'future_unsettle_brokerage.tw.json'
        break
    if case('交易人'):
        cursor.execute("""
             SELECT SKID,tDate,USettle,D_USettle FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID='TX' and SKType='0' limit 5;
		""")
		rowarrays_file = 'future_unsettle_0.tw.json'
        break
    if case('特定法人'):
		cursor.execute("""
					 SELECT SKID,tDate,USettle,D_USettle FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID='TX' and SKType='1' limit 5;
		""")
		rowarrays_file = 'future_unsettle_1.tw.json'
        break
    if case('非特定法人'): 
        cursor.execute("""
             SELECT SKID,tDate,USettle,D_USettle FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID='TX' and SKType='2' limit 5;
		""")
		rowarrays_file = 'future_unsettle_2.tw.json'
		break
	rows = cursor.fetchall()
	# Convert query to row arrays
	rowarray_list = []
	for row in rows:
		t = (str(row[1]),float(row[2]))
		rowarray_list.append(t)
	j = json.dumps(rowarray_list)
	f = open(rowarrays_file,'w')
	print >> f, j

def genSKIDbuysell(SKID='TX',Institute='外資及陸資'):
#外資及陸資					future_SKID_foreign
#自營商 					future_SKID_brokerage
#SKType='0' '交易人' 		future_SKID_0
#SKType='1' '特定法人' 	future_SKID_1
#SKType='2' '非特定法人'	future_SKID_2
    for case in switch(Institute):
    if case('外資及陸資'):
		sqlquery= 'SELECT SKID,tDate,10Buy,10Sell FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID=\'%s\' and SKType='1' limit 5;' % (SKID)
		rowarrays_file = 'future_%s_foreign.tw.json' % (SKID)
        break
    if case('自營商'):
		sqlquery= 'SELECT SKID,tDate,10Buy,10Sell FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID=\'%s\' and SKType='1' limit 5;' % (SKID)
		rowarrays_file = 'future_unsettle_brokerage.tw.json'
        break
    if case('交易人'):
		sqlquery= 'SELECT SKID,tDate,10Buy,10Sell FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID=\'%s\' and SKType='0' limit 5;' % (SKID)
		rowarrays_file = 'future_%s_foreign.tw.json' % (SKID)
        break
    if case('特定法人'):
		sqlquery= 'SELECT SKID,tDate,10Buy,10Sell FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID=\'%s\' and SKType='1' limit 5;' % (SKID)
		rowarrays_file = 'future_%s_1.tw.json' % (SKID)
        break
    if case('非特定法人'): 
		sqlquery= 'SELECT SKID,tDate,10Buy,10Sell FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID=\'%s\' and SKType='2' limit 5;' % (SKID)
		rowarrays_file = 'future_%s_2.tw.json' % (SKID)
		break
	cursor.execute(sqlquery)
	rows = cursor.fetchall()
	# Convert query to row arrays
	rowarray_list = []
	for row in rows:
		t = (str(row[1]),float(row[2]))
		rowarray_list.append(t)
	j = json.dumps(rowarray_list)
	f = open(rowarrays_file,'w')
	print >> f, j
	
def genbuysell(Institute='外資及陸資'):
#外資及陸資					future_SKID_foreign
#自營商 					future_SKID_brokerage
#SKType='0' '交易人' 		future_SKID_0
#SKType='1' '特定法人' 	future_SKID_1
#SKType='2' '非特定法人'	future_SKID_2
    for case in switch(Institute):
    if case('外資及陸資'):
		sqlquery= 'select Institute,tDate,Buy,Short from institute_future_summary where  tDate>ADDDATE(now(),-14) and Institute=\'%s\';' % (Institute)
		rowarrays_file = 'future_foreign.tw.json' 
        break
    if case('自營商'):
		sqlquery= 'select Institute,tDate,Buy,Short from institute_future_summary where  tDate>ADDDATE(now(),-14) and Institute=\'%s\';' % (Institute)
		rowarrays_file = 'future_brokerage.tw.json'
        break
    if case('投信'):
		sqlquery= 'select Institute,tDate,Buy,Short from institute_future_summary where  tDate>ADDDATE(now(),-14) and Institute=\'%s\';' % (Institute)
		rowarrays_file = 'future_brokerage.tw.json'
        break
    if case('三大法人'):
		sqlquery= 'SELECT SKID,tDate,10Buy,10Sell FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID=\'%s\' and SKType='1' limit 5;' % (Institute)
		rowarrays_file = 'future_Institute.tw.json' 
        break
    if case(): # default 
		sqlquery= 'SELECT SKID,tDate,10Buy,10Sell FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID=\'%s\' and SKType='2' limit 5;' % ('三大法人')
		rowarrays_file = 'future_Institute.tw.json' 
		break
	cursor.execute(sqlquery)
	rows = cursor.fetchall()
	# Convert query to row arrays
	rowarray_list = []
	for row in rows:
		t = (str(row[1]),float(row[2]))
		rowarray_list.append(t)
	j = json.dumps(rowarray_list)
	f = open(rowarrays_file,'w')
	print >> f, j
genUnSettle(Institute='外資及陸資')
genUnSettle(Institute='自營商')
genUnSettle(Institute='交易人')
genUnSettle(Institute='特定法人')
genUnSettle(Institute='非特定法人')
#future_10buysell
#############################################################################################################
cursor.execute("""
             SELECT SKID,tDate,10Buy,10Sell FROM institute_future_10 where  tDate>ADDDATE(now(),-14) and SKID='TX' and SKType='1' limit 5;
""")

rows = cursor.fetchall()

# Convert query to row arrays
rowarray_list = []
for row in rows:
    t = (str(row[1]),float(row[2]),float(row[3]))
    rowarray_list.append(t)

j = json.dumps(rowarray_list)
rowarrays_file = 'future10_10buysell.tw.json'
f = open(rowarrays_file,'w')
print >> f, j

#外資及陸資 買賣超;
cursor.execute("""
             select Institute,tDate,Buy,Short from institute_future_summary where  tDate>ADDDATE(now(),-14) and Institute='外資及陸資';""")

rows = cursor.fetchall()

# Convert query to row arrays
rowarray_list = []
for row in rows:
    t = (str(row[1]),float(row[2]),float(row[3]))
    rowarray_list.append(t)

j = json.dumps(rowarray_list)
rowarrays_file = 'future_buysell_foreign.tw.json'
f = open(rowarrays_file,'w')
print >> f, j

#投信;
cursor.execute("""
             select Institute,tDate,Buy,Short from institute_future_summary where  tDate>ADDDATE(now(),-14) and Institute='投信';""")

rows = cursor.fetchall()

# Convert query to row arrays
rowarray_list = []
for row in rows:
    t = (str(row[1]),float(row[2]),float(row[3]))
    rowarray_list.append(t)

j = json.dumps(rowarray_list)
rowarrays_file = 'future_buysell_fund.tw.json'
f = open(rowarrays_file,'w')
print >> f, j

#自營商;
cursor.execute("""
             select Institute,tDate,Buy,Short from institute_future_summary where  tDate>ADDDATE(now(),-14) and Institute='自營商';""")

rows = cursor.fetchall()

# Convert query to row arrays
rowarray_list = []
for row in rows:
    t = (str(row[1]),float(row[2]),float(row[3]))
    rowarray_list.append(t)

j = json.dumps(rowarray_list)
rowarrays_file = 'future_buysell_brokerage.tw.json'
f = open(rowarrays_file,'w')
print >> f, j

cursor.close()
