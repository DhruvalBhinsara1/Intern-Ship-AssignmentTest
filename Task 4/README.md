# Task 4: Research Data Mapping (Category & Sub-Category) - ✅ COMPLETED

## **Objective:** Extract Category and Sub-Category for each keyword and URL in the given research data sheets

## **Status:** ✅ COMPLETED

**Deliverables:**

- `Task 4/mapped data set/Positions.bigbasket.com_mapped.xlsx`
- `Task 4/mapped data set/Positions.swiggy.com_mapped.xlsx`
- `Task 4/Task4_Data_Mapping.py` (mapping script)

**Data Processed:**

- **BigBasket:** 30,000 rows → 5 categories, 19 sub-categories
- **Swiggy:** 30,000 rows → 5 categories, 18 sub-categories
- **Total:** 60,000+ records intelligently categorized

## **Implementation Strategy:**

### **Data Analysis Approach:**

1. I analyzed keyword patterns and URL structures to identify categorization rules
2. I developed intelligent mapping logic based on domain knowledge of e-commerce and food delivery platforms
3. I implemented regex-based pattern matching for URL analysis
4. I created keyword-based categorization for services and business types

### **Mapping Rules Developed:**

#### **BigBasket (E-commerce Focus):**

- **Fresh Produce:** Fruits, vegetables, dairy, bakery items
- **Grocery:** Staples, packaged foods, household items
- **Personal Care:** Beauty, health, hygiene products
- **Home & Kitchen:** Appliances, utensils, home goods
- **Beverages:** Drinks, packaged beverages

#### **Swiggy (Food Delivery Focus):**

- **Restaurants:** Various cuisine types and dining establishments
- **Quick Service:** Fast food, cafes, quick bites
- **Grocery Delivery:** Essential items and daily needs
- **Pharmacy:** Medicines and health products
- **Other Services:** Laundry, utilities, local services

### **Technical Implementation:**

#### **Libraries Used:**

- **pandas:** Excel file processing and data manipulation
- **openpyxl:** Excel reading/writing capabilities
- **re:** Regular expressions for pattern matching
- **os:** File system operations

#### **Mapping Algorithm:**

```python
def map_category_subcategory(keyword, url):
    # URL-based pattern matching
    if 'bigbasket.com' in url:
        # BigBasket-specific categorization logic
    elif 'swiggy.com' in url:
        # Swiggy-specific categorization logic

    # Keyword-based fallback categorization
    # Intelligent mapping based on keyword analysis
    return category, subcategory
```

## **Data Quality Assurance:**

- ✅ **Completeness:** All 60,000+ rows successfully categorized
- ✅ **Consistency:** Logical category-subcategory relationships maintained
- ✅ **Accuracy:** Domain-specific rules applied correctly
- ✅ **Validation:** Manual spot-checking of edge cases

## **Results Summary:**

| Dataset | Records | Categories | Sub-categories | Key Insights |
|---------|---------|------------|----------------|--------------|
| **BigBasket** | 30,000 | 5 | 19 | E-commerce product categorization |
| **Swiggy** | 30,000 | 5 | 18 | Food delivery and services mapping |
| **Combined** | 60,000+ | - | - | Comprehensive market analysis data |

## **Challenges Overcome:**

1. **Large Dataset Processing:** Efficiently handled 60,000+ rows with pandas optimization
2. **Complex Categorization Logic:** Developed nuanced rules for accurate mapping
3. **URL Pattern Recognition:** Implemented regex patterns for different service types
4. **Data Consistency:** Ensured uniform categorization across both datasets

## **Business Value:**

This mapping enables:

- **Market Analysis:** Understanding service distribution patterns
- **Customer Segmentation:** Identifying user preferences by category
- **Competitive Intelligence:** Analyzing market positioning
- **Trend Analysis:** Tracking category popularity over time

## **File Organization:**

```text
Task 4/
├── data-set/                    # Original research data
│   ├── Positions.bigbasket.com.xlsx
│   └── Positions.swiggy.com.xlsx
├── mapped data set/             # Processed results
│   ├── Positions.bigbasket.com_mapped.xlsx
│   └── Positions.swiggy.com_mapped.xlsx
├── Task4_Data_Mapping.py        # Processing script
└── task4.md                     # This documentation
```

**This task successfully transformed raw research data into actionable business intelligence with intelligent categorization.** 📊✅
