<!-- converted from OSCP_B2B_Scenario_Document.docx -->

OSCP Wholesale B2B Pricing
Scenario Document — Real World Business Coverage

Version: 1.0       Status: Draft       Team: OSCP Professionals
App Listing: apps.shopify.com/custom-pricing-wholesale
# 1. Purpose & Scope
This document maps every feature of the OSCP B2B Wholesale Pricing Shopify app to real-world merchant scenarios. It defines what the app does for each type of merchant, how the system responds to customer actions, and the acceptance criteria the development team must satisfy. It also explicitly lists scenarios that are out of scope for the current version.

Audience: Product managers, junior developers, QA engineers, and merchant support staff.

How to use this document: Section 2 provides a feature summary. Section 3 contains the full scenario tables — one per scenario. Section 4 lists out-of-scope scenarios with explicit decisions and reasons.

# 2. Feature & Scenario Summary
The table below maps each app feature to its scenario IDs, priority, and the merchant types it serves.


# 3. Scenario Detail Tables
Each table below represents one real-world scenario. Rows are: merchant context, configuration, what the customer does, what the system must do, edge cases, and acceptance criteria.

## 3.1 Quantity Break Pricing





## 3.2 Customer Tag-Based Tier Pricing





## 3.3 Markets-Based Pricing



## 3.4 Cart-Level Discount





## 3.5 Order Limits





## 3.6 B2B Registration Form



## 3.7 Quick Order / Bulk Order Form



## 3.8 Tax Display by Country



## 3.9 Bulk CSV Import / Export



## 3.10 Auto Order Tagging



## 3.11 Hide Shipping Methods



## 3.12 Email Notifications


# 4. Out-of-Scope Scenarios
The following scenarios were considered and explicitly decided against for the current version. These are not oversights — they are recorded decisions.



# 5. Glossary
Customer tag: A label applied to a Shopify customer account used to segment customers (e.g., 'wholesale', 'vip', 'retailer').
Tier / Quantity break: A pricing rule that changes the unit price or discount when the quantity in the cart reaches a defined threshold.
PDP: Product Detail Page — the individual product page on the storefront.
Cart level discount: A discount applied to the order total (not individual products), triggered by cart value or item count.
Shopify Market: A regional store configuration in Shopify that allows different currencies, languages, and pricing per region.
Quick Order Form: A form that lets B2B customers enter multiple SKUs and quantities at once, adding all items to the cart in a single action.
MOQ: Minimum Order Quantity — the smallest number of units a merchant will accept in a single order.
Metafield: Custom data fields on Shopify products or variants used to store extra attributes like brand, warehouse, or material.
| Feature ID | Feature name | Scenarios | Priority | Merchant type served |
| --- | --- | --- | --- | --- |
| FEAT-01 | Quantity Break Pricing | SCN-001, SCN-002 | High | Wholesale, bulk, volume sellers |
| FEAT-02 | Customer Tag Tier Pricing | SCN-003, SCN-004 | High | B2B with multiple customer segments |
| FEAT-03 | Markets-Based Pricing | SCN-005 | High | International / multi-region sellers |
| FEAT-04 | Cart Level Discount | SCN-006, SCN-007 | Med | General B2B and retail merchants |
| FEAT-05 | Order Limits (Min / Max) | SCN-008, SCN-009 | High | Wholesale suppliers, manufacturers |
| FEAT-06 | B2B Registration Form | SCN-010 | High | Brands vetting wholesale accounts |
| FEAT-07 | Quick / Bulk Order Form | SCN-011 | High | Repeat B2B buyers with known SKUs |
| FEAT-08 | Tax Display by Country | SCN-012 | Med | International B2B / EU VAT sellers |
| FEAT-09 | Bulk CSV Import/Export | SCN-013 | Med | Large catalogues, many variants |
| FEAT-10 | Auto Order Tagging | SCN-014 | Med | Multi-brand / multi-warehouse stores |
| FEAT-11 | Hide Shipping Methods | SCN-015 | Med | Mixed B2B + retail on same store |
| FEAT-12 | Email Notifications | SCN-016 | Med | Registration workflow automation |
| SCN-001  ·  Quantity Break Pricing — Percentage off | SCN-001  ·  Quantity Break Pricing — Percentage off |
| --- | --- |
| Merchant type | Wholesale distributor / bulk seller |
| Merchant goal | Incentivise customers to buy larger quantities by offering percentage discounts at defined quantity thresholds |
| Config / feature used | Quantity Break Pricing — Percentage Off per unit |
| Config value / setting | Buy 10 → 5% off · Buy 20 → 10% off · Buy 30 → 15% off |
| Customer action | Adds 25 units of a product to the cart |
| System response | Tier 2 (10% off) is automatically applied. Price per unit updates in cart. Tier pricing widget on the product page highlights the active tier. |
| Edge cases | Customer adds exactly the threshold quantity (e.g., 10) — discount must apply
Customer removes items and falls below a threshold — discount must be removed
Quantity is 0 or empty — no discount, no error
Discount stacked with a Shopify discount code — verify compatibility |
| Acceptance criteria | Cart total reflects correct discounted price per unit for the active tier
Tier widget on PDP highlights the correct tier in real time
Removing items downgrades tier and recalculates price automatically
No JavaScript errors in console during quantity change |
| Priority | High |
| SCN-002  ·  Quantity Break Pricing — Fixed price per unit | SCN-002  ·  Quantity Break Pricing — Fixed price per unit |
| --- | --- |
| Merchant type | Manufacturer selling direct to trade accounts |
| Merchant goal | Show trade customers a clear, predictable price ladder rather than percentage discounts |
| Config / feature used | Quantity Break Pricing — Fixed Price Per Unit |
| Config value / setting | Original $300 · Buy 10 → $280 each · Buy 20 → $260 each · Buy 30 → $240 each |
| Customer action | Adds 22 units to the cart |
| System response | System applies $260 per unit (Tier 2). Cart line total = 22 × $260 = $5,720. PDP tier table highlights Tier 2 row. |
| Edge cases | Fixed price higher than original price — should be blocked or flagged in admin
Multiple variants of the same product — price per variant must be independent
Currency conversion in multi-currency store — fixed price must convert correctly |
| Acceptance criteria | Cart shows correct fixed unit price for the threshold reached
PDP tier widget shows all tiers and highlights the active one
Price does not flicker or revert on page reload |
| Priority | High |
| SCN-003  ·  Customer Tag-Based Tier Pricing — Wholesale group | SCN-003  ·  Customer Tag-Based Tier Pricing — Wholesale group |
| --- | --- |
| Merchant type | B2B store serving mixed retail and wholesale customers |
| Merchant goal | Show different price tiers to wholesale-tagged customers without affecting retail shoppers |
| Config / feature used | Customer Tag-Based Tier Pricing |
| Config value / setting | Tag: 'wholesale' · Buy 10 → 10% off · Buy 20 → 15% off |
| Customer action | Logged-in wholesale customer adds 15 units to cart |
| System response | Tier 1 (10% off) is applied exclusively for this customer. Retail customers viewing the same product see standard pricing with no tier discount. |
| Edge cases | Customer has both 'wholesale' and 'vip' tags — most favourable rule should apply
Customer logs out mid-session — discount must be removed from cart
Guest customer reaches the quantity threshold — no wholesale discount shown
Admin removes tag from customer account — discount must not apply on next login |
| Acceptance criteria | Wholesale customer sees tier pricing on PDP; retail customer does not
Correct tier activates based on cart quantity
Tag removal takes effect within one session refresh |
| Priority | High |
| SCN-004  ·  Customer Tag-Based Tier Pricing — Multiple customer groups | SCN-004  ·  Customer Tag-Based Tier Pricing — Multiple customer groups |
| --- | --- |
| Merchant type | Distributor managing retailers, VIP accounts and general public |
| Merchant goal | Maintain separate pricing structures for each customer segment from one admin panel |
| Config / feature used | Customer Tag-Based Tier Pricing — multiple tag rules |
| Config value / setting | Tag: 'retailer' · Buy 5 → 4%, Buy 10 → 8% · Tag: 'vip' · Buy 5 → 12%, Buy 10 → 18% |
| Customer action | VIP-tagged customer adds 8 units to cart |
| System response | VIP Tier 1 (12% off) is applied. A retailer adding the same 8 units would receive 4% off. An untagged guest receives no discount. |
| Edge cases | Two rules with overlapping tag conditions — document expected priority
Rule exists for a tag that no customer currently holds — rule is saved but inactive
Admin edits a live rule — existing open carts must recalculate on next page load |
| Acceptance criteria | Each tag group receives exactly its configured discount, not another group's
Dashboard shows all tag rules and their current status (active / no matching customers) |
| Priority | High |
| SCN-005  ·  Markets-Based Pricing — Region-specific volume discounts | SCN-005  ·  Markets-Based Pricing — Region-specific volume discounts |
| --- | --- |
| Merchant type | International brand selling wholesale across multiple Shopify Markets |
| Merchant goal | Offer different discount structures per region to reflect local market conditions and currency |
| Config / feature used | Markets-Based Pricing |
| Config value / setting | USA (USD): Buy 10 → 5%, Buy 20 → 10% · Europe (EUR): Buy 10 → 10%, Buy 20 → 20% |
| Customer action | European wholesale customer adds 12 units to cart |
| System response | European tier (10% off at qty 10) is applied and price is displayed in EUR. A US customer adding the same quantity would receive 5% off in USD. |
| Edge cases | Customer switches their market/region mid-session — pricing must update
Market has no pricing rule configured — fall back to global rule or no discount
Currency conversion rate changes — display must reflect Shopify's current rate |
| Acceptance criteria | Correct market-specific discount applied based on customer's Shopify Market
Prices display in the correct currency for the market
Fallback to default pricing when no market rule exists |
| Priority | High |
| SCN-006  ·  Cart-Level Discount — Cart value threshold | SCN-006  ·  Cart-Level Discount — Cart value threshold |
| --- | --- |
| Merchant type | General B2B or retail merchant wanting to reward high-value orders |
| Merchant goal | Increase average order value by offering a flat discount when cart total exceeds a threshold |
| Config / feature used | Cart Level Discount — by cart value |
| Config value / setting | $20 off for orders over $200 |
| Customer action | Customer's cart reaches $220 total |
| System response | $20 is automatically deducted at cart level. Order summary shows subtotal, discount line ($20), and new total ($200). |
| Edge cases | Cart drops below $200 after removing an item — discount must be removed
Cart is exactly $200 — discount applies (boundary condition)
Cart discount combined with product-level tier discount — verify total is correct
Multiple currencies — threshold must be evaluated in the correct currency |
| Acceptance criteria | Discount line appears in cart summary only when threshold is met
Discount is removed automatically if cart drops below threshold
Final checkout total is mathematically correct |
| Priority | Med |
| SCN-007  ·  Cart-Level Discount — Item quantity threshold | SCN-007  ·  Cart-Level Discount — Item quantity threshold |
| --- | --- |
| Merchant type | Stationery / office supplies merchant |
| Merchant goal | Reward customers who buy in bulk by giving a percentage off when they reach an item count |
| Config / feature used | Cart Level Discount — by item quantity |
| Config value / setting | 10% off when buying more than 10 items |
| Customer action | Customer adds 11 items across different products to cart |
| System response | 10% discount applied to cart total. Summary shows subtotal and a 10% discount line. |
| Edge cases | Items removed to bring count to exactly 10 — boundary: discount should still apply
Mixed cart of discounted and non-discounted items — cart discount applies to overall total
Customer uses a Shopify coupon code alongside cart discount — verify stacking behaviour |
| Acceptance criteria | Discount activates at the correct item count
Discount is removed when count falls below threshold
Cart summary clearly shows the discount as a separate line |
| Priority | Med |
| SCN-008  ·  Order Limits — Minimum order value | SCN-008  ·  Order Limits — Minimum order value |
| --- | --- |
| Merchant type | Wholesale supplier wanting to avoid small unprofitable orders |
| Merchant goal | Block checkout when the cart value is below the minimum order threshold and guide customers to add more |
| Config / feature used | Order Limit — Minimum cart value |
| Config value / setting | Minimum order value: $150 |
| Customer action | Customer tries to proceed to checkout with an $80 cart |
| System response | Checkout is blocked. A customisable notice is displayed: 'Add $70 more to place your order.' Checkout button is disabled until the threshold is met. |
| Edge cases | Cart is exactly $150 — checkout must be allowed
Customer applies a discount code that reduces total below $150 — block must trigger
Minimum set to $0 — feature is effectively disabled, no block shown
Multiple currencies — minimum evaluated in store's base currency |
| Acceptance criteria | Checkout is blocked and message shows the exact shortfall amount
Checkout is enabled as soon as cart meets the minimum
Message is readable and matches the customised text set in admin |
| Priority | High |
| SCN-009  ·  Order Limits — Minimum & maximum order quantity | SCN-009  ·  Order Limits — Minimum & maximum order quantity |
| --- | --- |
| Merchant type | Manufacturer with inventory constraints |
| Merchant goal | Prevent orders that are too small (below MOQ) or too large (exceeding stock capacity) from being placed |
| Config / feature used | Order Limit — Minimum quantity + Maximum quantity |
| Config value / setting | Min: 10 units · Max: 500 units |
| Customer action | Customer A attempts checkout with 5 units. Customer B attempts checkout with 600 units. |
| System response | Customer A sees: 'Minimum order is 10 units — add 5 more to continue.' Customer B sees: 'Maximum order is 500 units — reduce your cart to continue.' Both checkouts are blocked. |
| Edge cases | Quantity is exactly at min or max — both should be allowed
Min > Max configured by mistake in admin — system should warn merchant
Mixed cart with some items having limits and some not — total quantity logic documented |
| Acceptance criteria | Both min and max limits block checkout with the correct, specific message
Boundary quantities (exactly min / exactly max) allow checkout
Admin receives a validation warning if min > max |
| Priority | High |
| SCN-010  ·  B2B Registration Form — Wholesale account application | SCN-010  ·  B2B Registration Form — Wholesale account application |
| --- | --- |
| Merchant type | B2B brand that wants to vet wholesale customers before granting access |
| Merchant goal | Collect business details from applicants, review them, and approve or reject wholesale accounts |
| Config / feature used | Registration Form — custom fields + email notifications |
| Config value / setting | Fields: Business name, VAT number, Annual turnover, Upload trade licence. Auto-email to merchant on submission. |
| Customer action | A retailer fills in and submits the wholesale registration form |
| System response | Merchant receives an email notification with form details. Customer receives a confirmation email. Account is placed in 'pending' state until merchant approves and applies the relevant customer tag. |
| Edge cases | Required field left blank — form must not submit and must highlight the missing field
Email notification fails to send — submission should still be saved
Merchant approves the same customer twice — idempotent tag application
File upload exceeds size limit — user shown a clear error |
| Acceptance criteria | Form submission is saved in the merchant's admin view
Merchant receives email within 2 minutes of submission
Customer receives confirmation email
Mandatory fields enforce validation before submission |
| Priority | High |
| SCN-011  ·  Quick Order Form — Multi-SKU bulk purchasing | SCN-011  ·  Quick Order Form — Multi-SKU bulk purchasing |
| --- | --- |
| Merchant type | Distributor with repeat wholesale customers who know their SKUs |
| Merchant goal | Let B2B customers place large orders quickly by entering SKUs and quantities without visiting individual product pages |
| Config / feature used | Quick Order Form — enabled in app settings |
| Config value / setting | Form enabled; up to 50 products per order; tiered pricing rules apply |
| Customer action | Customer enters 12 SKUs with quantities into the Quick Order Form and clicks 'Add All to Cart' |
| System response | All 12 line items are added to cart in a single action. Any applicable tiered discounts are calculated per SKU. Cart is updated and customer is redirected to cart page. |
| Edge cases | SKU does not exist — row shows 'SKU not found' error; other SKUs still added
SKU is out of stock — row flagged; customer can continue with remaining items
Duplicate SKU entered — quantities are combined into one line
More than 50 SKUs entered — system caps at 50 and notifies customer |
| Acceptance criteria | All valid SKUs are added to cart with correct quantities
Tiered pricing is applied per SKU based on quantity entered
Invalid or out-of-stock SKUs are clearly flagged without blocking valid items
Form resets cleanly after successful submission |
| Priority | High |
| SCN-012  ·  Tax Display — Country-based inclusive/exclusive tax on PDP | SCN-012  ·  Tax Display — Country-based inclusive/exclusive tax on PDP |
| --- | --- |
| Merchant type | International seller with B2B customers in tax-registered regions (e.g., EU VAT) |
| Merchant goal | Show tax-inclusive prices to consumers and tax-exclusive prices to VAT-registered businesses depending on their country |
| Config / feature used | Tax Display — country-based tax configuration |
| Config value / setting | UK: show price inclusive of 20% VAT. Germany: show price inclusive of 19% VAT. USA: show price exclusive of tax. |
| Customer action | UK customer views a product priced at £100 ex-VAT |
| System response | PDP displays £120 (inc. 20% VAT) alongside the tier pricing widget. A US customer viewing the same product sees $100 + tax. |
| Edge cases | Customer's country cannot be detected (no IP data) — fall back to store default
Tax rate changes (e.g., government update) — admin must be able to update rate
Product is tax-exempt — zero tax displayed, not an error |
| Acceptance criteria | Correct tax-inclusive or exclusive price shown based on detected country
Tax amount is visually clear alongside tier pricing widget
Fallback works gracefully when country is unknown |
| Priority | Med |
| SCN-013  ·  Bulk CSV Import — Pricing rules at scale | SCN-013  ·  Bulk CSV Import — Pricing rules at scale |
| --- | --- |
| Merchant type | Large wholesale merchant with hundreds of variants across many products |
| Merchant goal | Load or update hundreds of discount rules in one step without manual data entry in the admin UI |
| Config / feature used | Bulk Export & Import — CSV upload |
| Config value / setting | Up to 200 variant-level rules per import; CSV matches sample template format |
| Customer action | Merchant uploads a CSV file with 180 discount rules |
| System response | All 180 rules are imported and active within the app. Merchant sees a success summary. Existing rules for the same variants are overwritten with the new values. |
| Edge cases | CSV has an invalid row (missing column) — import fails cleanly with row-level error report
CSV exceeds 200 rows on free plan — system blocks import and shows upgrade prompt
Same variant appears twice in the CSV — last row wins (documented behaviour)
CSV uses wrong currency codes — validation error returned |
| Acceptance criteria | Valid CSV imports all rules and confirms count to merchant
Invalid rows are reported with row number and reason; valid rows still import
Existing rules are correctly overwritten, not duplicated |
| Priority | Med |
| SCN-014  ·  Auto Order Tag — Tag orders by product metafield | SCN-014  ·  Auto Order Tag — Tag orders by product metafield |
| --- | --- |
| Merchant type | Multi-brand or multi-warehouse merchant needing automated order routing |
| Merchant goal | Automatically tag placed orders based on product attributes (brand, warehouse) to route them to the correct fulfilment team without manual intervention |
| Config / feature used | Auto Order Tag — metafield-based tagging rules |
| Config value / setting | Metafield: product.brand = 'BrandA' → tag order 'brand-a'. Metafield: product.warehouse = 'WH-North' → tag order 'wh-north' |
| Customer action | Customer places an order containing a BrandA product and a WH-North product |
| System response | Order is automatically tagged with both 'brand-a' and 'wh-north' in Shopify admin. Fulfilment teams can filter by tag to see their relevant orders. |
| Edge cases | Order contains products with no matching metafield — no tag added for that product; other tags still applied
Two products trigger the same tag — tag applied once (no duplicate tags)
Metafield value changes after order is placed — existing order tags are not retroactively changed
Order cancelled — tags remain on order for audit trail |
| Acceptance criteria | Correct tags appear on the order in Shopify admin immediately after placement
No duplicate tags are applied
Orders with no matching metafields receive no spurious tags |
| Priority | Med |
| SCN-015  ·  Hide Shipping Methods — Customer-tag-based checkout control | SCN-015  ·  Hide Shipping Methods — Customer-tag-based checkout control |
| --- | --- |
| Merchant type | B2B merchant offering different fulfilment options to wholesale vs retail customers |
| Merchant goal | Show 'Freight delivery' only to wholesale-tagged customers and hide it from retail shoppers to avoid confusion and misuse |
| Config / feature used | Hide Shipping Methods — tag-based rule |
| Config value / setting | Show 'Freight delivery' only for customers tagged 'wholesale'. Hide for all others. |
| Customer action | Retail (untagged) customer reaches checkout |
| System response | 'Freight delivery' is hidden. Only standard shipping options are displayed. A wholesale-tagged customer checking out sees 'Freight delivery' as an available option. |
| Edge cases | Customer has no tag — all hidden methods remain hidden
All shipping methods are hidden for a customer — checkout must not break; at least one method should always be visible or a clear message shown
Merchant adds a new shipping method — new method appears by default until a hide rule is configured |
| Acceptance criteria | Wholesale-tagged customer sees freight option; retail customer does not
Checkout does not error when a method is hidden
Hiding rules update within one checkout page reload |
| Priority | Med |
| SCN-016  ·  Personalised Email Notifications — Registration workflow | SCN-016  ·  Personalised Email Notifications — Registration workflow |
| --- | --- |
| Merchant type | B2B brand using the registration form to onboard wholesale accounts |
| Merchant goal | Automatically notify the merchant when a new B2B registration is submitted, and keep the applicant informed of their application status |
| Config / feature used | Personalised Email Notification Settings |
| Config value / setting | Merchant notification: custom subject + body. Applicant confirmation email: custom message with business name field merged in. |
| Customer action | Wholesale applicant submits the B2B registration form |
| System response | Merchant email sent within 2 minutes with form data summary. Applicant receives confirmation email with their business name merged into the template. Both emails render correctly on mobile. |
| Edge cases | Merchant's email address is incorrect — email bounces; form data still saved in admin
Email template has a missing merge field — should render blank gracefully, not crash
Applicant provides invalid email — submission is still saved; merchant is still notified |
| Acceptance criteria | Merchant receives email with all submitted field values within 2 minutes
Applicant receives confirmation email with correctly merged data
Both emails are readable on desktop and mobile email clients |
| Priority | Med |
| ID | Scenario description | Reason not building | Revisit | Decided by |
| --- | --- | --- | --- | --- |
| SCN-X01 | Customer-level fixed price per individual SKU (different price per customer, not per tag group) | High implementation complexity; Shopify API limits individual customer price overrides at scale | Q3 review | Team |
| SCN-X02 | Multiple cart-level discount rules (e.g., $20 off + 10% off simultaneously) | Current cart discount supports one rule only; requires architectural change | Q2 review | Team |
| SCN-X03 | Net 30 / net 60 payment terms at checkout | Outside scope of pricing app; better handled by a dedicated payment terms app | Not planned | Team |
| SCN-X04 | Customer-tag-based cart discount (different cart thresholds per tag group) | Planned future feature; not yet built | Q2 development | Team |