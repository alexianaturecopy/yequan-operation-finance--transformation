-- ============================================================================
-- EXECUTIVE OPERATIONS DASHBOARD - SQL QUERIES
-- Multi-Unit Financial Analysis Examples
-- ============================================================================
-- Business Context: These queries demonstrate strategic financial analysis
-- that a CFO would run for Board reporting, executive reviews, and planning
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. CORPORATE PERFORMANCE SUMMARY
-- Purpose: Monthly Board reporting KPIs
-- Business Use: Executive summary for Board packages
-- ----------------------------------------------------------------------------
SELECT 
    DATE_TRUNC('month', date) as month,
    COUNT(DISTINCT unit_id) as active_units,
    SUM(revenue) as total_revenue,
    SUM(gross_profit) as total_gross_profit,
    ROUND(SUM(gross_profit) / NULLIF(SUM(revenue), 0) * 100, 2) as corporate_gross_margin_pct,
    SUM(operating_income) as total_operating_income,
    ROUND(SUM(operating_income) / NULLIF(SUM(revenue), 0) * 100, 2) as corporate_operating_margin_pct,
    SUM(headcount) as total_headcount,
    ROUND(SUM(revenue) / SUM(headcount), 0) as revenue_per_employee
FROM monthly_pnl
WHERE date >= '2024-01-01'
GROUP BY DATE_TRUNC('month', date)
ORDER BY month DESC;


-- ----------------------------------------------------------------------------
-- 2. UNIT PERFORMANCE RANKING
-- Purpose: Identify top and bottom performers
-- Business Use: Resource allocation decisions, strategic planning
-- ----------------------------------------------------------------------------
WITH current_quarter AS (
    SELECT 
        unit_id,
        unit_name,
        vertical,
        region,
        SUM(revenue) as qtd_revenue,
        SUM(operating_income) as qtd_operating_income,
        AVG(operating_margin_pct) as avg_operating_margin,
        AVG(revenue_variance) as avg_revenue_variance,
        MAX(headcount) as current_headcount
    FROM monthly_pnl
    WHERE quarter = 'Q4' AND date >= '2024-10-01'
    GROUP BY unit_id, unit_name, vertical, region
)
SELECT 
    unit_name,
    vertical,
    region,
    qtd_revenue,
    qtd_operating_income,
    avg_operating_margin,
    CASE 
        WHEN avg_operating_margin >= 25 THEN 'Star Performer'
        WHEN avg_operating_margin >= 15 THEN 'Solid Performer'
        WHEN avg_operating_margin >= 5 THEN 'Needs Improvement'
        ELSE 'Critical Attention Required'
    END as performance_tier,
    avg_revenue_variance,
    current_headcount,
    ROUND(qtd_revenue / current_headcount, 0) as revenue_per_employee
FROM current_quarter
ORDER BY avg_operating_margin DESC;


-- ----------------------------------------------------------------------------
-- 3. MARGIN COMPRESSION ANALYSIS
-- Purpose: Identify units with declining profitability
-- Business Use: Early warning system, cost optimization priorities
-- ----------------------------------------------------------------------------
WITH margin_trend AS (
    SELECT 
        unit_id,
        unit_name,
        date,
        operating_margin_pct,
        LAG(operating_margin_pct, 3) OVER (PARTITION BY unit_id ORDER BY date) as margin_3mo_ago,
        LAG(operating_margin_pct, 6) OVER (PARTITION BY unit_id ORDER BY date) as margin_6mo_ago
    FROM monthly_pnl
)
SELECT 
    unit_name,
    operating_margin_pct as current_margin,
    margin_3mo_ago,
    margin_6mo_ago,
    ROUND(operating_margin_pct - margin_3mo_ago, 2) as margin_change_3mo,
    ROUND(operating_margin_pct - margin_6mo_ago, 2) as margin_change_6mo,
    CASE 
        WHEN (operating_margin_pct - margin_6mo_ago) < -5 THEN '🔴 Severe Compression'
        WHEN (operating_margin_pct - margin_6mo_ago) < -2 THEN '🟠 Moderate Compression'
        WHEN (operating_margin_pct - margin_6mo_ago) > 2 THEN '🟢 Improving'
        ELSE '⚪ Stable'
    END as margin_status
FROM margin_trend
WHERE date = (SELECT MAX(date) FROM monthly_pnl)
ORDER BY margin_change_6mo ASC;


-- ----------------------------------------------------------------------------
-- 4. BUDGET VARIANCE ANALYSIS
-- Purpose: Track actual vs budget performance
-- Business Use: Monthly CFO review, explaining variances to Board
-- ----------------------------------------------------------------------------
SELECT 
    unit_name,
    vertical,
    DATE_TRUNC('month', date) as month,
    revenue as actual_revenue,
    budget_revenue,
    revenue_variance,
    ROUND(revenue_variance / NULLIF(budget_revenue, 0) * 100, 2) as revenue_variance_pct,
    operating_income as actual_operating_income,
    budget_operating_income,
    operating_income_variance,
    ROUND(operating_income_variance / NULLIF(budget_operating_income, 0) * 100, 2) as oi_variance_pct,
    CASE 
        WHEN revenue_variance > 0 AND operating_income_variance > 0 THEN '✅ Beat on Both'
        WHEN revenue_variance > 0 AND operating_income_variance < 0 THEN '⚠️ Revenue Beat, Margin Miss'
        WHEN revenue_variance < 0 AND operating_income_variance < 0 THEN '❌ Missed on Both'
        ELSE '📊 Mixed Performance'
    END as performance_flag
FROM monthly_pnl
WHERE date >= '2024-01-01'
ORDER BY month DESC, revenue_variance_pct DESC;


-- ----------------------------------------------------------------------------
-- 5. CONTRACTOR SPEND ANALYSIS
-- Purpose: Identify over-reliance on contractors vs FTE
-- Business Use: Cost optimization, hiring planning
-- ----------------------------------------------------------------------------
WITH contractor_analysis AS (
    SELECT 
        unit_id,
        unit_name,
        AVG(contractor_cost) as avg_contractor_cost,
        AVG(personnel_cost) as avg_personnel_cost,
        AVG(contractor_cost + personnel_cost) as avg_total_labor_cost
    FROM monthly_pnl
    WHERE date >= '2024-07-01'  -- Last 6 months
    GROUP BY unit_id, unit_name
)
SELECT 
    unit_name,
    ROUND(avg_contractor_cost, 0) as avg_monthly_contractor_spend,
    ROUND(avg_personnel_cost, 0) as avg_monthly_fte_spend,
    ROUND(avg_contractor_cost / NULLIF(avg_total_labor_cost, 0) * 100, 1) as contractor_pct_of_labor,
    CASE 
        WHEN (avg_contractor_cost / NULLIF(avg_total_labor_cost, 0) * 100) > 30 THEN '🔴 High Contractor Reliance'
        WHEN (avg_contractor_cost / NULLIF(avg_total_labor_cost, 0) * 100) > 20 THEN '🟠 Above Target'
        ELSE '🟢 Healthy Mix'
    END as labor_mix_status,
    ROUND((avg_contractor_cost * 0.20) / 12, 0) as potential_annual_savings_if_converted
FROM contractor_analysis
ORDER BY contractor_pct_of_labor DESC;


-- ----------------------------------------------------------------------------
-- 6. MULTI-UNIT CONSOLIDATION
-- Purpose: Corporate-level P&L with eliminations
-- Business Use: External financial reporting, Board packages
-- ----------------------------------------------------------------------------
WITH unit_pnl AS (
    SELECT 
        DATE_TRUNC('quarter', date) as quarter,
        SUM(revenue) as total_revenue,
        SUM(cogs) as total_cogs,
        SUM(gross_profit) as total_gross_profit,
        SUM(personnel_cost) as total_personnel,
        SUM(contractor_cost) as total_contractors,
        SUM(marketing) as total_marketing,
        SUM(other_opex) as total_other_opex,
        SUM(total_opex) as total_operating_expenses,
        SUM(operating_income) as total_operating_income
    FROM monthly_pnl
    WHERE date >= '2024-01-01'
    GROUP BY DATE_TRUNC('quarter', date)
)
SELECT 
    quarter,
    total_revenue,
    total_cogs,
    total_gross_profit,
    ROUND(total_gross_profit / NULLIF(total_revenue, 0) * 100, 2) as gross_margin_pct,
    total_personnel,
    total_contractors,
    total_marketing,
    total_other_opex,
    total_operating_expenses,
    total_operating_income,
    ROUND(total_operating_income / NULLIF(total_revenue, 0) * 100, 2) as operating_margin_pct
FROM unit_pnl
ORDER BY quarter DESC;


-- ----------------------------------------------------------------------------
-- 7. GROWTH EFFICIENCY ANALYSIS
-- Purpose: Evaluate quality of growth (revenue growth vs margin impact)
-- Business Use: Strategic planning, M&A analysis
-- ----------------------------------------------------------------------------
WITH growth_metrics AS (
    SELECT 
        unit_id,
        unit_name,
        vertical,
        date,
        revenue,
        operating_margin_pct,
        LAG(revenue, 6) OVER (PARTITION BY unit_id ORDER BY date) as revenue_6mo_ago,
        LAG(operating_margin_pct, 6) OVER (PARTITION BY unit_id ORDER BY date) as margin_6mo_ago
    FROM monthly_pnl
)
SELECT 
    unit_name,
    vertical,
    ROUND(((revenue - revenue_6mo_ago) / NULLIF(revenue_6mo_ago, 0)) * 100, 1) as revenue_growth_6mo_pct,
    operating_margin_pct as current_margin,
    margin_6mo_ago,
    ROUND(operating_margin_pct - margin_6mo_ago, 2) as margin_change,
    CASE 
        WHEN ((revenue - revenue_6mo_ago) / NULLIF(revenue_6mo_ago, 0)) > 0.15 
             AND (operating_margin_pct - margin_6mo_ago) > 0 THEN '🌟 Efficient Growth'
        WHEN ((revenue - revenue_6mo_ago) / NULLIF(revenue_6mo_ago, 0)) > 0.15 
             AND (operating_margin_pct - margin_6mo_ago) < -3 THEN '⚠️ Growth at Margin Cost'
        WHEN ((revenue - revenue_6mo_ago) / NULLIF(revenue_6mo_ago, 0)) < 0.05 THEN '🐌 Low Growth'
        ELSE '📊 Moderate Growth'
    END as growth_quality
FROM growth_metrics
WHERE date = (SELECT MAX(date) FROM monthly_pnl)
  AND revenue_6mo_ago IS NOT NULL
ORDER BY revenue_growth_6mo_pct DESC;


-- ----------------------------------------------------------------------------
-- 8. RESOURCE ALLOCATION OPTIMIZATION
-- Purpose: Identify misallocated resources
-- Business Use: Annual planning, reallocation decisions
-- ----------------------------------------------------------------------------
WITH unit_efficiency AS (
    SELECT 
        ra.unit_name,
        ra.vertical,
        ra.annual_budget,
        ra.total_headcount,
        SUM(pnl.revenue) as ytd_revenue,
        SUM(pnl.operating_income) as ytd_operating_income,
        ROUND(SUM(pnl.revenue) / ra.total_headcount, 0) as revenue_per_employee,
        ROUND(SUM(pnl.operating_income) / ra.annual_budget * 100, 2) as roi_on_budget
    FROM resource_allocation ra
    JOIN monthly_pnl pnl ON ra.unit_id = pnl.unit_id
    WHERE pnl.date >= '2024-01-01'
    GROUP BY ra.unit_name, ra.vertical, ra.annual_budget, ra.total_headcount
)
SELECT 
    unit_name,
    vertical,
    annual_budget,
    total_headcount,
    ytd_revenue,
    ytd_operating_income,
    revenue_per_employee,
    roi_on_budget,
    CASE 
        WHEN roi_on_budget > 25 AND revenue_per_employee > 1000000 THEN '💎 High Efficiency - Invest More'
        WHEN roi_on_budget < 10 OR revenue_per_employee < 500000 THEN '🔍 Low Efficiency - Review'
        ELSE '📊 Average Efficiency'
    END as efficiency_rating
FROM unit_efficiency
ORDER BY roi_on_budget DESC;


-- ----------------------------------------------------------------------------
-- 9. EXECUTIVE ALERT QUERY
-- Purpose: Automated flagging of issues requiring C-suite attention
-- Business Use: Weekly exec reviews, automated monitoring
-- ----------------------------------------------------------------------------
WITH latest_month AS (
    SELECT MAX(month) as max_month FROM monthly_pnl
),
performance_flags AS (
    SELECT 
        pnl.unit_id,
        pnl.unit_name,
        pnl.revenue_variance,
        pnl.operating_income_variance,
        pnl.operating_margin_pct,
        (pnl.contractor_cost / NULLIF(pnl.contractor_cost + pnl.personnel_cost, 0)) * 100 as contractor_pct,
        om.dso_days
    FROM monthly_pnl pnl
    JOIN operational_metrics om ON pnl.unit_id = om.unit_id AND pnl.date = om.date
    CROSS JOIN latest_month
    WHERE pnl.month = latest_month.max_month
)
SELECT 
    unit_name,
    CASE 
        WHEN revenue_variance < -1000000 THEN 'Revenue Significantly Below Budget'
        WHEN operating_margin_pct < 10 THEN 'Operating Margin Below Target'
        WHEN contractor_pct > 40 THEN 'Excessive Contractor Spend'
        WHEN dso_days > 60 THEN 'Collections Issue - High DSO'
        ELSE 'No Major Issues'
    END as alert_type,
    CASE 
        WHEN revenue_variance < -1000000 OR operating_margin_pct < 5 THEN 'HIGH'
        WHEN contractor_pct > 40 OR dso_days > 60 THEN 'MEDIUM'
        ELSE 'LOW'
    END as severity,
    revenue_variance,
    operating_margin_pct,
    contractor_pct,
    dso_days
FROM performance_flags
WHERE revenue_variance < -500000 
   OR operating_margin_pct < 15 
   OR contractor_pct > 30 
   OR dso_days > 50
ORDER BY 
    CASE 
        WHEN revenue_variance < -1000000 OR operating_margin_pct < 5 THEN 1
        WHEN contractor_pct > 40 OR dso_days > 60 THEN 2
        ELSE 3 
    END;


-- ============================================================================
-- CFO INSIGHTS: What These Queries Demonstrate
-- ============================================================================
-- 1. Strategic Thinking: Not just reporting, but analysis that drives decisions
-- 2. Multi-dimensional View: Financial, operational, and human capital metrics
-- 3. Variance Analysis: Budget vs actual at corporate and unit levels
-- 4. Efficiency Metrics: Revenue per employee, ROI on budget
-- 5. Early Warning System: Automated alerts for issues requiring intervention
-- 6. Resource Optimization: Data-driven reallocation recommendations
-- 7. Board Reporting: Executive-level summaries for governance
-- 8. Operational Excellence: Linking financial performance to operational drivers
-- ============================================================================
