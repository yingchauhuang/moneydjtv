#產業大分類 ID char(8),
#大分類 Name varvar(50),
#中分類 ID char(8),
#中分類 Name varvar(50),
#簡體大分類名 varvar(50),
#簡體中分類名 varvar(50)


  create procedure [dbo].[spj_MDA00224]  as  
  begin   
  select zb000010, zb000020, zb870020, BKName, (select zb870210 from za870000 where zb870020 = zb000010) C9CName, zb870210   from za000000    join za870000 on zb000010 = zb870040    join (select BKID = zb000010, BKName = zb000020 from za000000) a on zb870020 = BKID    where zb000010 like 'C9%'   order by zb000010  end    
  
  
#Menu 主分類 nvarchar(50),
#MenuMenu次分類 nvarchar(50),
#MenuMenuID varvar(8)
   create procedure [dbo].[spj_MDA00226]  as  begin   select col001, col002, col003   from MBMenu   order by col003  end  
   
   
   
    create procedure [dbo].[spj_MDA00227]   as  
	begin   /* result: 大產業ID, Name */   
	select zb000010, rtrim( zb000020) zb000020   from za000000    where zb000010 like 'C9%'   order by zb000010  
	end  
	
	
#StockID char(8),
#StockName varchar(40),
#Date smalldatetime,
#外資買賣超 int,
#投信買賣超 int,
#自營商買賣超 ,int,
#三大法人買賣超 ,int,
#外資持股比率 decimal(5,2),
#融資餘額 int,
#融資使用率 decimal(5,2),
#融券餘額 int,
#券資比 decdecimal(5,2)
  create procedure [dbo].[spj_MDA02811] (
  @IndustryID char(8) = 'C011010', 
  @Period char(1) = 'D', 
  @StartDate smalldatetime = null, 
  @EndDate smalldatetime = null)  
  as  begin   
  set nocount on   
  declare @IDTbl table (IID varchar(8) primary key)   
  declare @TmpTbl table (js10j010 smalldatetime, js10j020 varchar(8), js10j110 int, js10j130 int, js10j150 int, js10j125 decimal(5,2), primary key (js10j010, js10j020))   
  insert @IDTbl (IID)   select zb956020 from za956000    where zb956030 = @IndustryID and zb956020 like 'AS[0-9]%'    order by zb956020     
  if @StartDate is null   
	begin    
		if @EndDate is null      set @EndDate = (select top 1 js10j010 from jdtws..js10j00d where js10j110 is not null order by js10j010 desc)    
		set @StartDate = @EndDate   
	end   
	else     
		if @EndDate is null      set @EndDate = '2038/1/1'     
		if @Period = 'W'   
			begin    
				if @StartDate > '1950/1/1' and datepart( weekday, @StartDate) > 2     
					set @StartDate = dateadd( day, 2 - datepart( weekday, @StartDate), @StartDate)    
				if @EndDate is not null and datepart( weekday, @EndDate) > 1     
					set @EndDate = dateadd( day, 7 - datepart( weekday, @EndDate), @EndDate)   
			end   
		else 
			if @Period = 'M'   
			begin    
				if day( @StartDate) > 1     
					set @StartDate = dateadd( day, 1 - day( @StartDate), @StartDate)    
					if @EndDate is not null    
						begin     
							set @EndDate = dateadd( month, 1, @EndDate)     
							set @EndDate = dateadd( day, -day( @EndDate), @EndDate)    
						end   
			end     
			declare @ID varchar(8)   
			declare CUR_TmpTbl CURSOR for    
			select IID from @IDTbl     
			open CUR_TmpTbl   
			fetch CUR_TmpTbl into @ID   
			while @@fetch_status = 0   
			begin    
				if @Period = 'D'     
						insert @TmpTbl ( js10j010, js10j020, js10j110, js10j130, js10j150, js10j125)     
						select js10j010, js10j020, js10j110, js10j130, js10j150, js10j125 
						from jdtws..js10j00d 
						where js10j020 = substring( @ID, 3, 6) and js10j010 
						between @StartDate and @EndDate 
						and js10j110 is not null     
				else 
					if @Period = 'W'     
						insert @TmpTbl ( js10j010, js10j020, js10j110, js10j130, js10j150, js10j125)     
						select js10j010, js10j020, js10j110, js10j130, js10j150, js10j125 from jdtws..js10j00w 
						where js10j020 = substring( @ID, 3, 6) and js10j010 
						between @StartDate and @EndDate 
						and js10j110 is not null     
				else 
					if @Period = 'M'     
						insert @TmpTbl ( js10j010, js10j020, js10j110, js10j130, js10j150, js10j125)     
						select js10j010, js10j020, js10j110, js10j130, js10j150, js10j125 from jdtws..js10j00m 
						where js10j020 = substring( @ID, 3, 6) and js10j010 
						between @StartDate and @EndDate 
						and js10j110 is not null       
				fetch CUR_TmpTbl into @ID   
			end   
			close CUR_TmpTbl   
			deallocate CUR_TmpTbl     
			select js10j020, zb000020, js10j010, js10j110, js10j130, js10j150, js10j110 + js10j130 + js10j150, js10j125   
			from @TmpTbl    
			join za000000 on zb000010 = 'AS' + js10j020  
			-- where js10j010 between @StartDate and @EndDate and js10j110 is not null    order by js10j020, js10j010 desc  
  end    