# Assignment 2 - Generative AI Usage Documentation

**Authors:** DIALLO Samba, DIOP Mouhamed  
**Course:** Data Engineering I - ESIEE Paris  
**Date:** January 2026  

---

## AI Tool Used

**Tool:** GitHub Copilot (Claude Sonnet 4.5)  
**Access Method:** VS Code integrated chat interface  
**Usage Period:** Throughout Assignment 2 development

---

## How We Used Generative AI

### 1. Database Connection Issues

**Problem:** Initial attempts to connect Spark to SQLite using JDBC failed with `ClassNotFoundException: org.sqlite.JDBC`

**AI Assistance:**
- Diagnosed that PySpark doesn't include SQLite JDBC driver by default
- Suggested alternative approach: use pandas as intermediary to load SQLite data
- Provided working code pattern: `sqlite3 → pandas → spark.createDataFrame()`

**Example Solution:**
```python
conn_read = sqlite3.connect(db_path)
customers_pd = pd.read_sql_query("SELECT * FROM customers", conn_read)
customers_df = spark.createDataFrame(customers_pd)
```

**Impact:** Resolved blocking issue and enabled data ingestion from SQLite database.

---

### 2. Variable Name Errors

**Problem:** Code referenced undefined variable `df` which didn't exist in our context

**AI Assistance:**
- Identified that template code was written for different dataset structure
- Helped adapt code to use actual DataFrame names: `customers_df`, `orders_df`, `sales_df`
- Updated all analysis queries to match our e-commerce schema

**Example Fix:**
```python
# Before (incorrect):
df.groupBy("user_id").count()

# After (correct):
sales_df.groupBy("customer_id", "name").agg(
    count("order_id").alias("total_orders"),
    sum("total_price").alias("total_spent")
)
```

**Impact:** Transformed generic template into working e-commerce analysis pipeline.

---

### 3. PySpark Function Name Issues

**Problem:** Code used `countDistinct()` which caused `NameError: name 'countDistinct' is not defined`

**AI Assistance:**
- Identified that PySpark uses `count_distinct()` (with underscore) not `countDistinct()`
- Explained the difference between SQL-style camelCase and PySpark's Python-style naming
- Updated all aggregation functions throughout the notebook

**Example Fix:**
```python
# Before (incorrect):
countDistinct("product_id")

# After (correct):
count_distinct("product_id")
```

**Impact:** Fixed all aggregation queries and enabled successful execution of analytics code.

---

### 4. Data Schema Understanding

**AI Assistance:**
- Helped understand the e-commerce schema relationships:
  - `customers` ← `orders` ← `order_items` → `products` → `brands`, `categories`
- Guided proper join order for creating complete sales dataset
- Suggested using appropriate join keys and avoiding ambiguous column references

**Example Pattern:**
```python
sales_df = order_items_df \
    .join(orders_df, "order_id") \
    .join(customers_df, "customer_id") \
    .join(products_df, "product_id") \
    .join(brands_df, "brand_id") \
    .join(categories_df, "category_id")
```

**Impact:** Successfully created denormalized sales dataset with all 638 records.

---

### 5. Code Documentation

**AI Assistance:**
- Suggested adding explanatory comments at the end of each cell
- Helped explain PySpark concepts like:
  - DataFrame transformations vs actions
  - Lazy evaluation and execution plans
  - Difference between parquet and CSV formats
- Provided clear explanations of what each analysis achieves

**Impact:** Improved code readability and demonstrated understanding of concepts.

---

## Summary of AI Contribution

### Problems Solved:
1. ✅ JDBC driver issue → pandas intermediary approach
2. ✅ Variable reference errors → adapted to actual schema
3. ✅ Function naming errors → corrected to PySpark syntax
4. ✅ Schema understanding → proper join design

### Skills Developed:
- Debugging PySpark errors effectively
- Understanding DataFrame operations and aggregations
- Adapting template code to specific use cases
- Writing clear technical documentation

### Learning Outcomes:
We learned that while AI tools are very helpful for:
- Identifying syntax errors and suggesting fixes
- Explaining framework-specific conventions (like PySpark naming)
- Providing alternative approaches when initial methods fail

We still need to:
- Understand our data schema and business logic
- Validate that AI-suggested fixes make sense for our context
- Test code thoroughly to ensure it works with our data
- Document our own understanding of the concepts

---

## Ethical Considerations

- All code was reviewed and understood before submission
- AI was used as a debugging assistant and learning tool, not as a copy-paste solution
- We adapted and contextualized all AI suggestions to our specific assignment requirements
- This documentation transparently discloses all AI usage per course requirements

---

## Conclusion

AI assistance significantly accelerated debugging and helped us overcome technical blockers (especially the JDBC issue). However, the core work of data analysis, understanding business logic, and interpreting results was performed by us. The AI acted as an intelligent pair programmer, helping us learn PySpark more efficiently while maintaining ownership of the assignment outcomes.
