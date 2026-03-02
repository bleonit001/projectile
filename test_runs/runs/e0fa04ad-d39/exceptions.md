# Invoice Exception Summary

**Invoice:** INV-013
**Vendor:** Lambda Consulting
**Amount:** USD 7500.0
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

## WARNING (2)

### [!] Missing vendor tax/VAT ID
- **Category:** compliance
- **Agent:** agent_f_compliance
- **Confidence:** 100%
- **Description:** Vendor tax ID is required but not present on invoice
- **Recommendation:** Request vendor tax ID before processing

### [!] High-value invoice without PO
- **Category:** anomaly
- **Agent:** agent_g_anomaly
- **Confidence:** 80%
- **Description:** Invoice for $7,500.00 has no PO reference – above auto-approve threshold of $5,000.00
- **Recommendation:** Require PO or manager approval for high-value non-PO invoices

## INFO (1)

### [i] Suspiciously round amount
- **Category:** anomaly
- **Agent:** agent_g_anomaly
- **Confidence:** 50%
- **Description:** Invoice amount 7500.0 is a round number – may warrant review

## Next Actions

1. Route for non-PO invoice approval
2. Request vendor tax ID before processing
3. Require PO or manager approval for high-value non-PO invoices
