-- Create Target database.schema.table --
CREATE DATABASE data_lake;

CREATE SCHEMA data_lake.my_app;
CREATE SCHEMA data_lake.elt_metadata;

CREATE TABLE data_lake.my_app.Orders (
 OrderId int,
 OrderStatus varchar(30),
 LastUpdated timestamp
);

CREATE TABLE data_lake.my_app.metadata_load (
 Load_Datetime timestamp,
 BinLog_Max_Pos int,
 Orders_Max_LastUpdated timestamp,
 PRIMARY KEY (Load_Datetime)
);