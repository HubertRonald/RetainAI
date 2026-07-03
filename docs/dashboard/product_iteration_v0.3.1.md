# RetainAI Dashboard Product Iteration v0.3.1

## Purpose

This iteration moves the Streamlit dashboard closer to a product-grade HR decision intelligence interface.

## Changes

- Brain-based RetainAI branding.
- Colored `AI` brand suffix.
- Header model chip synchronized with sidebar model selector.
- Removed orphan dark bars caused by raw HTML wrappers around Streamlit widgets.
- Responsive KPI grid.
- Improved spacing between filters, KPIs and charts.
- Filtered dashboard snapshot export.
- Bedrock-ready structured explanation payload.
- Row-level SHAP explanations for tree models.
- Interactive Explainability Explorer charts.

## Design Notes

Streamlit widgets should not be wrapped with raw opening and closing HTML tags because Streamlit does not preserve that DOM hierarchy reliably.

Use HTML components only for complete static visual blocks.

Use Streamlit widgets directly for inputs, file uploaders, tabs and buttons.

## Practical Explainability Flow

```text
Upload CSV/XLSX
    ↓
Validate columns
    ↓
Predict attrition risk
    ↓
Select employee row
    ↓
Generate row-level explanation
    ↓
Build Bedrock-ready explanation payload
```

## Remaining Work

- Export dashboard as visual PDF/PNG snapshot.
- Add true feature value coloring to interactive SHAP distribution.
- Add Retention Advisor prompt template.
- Add API-backed prediction mode.
