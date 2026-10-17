// =============================================================================
// Power Query (M) Scripts: Commercial Sales Performance Data Model
// Target: Power BI Desktop Advanced Editor
// =============================================================================

// -----------------------------------------------------------------------------
// SCRIPT 1: Dim_Date (Dynamic Calendar Dimension)
// Generates a continuous calendar based on the range of Fact_Sales[Order Date]
// -----------------------------------------------------------------------------
let
    StartDate = #date(2014, 1, 1),
    EndDate = #date(2018, 12, 31),
    TotalDays = Duration.Days(Duration.From(EndDate - StartDate)) + 1,
    DateList = List.Dates(StartDate, TotalDays, #duration(1, 0, 0, 0)),
    TableFromList = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    SetDateType = Table.TransformColumnTypes(TableFromList, {{"Date", type date}}),
    AddYear = Table.AddColumn(SetDateType, "Year", each Date.Year([Date]), Int64.Type),
    AddMonthNo = Table.AddColumn(AddYear, "Month Number", each Date.Month([Date]), Int64.Type),
    AddMonthName = Table.AddColumn(AddMonthNo, "Month Name", each Date.MonthName([Date]), type text),
    AddShortMonth = Table.AddColumn(AddMonthName, "Short Month", each Text.Start([Month Name], 3), type text),
    AddYearMonth = Table.AddColumn(AddShortMonth, "Year-Month", each Date.ToText([Date], "yyyy-MM"), type text),
    AddQuarter = Table.AddColumn(AddYearMonth, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    AddDayOfWeek = Table.AddColumn(AddQuarter, "Day of Week", each Date.DayOfWeekName([Date]), type text),
    AddDayOfWeekNo = Table.AddColumn(AddDayOfWeek, "Day of Week Number", each Date.DayOfWeek([Date], Day.Monday) + 1, Int64.Type)
in
    AddDayOfWeekNo


// -----------------------------------------------------------------------------
// SCRIPT 2: Fact_Sales Ingestion & Transformation
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("data/Fact_Sales.csv"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"Row ID", Int64.Type}, 
        {"Order ID", type text}, 
        {"Order Date", type date}, 
        {"Ship Date", type date}, 
        {"Ship Mode", type text}, 
        {"Customer ID", type text}, 
        {"Product ID", type text}, 
        {"Postal Code", type text}, 
        {"Sales", type number}, 
        {"Quantity", Int64.Type}, 
        {"Discount", type number}, 
        {"Profit", type number}
    })
in
    ChangeTypes


// -----------------------------------------------------------------------------
// SCRIPT 3: Dim_Customer Transformation
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("data/Dim_Customer.csv"), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"Customer ID", type text}, 
        {"Customer Name", type text}, 
        {"Segment", type text}
    }),
    RemoveDuplicates = Table.Distinct(ChangeTypes, {"Customer ID"})
in
    RemoveDuplicates


// -----------------------------------------------------------------------------
// SCRIPT 4: Dim_Product Transformation
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("data/Dim_Product.csv"), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"Product ID", type text}, 
        {"Category", type text}, 
        {"Sub-Category", type text}, 
        {"Product Name", type text}
    }),
    RemoveDuplicates = Table.Distinct(ChangeTypes, {"Product ID"})
in
    RemoveDuplicates


// -----------------------------------------------------------------------------
// SCRIPT 5: Dim_Location Transformation
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("data/Dim_Location.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"Postal Code", type text}, 
        {"City", type text}, 
        {"State", type text}, 
        {"Region", type text}, 
        {"Country", type text}
    }),
    RemoveDuplicates = Table.Distinct(ChangeTypes, {"Postal Code"})
in
    RemoveDuplicates
