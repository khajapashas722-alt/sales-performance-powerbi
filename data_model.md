# Power BI Star Schema Data Model: Sales Performance

The Sales Performance dashboard is engineered around an industry-standard **Star Schema** to ensure high query performance, clean filter propagation, and intuitive DAX authoring.

```mermaid
erDiagram
    DIM_CUSTOMER ||--o{ FACT_SALES : filters
    DIM_PRODUCT ||--o{ FACT_SALES : filters
    DIM_LOCATION ||--o{ FACT_SALES : filters
    DIM_DATE ||--o{ FACT_SALES : filters

    FACT_SALES {
        int Row_ID PK
        string Order_ID
        date Order_Date FK
        date Ship_Date
        string Ship_Mode
        string Customer_ID FK
        string Product_ID FK
        string Postal_Code FK
        decimal Sales
        int Quantity
        decimal Discount
        decimal Profit
    }

    DIM_CUSTOMER {
        string Customer_ID PK
        string Customer_Name
        string Segment
    }

    DIM_PRODUCT {
        string Product_ID PK
        string Category
        string Sub_Category
        string Product_Name
    }

    DIM_LOCATION {
        string Postal_Code PK
        string City
        string State
        string Region
        string Country
    }

    DIM_DATE {
        date Date PK
        int Year
        int MonthNumber
        string MonthName
        string YearMonth
        string Quarter
        int DayOfWeek
    }
```

---

## Relationship Specifications
1. **`Dim_Customer[Customer_ID]` $\xrightarrow{1:M}$ `Fact_Sales[Customer_ID]`**
   - Cardinality: One-to-Many ($1:*$)
   - Cross-filter direction: Single (Dimension filters Fact)
2. **`Dim_Product[Product_ID]` $\xrightarrow{1:M}$ `Fact_Sales[Product_ID]`**
   - Cardinality: One-to-Many ($1:*$)
   - Cross-filter direction: Single
3. **`Dim_Location[Postal_Code]` $\xrightarrow{1:M}$ `Fact_Sales[Postal_Code]`**
   - Cardinality: One-to-Many ($1:*$)
   - Cross-filter direction: Single
4. **`Dim_Date[Date]` $\xrightarrow{1:M}$ `Fact_Sales[Order_Date]`**
   - Cardinality: One-to-Many ($1:*$)
   - Cross-filter direction: Single (Marked as Official Date Table in Power BI)
