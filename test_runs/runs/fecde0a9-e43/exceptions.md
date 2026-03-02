# Invoice Exception Summary

**Invoice:** INV-003
**Vendor:** Gamma LLC
**Amount:** USD 11033.0
**Priority:** high
**Recommended Action:** route_for_approval
**Approver:** manager

---

## ERROR (1)

### [!!] Total amount variance exceeds tolerance
- **Category:** price_variance
- **Agent:** agent_e_matching
- **Confidence:** 100%
- **Description:** Invoice total (11033.0) vs PO total (8500.0): variance 850.0 (10.0%)
- **Recommendation:** Review pricing and approve variance

## WARNING (3)

### [!] Line 1: quantity variance 10.0%
- **Category:** quantity_variance
- **Agent:** agent_e_matching
- **Confidence:** 100%
- **Description:** Invoice qty (110.0) vs PO qty (100.0): 10.0% variance (tolerance: ±5.0%)

### [!] Line 2: quantity variance 10.0%
- **Category:** quantity_variance
- **Agent:** agent_e_matching
- **Confidence:** 100%
- **Description:** Invoice qty (55.0) vs PO qty (50.0): 10.0% variance (tolerance: ±5.0%)

### [!] Missing vendor tax/VAT ID
- **Category:** compliance
- **Agent:** agent_f_compliance
- **Confidence:** 100%
- **Description:** Vendor tax ID is required but not present on invoice
- **Recommendation:** Request vendor tax ID before processing

## Next Actions

1. Review pricing and approve variance
2. Request vendor tax ID before processing
