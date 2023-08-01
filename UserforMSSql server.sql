USE [master]
GO

CREATE LOGIN [etl] WITH PASSWORD=N'etlpass', DEFAULT_DATABASE=[AdventureWorksDW2019], DEFAULT_LANGUAGE=[us_english], CHECK_EXPIRATION=ON, CHECK_POLICY=ON
GO
alter login etl with password=N'etlpass'

use AdventureWorksDW2019
go 
CREATE USER [etl] FOR LOGIN [etl] WITH DEFAULT_SCHEMA=[dbo]
go
Alter ROLE [db_datareader] add member [etl]
go

use master 
go
grant connect sql to [etl]

