# Invoice Exception Summary

**Invoice:** CN-001
**Vendor:** Acme Corp
**Amount:** USD -472.0
**Priority:** high
**Recommended Action:** route_for_approval
**Approver:** manager

---

## ERROR (1)

### [!!] No purchase order for matching
- **Category:** missing_po
- **Agent:** agent_e_matching
- **Confidence:** 100%
- **Description:** Invoice has no associated PO and policy requires PO matching
- **Recommendation:** Route for non-PO invoice approval

## WARNING (3)

### [!] Line 1: negative amount
- **Category:** validation_error
- **Agent:** agent_d_validation
- **Confidence:** 100%
- **Description:** Line item 1 has negative amount: -250.0

### [!] Line 2: negative amount
- **Category:** validation_error
- **Agent:** agent_d_validation
- **Confidence:** 100%
- **Description:** Line item 2 has negative amount: -150.0

### [!] Missing vendor tax/VAT ID
- **Category:** compliance
- **Agent:** agent_f_compliance
- **Confidence:** 100%
- **Description:** Vendor tax ID is required but not present on invoice
- **Recommendation:** Request vendor tax ID before processing

## Next Actions

1. Route for non-PO invoice approval
2. Request vendor tax ID before processing
