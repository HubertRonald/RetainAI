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
