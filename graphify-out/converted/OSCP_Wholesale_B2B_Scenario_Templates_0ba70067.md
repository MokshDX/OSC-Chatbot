<!-- converted from OSCP_Wholesale_B2B_Scenario_Templates.xlsx -->

## Sheet: Scenario Master
| OSCP Wholesale B2B Pricing — Scenario Master |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| One row per scenario. Covers all feature areas. Reference rows in feature sheets for deep-dive config.    [App: custom-pricing-wholesale] |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Scenario ID | Feature Area | Scenario Name | Merchant Archetype | Who Is The Customer | Business Goal | App Config Used | Pricing Rule Type | Customer Tag(s) | Trigger (What Happens) | Expected Admin Behavior | Expected Storefront Output | Edge Cases | Acceptance Criteria | Priority (H/M/L) | Status |
| SCN-001 | Tiered / Volume Pricing | Wholesale tier: 10% off for tag "wholesale" | Distributor / Reseller | B2B buyer with "wholesale" tag | Offer lower margin to volume buyers | Customer tag rule: wholesale → 10% off all products | Percentage discount by tag | wholesale | Tagged customer views any product page | Rule engine applies 10% reduction to all product prices for tagged customer | PDP shows crossed-out retail price + discounted price; cart reflects discounted total | Customer has multiple tags — highest discount wins. Guest (no tag) sees retail price. | 1) Tagged customer sees discounted price on PDP
2) Cart total matches discounted price
3) Untagged customer sees original price | H | Draft |
| SCN-002 | Quantity Breaks | Buy 10–19 units → 5%, 20+ → 12% on SKU-level | Manufacturer selling direct | Any customer / bulk buyer | Reward larger order quantities | Quantity break rule on product variant: 10–19 = 5%, 20+ = 12% | Quantity-based tiered % | all / untagged | Customer changes qty in cart or PDP quantity selector | App evaluates qty brackets in real time and updates price | Tier pricing table displayed on PDP; cart line item price updates as qty changes | Qty drop below tier threshold mid-session — price reverts. Mixed variants in cart counted separately. | 1) Tier table visible on PDP
2) Price updates on qty change without page reload
3) Each variant tier evaluated independently | H | Draft |
| SCN-003 | Custom Fixed Price | VIP account "acme-corp" has fixed $8.50 per unit on SKU-789 | B2B key account | Named account customer (tagged "acme-corp") | Honor negotiated contract price | Fixed price rule: tag=acme-corp, variant=SKU-789, price=$8.50 | Fixed price by tag + variant | acme-corp | acme-corp tagged user adds SKU-789 to cart | App overrides Shopify variant price with fixed $8.50 for this tag | PDP shows $8.50 (no crossed-out price). Cart shows $8.50/unit. | Same SKU in different currency market — must convert or block. Multiple fixed rules for same tag+variant → app applies most specific. | 1) Price shown is exactly $8.50
2) No other discount stacks unless configured
3) Other customers see standard price | H | Draft |
| SCN-004 | B2B Registration Form | Prospect submits wholesale registration form | New wholesale prospect | Unverified visitor wanting B2B account | Capture and qualify leads | Custom registration form with fields: Company, VAT, Order Volume. Auto-tag on approval. | Registration workflow | (pending until approved) | Visitor clicks "Apply for wholesale" CTA | Form submission creates customer record; sends approval email; admin reviews in dashboard | Thank-you message shown. Customer cannot access wholesale prices until approved. | Duplicate email submission. Form submitted without required fields. Admin never approves — customer stuck. | 1) Required fields validated before submit
2) Admin receives notification
3) Wholesale prices not visible pre-approval | H | Draft |
| SCN-005 | Quick Order Form | B2B buyer adds 12 SKUs by pasting a list | Distributor reordering monthly stock | Approved wholesale customer | Reduce reorder friction | Quick Order Form enabled; tiered pricing active | Bulk SKU entry | wholesale | Customer navigates to Quick Order page, enters SKUs + qtys | App resolves SKUs, applies relevant pricing rules, adds all items to cart in one action | Items listed with resolved names, applicable tier prices, and add-to-cart confirmation | Invalid SKU in list — row shows error, rest proceed. SKU out of stock — flagged inline. | 1) Valid SKUs resolve to product + price
2) Invalid SKUs shown with error row
3) Cart reflects all tier/tag pricing | M | Draft |
| SCN-006 | Cart / Amount-Based Discount | Spend $500+ → extra 8% off cart total | Wholesale buyer placing large order | Any logged-in B2B customer | Drive higher cart value | Cart discount rule: order >= $500 → 8% off cart total | Cart value threshold discount | all-b2b | Customer reaches cart with subtotal ≥ $500 | App evaluates cart subtotal post line-item pricing and applies cart-level discount | Cart summary shows line subtotal, then discount row "Order discount: −8%", then final total | Discount stacking with Shopify native discount codes. Cart drops below $500 after edit — discount removed. | 1) Discount applied automatically when threshold met
2) Discount removed if cart edited below threshold
3) Discount row visible in cart summary | M | Draft |
| SCN-007 | Multi-Currency / Markets | UK wholesale customer sees GBP tier pricing | International distributor | EU/UK B2B buyer | Serve international B2B without manual conversion | Shopify Markets enabled; pricing rules set in USD; currency conversion active | Multi-currency percentage discount | wholesale-uk | Tagged customer browses from UK Market | App applies tag-based discount; Shopify Markets converts display price to GBP | PDP shows tier price in GBP. Cart total in GBP. No USD leaking through. | Rounding differences between Shopify conversion and app calculation. Currency not supported by merchant. | 1) All prices displayed in customer's market currency
2) Discount percentage is consistent regardless of currency
3) No currency mismatch in cart vs PDP | M | Draft |
| SCN-008 | Tax Display on PDP | EU B2B customer sees tier price table with VAT included | EU wholesale buyer | VAT-registered business buyer in EU | Regulatory compliance + price transparency | Tax display enabled; country = DE; VAT rate = 19% | Country-based tax display | wholesale-eu | EU tagged customer views product page | App renders tier pricing widget with ex-VAT and inc-VAT columns based on customer country | Tier table on PDP shows: "Price excl. VAT | Price incl. VAT (19%)" per tier row | Customer switches country mid-session. VAT rate changes. Non-EU customer should not see VAT column. | 1) VAT column appears only for applicable countries
2) VAT amount correct per country rate
3) Ex-VAT price matches configured rule price | M | Draft |
| SCN-009 | CSV Bulk Import | Merchant uploads 2,000-row pricing rule CSV | Large catalogue merchant | Merchant / store admin | Avoid manual rule entry at scale | CSV import feature; format: SKU, customer_tag, price_type, value | Bulk rule import | N/A (admin action) | Admin uploads CSV via Import screen | App validates CSV, shows error summary for bad rows, imports valid rows, skips errors | Success banner: "1,987 rules imported. 13 rows skipped." Error log downloadable. | Duplicate rules in CSV — last row wins or first? Encoding issues (UTF-8 vs Latin). Missing required columns. | 1) Import completes without crashing on bad rows
2) Error rows reported with row number + reason
3) Existing rules for same SKU+tag — behaviour documented | L | Draft |
| SCN-010 | Manual Order (Admin) | Rep creates manual order for wholesale customer at negotiated price | B2B sales rep workflow | Sales rep using Shopify admin | Close deals offline with custom pricing | Manual order creation enabled; fixed price rule for customer tag active | Manual order + tag pricing | key-account | Rep creates draft order in Shopify admin for tagged customer | App pricing rules apply to manually created draft orders, overriding variant default price | Draft order line items show rule-adjusted price. Rep can submit for review or invoice. | Rep manually overrides price on top of rule price — both changes should stack or last write wins. | 1) Tag-based rule applied on draft order creation
2) Rep can see discounted price before confirming
3) Order confirmation email shows rule-adjusted price | L | Draft |
## Sheet: Feature Areas
| OSCP Wholesale B2B — Feature Areas Reference |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Use these codes in the Scenario Master "Feature Area" column for consistency. |  |  |  |  |  |  |  |
| Feature Area Code | Feature Area Name | Description | Key Config Fields | Pricing Rule Types | Customer Tag Required? | Shopify Dependency | Notes |
| FA-01 | Tiered / Volume Pricing | Percentage or fixed discount by customer tag, applied across all products, collections, or specific variants | Tag name, discount type (%), scope (all/collection/product/variant) | Percentage by tag, Fixed price by tag | Yes | Shopify Functions / Script |  |
| FA-02 | Quantity Breaks | Price changes based on qty ordered. Set min-max qty brackets with corresponding discount per product or variant | Min qty, max qty, discount %, scope | Quantity-based tiered % | Optional | Cart transforms / Functions | Brackets must be non-overlapping |
| FA-03 | Fixed Price Rules | Override price to a specific value for a tag+variant combination. Ignores Shopify base price. | Tag, variant ID, fixed price, currency | Fixed price by tag+variant | Yes | Storefront API | Most specific rule wins |
| FA-04 | Cart / Amount Discount | Discount applied to cart subtotal when threshold met. Stacks or excludes from line-item discounts. | Cart threshold ($), discount %, stacking config | Cart value threshold | Optional | Shopify Discount / Functions | Check stack behaviour with native codes |
| FA-05 | B2B Registration Form | Custom form for wholesale account applications. Fields configurable per group. Auto-tag on approval. | Form fields, required/optional, approval workflow, auto-tag name | Workflow (not pricing) | Post-approval | Customer API, Email | Form template selection available |
| FA-06 | Quick Order Form | SKU-based bulk order entry. Resolves names and prices. Cart add in one action. | Form enabled toggle, max SKUs per order, allowed tags | Inherits active pricing rules | Yes (to see B2B price) | Storefront / Cart API | Up to 50 products per order |
| FA-07 | Multi-Currency / Markets | Pricing rules in base currency; Shopify Markets handles conversion. Ensure % discounts work cross-currency. | Markets enabled, base currency, rounding rule | All rule types | Optional | Shopify Markets API | Test rounding edge cases |
| FA-08 | Tax Display (PDP Widget) | Show tier prices with inc/excl VAT per country on PDP. Widget customisable. | Tax display toggle, country list, VAT rates, widget theme | Display only (no pricing impact) | Optional | Tax API, Geolocation | Regulatory in EU markets |
| FA-09 | CSV Bulk Import / Export | Import pricing rules in bulk via CSV. Export current rules for audit or backup. | CSV column mapping, conflict resolution (overwrite/skip) | All rule types | N/A (admin tool) | File upload API | Define expected CSV schema clearly |
| FA-10 | Manual Order Support | Pricing rules applied when admin/rep creates draft orders in Shopify admin. | Manual order toggle, tag resolution on draft | Inherits active rules | Yes | Draft Order API | Rep override should be logged |
## Sheet: Merchant Archetypes
| OSCP Wholesale B2B — Merchant Archetypes |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Use these archetypes in the Scenario Master to ensure realistic scenario coverage. |  |  |  |  |  |  |  |  |
| Archetype ID | Archetype Name | Typical Business | B2B Customer Type | Pricing Strategy | Key Features Needed | Avg Order Size | Multi-Currency? | Priority for OSCP |
| MA-01 | Manufacturer / Brand | Consumer goods brand selling direct to retailers | Retailer, chain buyer | Fixed wholesale %, tiered qty breaks | FA-01, FA-02, FA-09 | High ($2K+) | Sometimes | H |
| MA-02 | Distributor / Reseller | Middleman buying in volume for redistribution | Named accounts, regional distributors | Tag-based fixed price per account | FA-01, FA-03, FA-10 | Very high ($5K+) | Yes | H |
| MA-03 | DTC with Wholesale Channel | D2C brand that also sells B2B via same Shopify store | Stockists, boutiques | % off for tagged wholesale customers | FA-01, FA-05, FA-06 | Medium ($500–2K) | No | H |
| MA-04 | Professional / Trade Only | Products sold only to verified professionals (beauty, medical, tools) | Verified trade customers | Full price but access-gated; may have qty breaks | FA-05, FA-02, FA-08 | Medium | No | M |
| MA-05 | International B2B | Merchant with customers across multiple countries / markets | EU, UK, APAC distributors | Market-specific tier pricing + VAT display | FA-07, FA-08, FA-01 | High | Yes | M |
| MA-06 | Large Catalogue B2B | Merchant with 1,000+ SKUs needing bulk rule management | Mixed B2B buyers | CSV-managed, collection-level rules | FA-09, FA-01, FA-02 | Medium–High | Sometimes | M |
| MA-07 | Key Account / Contract | Merchant with named accounts having negotiated contract prices | Single named company buyers | Fixed price per tag+SKU; manual order flow | FA-03, FA-10, FA-04 | Very high | Sometimes | H |
## Sheet: Acceptance Criteria Bank
| OSCP Wholesale B2B — Acceptance Criteria Bank |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Reusable binary pass/fail criteria. Copy AC IDs into Scenario Master col "Acceptance Criteria". |  |  |  |  |  |
| AC ID | Feature Area | Criterion (pass/fail statement) | Test Input | Expected Output | Who Verifies |
| AC-01 | FA-01 Tiered Pricing | Tagged customer sees discounted price on PDP | Login as tagged customer; visit product page | Price shown = base × (1 − discount%) | QA / Dev |
| AC-02 | FA-01 Tiered Pricing | Untagged / guest customer sees original Shopify price | Browse as guest; visit same product page | Price shown = Shopify variant price | QA / Dev |
| AC-03 | FA-01 Tiered Pricing | Cart total = sum of discounted line items (no rounding error) | Add 3 products as tagged customer | Cart total matches manual calculation to 2dp | QA |
| AC-04 | FA-02 Qty Breaks | Tier price updates without page reload when qty changes | Change qty selector on PDP from 9 → 10 (tier boundary) | Price updates in < 1s; no full reload | QA / Dev |
| AC-05 | FA-02 Qty Breaks | Tier table visible on PDP showing all configured brackets | Visit product with qty break rule | Table shows each bracket row with price | QA |
| AC-06 | FA-02 Qty Breaks | Cart price reflects tier at qty in cart, not qty at time of add | Add 5 units, then edit to 20 in cart | Cart price recalculates to 20-unit tier | QA |
| AC-07 | FA-03 Fixed Price | Tagged customer sees exact fixed price (not % of base) | Login as tagged; visit variant with fixed price rule | Price displayed = configured fixed value | QA / Dev |
| AC-08 | FA-03 Fixed Price | Other customers are unaffected by fixed price rule | Login as differently-tagged customer | Price = standard price (no bleed-through) | QA |
| AC-09 | FA-04 Cart Discount | Cart discount row appears when threshold met | Build cart to exactly threshold amount | Discount row visible in cart summary | QA |
| AC-10 | FA-04 Cart Discount | Cart discount removed if cart edited below threshold | Start above threshold, remove item to go below | Discount row disappears; total recalculates | QA |
| AC-11 | FA-05 Registration | Required form fields prevent submission if empty | Submit form with blank required field | Inline validation error shown; form not submitted | QA |
| AC-12 | FA-05 Registration | Wholesale prices not visible pre-approval | Complete registration; do not approve; browse products | Standard retail prices shown | QA |
| AC-13 | FA-05 Registration | Admin receives email notification on form submission | Submit a test registration | Admin inbox receives notification within 2 min | QA |
| AC-14 | FA-06 Quick Order | Valid SKU resolves to product name + applicable price | Enter known SKU in Quick Order form | Product name and discounted price shown in row | QA / Dev |
| AC-15 | FA-06 Quick Order | Invalid SKU shows inline error, does not block other rows | Enter mix of valid + invalid SKUs | Invalid row shows error; valid rows proceed to cart | QA |
| AC-16 | FA-07 Multicurrency | Discount % consistent regardless of display currency | Login tagged from UK market; view product | GBP price = (USD base × discount%) converted — not re-discounted | QA / Dev |
| AC-17 | FA-08 Tax Display | VAT column appears only for configured countries | Visit PDP from DE market (VAT country) | Inc-VAT column visible; from US market — no VAT column | QA |
| AC-18 | FA-09 CSV Import | Bad rows reported with row number and reason, not silently dropped | Upload CSV with 5 intentionally bad rows | Error log shows row numbers + failure reason for each | QA / Dev |
| AC-19 | FA-10 Manual Order | Draft order line prices reflect active tag-based rules | Create draft order in admin for tagged customer | Line item prices = tag-discounted prices, not Shopify default | QA / Dev |
## Sheet: Edge Cases Register
| OSCP Wholesale B2B — Edge Cases Register |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Known edge cases per feature. Link to scenarios. Flag risk level for sprint planning. |  |  |  |  |  |  |
| EC ID | Feature Area | Edge Case Description | Trigger Condition | Expected Behavior | Risk Level | Linked Scenario |
| EC-01 | FA-01 | Customer has multiple tags with different discount % | User tagged "wholesale" (10%) and "vip" (20%) | Apply highest discount (or most specific — document rule clearly) | High | SCN-001 |
| EC-02 | FA-01 | Tag removed from customer mid-session | Admin removes tag while customer is browsing | Next page load reflects retail price; cart may hold old price until refresh | Medium | SCN-001 |
| EC-03 | FA-02 | Qty brackets overlap in config | Admin sets 10–20 = 5% and 15–25 = 10% | Validation error on save; overlapping brackets should be blocked | High | SCN-002 |
| EC-04 | FA-02 | Qty reduced in cart below bracket minimum | Customer reduces qty from 20 to 8 in cart | Price reverts to next applicable bracket or full price | Medium | SCN-002 |
| EC-05 | FA-03 | Fixed price rule currency differs from store default | Rule set in USD; merchant switches to EUR-only store | Documented behaviour: rule price treated as store base currency | High | SCN-003 |
| EC-06 | FA-03 | Two fixed price rules for same tag + variant | Admin creates duplicate rule | App uses most recently created rule OR blocks duplicate — must be defined | High | SCN-003 |
| EC-07 | FA-04 | Cart discount + Shopify native discount code applied | Customer enters discount code on cart with auto-discount active | Define stacking policy: additive, highest wins, or block code | High | SCN-006 |
| EC-08 | FA-05 | Duplicate email on registration form | Existing customer submits registration form again | Link to existing account or show "already registered" message | Medium | SCN-004 |
| EC-09 | FA-06 | SKU entered in Quick Order form is out of stock | Customer enters OOS variant SKU | Row shows "Out of stock" indicator; excluded from add-to-cart | Medium | SCN-005 |
| EC-10 | FA-06 | More than 50 SKUs entered in Quick Order | Customer pastes 60 SKU rows | First 50 processed; remaining shown with "limit reached" notice | Low | SCN-005 |
| EC-11 | FA-07 | Shopify Markets currency conversion creates rounding mismatch | Tier price in USD = $9.99; GBP equivalent rounds differently | Define rounding rule: always round to 2dp in display currency | Medium | SCN-007 |
| EC-12 | FA-08 | Customer changes country mid-session (VPN or manual) | Browsing as DE then switches to US | Tax display updates on next PDP load; no stale VAT shown in cart | Medium | SCN-008 |
| EC-13 | FA-09 | CSV uploaded with non-UTF-8 encoding | Merchant exports from Excel with Latin-1 encoding | App detects encoding issue; shows error before import; suggests re-save as UTF-8 | Medium | SCN-009 |
| EC-14 | FA-09 | CSV import conflicts with existing rules | Import contains rule for tag+SKU that already has a rule | Configurable: overwrite / skip / create duplicate — must be documented | High | SCN-009 |
| EC-15 | FA-10 | Rep manually overrides price on top of rule-adjusted price | Draft order has $8.50 rule price; rep types $7.00 | Last write wins (rep override), but original rule price logged for audit | Low | SCN-010 |