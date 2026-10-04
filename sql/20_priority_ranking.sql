WITH kpi AS (
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
),
scored AS (
    SELECT
        *,
        (revenue_variance_pct < -0.05)
        + (gross_margin_pct < 0.30)
        + (cash_conversion_pct < 0.85)
        + (retention_pct < 0.90)
        + (controllable_contribution < 0) AS adverse_driver_count
    FROM kpi
)
SELECT
    period,
    business_unit,
    revenue_variance_pct,
    gross_margin_pct,
    controllable_contribution,
    cash_conversion_pct,
    retention_pct,
    adverse_driver_count,
    CASE
        WHEN adverse_driver_count >= 3 THEN 'high'
        WHEN adverse_driver_count >= 1 THEN 'medium'
        ELSE 'monitor'
    END AS priority
FROM scored
ORDER BY adverse_driver_count DESC, business_unit;
