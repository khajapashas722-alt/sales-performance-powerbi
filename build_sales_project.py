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
                {"name": "Day of Week Number", "dataType": "int64", "sourceColumn": "Day of Week Number"},
                {"name": "Month-Year Date", "dataType": "dateTime", "sourceColumn": "Month-Year Date", "formatString": "yyyy-MM-dd"}
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
                            '    AddDayOfWeekNo = Table.AddColumn(AddDayOfWeek, "Day of Week Number", each Date.DayOfWeek([Date], Day.Monday) + 1, Int64.Type),',
                            '    AddMonthYearDate = Table.AddColumn(AddDayOfWeekNo, "Month-Year Date", each #date(Date.Year([Date]), Date.Month([Date]), 1), type date)',
                            "in",
                            "    AddMonthYearDate"
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

def make_textbox(name, x, y, width, height, z, text, font_size="15pt"):
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "textbox",
            "objects": {
                "general": [{
                    "properties": {
                        "paragraphs": [{
                            "textRuns": [{
                                "value": text,
                                "textStyle": {"fontFamily": "Segoe UI", "fontSize": font_size, "fontWeight": "bold", "color": "#1A365D"}
                            }]
                        }]
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_card(name, x, y, width, height, z, table_name, measure_name):
    q_ref = f"{table_name}.{measure_name}"
    alias = "m"
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "card",
            "projections": {
                "Values": [{"queryRef": q_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": alias, "Entity": table_name, "Type": 0}],
                "Select": [{
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": alias}},
                        "Property": measure_name
                    },
                    "Name": q_ref
                }]
            },
            "objects": {
                "labels": [{
                    "properties": {
                        "fontSize": {"expr": {"Literal": {"Value": "20D"}}},
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "categoryLabels": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "10D"}}},
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#64748B'"}}}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_slicer(name, x, y, width, height, z, table_name, col_name, title_text=None):
    q_ref = f"{table_name}.{col_name}"
    alias = "s"
    objects = {
        "data": [{
            "properties": {
                "mode": {"expr": {"Literal": {"Value": "'Dropdown'"}}}
            }
        }],
        "header": [{
            "properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "fontSize": {"expr": {"Literal": {"Value": "10D"}}}
            }
        }],
        "items": [{
            "properties": {
                "fontSize": {"expr": {"Literal": {"Value": "10D"}}}
            }
        }]
    }
    if title_text:
        objects["header"][0]["properties"]["titleText"] = {"expr": {"Literal": {"Value": f"'{title_text}'"}}}
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "slicer",
            "projections": {
                "Values": [{"queryRef": q_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": alias, "Entity": table_name, "Type": 0}],
                "Select": [{
                    "Column": {
                        "Expression": {"SourceRef": {"Source": alias}},
                        "Property": col_name
                    },
                    "Name": q_ref
                }]
            },
            "objects": objects
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_line_chart(name, x, y, width, height, z, cat_table, cat_col, measure_table, measures, title_text="Monthly Revenue & Profit Trend"):
    cat_ref = f"{cat_table}.{cat_col}"
    projections = {
        "Category": [{"queryRef": cat_ref, "active": True}],
        "Y": [{"queryRef": f"{measure_table}.{m}"} for m in measures]
    }
    select_items = [{
        "Column": {
            "Expression": {"SourceRef": {"Source": "d"}},
            "Property": cat_col
        },
        "Name": cat_ref
    }]
    for m in measures:
        select_items.append({
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": m
            },
            "Name": f"{measure_table}.{m}"
        })
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "lineChart",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "d", "Entity": cat_table, "Type": 0},
                    {"Name": "m", "Entity": measure_table, "Type": 0}
                ],
                "Select": select_items
            },
            "objects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "categoryAxis": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "axisType": {"expr": {"Literal": {"Value": "'Scalar'"}}},
                        "showAxisTitle": {"expr": {"Literal": {"Value": "true"}}},
                        "axisTitle": {"expr": {"Literal": {"Value": "'Order Month (Continuous Timeline)'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "9D"}}}
                    }
                }],
                "valueAxis": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "showAxisTitle": {"expr": {"Literal": {"Value": "true"}}},
                        "axisTitle": {"expr": {"Literal": {"Value": "'Amount ($)'"}}}
                    }
                }],
                "legend": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "position": {"expr": {"Literal": {"Value": "'TopRight'"}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_bar_chart(name, x, y, width, height, z, cat_table, cat_col, measure_table, measures, title_text="Sales & Profitability by Product Category"):
    cat_ref = f"{cat_table}.{cat_col}"
    projections = {
        "Category": [{"queryRef": cat_ref, "active": True}],
        "Y": [{"queryRef": f"{measure_table}.{m}"} for m in measures]
    }
    select_items = [{
        "Column": {
            "Expression": {"SourceRef": {"Source": "c"}},
            "Property": cat_col
        },
        "Name": cat_ref
    }]
    for m in measures:
        select_items.append({
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": m
            },
            "Name": f"{measure_table}.{m}"
        })
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "clusteredBarChart",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_table, "Type": 0},
                    {"Name": "m", "Entity": measure_table, "Type": 0}
                ],
                "Select": select_items
            },
            "objects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "legend": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "position": {"expr": {"Literal": {"Value": "'TopRight'"}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_pie_chart(name, x, y, width, height, z, cat_table, cat_col, measure_table, measure_name, title_text="Revenue Distribution by Region"):
    cat_ref = f"{cat_table}.{cat_col}"
    m_ref = f"{measure_table}.{measure_name}"
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "pieChart",
            "projections": {
                "Category": [{"queryRef": cat_ref}],
                "Y": [{"queryRef": m_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "l", "Entity": cat_table, "Type": 0},
                    {"Name": "m", "Entity": measure_table, "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "l"}},
                            "Property": cat_col
                        },
                        "Name": cat_ref
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": measure_name
                        },
                        "Name": m_ref
                    }
                ]
            },
            "objects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "legend": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "position": {"expr": {"Literal": {"Value": "'Right'"}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_table(name, x, y, width, height, z, from_tables, fields, title_text=None):
    from_map = {tbl: f"t{i}" for i, tbl in enumerate(from_tables)}
    from_list = [{"Name": alias, "Entity": tbl, "Type": 0} for tbl, alias in from_map.items()]
    projections = {
        "Values": [{"queryRef": f"{tbl}.{prop}"} for tbl, prop, is_m in fields]
    }
    select_items = []
    for tbl, prop, is_m in fields:
        alias = from_map[tbl]
        q_ref = f"{tbl}.{prop}"
        if is_m:
            select_items.append({
                "Measure": {
                    "Expression": {"SourceRef": {"Source": alias}},
                    "Property": prop
                },
                "Name": q_ref
            })
        else:
            select_items.append({
                "Column": {
                    "Expression": {"SourceRef": {"Source": alias}},
                    "Property": prop
                },
                "Name": q_ref
            })
    objects = {
        "stylePreset": [{
            "properties": {
                "name": {"expr": {"Literal": {"Value": "'Condensed'"}}}
            }
        }],
        "values": [{
            "properties": {
                "fontSize": {"expr": {"Literal": {"Value": "9D"}}},
                "wordWrap": {"expr": {"Literal": {"Value": "true"}}}
            }
        }],
        "columnHeaders": [{
            "properties": {
                "fontSize": {"expr": {"Literal": {"Value": "9D"}}},
                "wordWrap": {"expr": {"Literal": {"Value": "true"}}},
                "autoSizeColumnWidth": {"expr": {"Literal": {"Value": "true"}}}
            }
        }]
    }
    if title_text:
        objects["title"] = [{
            "properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                "fontSize": {"expr": {"Literal": {"Value": "11D"}}},
                "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
            }
        }]
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "tableEx",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": from_list,
                "Select": select_items
            },
            "objects": objects
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_matrix(name, x, y, width, height, z, row_fields, value_measures, title_text="Product Category & Sub-Category Performance Matrix"):
    projections = {
        "Rows": [{"queryRef": f"{tbl}.{prop}"} for tbl, prop in row_fields],
        "Values": [{"queryRef": f"_Measures.{m}"} for m in value_measures]
    }
    from_list = [
        {"Name": "p", "Entity": "Dim_Product", "Type": 0},
        {"Name": "m", "Entity": "_Measures", "Type": 0}
    ]
    select_items = []
    for tbl, prop in row_fields:
        select_items.append({
            "Column": {
                "Expression": {"SourceRef": {"Source": "p"}},
                "Property": prop
            },
            "Name": f"{tbl}.{prop}"
        })
    for m in value_measures:
        select_items.append({
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": m
            },
            "Name": f"_Measures.{m}"
        })
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "pivotTable",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": from_list,
                "Select": select_items
            },
            "objects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "rowHeaders": [{
                    "properties": {
                        "stepped": {"expr": {"Literal": {"Value": "false"}}},
                        "showExpandCollapseButtons": {"expr": {"Literal": {"Value": "true"}}}
                    }
                }],
                "subTotals": [{
                    "properties": {
                        "rowSubtotals": {"expr": {"Literal": {"Value": "true"}}},
                        "perRowLevel": {"expr": {"Literal": {"Value": "true"}}},
                        "grandTotal": {"expr": {"Literal": {"Value": "true"}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_scatter(name, x, y, width, height, z, cat_table, cat_col, x_measure, y_measure, size_measure, title_text="Margin Sensitivity vs. Discounting by Sub-Category"):
    projections = {
        "Category": [{"queryRef": f"{cat_table}.{cat_col}"}],
        "X": [{"queryRef": f"_Measures.{x_measure}"}],
        "Y": [{"queryRef": f"_Measures.{y_measure}"}],
        "Size": [{"queryRef": f"_Measures.{size_measure}"}]
    }
    from_list = [
        {"Name": "p", "Entity": cat_table, "Type": 0},
        {"Name": "m", "Entity": "_Measures", "Type": 0}
    ]
    select_items = [
        {
            "Column": {
                "Expression": {"SourceRef": {"Source": "p"}},
                "Property": cat_col
            },
            "Name": f"{cat_table}.{cat_col}"
        },
        {
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": x_measure
            },
            "Name": f"_Measures.{x_measure}"
        },
        {
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": y_measure
            },
            "Name": f"_Measures.{y_measure}"
        },
        {
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": size_measure
            },
            "Name": f"_Measures.{size_measure}"
        }
    ]
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "scatterChart",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": from_list,
                "Select": select_items
            },
            "objects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "categoryAxis": [{
                    "properties": {
                        "showAxisTitle": {"expr": {"Literal": {"Value": "true"}}},
                        "axisTitle": {"expr": {"Literal": {"Value": f"'{x_measure}'"}}}
                    }
                }],
                "valueAxis": [{
                    "properties": {
                        "showAxisTitle": {"expr": {"Literal": {"Value": "true"}}},
                        "axisTitle": {"expr": {"Literal": {"Value": f"'{y_measure}'"}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def generate_sales_report_layout():
    # Page 1 Visuals: Executive Sales Overview (Canvas: 1280 x 720)
    p1_visuals = [
        make_textbox("HeaderVisual", 20, 8, 1240, 36, 1000, "Commercial Sales & Profitability Performance Dashboard", "14pt"),
        make_slicer("Slicer_Year", 20, 48, 220, 70, 1500, "Dim_Date", "Year", "Order Year"),
        make_slicer("Slicer_Region", 260, 48, 220, 70, 1501, "Dim_Location", "Region", "Region"),
        make_slicer("Slicer_Segment", 500, 48, 240, 70, 1502, "Dim_Customer", "Segment", "Customer Segment"),
        make_card("Card_TotalRevenue", 20, 130, 236, 82, 2000, "_Measures", "Total Revenue"),
        make_card("Card_TotalProfit", 271, 130, 236, 82, 2001, "_Measures", "Total Profit"),
        make_card("Card_ProfitMargin", 522, 130, 236, 82, 2002, "_Measures", "Profit Margin %"),
        make_card("Card_TotalOrders", 773, 130, 236, 82, 2003, "_Measures", "Total Orders"),
        make_card("Card_AOV", 1024, 130, 236, 82, 2004, "_Measures", "Average Order Value (AOV)"),
        make_line_chart("Chart_MonthlyTrend", 20, 228, 800, 224, 3000, "Dim_Date", "Month-Year Date", "_Measures", ["Total Revenue", "Total Profit"], "Monthly Revenue & Profit Trend (2014 - 2017)"),
        make_pie_chart("Chart_RegionDonut", 835, 228, 425, 224, 3001, "Dim_Location", "Region", "_Measures", "Total Revenue", "Revenue Distribution by Region"),
        make_bar_chart("Chart_CategoryPerformance", 20, 468, 550, 236, 3002, "Dim_Product", "Category", "_Measures", ["Total Revenue", "Total Profit"], "Sales & Profitability by Product Category"),
        make_table("Table_SegmentPerformance", 585, 468, 675, 236, 3003, ["Dim_Customer", "_Measures"], [
            ("Dim_Customer", "Segment", False),
            ("_Measures", "Total Revenue", True),
            ("_Measures", "Total Profit", True),
            ("_Measures", "Profit Margin %", True),
            ("_Measures", "Total Orders", True)
        ], "Customer Segment Performance Matrix")
    ]
    
    # Page 2 Visuals: Product & Profitability Matrix (Canvas: 1280 x 720)
    p2_visuals = [
        make_textbox("HeaderVisual_P2", 20, 10, 1240, 40, 1000, "Product Category & Margin Analysis Matrix", "15pt"),
        make_card("Card_P2_Revenue", 20, 60, 295, 86, 2000, "_Measures", "Total Revenue"),
        make_card("Card_P2_Profit", 335, 60, 295, 86, 2001, "_Measures", "Total Profit"),
        make_card("Card_P2_Margin", 650, 60, 295, 86, 2002, "_Measures", "Profit Margin %"),
        make_card("Card_P2_AvgDiscount", 965, 60, 295, 86, 2003, "_Measures", "Average Discount %"),
        make_matrix("Matrix_SubCategory", 20, 162, 740, 265, 3000, [
            ("Dim_Product", "Category"),
            ("Dim_Product", "Sub-Category")
        ], ["Total Revenue", "Total Profit", "Profit Margin %"], "Product Category & Sub-Category Performance Matrix"),
        make_scatter("Scatter_DiscountMargin", 780, 162, 480, 265, 3001, "Dim_Product", "Sub-Category", "Average Discount %", "Profit Margin %", "Total Revenue", "Margin Sensitivity vs. Discounting by Sub-Category"),
        make_table("Table_TopProducts", 20, 445, 1240, 260, 3002, ["Dim_Product", "_Measures"], [
            ("Dim_Product", "Product Name", False),
            ("Dim_Product", "Category", False),
            ("_Measures", "Total Revenue", True),
            ("_Measures", "Total Profit", True),
            ("_Measures", "Profit Margin %", True),
            ("_Measures", "Total Units Sold", True)
        ], "Top Products Performance & Volume Breakdown")
    ]
    
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
                "visualContainers": p1_visuals,
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
                "visualContainers": p2_visuals,
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
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": "sales-performance-dashboard.Report"
                }
            }
        ],
        "settings": {
            "enableAutoRecovery": True
        }
    }
    with open(pbip_file, "w", encoding="utf-8") as f:
        json.dump(pbip_content, f, indent=2)
        
    # definition.pbir
    pbir_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/1.0.0/schema.json",
        "version": "1.0",
        "datasetReference": {
            "byPath": {
                "path": "../sales-performance-dashboard.SemanticModel"
            }
        }
    }
    with open(os.path.join(rep_dir, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump(pbir_content, f, indent=2)
        
    # report.json
    with open(os.path.join(rep_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(layout, f, indent=2)
        
    # definition.pbism
    pbism_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
        "version": "1.0"
    }
    with open(os.path.join(sem_dir, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump(pbism_content, f, indent=2)
        
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
