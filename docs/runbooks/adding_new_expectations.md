# Adding New Expectations Runbook

This guide walks through extending the Great Expectations suites with new business validation rules.

## Prerequisites

- Great Expectations 0.18.x installed
- Familiarity with GE expectation types

## Steps

### 1. Identify the Validation Rule

Before writing code, clearly define:
- Which column(s) the rule applies to
- The expected condition (range, regex, set membership, etc.)
- The severity (warning vs. hard failure)

### 2. Add to the Appropriate Suite

Edit the JSON suite file in `data_quality/great_expectations/expectations/`:

**For raw data validations** — edit `raw_customers_suite.json`:
```json
{
  "expectation_type": "expect_column_values_to_be_between",
  "kwargs": {
    "column": "age",
    "min_value": 18,
    "max_value": 100
  }
}
```

**For curated data validations** — edit `curated_customers_suite.json`:
```json
{
  "expectation_type": "expect_column_values_to_be_in_set",
  "kwargs": {
    "column": "state",
    "value_set": ["CA", "NY", "TX", "FL"]
  }
}
```

### 3. Common Expectation Types

| Type | Use Case | Example |
|------|----------|---------|
| `expect_column_values_to_not_be_null` | Required fields | `customer_id` must exist |
| `expect_column_values_to_match_regex` | Format validation | Email, SSN patterns |
| `expect_column_values_to_be_between` | Numeric ranges | Age 18-90, credit score 300-850 |
| `expect_column_values_to_be_in_set` | Categorical values | State codes, status flags |
| `expect_column_values_to_be_unique` | Uniqueness constraints | `customer_id`, `email` |

### 4. Test the New Expectation

Run the validation suite locally:
```bash
python -m data_quality.checkpoint_runner
```

Or run the full test suite:
```bash
./scripts/run_tests.sh
```

### 5. Update Documentation

Add the new rule to the Data Quality section in README.md with:
- The business justification
- The expected failure rate threshold
- The quarantine routing behavior

## Troubleshooting

- **"Expectation not recognized"** — Verify the expectation type name is spelled correctly
- **"Column not found"** — Check the column name matches the CSV header exactly
- **High failure rate** — The synthetic generator may need adjustment to match the new rule

