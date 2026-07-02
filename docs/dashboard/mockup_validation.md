# Dashboard Mockup Validation

## Questions

```text
Does every page have a clear purpose?
Does every chart map to an available data source?
Does every visual element have a module/API source?
Does every required artifact exist?
Does the layout follow the fancy dark theme?
Does local mode work without API?
Does API mode have a clear fallback?
```

## Checklist

```text
[ ] Dashboard has exactly four initial pages.
[ ] Each page maps to one analytical experience.
[ ] Each page has at least one local data source.
[ ] Each page has a future API domain.
[ ] Executive Overview uses historical data only.
[ ] Prediction Center uses uploaded or sample prediction data.
[ ] Explainability Explorer uses existing SHAP artifacts.
[ ] Survival Analytics uses existing survival artifacts.
[ ] No page recomputes expensive modeling logic.
[ ] No page requires external font access.
[ ] Layout uses dark theme tokens.
[ ] Sidebar controls do not duplicate page-level controls.
[ ] Mockup can be validated before Streamlit implementation.
```

---

# Product Dashboard Iteration Notes

This iteration fixes three implementation gaps:

1. Dashboard chart functions must be importable from `modules.dashboard.charts`.
2. Streamlit widgets used across sidebar and pages must define unique keys.
3. Navigation should use visible icons and a product-oriented sidebar.

Additional dashboard validation checks:

```text
[ ] attrition_rate_by_category is available.
[ ] histogram_by_attrition is available.
[ ] Explainability model selector has a unique key.
[ ] Sidebar model selector has a unique key.
[ ] Data Dictionary page is linked from sidebar.
[ ] Survival Analytics uses interactive Plotly charts.
```
