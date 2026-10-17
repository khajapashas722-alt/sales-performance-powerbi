# Sales Performance & Commercial Analytics Dashboard (Power BI)

An enterprise business intelligence data modeling and dashboard project designed in Power BI, implementing a production Star Schema, dynamic Time Intelligence DAX measures, automated Power Query M ingestion, and interactive multi-page reporting.

---

## 1. Project Overview & Business Problem
Commercial sales organizations struggle with fragmented reporting across transactional point-of-sale systems, logistics fulfillment tracking, and regional territories. Without a unified analytical semantic model, business leaders face inconsistent revenue reporting, conflicting KPI definitions, and difficulty evaluating Year-over-Year (YoY) trajectory.

This project delivers a complete enterprise semantic data model and executive report architecture. Designed around a Star Schema connecting 9,994 sales transaction rows to customer, product, location, and date dimensions, this project implements advanced DAX calculations (AOV, Profit Margin, YoY Growth, Time Intelligence) to empower executive decision-making.

> [!NOTE]
> **Environment & Deliverable Documentation**: Power BI Desktop is not installed on this local server environment. In strict adherence to engineering authenticity, this repository provides all underlying dimensional datasets, Power Query M transformation scripts, complete DAX calculation libraries, data modeling schemas, visual wireframes, and exact reproduction instructions to build or inspect the report in Power BI Desktop.

---

## 2. Business Objectives & Analytical Questions
1. **Financial Health & Volume**: What is total commercial gross merchandise value (GMV), net margin %, and unique order volume?
2. **Time-Series Momentum**: How does sales performance compare against Prior Year (PY) benchmarks using Year-over-Year (YoY) time intelligence?
3. **Product Portfolio Dynamics**: Which product sub-categories deliver strong margins versus those that destroy profit due to heavy discounting?
4. **Customer Lifetime Value**: What are the purchasing patterns across consumer, corporate, and home office client segments?
5. **Geographic Distribution**: Which regional territories (West, East, Central, South) drive the highest gross margins?

---

## 3. Technology Stack & Architectural Standards
- **Platform**: Microsoft Power BI Desktop / Power BI Service
- **Data Modeling**: Star Schema (1 Fact Table, 4 Dimension Tables)
- **Calculation Engine**: Tabular Model / DAX (Data Analysis Expressions)
- **ETL Engine**: Power Query / M Formula Language
- **Storage Mode**: Import Mode for rapid sub-second in-memory query performance

---

## 4. Repository & Project Structure
```text
sales-performance-powerbi/
├── data/
│   ├── Fact_Sales.csv                  # Core transactional fact table (9,994 rows)
│   ├── Dim_Customer.csv                # Customer dimension (793 records)
│   ├── Dim_Product.csv                 # Product catalog dimension (1,894 records)
│   └── Dim_Location.csv                # Postal & territorial dimension (632 records)
├── data_model.md                       # Mermaid Star Schema diagram & cardinality docs
├── dax_measures.dax                    # Complete DAX formula library with inline comments
├── power_query_transformations.m       # Power Query M-scripts for all tables & calendar
├── report_setup_guide.md               # Step-by-step reproduction instructions for Power BI
├── PROJECT_WALKTHROUGH.md              # Beginner tutorial, DAX guide & exercises
└── README.md                           # Complete documentation & interview guide
```

---

## 5. Star Schema Architecture

```
                 +-------------------+
                 |    Dim_Date       |
                 +-------------------+
                           | 1
                           |
                           | *
+-------------------+      |      +-------------------+
|   Dim_Customer    |------+------|    Dim_Product    |
+-------------------+ 1    |    1 +-------------------+
         \                 |                 /
          \ *              | *             * /
       +---------------------------------------+
       |              Fact_Sales               |
       +---------------------------------------+
                           | *
                           |
                           | 1
                 +-------------------+
                 |   Dim_Location    |
                 +-------------------+
```

*(See [data_model.md](data_model.md) for full attribute schema and Mermaid diagram).*

---

## 6. Core DAX Measures & Formulations

All measures are cataloged in `dax_measures.dax`. Highlights include:

### 1. Base Revenue & Margin
```dax
Total Revenue = SUM(Fact_Sales[Sales])
Total Profit = SUM(Fact_Sales[Profit])
Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)
```

### 2. Time Intelligence (Year-over-Year)
```dax
Revenue Prior Year (PY) = 
CALCULATE(
    [Total Revenue], 
    SAMEPERIODLASTYEAR(Dim_Date[Date])
)

YoY Revenue Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Prior Year (PY)], 
    [Revenue Prior Year (PY)], 
    0
)
```

### 3. Dynamic Customer Ranking
```dax
Customer Sales Rank = 
IF(
    HASONEVALUE(Dim_Customer[Customer_Name]),
    RANKX(ALL(Dim_Customer[Customer_Name]), [Total Revenue], , DESC, Dense),
    BLANK()
)
```

---

## 7. Validated Business Findings
When processed through the dimensional model:
- **Total Revenue**: **$2,297,200.86**
- **Total Profit**: **$286,397.02**
- **Profit Margin**: **12.47%**
- **Total Orders**: **5,009 unique purchase orders** (9,994 line items)
- **Top Category**: **Technology** leads net profit contribution with **$145,454.95** (17.4% margin), whereas **Furniture** generates only **$18,451.27** (2.49% margin) due to steep discounting on Tables (-$17.7k net loss).

---

## 8. Interview Preparation: 10 Core Power BI Questions & Answers

### Q1: Why is a Star Schema preferred over a single flat table in Power BI?
**Answer**:
1. **Performance**: VertiPaq columnar database compresses dimensional tables with low cardinality significantly better than a wide flat table with repeated strings.
2. **Filter Integrity**: Star Schemas avoid ambiguous bi-directional filter relationships and prevent circular dependency errors.
3. **Simplicity**: DAX measures (especially Time Intelligence) are cleaner and execute faster when dimension attributes are isolated from transactional facts.

### Q2: What is the difference between `DIVIDE(A, B, 0)` and `A / B` in DAX?
**Answer**: Using the `/` operator returns `#DIV/0!` if the denominator is zero or null. The `DIVIDE()` function internally performs error handling, gracefully returning an alternate result (such as 0 or blank) without failing or generating visual errors on the canvas.

### Q3: How does `CALCULATE()` modify filter context in DAX?
**Answer**: `CALCULATE()` is the only DAX function capable of altering the existing evaluation filter context. It evaluates its filter arguments, overrides or merges them with the ambient filter context, and then evaluates the expression under this newly modified context.

### Q4: Why must a dedicated Date table be marked as an official Date Table?
**Answer**: Marking a table as a Date Table tells the Power BI engine to disable auto date/time hierarchies for that table and ensures that Time Intelligence functions (like `SAMEPERIODLASTYEAR`, `TOTALYTD`, `DATEADD`) operate accurately across contiguous calendar dates without missing-day artifacts.

### Q5: What is the difference between `SUM()` and `SUMX()`?
**Answer**: `SUM()` is an aggregator that sums a single column directly. `SUMX()` is an iterator that steps through a table row-by-row, evaluates an expression at each row (row context), and then sums the results. For example: `SUMX(Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[Price])`.

### Q6: How do you handle column sorting for Month Names in Power BI?
**Answer**: By selecting the `Month Name` column in table view, navigating to the **Column Tools** tab, and choosing **Sort by Column** -> `Month Number`. This prevents alphabetical sorting (April, August, December) and enforces chronological ordering (January to December).

### Q7: What is the purpose of `ALL()` in ranking and percentage calculations?
**Answer**: `ALL()` removes existing filter context from a table or column. In `RANKX(ALL(Dim_Customer[Customer_Name]), [Total Revenue])`, `ALL()` allows the ranking function to evaluate all customers across the entire dimension rather than just the single filtered customer on that specific visual row.

### Q8: What is the difference between Implicit and Explicit DAX measures?
**Answer**: Implicit measures are created automatically when a user drags a numerical column (e.g. `Sales`) onto a visual and Power BI defaults to Sum. Explicit measures are author-created DAX expressions (e.g. `Total Revenue = SUM(Fact_Sales[Sales])`). Explicit measures are mandatory in professional models because they are reusable, self-documenting, and can be referenced by other complex measures.

### Q9: How does cross-filtering direction impact report performance?
**Answer**: Single-direction filtering propagates filters from the 1-side (Dimensions) to the *-side (Fact table). Bi-directional filtering allows filters to flow both ways, which can introduce ambiguity, Cartesian product loops, and severe performance degradation in enterprise models. Best practice is to maintain single-directional filtering wherever possible.

### Q10: How would you optimize a slow-performing Power BI report?
**Answer**:
1. Run **Performance Analyzer** to identify slow visuals (DAX query vs Visual display time).
2. Use **DAX Studio** to inspect VertiPaq storage metrics, eliminating unused high-cardinality columns (e.g., timestamps, GUIDs).
3. Replace slow iterators with optimized column-store aggregations.
4. Reduce the count of visuals per page and minimize visual-level filters.
