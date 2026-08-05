# Theme compatibility

*Advance FAQ*

## To change color of discount grid on frontend?

Go to Sales Channel → Online Store → Edit Code → Assets → Theme CSS file

Add the below code at the bottom of `.css` file:

```css
<style>
    #oscpPriceGrid th
{
color: white !important;
background-color: #557b97 !important;
}
</style>
```

## How to create offer for Product and its Variants based on Customer Tags?

On App Dashboard, Click on Tiered Pricing for Variants, New tab will open to select
product, Select products and click on Add button, Here you can apply Wholesale pricing to
each Variants based on Customer Tags

## How to create offer for Products and Collections based on Customers Groups?

On App Dashboard, Click on Create Offer Tab Mention Offer Name, Offer Details (Wholesale
Pricing) Apply discount to Selected Products or Selected Collections Assign discount to
Customer Groups

1. All Customers
2. Logged in Customers
3. Customers with Specific Tags

## The Discount Table is not reflecting on the Product Page?

1. **Extension setup:** In Shopify admin, click Sales Channel → Online Store →
   Customization → App Embeds → Enable Custom Price Grid
2. **Block Setup:** In Shopify admin, click Sales Channel → Online Store → Customization
   → In Home Page drop down select Products v Click on Default Product → In Product
   information click on Add block → In APPS click on Custom Price Grid → Drag and drop
   Custom Price Grid below Price (in Product information)
3. Check Dashboard if App is Enabled (ON)
4. The Offer / Discount created is Enabled (ON) On Offer List Page
5. If any other Price related App is installed, it may conflict with our App. So you can
   disable other pricing related Apps in order to view the Wholesale Table on the product
   page.

## The Discount price is not reflecting on the Cart Page?

In Shopify admin, click Sales Channel → Online Store → Customization → App Embeds → Click
on Wholesale Price

Enter element ID or Class of the following Input boxes

## The Discount price is not reflecting in the Mini Cart?

In Shopify admin, click Sales Channel → Online Store → Customization → App Embeds → Click
on Wholesale Price

Enter element ID or Class of the following Input boxes

## The Discount price is not reflecting when I click on the "Checkout" button on cart page and Cart Drawer (Mini cart)?

In Shopify admin, click Sales Channel → Online Store → Customization → App Embeds → Click
on Wholesale Price

Enter element ID or Class of the following Line Item:

For Checkout button on Cart Page and Cart Drawer

HTML reference for Checkout button on the Cart Page and Cart Drawer (ID or class) in
Checkout Button input box

## The Discount price is not reflecting when I click on the "Add to Cart" button?

In Shopify admin, click Sales Channel → Online Store → Customization → App Embeds → Click
on Wholesale Price

Enter element ID or Class of the following Line Item:

For Add to Cart button

HTML reference for Add to cart button on the Product page (ID or class) in Add To Cart
button input box

## How can I display discounted price for single quantity on product page?

To avoid pricing grid on product page and directly display discounted price, follow these
steps:

Theme Setup (Left Navigation in App) → Select Theme (click on Continue) → App Block Setup
→ Click on Add Discounted Price → Move Discounted Price below default Price block →
Disable Wholesale Price (Grid) → Save changes

## Why is the price grid not appearing on the product page?

If the price grid is not displayed on the product page, it may be due to customizations
made to the product page. In this case, please check the cart page to see if the pricing
rules are applied there and on the checkout page. If the rules are working on the cart
page, the issue is likely due to the customizations on the product page.
