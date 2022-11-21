drop database if exists QAProject;
create database if not exists QAProject;
use QAProject;
DROP TABLE if exists Customer cascade;
DROP TABLE if exists Addresses cascade;
DROP TABLE if exists PaymentInfo cascade;
DROP TABLE if exists Purchases cascade;
DROP TABLE if exists Guest cascade;
DROP TABLE if exists OrderLineItem cascade;
DROP TABLE if exists CartItem cascade;
DROP TABLE if exists Inventory cascade;
DROP TABLE if exists Shoes cascade;

CREATE TABLE Shoes (
	ShoeID		INT		PRIMARY KEY,
    ShoeName	VARCHAR(20)	NOT NULL,
    Cost		FLOAT(6)	NOT NULL,
    CustPrice	FLOAT(6)	NOT NULL,
    Brand 		ENUM('Nike','Addidas','Other'),
    ShoeType	ENUM('Tennis','Running','Other'),
    Color		ENUM('Red','Blue',''),
    Gender		ENUM('Male','Female')
    -- PicturePath 
    );

CREATE TABLE Inventory (
	StockID		INT		PRIMARY KEY,
    ShoeID		INT		NOT NULL,
    Size		FLOAT(3)	NOT NULL,
    Quantity	INT		NOT NULL,
CONSTRAINT FK_Inventory FOREIGN KEY (ShoeID) REFERENCES Shoes(ShoeID));

CREATE TABLE Customer (
	UserID		INT		NOT NULL AUTO_INCREMENT,
    FirstName	VARCHAR(10)		NOT NULL,
    LastName	VARCHAR(15)		NOT NULL,
    email		VARCHAR(25)		NOT NULL,
    UserPW		VARCHAR(64)		NOT NULL,
    PRIMARY KEY(UserID)
    );

CREATE TABLE CartItem (
	UserID		INT			NOT NULL,
    StockID		INT			NOT NULL,
    Quantity	INT			NOT NULL,
CONSTRAINT PK_CartItem PRIMARY KEY (UserID, StockID),
CONSTRAINT FK1_CartItem FOREIGN KEY (UserID) REFERENCES Customer(UserID),
CONSTRAINT FK2_CartItem FOREIGN KEY (StockID) REFERENCES Inventory(StockID));

CREATE TABLE Guest (
	GuestID		INT			PRIMARY KEY,
    email		VARCHAR(35)	NOT NULL
    );

CREATE TABLE Addresses (
	AddressID	INT				PRIMARY KEY,
    UserID		INT				NOT NULL,
	Street1		VARCHAR(30)		NOT NULL,
    Street2		VARCHAR(30)		NOT NULL,
    City		VARCHAR(25)		NOT NULL,
    State		VARCHAR(15)		NOT NULL,
    Purpose		ENUM("Shipping", "PaymentInfo", "Both") NOT NULL,
CONSTRAINT FK_Addresses FOREIGN KEY (UserID) REFERENCES Customer(UserID));

CREATE TABLE PaymentInfo (
	PaymentID	INT				PRIMARY KEY,
    AddressID	INT				NOT NULL,
    UserID		INT,
    NameOnCard	VARCHAR(35)		NOT NULL,
    CardNum		INT				NOT NULL,
    CVC			INT				NOT NULL,
    ExDate		DATE			NOT NULL,
CONSTRAINT FK1_PaymentInfo FOREIGN KEY (AddressID) REFERENCES Addresses(AddressID),
CONSTRAINT FK2_PaymentInfo FOREIGN KEY (UserID) REFERENCES Customer(UserID));

CREATE TABLE Purchases (
	PurchaseID	INT			PRIMARY KEY,
    UserID		INT,
    GuestID		INT,
    AddressID	INT			NOT NULL,
    PaymentID	INT			NOT NULL,
    ShippingStatus ENUM("To Ship", "Ready to Ship", "Shipping", "Delivered") NOT NULL,
    OrderDate	DATETIME	NOT NULL,
    OrderTotal	FLOAT(8)	NOT NULL,
CONSTRAINT FK1_Purchases FOREIGN KEY (UserID) REFERENCES Customer(UserID),
CONSTRAINT FK2_Purchases FOREIGN KEY (GuestID) REFERENCES Guest(GuestID),
CONSTRAINT FK3_Purchases FOREIGN KEY (AddressID) REFERENCES Addresses(AddressID),
CONSTRAINT FK4_Purchases FOREIGN KEY (PaymentID) REFERENCES PaymentInfo(PaymentID));

CREATE TABLE OrderLineItem (
	PurchaseID	INT		NOT NULL,
    StockID		INT		NOT NULL,
    Quantity	INT		NOT NULL,
CONSTRAINT PK_OLI PRIMARY KEY (PurchaseID, StockID),
CONSTRAINT FK1_OLI FOREIGN KEY (PurchaseID) REFERENCES Purchases(PurchaseID),
CONSTRAINT FK2_OLI FOREIGN KEY (StockID) REFERENCES Inventory(StockID));
