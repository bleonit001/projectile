# Invoice Exception Summary

**Invoice:** INV-002
**Vendor:** Beta Industries
**Amount:** USD 3776.0
**Priority:** normal
**Recommended Action:** approve_and_post
**Approver:** auto

---

## WARNING (2)

### [!] No GRN for 3-way matching
- **Category:** missing_grn
- **Agent:** agent_e_matching
- **Confidence:** 100%
- **Description:** GRN required for goods invoices but none found
- **Recommendation:** Obtain goods receipt confirmation before payment

### [!] Missing vendor tax/VAT ID
- **Category:** compliance
- **Agent:** agent_f_compliance
- **Confidence:** 100%
- **Description:** Vendor tax ID is required but not present on invoice
- **Recommendation:** Request vendor tax ID before processing

## Next Actions

1. Obtain goods receipt confirmation before payment
2. Request vendor tax ID before processing
