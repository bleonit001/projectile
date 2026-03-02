# Invoice Exception Summary

**Invoice:** INV-008
**Vendor:** Sakura Electronics
**Amount:** JPY 1980000.0
**Priority:** normal
**Recommended Action:** route_for_approval
**Approver:** director

---

## WARNING (5)

### [!] Currency 'JPY' not in allowed list
- **Category:** compliance
- **Agent:** agent_d_validation
- **Confidence:** 100%
- **Description:** Invoice currency JPY is not in allowed currencies: ['USD', 'EUR', 'GBP', 'CHF']
- **Recommendation:** Verify currency and check FX handling

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

### [!] Overall effective tax rate mismatch
- **Category:** tax_mismatch
- **Agent:** agent_f_compliance
- **Confidence:** 90%
- **Description:** Effective tax rate 10.0% differs from expected 18.0%

### [!] Non-standard currency: JPY
- **Category:** compliance
- **Agent:** agent_f_compliance
- **Confidence:** 100%
- **Description:** Currency 'JPY' is not in allowed list: ['USD', 'EUR', 'GBP', 'CHF']
- **Recommendation:** Verify currency handling and FX conversion

## INFO (1)

### [i] Suspiciously round amount
- **Category:** anomaly
- **Agent:** agent_g_anomaly
- **Confidence:** 50%
- **Description:** Invoice amount 1980000.0 is a round number – may warrant review

## Next Actions

1. Verify currency and check FX handling
2. Obtain goods receipt confirmation before payment
3. Request vendor tax ID before processing
4. Verify currency handling and FX conversion
