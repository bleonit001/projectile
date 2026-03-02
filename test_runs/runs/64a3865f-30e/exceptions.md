# Invoice Exception Summary

**Invoice:** INV-012
**Vendor:** Kappa Indu
**Amount:** USD 1500.0
**Priority:** high
**Recommended Action:** route_for_approval
**Approver:** manager

---

## ERROR (4)

### [!!] Low confidence: invoice_date
- **Category:** low_confidence
- **Agent:** agent_b_extraction
- **Confidence:** 0%
- **Description:** Field 'invoice_date' has confidence 0.00 (threshold: 0.7)
- **Recommendation:** Manual review recommended

### [!!] Vendor not found in master data
- **Category:** new_vendor
- **Agent:** agent_c_vendor
- **Confidence:** 100%
- **Description:** Vendor 'Kappa Indu' could not be matched to any vendor in master data (best score: 76.92307692307692)
- **Recommendation:** Create new vendor record or verify vendor name

### [!!] Missing mandatory field: invoice_date
- **Category:** validation_error
- **Agent:** agent_d_validation
- **Confidence:** 100%
- **Description:** Required field 'invoice_date' is missing or empty
- **Recommendation:** Provide invoice_date before processing

### [!!] No purchase order for matching
- **Category:** missing_po
- **Agent:** agent_e_matching
- **Confidence:** 100%
- **Description:** Invoice has no associated PO and policy requires PO matching
- **Recommendation:** Route for non-PO invoice approval

## WARNING (5)

### [!] Total may not match line items
- **Category:** total_mismatch
- **Agent:** agent_d_validation
- **Confidence:** 90%
- **Description:** Header total (1500.0) differs from computed total (1200.0). Difference: 300.0

### [!] Line 1: amount mismatch
- **Category:** validation_error
- **Agent:** agent_d_validation
- **Confidence:** 100%
- **Description:** Line 1: qty (0.0) × price (0.0) = 0.0, but amount is 1200.0

### [!] Line 1: zero quantity with non-zero amount
- **Category:** validation_error
- **Agent:** agent_d_validation
- **Confidence:** 100%
- **Description:** Line 1 has zero quantity but amount 1200.0

### [!] Missing vendor tax/VAT ID
- **Category:** compliance
- **Agent:** agent_f_compliance
- **Confidence:** 100%
- **Description:** Vendor tax ID is required but not present on invoice
- **Recommendation:** Request vendor tax ID before processing

### [!] Invoice structure incomplete
- **Category:** compliance
- **Agent:** agent_f_compliance
- **Confidence:** 100%
- **Description:** Missing required elements: Missing invoice date
- **Recommendation:** Ensure invoice meets minimum structural requirements

## INFO (1)

### [i] Suspiciously round amount
- **Category:** anomaly
- **Agent:** agent_g_anomaly
- **Confidence:** 50%
- **Description:** Invoice amount 1500.0 is a round number – may warrant review

## Next Actions

1. Manual review recommended
2. Create new vendor record or verify vendor name
3. Provide invoice_date before processing
4. Route for non-PO invoice approval
5. Request vendor tax ID before processing
6. Ensure invoice meets minimum structural requirements
