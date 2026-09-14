def emi(principal, annual_rate_pct, years):
    r=annual_rate_pct/12/100
    n=years*12
    if r==0: return principal/n
    return principal*r*(1+r)**n/((1+r)**n-1)

def future_value(value, annual_growth_pct, years):
    return value*(1+annual_growth_pct/100)**years

def investment_summary(purchase_price, down_payment_pct, annual_rate_pct, loan_years,
                       monthly_rent, monthly_maintenance, annual_property_tax,
                       transaction_cost_pct, annual_growth_pct, years):
    down=purchase_price*down_payment_pct/100
    loan=max(0,purchase_price-down)
    monthly_emi=emi(loan,annual_rate_pct,loan_years) if loan else 0
    annual_rent=monthly_rent*12
    annual_cost=monthly_maintenance*12+annual_property_tax
    gross_yield=annual_rent/purchase_price*100 if purchase_price else 0
    net_yield=(annual_rent-annual_cost)/purchase_price*100 if purchase_price else 0
    future=future_value(purchase_price,annual_growth_pct,years)
    appreciation=future-purchase_price
    total_invested=down+purchase_price*transaction_cost_pct/100
    roi=(appreciation + (annual_rent-annual_cost)*years - total_invested)/total_invested*100 if total_invested else 0
    return {"down_payment":down,"loan_amount":loan,"monthly_emi":monthly_emi,
            "gross_yield_pct":gross_yield,"net_yield_pct":net_yield,
            "future_value":future,"capital_appreciation":appreciation,
            "estimated_roi_pct":roi,"total_initial_investment":total_invested}

def appreciation_projection(current_price, base_growth, infra_score):
    adj=base_growth*(1+max(0,min(infra_score,100))/300)
    return {1: current_price*(1+adj/100),
            3: current_price*(1+adj/100)**3,
            5: current_price*(1+adj/100)**5}
