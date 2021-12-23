-- Create tables to load in our csvs
create table DailyData(
    date datetime,
    volume int,
    open decimal(10,2),
    high decimal(10,2),
    low decimal(10,2),
    close decimal(10,2),
    adjclose decimal(10,2),
    symbol char(5),
    primary key(symbol, date)
);

create table YearlyData(
	symbol char(5),
  	revenue int,
  	revenueGrowth decimal(3,3),
  	netIncome int,
  	eps decimal(3,3),
  	freeCashFlowMargin decimal(3,3),
  	netProfitMargin decimal(3,3),
  	currentRatio decimal(3,3),
  	returnOnEquity decimal(3,3),
  	PEratio decimal(10,4),
  	revenuePerShare decimal(10,4),
  	marketCap int,
  	PEratio2 decimal(10,4),
  	dividendYield decimal(3,3),
  	ROIC decimal(3,3),
  	3yrRevenueGrowth decimal(3,3),
  	year int,
  	primary key(symbol,year)
);

create table Company(
	symbol char(5),
  	name varchar(100),
  	sector varchar(100),
  	industry varchar(100),
  	summaryQuote varchar(100),
  	CEOAge int default NULL,
  	CEOName varchar(100),
  	City varchar(100),
  	stateCountry varchar(100),
  	fiscalDateEnd varchar(100),
  	employees int default NULL,
  	yearFounded int default NULL,
  	dateFounded varchar(100),
  	primary key(symbol)
);

create table Comments(
    symbol char(5) NOT NULL,
    commentID int NOT NULL AUTO_INCREMENT,
  	commentText varchar(500),
  	date datetime,
  	primary key(commentID)
);

create table AnalystInfo(
  articleID int NOT NULL,
  headline varchar(250),
  date datetime,
  symbol char(5),
  primary key(articleID)
);

-- ADD foreign keys
ALTER TABLE DailyData
ADD FOREIGN KEY (symbol) REFERENCES Company(symbol);

ALTER TABLE AnalystInfo
ADD FOREIGN KEY (symbol) REFERENCES Company(symbol);

ALTER TABLE YearlyData
ADD FOREIGN KEY (symbol) REFERENCES Company(symbol);

ALTER TABLE Comments
ADD FOREIGN KEY (symbol) REFERENCES Company(symbol);

-- Load in the csvs into our table
load data infile '/var/lib/mysql-files/18-Stocks/fh_5yrs.csv' ignore into table DailyData
character set latin1
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data infile '/var/lib/mysql-files/Group61/yearlyData.csv' ignore into table YearlyData
character set latin1
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;


load data infile '/var/lib/mysql-files/Group61/company.csv' ignore into table Company
character set latin1
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;


load data infile '/var/lib/mysql-files/18-Stocks/analyst_ratings_processed.csv' ignore into table AnalystInfo
character set latin1
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;



-- Company - City - Country Relation
create table StateCountry(
	stateCountryID int not null auto_increment,
  	countryName varchar(100),
  	primary key(stateCountryID)
);

create table City(
	cityID int not null auto_increment,
  	cityName varchar(100),
  	primary key(cityID)
);

create table CityInCountry(
	stateCountryID int,
  	cityID int,
  	primary key(stateCountryID, cityID)
);

create table CompanyInCity(
	cityID int,
  	symbol char(5),
  	primary key(cityID, symbol)
);


-- CEO - Company relation
create table CEO(
	ceoID int not null auto_increment,
  	name varchar(100),
  	age int,
  	primary key(ceoID)
);

create table CEOruns(
	ceoID int,
  	symbol char(5),
  	primary key(ceoID, symbol)
);

-- Industry - Sector - Company Relation
create table Sector(
	sectorID int not null auto_increment,
  	sectorName varchar(100),
  	primary key(sectorID)
);

create table Industry(
	industryID int not null auto_increment,
  	industryName varchar(100),
  	primary key(industryID)
);

create table CompanyInIndustry(
	industryID int,
  	symbol char(5),
  	primary key(industryID, symbol)
);

create table IndustryInSector(
	sectorID int,
  	industryID int,
	primary key(sectorID, industryID)
);


----------------------------------------------------
-- CITY - COUNTRY
insert into City(cityName) select distinct city from Company;
insert into StateCountry(countryName) select distinct stateCountry from Company;

insert into CityInCountry (cityID, stateCountryID) select distinct cityID, stateCountryID from City inner join Company on Company.city = City.cityName inner join StateCountry on Company.stateCountry = StateCountry.countryName;
insert into CompanyInCity (cityID, symbol) select distinct cityID, symbol from City inner join Company on Company.city = City.cityName;


-- CEO
insert into CEO(name, age) select distinct CEOName, CEOAge from Company;
insert into CEOruns(ceoID, symbol) select distinct ceoID, symbol from CEO inner join Company on Company.CEOName = CEO.name;


-- INDUSTRY - SECTOR 
insert into Industry(industryName) select distinct industry from Company;
insert into Sector(sectorName) select distinct sector from Company;

insert into IndustryInSector (industryID, sectorID) select distinct industryID, sectorID from Sector inner join Company on Company.sector = Sector.sectorName inner join Industry on Company.industry = Industry.industryName;
insert into CompanyInIndustry (industryID, symbol) select distinct industryID, symbol from Industry inner join Company on Company.industry = Industry.industryName;


-- Drop Company attributes
alter table Company drop column sector;
alter table Company drop column industry;
alter table Company drop column CEOAge;
alter table Company drop column CEOName;
alter table Company drop column City;
alter table Company drop column stateCountry;
alter table Company drop column dateFounded;


-- Add check constraints on tables
ALTER TABLE Company
MODIFY symbol char(5) NOT NULL;

ALTER TABLE Company
MODIFY name varchar(100) NOT NULL;

ALTER TABLE Company
ADD CHECK (employees >= 0);



ALTER TABLE Comments
MODIFY symbol char(5) NOT NULL;

ALTER TABLE Comments
MODIFY commentText varchar(500) NOT NULL;


ALTER TABLE AnalystInfo
MODIFY symbol char(5) NOT NULL;

ALTER TABLE AnalystInfo
MODIFY headline varchar(250) NOT NULL;

ALTER TABLE YearlyData
MODIFY symbol char(5) NOT NULL;

ALTER TABLE YearlyData 
MODIFY year int NOT NULL;

ALTER TABLE YearlyData
ADD CHECK (year >= 1970);

ALTER TABLE CEO
ADD CHECK (age >= 0);

ALTER TABLE DailyData
MODIFY symbol char(5) NOT NULL;

ALTER TABLE DailyData
MODIFY date datetime NOT NULL;

ALTER TABLE DailyData ADD CHECK (volume >= 0);

ALTER TABLE DailyData ADD CHECK (open >= 0);

ALTER TABLE DailyData ADD CHECK (high >= 0);

ALTER TABLE DailyData ADD CHECK (low >= 0);

ALTER TABLE DailyData ADD CHECK (close >= 0);

ALTER TABLE DailyData ADD CHECK (adjclose >= 0);