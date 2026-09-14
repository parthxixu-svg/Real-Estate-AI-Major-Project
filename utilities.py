def inr(value):
    try:
        return f"₹{value:,.0f}"
    except Exception:
        return "₹0"
