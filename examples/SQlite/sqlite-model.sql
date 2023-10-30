/*==============================================================*/
/* Table: "Customer"                                               */
/*==============================================================*/
CREATE TABLE Customer (
    ID INTEGER PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT,
    City TEXT,
    Country TEXT,
    Phone TEXT
);

/*==============================================================*/
/* Index: IndexCustomerName                                     */
/*==============================================================*/
create index IndexCustomerName on Customer (
LastName ASC,
FirstName ASC
);

/*==============================================================*/
/* Table: "Order"                                               */
/*==============================================================*/

CREATE TABLE "Order" (
    ID INTEGER PRIMARY KEY,
    OrderDate DATE NOT NULL,
    OrderNumber TEXT,
    CustomerID INTEGER,
    TotalAmount REAL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(ID)
);

/*==============================================================*/
/* Index: IndexOrderCustomerId                                  */
/*==============================================================*/
create index IndexOrderCustomerId on "Order" (
CustomerId ASC
);


/*==============================================================*/
/* Index: IndexOrderOrderDate                                   */
/*==============================================================*/
create index IndexOrderOrderDate on "Order" (
OrderDate ASC
);


/*==============================================================*/
/* Table: "OrderItem"                                               */
/*==============================================================*/

CREATE TABLE OrderItem (
    ID INTEGER PRIMARY KEY,
    OrderID INTEGER,
    ProductID INTEGER,
    UnitPrice REAL,
    Quantity INTEGER,
    FOREIGN KEY (OrderID) REFERENCES "Order"(ID),
    FOREIGN KEY (ProductID) REFERENCES Product(ID)
);


/*==============================================================*/
/* Index: IndexOrderItemOrderId                                 */
/*==============================================================*/
create index IndexOrderItemOrderId on OrderItem (
OrderId ASC
);


/*==============================================================*/
/* Index: IndexOrderItemProductId                               */
/*==============================================================*/
create index IndexOrderItemProductId on OrderItem (
ProductId ASC
);

/*==============================================================*/
/* Table: "Supplier"                                               */
/*==============================================================*/
CREATE TABLE Supplier (
    ID INTEGER PRIMARY KEY,
    CompanyName TEXT,
    ContactName TEXT,
    City TEXT,
    Country TEXT,
    Phone TEXT,
    Fax TEXT
);

/*==============================================================*/
/* Index: IndexSupplierName                                     */
/*==============================================================*/
create index IndexSupplierName on Supplier (
CompanyName ASC
);


/*==============================================================*/
/* Index: IndexSupplierCountry                                  */
/*==============================================================*/
create index IndexSupplierCountry on Supplier (
Country ASC
);

/*==============================================================*/
/* Table: "Product"                                               */
/*==============================================================*/

CREATE TABLE Product (
    ID INTEGER PRIMARY KEY,
    ProductName TEXT,
    SupplierID INTEGER,
    UnitPrice REAL,
    Package TEXT,
    IsDiscontinued INTEGER,
    FOREIGN KEY (SupplierID) REFERENCES Supplier (ID)
);


/*==============================================================*/
/* Index: IndexProductSupplierId                                */
/*==============================================================*/
create index IndexProductSupplierId on Product (
SupplierId ASC
);

/*==============================================================*/
/* Index: IndexProductName                                      */
/*==============================================================*/
create index IndexProductName on Product (
ProductName ASC
);







