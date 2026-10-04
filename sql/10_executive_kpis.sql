SELECT
    period,
    business_unit,
    CASE
        WHEN budget_revenue = 0 THEN 0
        ELSE (revenue - budget_revenue) / budget_revenue
    END AS revenue_variance_pct,
    CASE
        WHEN revenue = 0 THEN 0
        ELSE gross_profit / revenue
    END AS gross_margin_pct,
    gross_profit - controllable_cost AS controllable_contribution,
    CASE
        WHEN billed_revenue = 0 THEN 0
        ELSE cash_collected / billed_revenue
    END AS cash_conversion_pct,
    CASE
        WHEN opening_customers = 0 THEN 0
        ELSE 1.0 * retained_customers / opening_customers
    END AS retention_pct
FROM fact_executive_period
ORDER BY period, business_unit;
