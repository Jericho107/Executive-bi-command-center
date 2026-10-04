CREATE TABLE IF NOT EXISTS fact_executive_period (
    period TEXT NOT NULL,
    business_unit TEXT NOT NULL,
    revenue REAL NOT NULL,
    budget_revenue REAL NOT NULL,
    gross_profit REAL NOT NULL,
    controllable_cost REAL NOT NULL,
    cash_collected REAL NOT NULL,
    billed_revenue REAL NOT NULL,
    retained_customers INTEGER NOT NULL,
    opening_customers INTEGER NOT NULL,
    PRIMARY KEY(period, business_unit)
);
