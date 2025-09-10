import requests

def fetch_orders_from_shopify(api_key, shop_name):
    url = f"https://{shop_name}.myshopify.com/admin/api/2025-01/orders.json"
    headers = {"X-Shopify-Access-Token": api_key}
    r = requests.get(url, headers=headers)
    return r.json()

def update_inventory(shop_name, api_key, product_id, quantity):
    url = f"https://{shop_name}.myshopify.com/admin/api/2025-01/inventory_levels/set.json"
    headers = {"X-Shopify-Access-Token": api_key}
    data = {"inventory_item_id": product_id, "available": quantity}
    r = requests.post(url, json=data, headers=headers)
    return r.json()
