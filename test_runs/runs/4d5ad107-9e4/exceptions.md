# Invoice Exception Summary

**Invoice:** INV-009
**Vendor:** Theta Supplies
**Amount:** USD 7500.0
**Priority:** high
**Recommended Action:** route_for_approval
**Approver:** manager

---

## ERROR (3)

### [!!] No purchase order for matching
- **Category:** missing_po
- **Agent:** agent_e_matching
- **Confidence:** 100%
- **Description:** Invoice has no associated PO and policy requires PO matching
- **Recommendation:** Route for non-PO invoice approval

### [!!] Line 1: tax rate mismatch
- **Category:** tax_mismatch
- **Agent:** agent_f_compliance
- **Confidence:** 95%
- **Description:** Tax rate 25.0% differs from expected 18% (tolerance: ±0.5%)
- **Recommendation:** Verify applicable tax rate for this line item

### [!!] Line 2: tax rate mismatch
- **Category:** tax_mismatch
- **Agent:** agent_f_compliance
- **Confidence:** 95%
- **Description:** Tax rate 25.0% differs from expected 18% (tolerance: ±0.5%)
- **Recommendation:** Verify applicable tax rate for this line item

## WARNING (2)

### [!] Missing vendor tax/VAT ID
- **Category:** compliance
- **Agent:** agent_f_compliance
- **Confidence:** 100%
- **Description:** Vendor tax ID is required but not present on invoice
- **Recommendation:** Request vendor tax ID before processing

### [!] Overall effective tax rate mismatch
- **Category:** tax_mismatch
- **Agent:** agent_f_compliance
- **Confidence:** 90%
- **Description:** Effective tax rate 25.0% differs from expected 18%

## INFO (1)

### [i] Suspiciously round amount
- **Category:** anomaly
- **Agent:** agent_g_anomaly
- **Confidence:** 50%
- **Description:** Invoice amount 7500.0 is a round number – may warrant review

## Next Actions

1. Route for non-PO invoice approval
2. Request vendor tax ID before processing
3. Verify applicable tax rate for this line item
