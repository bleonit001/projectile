# Invoice Exception Summary

**Invoice:** INV-005
**Vendor:** Epsilon Services
**Amount:** USD 6490.0
**Priority:** high
**Recommended Action:** route_for_approval
**Approver:** manager

---

## ERROR (2)

### [!!] Subtotal does not match line items
- **Category:** total_mismatch
- **Agent:** agent_d_validation
- **Confidence:** 100%
- **Description:** Header subtotal (5500.0) does not equal sum of line items (5000.0). Difference: 500.0
- **Recommendation:** Verify line item amounts and subtotal

### [!!] No purchase order for matching
- **Category:** missing_po
- **Agent:** agent_e_matching
- **Confidence:** 100%
- **Description:** Invoice has no associated PO and policy requires PO matching
- **Recommendation:** Route for non-PO invoice approval

## WARNING (1)

### [!] Missing vendor tax/VAT ID
- **Category:** compliance
- **Agent:** agent_f_compliance
- **Confidence:** 100%
- **Description:** Vendor tax ID is required but not present on invoice
- **Recommendation:** Request vendor tax ID before processing

## Next Actions

1. Verify line item amounts and subtotal
2. Route for non-PO invoice approval
3. Request vendor tax ID before processing
