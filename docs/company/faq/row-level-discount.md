# Row Level Discount

*Advance FAQ*

## Does the discount apply before or after shipping/tax?

Row-level discounts apply before shipping and tax are calculated. This ensures accurate
tax calculations.

## Can I set tiered discounts at row level (e.g., 10% off for $100, 15% off for $500)?

To achieve this, you'll need to create two separate offers — one for 10% off at $100 and
another for 15% off at $500.

## What if a customer removes one product and the cart value drops below the minimum threshold?

The discount will be recalculated. If the new cart subtotal is below the defined minimum
value (e.g., $100), the discount will no longer apply.

## Can the app differentiate discounts between selected products and non-selected products in the cart?

No, currently the app only provides the option to apply row-level discounts to all
products in the cart.

## In the scenario of two products worth $200 each with a 10% discount, how does the app apply the discount?

If the minimum order value of $100 is met, each product row (worth $200) will receive a
10% discount.

- Product A: $200 → $180
- Product B: $200 → $180
- Total discounted cart: $360
