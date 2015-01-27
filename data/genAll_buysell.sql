-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`yhuang`@`%` PROCEDURE `genALL_buysell`()
BEGIN
	SELECT '臺股現貨' as SKName,tDate,Institute,'買' as '交易類別',IFNULL(Buy,0) as '金額' FROM marketdata.institute_tse_summary where  tDate>ADDDATE(now(),-14) and Institute='外資及陸資'
	union 
	SELECT '臺股現貨' as SKName,tDate,Institute,'賣' as '交易類別',IFNULL(Sell,0) as '金額' FROM marketdata.institute_tse_summary where  tDate>ADDDATE(now(),-14) and Institute='外資及陸資'
	union
	SELECT '臺股現貨' as SKName,tDate,Institute,'買' as '交易類別',IFNULL(Buy,0) as '金額' FROM marketdata.institute_tse_summary where  tDate>ADDDATE(now(),-14) and Institute='投信'
	union 
	SELECT '臺股現貨' as SKName,tDate,Institute,'賣' as '交易類別',IFNULL(Sell,0) as '金額' FROM marketdata.institute_tse_summary where  tDate>ADDDATE(now(),-14) and Institute='投信'
	union
	SELECT '臺股現貨' as SKName,tDate,Institute,'買' as '交易類別',IFNULL(Buy,0) as '金額'  FROM marketdata.institute_tse_summary where  tDate>ADDDATE(now(),-14) and Institute='自營商(自行買賣)'
	union 
	SELECT '臺股現貨' as SKName,tDate,Institute,'賣' as '交易類別',IFNULL(Sell,0) as '金額' FROM marketdata.institute_tse_summary where  tDate>ADDDATE(now(),-14) and Institute='自營商(自行買賣)'
	union
	SELECT '臺股現貨' as SKName,tDate,Institute,'買' as '交易類別',IFNULL(Buy,0) as '金額' FROM marketdata.institute_tse_summary where  tDate>ADDDATE(now(),-14) and Institute='自營商(避險)'
	union 
	SELECT '臺股現貨' as SKName,tDate,Institute,'賣' as '交易類別',IFNULL(Sell,0) as '金額' FROM marketdata.institute_tse_summary where  tDate>ADDDATE(now(),-14) and Institute='自營商(避險)'
	union
	SELECT '臺股現貨' as SKName,tDate,'三大法人','買' as '交易類別',IFNULL(Buy,0) as '金額' FROM marketdata.institute_tse_summary where  tDate>ADDDATE(now(),-14) and Institute='合計'
	union 
	SELECT '臺股現貨' as SKName,tDate,'三大法人','賣' as '交易類別',IFNULL(Sell,0) as '金額' FROM marketdata.institute_tse_summary where  tDate>ADDDATE(now(),-14) and Institute='合計'
	union
	SELECT '臺股現貨' as SKName,tDate,'融資','買' as '交易類別',IFNULL(Buy,0) as '金額' FROM marketdata.institute_tse_credict_summary where  tDate>ADDDATE(now(),-14) and substring(Type,1,4)='融資金額'
	union
	SELECT '臺股現貨' as SKName,tDate,'融資','賣' as '交易類別',IFNULL(Sell,0) as '金額' FROM marketdata.institute_tse_credict_summary where  tDate>ADDDATE(now(),-14) and substring(Type,1,4)='融資金額'
	union
	SELECT '臺股現貨' as SKName,tDate,'融券','買' as '交易類別',IFNULL(Buy,0) as '金額' FROM marketdata.institute_tse_credict_summary where  tDate>ADDDATE(now(),-14) and Type='融券(交易單位)'
	union
	SELECT '臺股現貨' as SKName,tDate,'融券','賣' as '交易類別',IFNULL(Sell,0) as '金額' FROM marketdata.institute_tse_credict_summary where  tDate>ADDDATE(now(),-14) and Type='融券(交易單位)'
	union
	# 台指期是指 多單 空單 增減
	select SKName,tDate,'自營商' as '法人','買' as '交易類別',IFNULL(Buy,0) as '金額' FROM  marketdata.institute_future_contract where  tDate>ADDDATE(now(),-14) and Institute='自營商' and substring(SKName,1,CHAR_LENGTH(trim('臺股期貨')))='臺股期貨' 
	union 
	select SKName,tDate,'自營商' as '法人','賣' as '交易類別',IFNULL(Short,0) as '金額' FROM  marketdata.institute_future_contract where  tDate>ADDDATE(now(),-14) and Institute='自營商' and substring(SKName,1,CHAR_LENGTH(trim('臺股期貨')))='臺股期貨' 
	union
	select SKName,tDate,'自營商' as '法人','買' as '交易類別',IFNULL(Buy,0) as '金額' FROM  marketdata.institute_future_contract where  tDate>ADDDATE(now(),-14) and Institute='外資及陸資' and substring(SKName,1,CHAR_LENGTH(trim('臺股期貨')))='臺股期貨' 
	union 
	select SKName,tDate,'自營商' as '法人','賣' as '交易類別',IFNULL(Short,0) as '金額' FROM  marketdata.institute_future_contract where  tDate>ADDDATE(now(),-14) and Institute='外資及陸資' and substring(SKName,1,CHAR_LENGTH(trim('臺股期貨')))='臺股期貨' 
	union
	SELECT SKName,tDate,'前十大交易人' as '法人','買' as '交易類別',IFNULL(10Buy,0) as '金額' FROM marketdata.institute_future_10 where  tDate>ADDDATE(now(),-14) and substring(SKName,1,CHAR_LENGTH(trim('臺股期貨')))='臺股期貨' and SKType='0' 
	union
	SELECT SKName,tDate,'前十大交易人' as '法人','賣' as '交易類別',IFNULL(10Sell,0) as '金額' FROM marketdata.institute_future_10 where  tDate>ADDDATE(now(),-14) and substring(SKName,1,CHAR_LENGTH(trim('臺股期貨')))='臺股期貨' and SKType='0' 
	union
	SELECT SKName,tDate,'前十大交易特定法人' as '法人','買' as '交易類別',IFNULL(10Buy,0) as '金額' FROM marketdata.institute_future_10 where  tDate>ADDDATE(now(),-14) and substring(SKName,1,CHAR_LENGTH(trim('臺股期貨')))='臺股期貨' and SKType='1' 
	union
	SELECT SKName,tDate,'前十大交易特定法人' as '法人','賣' as '交易類別',IFNULL(10Sell,0) as '金額' FROM marketdata.institute_future_10 where  tDate>ADDDATE(now(),-14) and substring(SKName,1,CHAR_LENGTH(trim('臺股期貨')))='臺股期貨' and SKType='1' 
	union
	SELECT SKName,tDate,'前十大交易非特定法人' as '法人','買' as '交易類別',IFNULL(10Buy,0) as '金額' FROM marketdata.institute_future_10 where  tDate>ADDDATE(now(),-14) and substring(SKName,1,CHAR_LENGTH(trim('臺股期貨')))='臺股期貨' and SKType='2' 
	union
	SELECT SKName,tDate,'前十大交易非特定法人' as '法人','賣' as '交易類別',IFNULL(10Sell,0) as '金額' FROM marketdata.institute_future_10 where  tDate>ADDDATE(now(),-14) and substring(SKName,1,CHAR_LENGTH(trim('臺股期貨')))='臺股期貨' and SKType='2' 
	union
	SELECT '臺指選擇權CALL',tDate,Institute as '法人','買' as '交易類別',IFNULL(Buy_Amt,0)   as '金額' FROM marketdata.institute_option_summary where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指選擇權' and trim(SKBuySell)='CALL'
	union
	SELECT '臺指選擇權CALL',tDate,Institute as '法人','賣' as '交易類別',IFNULL(Short_Amt,0) as '金額' FROM marketdata.institute_option_summary where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指選擇權' and trim(SKBuySell)='CALL'
	union
	SELECT '臺指選擇權PUT',tDate,Institute as '法人','買' as '交易類別',IFNULL(Buy_Amt,0)   as '金額' FROM marketdata.institute_option_summary where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指選擇權' and trim(SKBuySell)='PUT'
	union
	SELECT '臺指選擇權PUT',tDate,Institute as '法人','賣' as '交易類別',IFNULL(Short_Amt,0) as '金額' FROM marketdata.institute_option_summary where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指選擇權' and trim(SKBuySell)='PUT'
	union
	SELECT '臺指選擇權CALL',tDate,'前十大交易人' as '法人','賣' as '交易類別',IFNULL(10Sell,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='買權' and SKType='0'
	union
	SELECT '臺指選擇權CALL',tDate,'前十大交易特定法人' as '法人','買' as '交易類別',IFNULL(10Buy,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='買權' and SKType='1'
	union
	SELECT '臺指選擇權CALL',tDate,'前十大交易特定法人' as '法人','賣' as '交易類別',IFNULL(10Sell,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='買權' and SKType='1'
	union
	SELECT '臺指選擇權CALL',tDate,'前十大交易非特定法人' as '法人','買' as '交易類別',IFNULL(10Buy,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='買權' and SKType='2'
	union
	SELECT '臺指選擇權CALL',tDate,'前十大交易非特定法人' as '法人','賣' as '交易類別',IFNULL(10Sell,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='買權' and SKType='2'
	union
	SELECT '臺指選擇權PUT',tDate,'前十大交易人' as '法人','買' as '交易類別',IFNULL(10Buy,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='賣權' and SKType='0'
	union
	SELECT '臺指選擇權PUT',tDate,'前十大交易人' as '法人','賣' as '交易類別',IFNULL(10Sell,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='賣權' and SKType='0'
	union
	SELECT '臺指選擇權PUT',tDate,'前十大交易特定法人' as '法人','買' as '交易類別',IFNULL(10Buy,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='賣權' and SKType='1'
	union
	SELECT '臺指選擇權PUT',tDate,'前十大交易特定法人' as '法人','賣' as '交易類別',IFNULL(10Sell,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='賣權' and SKType='1'
	union
	SELECT '臺指選擇權PUT',tDate,'前十大交易非特定法人' as '法人','買' as '交易類別',IFNULL(10Buy,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='賣權' and SKType='2'
	union
	SELECT '臺指選擇權PUT',tDate,'前十大交易非特定法人' as '法人','賣' as '交易類別',IFNULL(10Sell,0) as '金額' FROM marketdata.institute_option_10 where  tDate>ADDDATE(now(),-14) and trim(SKName)='臺指' and trim(SKBuySell)='賣權' and SKType='2';
END