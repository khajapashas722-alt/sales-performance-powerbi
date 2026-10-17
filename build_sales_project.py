import json
import zipfile
import os
import uuid

def generate_sales_model():
    base_dir = r"C:/Users/shakj/Documents/data-analytics-portfolio/power-bi/sales-performance-powerbi"
    data_dir = f"{base_dir}/data"
    
    # Path with forward slashes for M queries
    fact_sales_path = f"{data_dir}/Fact_Sales.csv".replace("\\", "/")
    dim_cust_path = f"{data_dir}/Dim_Customer.csv".replace("\\", "/")
    dim_prod_path = f"{data_dir}/Dim_Product.csv".replace("\\", "/")
    dim_loc_path = f"{data_dir}/Dim_Location.csv".replace("\\", "/")
    
    # Tables definitions
    tables = [
        {
            "name": "Fact_Sales",
            "columns": [
                {"name": "Row ID", "dataType": "int64", "sourceColumn": "Row ID"},
                {"name": "Order ID", "dataType": "string", "sourceColumn": "Order ID"},
                {"name": "Order Date", "dataType": "dateTime", "sourceColumn": "Order Date", "formatString": "yyyy-MM-dd"},
                {"name": "Ship Date", "dataType": "dateTime", "sourceColumn": "Ship Date", "formatString": "yyyy-MM-dd"},
                {"name": "Ship Mode", "dataType": "string", "sourceColumn": "Ship Mode"},
                {"name": "Customer ID", "dataType": "string", "sourceColumn": "Customer ID"},
                {"name": "Product ID", "dataType": "string", "sourceColumn": "Product ID"},
                {"name": "Postal Code", "dataType": "string", "sourceColumn": "Postal Code"},
                {"name": "Sales", "dataType": "double", "sourceColumn": "Sales", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Quantity", "dataType": "int64", "sourceColumn": "Quantity", "formatString": "#,0"},
                {"name": "Discount", "dataType": "double", "sourceColumn": "Discount", "formatString": "0.00%"},
                {"name": "Profit", "dataType": "double", "sourceColumn": "Profit", "formatString": "$#,0.00;($#,0.00);$#,0.00"}
            ],
            "partitions": [
                {
                    "name": "Fact_Sales-Partition",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": [
                            "let",
                            f'    Source = Csv.Document(File.Contents("{fact_sales_path}"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                            '    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                            '    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {',
                            '        {"Row ID", Int64.Type},',
                            '        {"Order ID", type text},',
                            '        {"Order Date", type date},',
                            '        {"Ship Date", type date},',
                            '        {"Ship Mode", type text},',
                            '        {"Customer ID", type text},',
                            '        {"Product ID", type text},',
                            '        {"Postal Code", type text},',
                            '        {"Sales", type number},',
                            '        {"Quantity", Int64.Type},',
                            '        {"Discount", type number},',
                            '        {"Profit", type number}',
                            '    })',
                            "in",
                            "    ChangeTypes"
                        ]
                    }
                }
            ]
        },
        {
            "name": "Dim_Customer",
            "columns": [
                {"name": "Customer ID", "dataType": "string", "sourceColumn": "Customer ID", "isKey": True},
                {"name": "Customer Name", "dataType": "string", "sourceColumn": "Customer Name"},
                {"name": "Segment", "dataType": "string", "sourceColumn": "Segment"}
            ],
            "partitions": [
                {
                    "name": "Dim_Customer-Partition",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": [
                            "let",
                            f'    Source = Csv.Document(File.Contents("{dim_cust_path}"), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                            '    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                            '    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {',
                            '        {"Customer ID", type text},',
                            '        {"Customer Name", type text},',
                            '        {"Segment", type text}',
                            '    }),',
                            '    RemoveDuplicates = Table.Distinct(ChangeTypes, {"Customer ID"})',
                            "in",
                            "    RemoveDuplicates"
                        ]
                    }
                }
            ]
        },
        {
            "name": "Dim_Product",
            "columns": [
                {"name": "Product ID", "dataType": "string", "sourceColumn": "Product ID", "isKey": True},
                {"name": "Category", "dataType": "string", "sourceColumn": "Category"},
                {"name": "Sub-Category", "dataType": "string", "sourceColumn": "Sub-Category"},
                {"name": "Product Name", "dataType": "string", "sourceColumn": "Product Name"}
            ],
            "partitions": [
                {
                    "name": "Dim_Product-Partition",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": [
                            "let",
                            f'    Source = Csv.Document(File.Contents("{dim_prod_path}"), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                            '    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                            '    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {',
                            '        {"Product ID", type text},',
                            '        {"Category", type text},',
                            '        {"Sub-Category", type text},',
                            '        {"Product Name", type text}',
                            '    }),',
                            '    RemoveDuplicates = Table.Distinct(ChangeTypes, {"Product ID"})',
                            "in",
                            "    RemoveDuplicates"
                        ]
                    }
                }
            ]
        },
        {
            "name": "Dim_Location",
            "columns": [
                {"name": "Postal Code", "dataType": "string", "sourceColumn": "Postal Code", "isKey": True},
                {"name": "City", "dataType": "string", "sourceColumn": "City"},
                {"name": "State", "dataType": "string", "sourceColumn": "State"},
                {"name": "Region", "dataType": "string", "sourceColumn": "Region"},
                {"name": "Country", "dataType": "string", "sourceColumn": "Country"}
            ],
            "partitions": [
                {
                    "name": "Dim_Location-Partition",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": [
                            "let",
                            f'    Source = Csv.Document(File.Contents("{dim_loc_path}"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                            '    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                            '    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {',
                            '        {"Postal Code", type text},',
                            '        {"City", type text},',
                            '        {"State", type text},',
                            '        {"Region", type text},',
                            '        {"Country", type text}',
                            '    }),',
                            '    RemoveDuplicates = Table.Distinct(ChangeTypes, {"Postal Code"})',
                            "in",
                            "    RemoveDuplicates"
                        ]
                    }
                }
            ]
        },
        {
            "name": "Dim_Date",
            "dataCategory": "Time",
            "columns": [
                {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "formatString": "yyyy-MM-dd", "isKey": True},
                {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
                {"name": "Month Number", "dataType": "int64", "sourceColumn": "Month Number"},
                {"name": "Month Name", "dataType": "string", "sourceColumn": "Month Name"},
                {"name": "Short Month", "dataType": "string", "sourceColumn": "Short Month", "sortByColumn": "Month Number"},
                {"name": "Year-Month", "dataType": "string", "sourceColumn": "Year-Month"},
                {"name": "Quarter", "dataType": "string", "sourceColumn": "Quarter"},
                {"name": "Day of Week", "dataType": "string", "sourceColumn": "Day of Week"},
                {"name": "Day of Week Number", "dataType": "int64", "sourceColumn": "Day of Week Number"}
            ],
            "partitions": [
                {
                    "name": "Dim_Date-Partition",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": [
                            "let",
                            "    StartDate = #date(2014, 1, 1),",
                            "    EndDate = #date(2018, 12, 31),",
                            "    TotalDays = Duration.Days(Duration.From(EndDate - StartDate)) + 1,",
                            '    DateList = List.Dates(StartDate, TotalDays, #duration(1, 0, 0, 0)),',
                            '    TableFromList = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),',
                            '    SetDateType = Table.TransformColumnTypes(TableFromList, {{"Date", type date}}),',
                            '    AddYear = Table.AddColumn(SetDateType, "Year", each Date.Year([Date]), Int64.Type),',
                            '    AddMonthNo = Table.AddColumn(AddYear, "Month Number", each Date.Month([Date]), Int64.Type),',
                            '    AddMonthName = Table.AddColumn(AddMonthNo, "Month Name", each Date.MonthName([Date]), type text),',
                            '    AddShortMonth = Table.AddColumn(AddMonthName, "Short Month", each Text.Start([Month Name], 3), type text),',
                            '    AddYearMonth = Table.AddColumn(AddShortMonth, "Year-Month", each Date.ToText([Date], "yyyy-MM"), type text),',
                            '    AddQuarter = Table.AddColumn(AddYearMonth, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),',
                            '    AddDayOfWeek = Table.AddColumn(AddQuarter, "Day of Week", each Date.DayOfWeekName([Date]), type text),',
                            '    AddDayOfWeekNo = Table.AddColumn(AddDayOfWeek, "Day of Week Number", each Date.DayOfWeek([Date], Day.Monday) + 1, Int64.Type)',
                            "in",
                            "    AddDayOfWeekNo"
                        ]
                    }
                }
            ]
        },
        {
            "name": "_Measures",
            "columns": [
                {"name": "RowKey", "dataType": "int64", "sourceColumn": "RowKey", "isHidden": True}
            ],
            "partitions": [
                {
                    "name": "_Measures-Partition",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": [
                            "let",
                            '    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlSKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [RowKey = _t]),',
                            '    ChangeTypes = Table.TransformColumnTypes(Source,{{"RowKey", Int64.Type}})',
                            "in",
                            "    ChangeTypes"
                        ]
                    }
                }
            ],
            "measures": [
                {"name": "Total Revenue", "expression": "SUM(Fact_Sales[Sales])", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Total Profit", "expression": "SUM(Fact_Sales[Profit])", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Total Cost", "expression": "[Total Revenue] - [Total Profit]", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Total Units Sold", "expression": "SUM(Fact_Sales[Quantity])", "formatString": "#,0"},
                {"name": "Total Orders", "expression": "DISTINCTCOUNT(Fact_Sales[Order ID])", "formatString": "#,0"},
                {"name": "Unique Customers", "expression": "DISTINCTCOUNT(Fact_Sales[Customer ID])", "formatString": "#,0"},
                {"name": "Profit Margin %", "expression": "DIVIDE([Total Profit], [Total Revenue], 0)", "formatString": "0.00%"},
                {"name": "Average Order Value (AOV)", "expression": "DIVIDE([Total Revenue], [Total Orders], 0)", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Average Discount %", "expression": "AVERAGE(Fact_Sales[Discount])", "formatString": "0.00%"},
                {"name": "Profit Per Unit", "expression": "DIVIDE([Total Profit], [Total Units Sold], 0)", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Revenue YTD", "expression": "TOTALYTD([Total Revenue], Dim_Date[Date])", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Profit YTD", "expression": "TOTALYTD([Total Profit], Dim_Date[Date])", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Revenue Prior Year (PY)", "expression": "CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Profit Prior Year (PY)", "expression": "CALCULATE([Total Profit], SAMEPERIODLASTYEAR(Dim_Date[Date]))", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "YoY Revenue Growth $", "expression": "VAR CurrentRevenue = [Total Revenue] VAR PriorRevenue = [Revenue Prior Year (PY)] RETURN IF(ISBLANK(PriorRevenue), BLANK(), CurrentRevenue - PriorRevenue)", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "YoY Revenue Growth %", "expression": "DIVIDE([YoY Revenue Growth $], [Revenue Prior Year (PY)], 0)", "formatString": "0.00%"},
                {"name": "YoY Profit Growth %", "expression": "DIVIDE([Total Profit] - [Profit Prior Year (PY)], [Profit Prior Year (PY)], 0)", "formatString": "0.00%"},
                {"name": "Customer Sales Rank", "expression": "IF(HASONEVALUE(Dim_Customer[Customer Name]), RANKX(ALL(Dim_Customer[Customer Name]), [Total Revenue], , DESC, Dense), BLANK())", "formatString": "#,0"},
                {"name": "Product Sales Rank", "expression": "IF(HASONEVALUE(Dim_Product[Product Name]), RANKX(ALL(Dim_Product[Product Name]), [Total Revenue], , DESC, Dense), BLANK())", "formatString": "#,0"},
                {"name": "Profit Margin Color Hex", "expression": "VAR Margin = [Profit Margin %] RETURN SWITCH(TRUE(), Margin >= 0.15, \"#2ECC71\", Margin >= 0.05, \"#F1C40F\", \"#E74C3C\")"}
            ]
        }
    ]
    
    # Relationships
    relationships = [
        {
            "name": "Fact_Sales_Customer_Rel",
            "fromTable": "Fact_Sales",
            "fromColumn": "Customer ID",
            "toTable": "Dim_Customer",
            "toColumn": "Customer ID",
            "crossFilteringBehavior": "oneDirection"
        },
        {
            "name": "Fact_Sales_Product_Rel",
            "fromTable": "Fact_Sales",
            "fromColumn": "Product ID",
            "toTable": "Dim_Product",
            "toColumn": "Product ID",
            "crossFilteringBehavior": "oneDirection"
        },
        {
            "name": "Fact_Sales_Location_Rel",
            "fromTable": "Fact_Sales",
            "fromColumn": "Postal Code",
            "toTable": "Dim_Location",
            "toColumn": "Postal Code",
            "crossFilteringBehavior": "oneDirection"
        },
        {
            "name": "Fact_Sales_Date_Rel",
            "fromTable": "Fact_Sales",
            "fromColumn": "Order Date",
            "toTable": "Dim_Date",
            "toColumn": "Date",
            "crossFilteringBehavior": "oneDirection"
        }
    ]
    
    model = {
        "name": "SalesPerformanceDataModel",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "sourceQueryCulture": "en-US",
            "tables": tables,
            "relationships": relationships
        }
    }
    return model

def generate_sales_report_layout():
    # Report layout JSON
    layout = {
        "id": 0,
        "resourcePackages": [],
        "sections": [
            {
                "id": 0,
                "name": "ReportSection_ExecutiveOverview",
                "displayName": "Executive Sales Overview",
                "filters": "[]",
                "ordinal": 0,
                "visualContainers": [
                    {
                        "x": 20, "y": 15, "z": 1000, "width": 1240, "height": 45,
                        "config": json.dumps({
                            "name": "HeaderVisual",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [{
                                        "properties": {
                                            "paragraphs": [{
                                                "textRuns": [{
                                                    "value": "Commercial Sales & Profitability Performance Dashboard",
                                                    "textStyle": {"fontFamily": "Segoe UI", "fontSize": "18pt", "fontWeight": "bold", "color": "#1A365D"}
                                                }]
                                            }]
                                        }
                                    }]
                                }
                            }
                        })
                    },
                    {
                        "x": 20, "y": 70, "z": 2000, "width": 230, "height": 95,
                        "config": json.dumps({
                            "name": "KpiCard_Revenue",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_Measures.Total Revenue"}]}
                            }
                        })
                    },
                    {
                        "x": 270, "y": 70, "z": 2001, "width": 230, "height": 95,
                        "config": json.dumps({
                            "name": "KpiCard_Profit",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_Measures.Total Profit"}]}
                            }
                        })
                    },
                    {
                        "x": 520, "y": 70, "z": 2002, "width": 230, "height": 95,
                        "config": json.dumps({
                            "name": "KpiCard_Margin",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_Measures.Profit Margin %"}]}
                            }
                        })
                    },
                    {
                        "x": 770, "y": 70, "z": 2003, "width": 230, "height": 95,
                        "config": json.dumps({
                            "name": "KpiCard_Orders",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_Measures.Total Orders"}]}
                            }
                        })
                    },
                    {
                        "x": 1020, "y": 70, "z": 2004, "width": 240, "height": 95,
                        "config": json.dumps({
                            "name": "KpiCard_AOV",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_Measures.Average Order Value (AOV)"}]}
                            }
                        })
                    },
                    {
                        "x": 20, "y": 180, "z": 3000, "width": 750, "height": 270,
                        "config": json.dumps({
                            "name": "MonthlyTrendChart",
                            "singleVisual": {
                                "visualType": "lineChart",
                                "projections": {
                                    "Category": [{"queryRef": "Dim_Date.Year-Month"}],
                                    "Y": [{"queryRef": "_Measures.Total Revenue"}, {"queryRef": "_Measures.Total Profit"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 790, "y": 180, "z": 3001, "width": 470, "height": 270,
                        "config": json.dumps({
                            "name": "RegionDonutChart",
                            "singleVisual": {
                                "visualType": "pieChart",
                                "projections": {
                                    "Category": [{"queryRef": "Dim_Location.Region"}],
                                    "Y": [{"queryRef": "_Measures.Total Revenue"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 20, "y": 465, "z": 3002, "width": 600, "height": 235,
                        "config": json.dumps({
                            "name": "CategoryBarChart",
                            "singleVisual": {
                                "visualType": "clusteredBarChart",
                                "projections": {
                                    "Category": [{"queryRef": "Dim_Product.Category"}],
                                    "Y": [{"queryRef": "_Measures.Total Revenue"}, {"queryRef": "_Measures.Total Profit"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 640, "y": 465, "z": 3003, "width": 620, "height": 235,
                        "config": json.dumps({
                            "name": "SegmentCustomerTable",
                            "singleVisual": {
                                "visualType": "tableEx",
                                "projections": {
                                    "Values": [
                                        {"queryRef": "Dim_Customer.Segment"},
                                        {"queryRef": "_Measures.Total Revenue"},
                                        {"queryRef": "_Measures.Total Profit"},
                                        {"queryRef": "_Measures.Profit Margin %"},
                                        {"queryRef": "_Measures.Total Orders"}
                                    ]
                                }
                            }
                        })
                    }
                ],
                "config": json.dumps({}),
                "width": 1280,
                "height": 720
            },
            {
                "id": 1,
                "name": "ReportSection_ProductProfitability",
                "displayName": "Product & Profitability Matrix",
                "filters": "[]",
                "ordinal": 1,
                "visualContainers": [
                    {
                        "x": 20, "y": 15, "z": 1000, "width": 1240, "height": 45,
                        "config": json.dumps({
                            "name": "HeaderVisual_P2",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [{
                                        "properties": {
                                            "paragraphs": [{
                                                "textRuns": [{
                                                    "value": "Product Category & Sub-Category Profitability Analysis",
                                                    "textStyle": {"fontFamily": "Segoe UI", "fontSize": "18pt", "fontWeight": "bold", "color": "#1A365D"}
                                                }]
                                            }]
                                        }
                                    }]
                                }
                            }
                        })
                    },
                    {
                        "x": 20, "y": 70, "z": 2000, "width": 700, "height": 380,
                        "config": json.dumps({
                            "name": "SubCategoryMatrix",
                            "singleVisual": {
                                "visualType": "pivotTable",
                                "projections": {
                                    "Rows": [{"queryRef": "Dim_Product.Category"}, {"queryRef": "Dim_Product.Sub-Category"}],
                                    "Values": [
                                        {"queryRef": "_Measures.Total Revenue"},
                                        {"queryRef": "_Measures.Total Profit"},
                                        {"queryRef": "_Measures.Profit Margin %"},
                                        {"queryRef": "_Measures.Average Discount %"}
                                    ]
                                }
                            }
                        })
                    },
                    {
                        "x": 740, "y": 70, "z": 2001, "width": 520, "height": 380,
                        "config": json.dumps({
                            "name": "DiscountVsMarginScatter",
                            "singleVisual": {
                                "visualType": "scatterChart",
                                "projections": {
                                    "Category": [{"queryRef": "Dim_Product.Sub-Category"}],
                                    "X": [{"queryRef": "_Measures.Average Discount %"}],
                                    "Y": [{"queryRef": "_Measures.Profit Margin %"}],
                                    "Size": [{"queryRef": "_Measures.Total Revenue"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 20, "y": 465, "z": 3000, "width": 1240, "height": 235,
                        "config": json.dumps({
                            "name": "TopProductsTable",
                            "singleVisual": {
                                "visualType": "tableEx",
                                "projections": {
                                    "Values": [
                                        {"queryRef": "Dim_Product.Product Name"},
                                        {"queryRef": "Dim_Product.Category"},
                                        {"queryRef": "_Measures.Total Revenue"},
                                        {"queryRef": "_Measures.Total Profit"},
                                        {"queryRef": "_Measures.Profit Margin %"},
                                        {"queryRef": "_Measures.Total Units Sold"}
                                    ]
                                }
                            }
                        })
                    }
                ],
                "config": json.dumps({}),
                "width": 1280,
                "height": 720
            }
        ],
        "config": json.dumps({"version": "5.50", "themeCollection": {"baseTheme": {"name": "CY24SU02", "version": "5.50"}}})
    }
    return layout

def main():
    base_dir = r"C:\Users\shakj\Documents\data-analytics-portfolio\power-bi\sales-performance-powerbi"
    model = generate_sales_model()
    layout = generate_sales_report_layout()
    
    # 1. PBIP Structure
    pbip_file = os.path.join(base_dir, "sales-performance-dashboard.pbip")
    sem_dir = os.path.join(base_dir, "sales-performance-dashboard.SemanticModel")
    rep_dir = os.path.join(base_dir, "sales-performance-dashboard.Report")
    
    os.makedirs(sem_dir, exist_ok=True)
    os.makedirs(rep_dir, exist_ok=True)
    
    # PBIP root file
    pbip_content = {
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": "sales-performance-dashboard.Report"
                }
            }
        ],
        "settings": {
            "enableAutoAuth": True
        }
    }
    with open(pbip_file, "w", encoding="utf-8") as f:
        json.dump(pbip_content, f, indent=2)
        
    # definition.pbir
    pbir_content = {
        "version": "1.0",
        "datasetReference": {
            "byPath": {
                "path": "../sales-performance-dashboard.SemanticModel"
            },
            "byConnection": None
        }
    }
    with open(os.path.join(rep_dir, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump(pbir_content, f, indent=2)
        
    # report.json
    with open(os.path.join(rep_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(layout, f, indent=2)
        
    # definition.pbism
    with open(os.path.join(sem_dir, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump({"version": "1.0"}, f, indent=2)
        
    # model.bim
    with open(os.path.join(sem_dir, "model.bim"), "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2)
        
    print(f"Created PBIP files at {pbip_file}")
    
    # 2. PBIT Template Structure (Open Packaging Conventions ZIP)
    pbit_file = os.path.join(base_dir, "sales-performance-dashboard.pbit")
    
    content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="" />
  <Override PartName="/Version" ContentType="" />
  <Override PartName="/Settings" ContentType="" />
  <Override PartName="/DataModelSchema" ContentType="" />
  <Override PartName="/Report/Layout" ContentType="" />
</Types>"""

    with zipfile.ZipFile(pbit_file, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml.encode("utf-8"))
        z.writestr("Version", "1.28".encode("utf-16le"))
        z.writestr("Settings", json.dumps({"Version": 3}).encode("utf-16le"))
        z.writestr("DataModelSchema", json.dumps(model).encode("utf-16le"))
        z.writestr("Report/Layout", json.dumps(layout).encode("utf-16le"))
        
    print(f"Created PBIT template at {pbit_file}")

if __name__ == "__main__":
    main()
