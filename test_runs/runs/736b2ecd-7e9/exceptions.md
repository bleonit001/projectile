# Invoice Exception Summary

**Invoice:** INV-004
**Vendor:** Delta Co
**Amount:** USD 6195.0
**Priority:** high
**Recommended Action:** route_for_approval
**Approver:** manager

---

## ERROR (2)

### [!!] Line 1: price variance 5.0%
- **Category:** price_variance
- **Agent:** agent_e_matching
- **Confidence:** 100%
- **Description:** Invoice price (105.0) vs PO price (100.0): 5.0% variance (tolerance: ±2.0%)

### [!!] Total amount variance exceeds tolerance
- **Category:** price_variance
- **Agent:** agent_e_matching
- **Confidence:** 100%
- **Description:** Invoice total (6195.0) vs PO total (5000.0): variance 250.0 (5.0%)
- **Recommendation:** Review pricing and approve variance

## WARNING (1)

### [!] Missing vendor tax/VAT ID
- **Category:** compliance
- **Agent:** agent_f_compliance
- **Confidence:** 100%
- **Description:** Vendor tax ID is required but not present on invoice
- **Recommendation:** Request vendor tax ID before processing

## Next Actions

1. Review pricing and approve variance
2. Request vendor tax ID before processing
