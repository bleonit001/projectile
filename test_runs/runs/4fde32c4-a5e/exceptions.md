# Invoice Exception Summary

**Invoice:** INV-010
**Vendor:** Unknown Supplier XYZ
**Amount:** USD 14160.0
**Priority:** high
**Recommended Action:** route_for_approval
**Approver:** manager

---

## ERROR (2)

### [!!] Vendor not found in master data
- **Category:** new_vendor
- **Agent:** agent_c_vendor
- **Confidence:** 100%
- **Description:** Vendor 'Unknown Supplier XYZ' could not be matched to any vendor in master data (best score: 22.857142857142854)
- **Recommendation:** Create new vendor record or verify vendor name

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

1. Create new vendor record or verify vendor name
2. Route for non-PO invoice approval
3. Request vendor tax ID before processing
