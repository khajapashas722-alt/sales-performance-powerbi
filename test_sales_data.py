"""
Unit & Parity Test Suite: Sales Performance Data Model
Verifies 100% semantic and mathematical parity against the raw CSV and portfolio benchmarks.
"""

import csv
import os

def test_sales_data_and_benchmarks():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sales_csv = os.path.join(base_dir, "data", "Fact_Sales.csv")
    cust_csv = os.path.join(base_dir, "data", "Dim_Customer.csv")
    prod_csv = os.path.join(base_dir, "data", "Dim_Product.csv")
    loc_csv = os.path.join(base_dir, "data", "Dim_Location.csv")
    
    assert os.path.exists(sales_csv), f"Fact_Sales CSV missing at {sales_csv}"
    assert os.path.exists(cust_csv), f"Dim_Customer CSV missing at {cust_csv}"
    assert os.path.exists(prod_csv), f"Dim_Product CSV missing at {prod_csv}"
    assert os.path.exists(loc_csv), f"Dim_Location CSV missing at {loc_csv}"
    
    with open(sales_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        sales_rows = list(reader)
        
    print(f"Loaded {len(sales_rows)} sales records.")
    assert len(sales_rows) == 9994, f"Expected 9,994 rows, found {len(sales_rows)}"
    
    # 1. Total Revenue, Profit, Margin, and Quantity
    total_revenue = sum(float(r["Sales"]) for r in sales_rows)
    total_profit = sum(float(r["Profit"]) for r in sales_rows)
    total_quantity = sum(int(float(r["Quantity"])) for r in sales_rows)
    unique_orders = len(set(r["Order ID"] for r in sales_rows))
    profit_margin = (total_profit / total_revenue) * 100.0
    
    print(f"Total Revenue: ${total_revenue:,.2f} (Expected: $2,297,200.86)")
    print(f"Total Profit: ${total_profit:,.2f} (Expected: $286,397.02)")
    print(f"Total Quantity: {total_quantity:,} (Expected: 37,873)")
    print(f"Total Orders: {unique_orders:,} (Expected: 5,009)")
    print(f"Profit Margin: {profit_margin:.2f}% (Expected: 12.47%)")
    
    assert round(total_revenue, 2) == 2297200.86, f"Revenue mismatch: {round(total_revenue, 2)}"
    assert round(total_profit, 2) == 286397.02, f"Profit mismatch: {round(total_profit, 2)}"
    assert total_quantity == 37873, f"Quantity mismatch: {total_quantity}"
    assert unique_orders == 5009, f"Order count mismatch: {unique_orders}"
    assert round(profit_margin, 2) == 12.47, f"Profit margin mismatch: {round(profit_margin, 2)}"
    
    # 2. Check Dimension Tables
    with open(cust_csv, "r", encoding="utf-8") as f:
        cust_rows = list(csv.DictReader(f))
    with open(prod_csv, "r", encoding="utf-8") as f:
        prod_rows = list(csv.DictReader(f))
    with open(loc_csv, "r", encoding="utf-8") as f:
        loc_rows = list(csv.DictReader(f))
        
    print(f"Customers: {len(cust_rows)} records")
    print(f"Products: {len(prod_rows)} records")
    print(f"Locations: {len(loc_rows)} records")
    
    assert len(cust_rows) == 793, f"Expected 793 customers, found {len(cust_rows)}"
    assert len(prod_rows) == 1894, f"Expected 1,894 product rows, found {len(prod_rows)}"
    assert len(set(r["Product ID"] for r in prod_rows)) == 1862, "Expected 1,862 unique Product IDs"
    assert len(loc_rows) == 632, f"Expected 632 location rows, found {len(loc_rows)}"
    
    # 3. Foreign Key Integrity (0 orphan records)
    cust_ids = set(r["Customer ID"] for r in cust_rows)
    prod_ids = set(r["Product ID"] for r in prod_rows)
    postal_codes = set(r["Postal Code"] for r in loc_rows)
    
    orphan_cust = [r for r in sales_rows if r["Customer ID"] not in cust_ids]
    orphan_prod = [r for r in sales_rows if r["Product ID"] not in prod_ids]
    orphan_postal = [r for r in sales_rows if r["Postal Code"] not in postal_codes]
    
    print(f"Orphan Customers: {len(orphan_cust)}")
    print(f"Orphan Products: {len(orphan_prod)}")
    print(f"Orphan Postal Codes: {len(orphan_postal)}")
    
    assert len(orphan_cust) == 0, f"Found orphan customer references: {len(orphan_cust)}"
    assert len(orphan_prod) == 0, f"Found orphan product references: {len(orphan_prod)}"
    assert len(orphan_postal) == 0, f"Found orphan postal codes: {len(orphan_postal)}"
    
    print("\nALL SALES BENCHMARKS VERIFIED SUCCESSFULLY WITH 100% PARITY!")

if __name__ == "__main__":
    test_sales_data_and_benchmarks()
