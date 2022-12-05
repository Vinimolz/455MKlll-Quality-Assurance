INSERT INTO Shoes VALUES(1001, 'SuperSpeed 1000', 55.99, 99.99, 'Nike', 'Running', 'White', 'Male', "nike1.jpg");
INSERT INTO Shoes VALUES(1002, "Fast Girl", 34.99, 74.99, 'Addidas', 'Running', 'Red', 'Female', "adidas.jpg");
INSERT INTO Shoes VALUES(1003, "The Charger", 47.89, 56.99, 'Hoka', 'Tennis', 'Red', 'Female', "hokas.jpg");
INSERT INTO Shoes VALUES(1004, 'The Elusive', 56.78, 89.99, 'Rads', 'Other', 'Blue', 'Male', "rads.jpg");
INSERT INTO Shoes VALUES(1005, 'SuperSpeed 2000', 56.78, 89.99, 'Nike', 'Running', 'White', 'Male', "nike.jpg");

INSERT INTO Inventory VALUES(10001, 1001, 9, 10);
INSERT INTO Inventory VALUES(10002, 1001, 10, 13);
INSERT INTO Inventory VALUES(10003, 1002, 7, 27);
INSERT INTO Inventory VALUES(10004, 1002, 8, 6);
INSERT INTO Inventory VALUES(10005, 1003, 4, 2);
INSERT INTO Inventory VALUES(10006, 1002, 4.5, 3);
INSERT INTO Inventory VALUES(10007, 1004, 10, 10);
INSERT INTO Inventory VALUES(10008, 1005, 12, 8);

-- INSERT INTO Customer VALUES(1, 'Luke', 'Smith', 'csluke@outlook.com', '1234');
-- INSERT INTO Customer VALUES(2, 'Vini', 'Molz', 'vinimolz@gmail.com', '1234');
-- INSERT INTO Customer VALUES(3, 'Donald', 'Trump', 'iamFamous@me.com', '1234');

-- these need to be updated
-- INSERT INTO CartItem VALUES(1, 10001, 1 );
-- INSERT INTO CartItem VALUES(1, 10002, 1 );
-- INSERT INTO CartItem VALUES(2, 10001, 3 );


-- INSERT INTO Guest VALUES(1, 'idontknow@gmail.com');
-- INSERT INTO Guest VALUES(2, 'surprise@gmail.com');

-- INSERT INTO Addresses VALUES(1,1, '6678 Test Ave', '', 'Test City', 'CA', "Both");
-- INSERT INTO Addresses VALUES(2,1, '2 Address Ave', 'Apt 12', 'Test City', 'FL', "Shipping");
-- INSERT INTO Addresses VALUES(3,2, 'Vini''s house St', '', 'Fresno', 'CA', "Shipping" );
-- INSERT INTO Addresses VALUES(4, null, '456 Ghost Ave', 'Apt 56', 'Test City', 'CA', "Shipping");
-- INSERT INTO Addresses VALUES(5, null, '456 Ghost Ave', 'Apt 56', 'Test City', 'CA', "PaymentInfo" );

-- INSERT INTO PaymentInfo VALUES(1,1,1, "Luke Smith", 1234123412341234, 123, "2024-03-01");
-- INSERT INTO PaymentInfo VALUES(2,1,1, "Luke Smith", 4321432143214321, 321, "2025-05-01");
-- INSERT INTO PaymentInfo VALUES(3,5, null, "Mark Atwater", 9999888877776666, 111, "2023-11-01" );


-- INSERT INTO Purchases VALUES(1,1, null,1,1, "Delivered", "2022-11-1 12:32:45", 100.00 );
-- INSERT INTO Purchases VALUES(2,1, null,2,2, "To Ship", "2022-11-30 01:24:56", 100.00);
-- INSERT INTO Purchases VALUES(3, null,1,4,3, "Shipping", "2022-11-30 03:47:18", 100.00 );

-- need to change
-- INSERT INTO OrderLineItem VALUES(1, 10001, 2);
-- INSERT INTO OrderLineItem VALUES(1, 10003, 1);
-- INSERT INTO OrderLineItem VALUES(2, 10001, 1);
-- INSERT INTO OrderLineItem VALUES(3, 10003, 1);
