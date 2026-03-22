# 👣 Break Down Products into Smaller Increments

**Commercial Value:**
Get feedback from customers as fast as possible with what you think is valuable, to validate the commercial side of it.

**Problem:**
- Launch a complete complex product fast in a hacky way → Customer does not use it due to usability errors and unclear problem/solution fit, plus it ships buggy.
- Try to launch a complex product at once → Endless loops of discussion on how to build it, and long development cycles until the product works technically.

---

## Principles

1. **End-to-end value:** Think through a user journey end-to-end — what functionality delivers value?
2. **Simplify:** For every piece of functionality ask:
   - If we remove this, will the user still get the value?
   - If we remove this, will the user still understand the value?
3. **Iteration:** Each iteration ships a set of features that provide additional value (1–2), ensuring fast cycles.
4. **Extensibility:** Build for extensibility — at least >80% of the system should be reusable in the next iteration.

**Definition:**
Value → a customer faces a problem and we solve it. E.g. a customer needs to download their load in Excel and we offer a download button.

---

## Examples

1. **End-to-end value:**
   - Bad: Show the user a yearly load profile in a "Forecasting" tab they would never find.
   - Good: Show the load profile within the procurement navigation where they already work.

2. **Simplify:**
   - Bad: In the first iteration, the user can simulate various load profiles.
   - Good: In the first iteration, the customer has only two options — a fixed load and adjustments to it.

3. **Iteration:**
   - Bad: In the first iteration, the customer has specialized input fields for every adjustment type.
   - Good: The customer has one generic input field for adjustments.

4. **Extensibility:**
   - Bad: Build a naming feature in the first iteration that gets thrown away in the second.
   - Good: Adjustments are kept generic so they can be extended in any form later.

---

## Tooling

> Frameworks give you direction on how to think about it, but not the answer. Be ready to ignore any framework when making a decision.
