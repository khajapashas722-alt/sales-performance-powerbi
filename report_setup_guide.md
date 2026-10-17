# Power BI Setup & Implementation Guide: Sales Performance Dashboard

This guide provides exact, step-by-step instructions to assemble, configure, and publish the Sales Performance report in **Power BI Desktop**.

---

## Step 1: Ingest Data via Power Query
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Ingest the following CSV files from the `data/` folder:
   - `Fact_Sales.csv`
   - `Dim_Customer.csv`
   - `Dim_Product.csv`
   - `Dim_Location.csv`
4. Click **Transform Data** to launch the Power Query Editor.

---

## Step 2: Create Dynamic Calendar Table (`Dim_Date`)
1. In Power Query, click **New Source** -> **Blank Query**.
2. Rename the query to `Dim_Date`.
3. Click **Advanced Editor** in the Home ribbon.
4. Replace the default snippet with **Script 1** from `power_query_transformations.m`.
5. Click **Done**.
6. Select column `Short Month` -> Click **Sort by Column** -> Choose `Month Number`.
7. Click **Close & Apply** to load the model into Power BI.

---

## Step 3: Establish Star Schema Relationships
1. In Power BI Desktop, navigate to the **Model View** (left-hand icon).
2. Create the following One-to-Many ($1:*$) single-directional relationships:
   - `Dim_Customer[Customer ID]` $\rightarrow$ `Fact_Sales[Customer ID]`
   - `Dim_Product[Product ID]` $\rightarrow$ `Fact_Sales[Product ID]`
   - `Dim_Location[Postal Code]` $\rightarrow$ `Fact_Sales[Postal Code]`
   - `Dim_Date[Date]` $\rightarrow$ `Fact_Sales[Order Date]`
3. Right-click on table `Dim_Date` -> Select **Mark as Date Table** -> Pick column `Date`.

---

## Step 4: Create DAX Measures Table
1. On the Home ribbon, click **Enter Data**.
2. Set Table Name to `_Measures` and click **Load**.
3. Right-click `_Measures` -> Select **New Measure**.
4. Copy and paste each measure formula from `dax_measures.dax`:
   - `Total Revenue`, `Total Profit`, `Profit Margin %`, `Total Units Sold`, `Total Orders`, `Average Order Value (AOV)`.
   - Time intelligence: `Revenue Prior Year (PY)`, `YoY Revenue Growth %`.
   - Set formatting: Currency (`$`) for Revenue, Percentage (`%`) with 1 decimal for Margin and Growth.
5. Delete the blank `Column1` from `_Measures` so the table displays a calculator icon at the top of the Data pane.

---

## Step 5: Construct Report Pages & Visual Layout

### Page 1: Executive Sales Overview (Canvas Size: 16:9 Standard)
- **Top Slicer Bar (Y: 10, Height: 50)**:
  - Slicer 1: `Dim_Date[Year]` (Tile / Horizontal orientation).
  - Slicer 2: `Dim_Location[Region]` (Dropdown).
  - Slicer 3: `Dim_Customer[Segment]` (Dropdown).
- **KPI Card Row (Y: 70, Height: 90)**:
  - Card 1: `[Total Revenue]` (Display Units: Millions or Thousands, e.g. `$2.30M`).
  - Card 2: `[Total Profit]` (e.g. `$286.4K`).
  - Card 3: `[Profit Margin %]` (e.g. `12.5%`).
  - Card 4: `[YoY Revenue Growth %]` (e.g. `+20.4%`).
  - Card 5: `[Average Order Value (AOV)]` (e.g. `$458.61`).
- **Main Visual Area (Left Side, Width: 60%)**:
  - **Line and Clustered Column Chart**:
    - X-Axis: `Dim_Date[Year-Month]`
    - Column Values: `[Total Revenue]`
    - Line Values: `[Total Profit]`
- **Main Visual Area (Right Side, Width: 40%)**:
  - **Donut Chart**: `[Total Revenue]` by `Dim_Location[Region]`.
  - **Clustered Bar Chart**: `[Total Revenue]` and `[Total Profit]` by `Dim_Product[Category]`.

### Page 2: Product & Profitability Matrix
- **Matrix Visual**:
  - Rows: `Dim_Product[Category]`, `Dim_Product[Sub-Category]`
  - Values: `[Total Revenue]`, `[Total Profit]`, `[Profit Margin %]`, `[Average Discount %]`
  - Conditional Formatting: Background color on `[Profit Margin %]` using rules (`>= 15%` Green, `< 0%` Red).
- **Scatter Plot**:
  - X-Axis: `[Average Discount %]`
  - Y-Axis: `[Profit Margin %]`
  - Size: `[Total Revenue]`
  - Legend: `Dim_Product[Category]`
  *(Highlights that discounts above 30% collapse profitability).*

---

## Step 6: Verification Against Excel Benchmark
Validate the loaded model:
- When no filters are selected, `[Total Revenue]` must equal **$2,297,200.86**.
- `[Total Profit]` must equal **$286,397.02**.
- `[Total Orders]` must equal **5,009**.
This confirms 100% mathematical parity across Python, Excel, and Power BI models.
