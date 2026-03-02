# Invoice Exception Summary

**Invoice:** INV-011
**Vendor:** Acme Corp
**Amount:** USD 48000.0
**Priority:** critical
**Recommended Action:** hold
**Approver:** director

---

## CRITICAL (1)

### [!!!] Bank account mismatch – possible fraud risk
- **Category:** bank_change
- **Agent:** agent_c_vendor
- **Confidence:** 100%
- **Description:** Bank account on invoice (NEW-BANK-999) differs from vendor master (BANK-001-ACME)
- **Recommendation:** Verify bank details directly with vendor before payment

## WARNING (3)

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

### [!] Amount just under approval threshold ($50,000.00)
- **Category:** anomaly
- **Agent:** agent_g_anomaly
- **Confidence:** 70%
- **Description:** Invoice amount $48,000.00 is within 5.0% below the $50,000.00 approval threshold
- **Recommendation:** Review for potential threshold manipulation

## INFO (1)

### [i] Suspiciously round amount
- **Category:** anomaly
- **Agent:** agent_g_anomaly
- **Confidence:** 50%
- **Description:** Invoice amount 48000.0 is a round number – may warrant review

## Next Actions

1. Verify bank details directly with vendor before payment
2. Obtain goods receipt confirmation before payment
3. Request vendor tax ID before processing
4. Review for potential threshold manipulation
