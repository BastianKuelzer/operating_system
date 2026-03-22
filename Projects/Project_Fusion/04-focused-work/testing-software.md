# 🧪 Testing Software

**Commercial Value:**
Test as fast as possible that no bad customer experience happens and that the tech team does not need to fix issues afterwards — fixing issues after deployment costs more time than catching them during testing.

**Problem:**
- No testing → errors deployed to production that cost more time to fix.
- Testing everything 100% → too much time invested, no overall progress.

---

## Principles

1. **Testing scrutiny:** Features with large impact (e.g., updating 100 AE sales presentations before a pitch day) need thorough testing. Small beta features need some testing but not extremely extensive.
2. **Speed:** Test as fast as possible to unblock engineering — same day or within a couple of hours if possible.
3. **Hierarchy:** Think from the customer first and main use cases. Does the number make sense? Does the happy flow make sense? Then go deeper into edge cases.
4. **Automate:** Use AI to write test scenarios and think about edge cases.

---

## Automation

- **Automation 1:** Langdock Assistant "Testing Software for Product Manager"
- **Automation 2:** Use Perplexity Browser, log into the product, copy-paste the output from Automation 1

---

## Test Case Template

| TEST CASE ID | TEST SCENARIO | TEST CASE | PRE-CONDITION | TEST STEPS | TEST DATA | EXPECTED RESULT | ACTUAL RESULT | STATUS |
|---|---|---|---|---|---|---|---|---|
| TC_001 | Scenario description | Specific case | Preconditions | Steps | Test data | Expected outcome | Actual outcome | PASS/FAIL |
