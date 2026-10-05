# Validation Report

**Audit date:** 2026-10-04  
**Repository:** `maryamzlf/jewelry-retail-analytics`  
**Validated source commit:** `14a263289c051eed700ea07deab25db5cf4a1828`  
**Final quality workflow:** run **#20** — success

## Scope

This audit rechecked the repository-facing project from source ingestion through analytical outputs, SQL logic, documentation, and Power BI preview consistency.

The validation covered:

- a clean rebuild from the public Kaggle source;
- structural normalization of the 13-field and 11-field source layouts;
- Python syntax and unit tests;
- 50 analytical regression, reconciliation, and data-quality controls;
- semantic comparison of regenerated full transaction and customer-RFM tables against the committed portfolio tables;
- semantic comparison of regenerated curated outputs against the committed CSV outputs;
- SQL/Python parity for RFM recency, quintile scoring, and tie-to-even FM rounding;
- portfolio-preview KPI and ranking checks;
- visible-project placeholder and attribution-marker review.

## Final reconciled snapshot

| Control | Validated result |
|---|---:|
| Transaction lines | 95,911 |
| Orders | 74,760 |
| Customers | 33,397 |
| Products | 9,613 |
| Gross sales | $33,179,324.75 |
| Average order value | $443.81 |
| Repeat customers | 8,976 |
| Repeat customer rate | 26.88% |
| Structurally repaired 11-field rows | 5,352 |
| Missing category code | 15.94% |
| Missing gemstone | 35.51% |

RFM segment counts also reconcile exactly:

- Champions: **2,362**
- At Risk: **1,995**
- Recent Customers: **10,997**
- Potential Loyalists: **7,399**
- Loyal Customers: **878**
- Hibernating: **9,766**

## Corrections made during this audit

### 1. SQL RFM parity

The SQL implementation previously used `DATEDIFF(day)` and `NTILE(5)`. Those are close to the Python logic but are not exact equivalents at elapsed-day and quintile-boundary rows.

The SQL now mirrors the Python implementation by using:

- elapsed whole-day recency from exact timestamps;
- deterministic row-number ranking with the same rank-based quintile boundaries as pandas `qcut`;
- the existing frequency business rules;
- tie-to-even FM rounding consistent with NumPy.

### 2. Merchandising preview

The repository preview for **Revenue by Gemstone** had an ordering discrepancy. The second bar showed `mix`, while the validated output ranks `Unknown` second after diamond.

The preview now follows the validated order:

1. diamond
2. Unknown
3. topaz
4. fianit

### 3. Pipeline reproducibility and identifier integrity

The analytics read path now keeps order, product, category, and customer identifiers explicitly as strings instead of allowing pandas to re-infer them. The small repository schema sample is regenerated directly from the validated clean table, so its field types stay aligned with the pipeline.

The validated analytics environment is pinned to the exact package versions used by the final green build.

### 4. SQL product-attribute parity

Product-level representative `metal` and `gem` values now follow the same rule in SQL as in Python: missing values are excluded when choosing the modal known attribute, and `Unknown` is used only when no known value exists.

### 5. Continuous validation

A new `.github/workflows/quality.yml` workflow now runs:

- Python syntax checks;
- six unit tests;
- full public-source rebuild;
- the 50-control analytical validation suite;
- regenerated-vs-committed table comparisons;
- Power BI preview consistency checks;
- SQL/Python parity checks;
- unfinished-placeholder checks.

The final workflow run completed successfully on run **#20**.

## Power BI validation scope

The GitHub repository does not contain the PBIX binary, and no accessible copy of `Maryam_Jewelry_Portfolio_FINAL.pbix` was available in the connected file library during this audit. Therefore, this audit independently revalidated the **Power BI input tables, documented semantic assumptions, repository previews, KPI values, and preview rankings**, but did not reopen the PBIX binary itself.

The historical Power BI QA record in `powerbi/build_checklist.md` remains the artifact-level record for the Desktop file.

## Attribution / generated-content review

No explicit model/vendor attribution, generated-by marker, placeholder prose, or unfinished implementation marker was found in the current visible project files. This does not prove how every line was authored; it means the repository does not contain an obvious attribution or generated-content artifact that would undermine the portfolio presentation.

## Result

The current repository is internally consistent across the reproducible Python pipeline, committed analytical tables, SQL logic, documented findings, and repository-facing dashboard previews. No unresolved numerical discrepancy was found after the corrections above.
