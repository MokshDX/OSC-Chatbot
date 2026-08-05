# Draft Order

*Advance FAQ*

## How are wholesale prices applied during checkout?

When a customer proceeds to checkout, the app intercepts the request and creates a Shopify
Draft Order with wholesale pricing applied directly. The discounted price is displayed
without using a strikethrough pricing format.

## How are Shopify discount coupons applied with Draft Orders?

Shopify discount coupons are applied after the wholesale or tier pricing discount has been
calculated.

**Example**

| Description | Amount |
| --- | --- |
| Product Price | $30 |
| Variant Tier Pricing Discount (10%) | -$3 |
| Draft Order Price | $27 |
| Shopify Discount Coupon | -$5 |
| Final Price | $22 |

In this example, the Shopify discount coupon is applied to the discounted Draft Order
price rather than the product's original price

## How can I identify orders created through Draft Order processing?

Every Draft Order and resulting Shopify Order created through the app includes the tag:

```text
oscp-order-processing
```

This tag can be used to identify and track orders processed by the app.

## Which wholesale features are currently supported with Draft Orders?

The current implementation supports Draft Order processing with variant-level tier
pricing. Additional wholesale pricing features will be added in future phases.

## Will Draft Order pricing be visible on the cart page?

No. In the current phase, Draft Order pricing is available only on the checkout page. The
cart page will continue to display the original product prices.

## What happens if I downgrade my app plan?

The Draft Order setting is not automatically removed when a plan is downgraded. Merchants
must manually review and re-save their app settings after changing plans.

## Why does the cart show the original product price?

In Draft Order mode, the cart page continues to display Shopify's regular product prices.
Wholesale pricing becomes visible only after the Draft Order is created and the customer
reaches the checkout page

## Is pricing validated securely?

Yes. All wholesale pricing calculations and discounts are verified server-side to ensure
customers receive the correct pricing and cannot manipulate discount values.

## What happens if a customer clicks Checkout multiple times?

The app includes duplicate-click protection. If the cart contents remain unchanged, the
same Draft Order will be reused within a 15-minute invoice reuse window instead of
creating multiple Draft Orders.
