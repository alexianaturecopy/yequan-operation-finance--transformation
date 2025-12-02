"""
Sample Data Generator for Executive Operations Dashboard

Business Context:
Generates realistic multi-unit business data for demonstration purposes.
Simulates 12 business units across different verticals with varying performance profiles.

This data mimics real-world scenarios:
- High-performing units (Units 1, 3, 7)
- Struggling units (Units 4, 10)
- Growing units with margin pressure (Unit 6)
- Stable performers (most others)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

class SampleDataGenerator:
    """Generates realistic multi-unit operational data"""
    
    def __init__(self):
        self.units = self._define_business_units()
        self.start_date = datetime(2024, 1, 1)
        self.end_date = datetime(2024, 12, 31)
        
    def _define_business_units(self):
        """Define 12 business units with different characteristics"""
        return [
            {'unit_id': 1, 'name': 'SaaS Platform', 'vertical': 'Software', 'region': 'North America', 'performance': 'high'},
            {'unit_id': 2, 'name': 'Enterprise Sales', 'vertical': 'Sales', 'region': 'North America', 'performance': 'medium'},
            {'unit_id': 3, 'name': 'Cloud Infrastructure', 'vertical': 'Infrastructure', 'region': 'Global', 'performance': 'high'},
            {'unit_id': 4, 'name': 'Mobile Products', 'vertical': 'Software', 'region': 'North America', 'performance': 'struggling'},
            {'unit_id': 5, 'name': 'Professional Services', 'vertical': 'Services', 'region': 'North America', 'performance': 'medium'},
            {'unit_id': 6, 'name': 'Data Analytics', 'vertical': 'Software', 'region': 'Global', 'performance': 'growing'},
            {'unit_id': 7, 'name': 'API Platform', 'vertical': 'Infrastructure', 'region': 'Global', 'performance': 'high'},
            {'unit_id': 8, 'name': 'EMEA Sales', 'vertical': 'Sales', 'region': 'EMEA', 'performance': 'medium'},
            {'unit_id': 9, 'name': 'Customer Success', 'vertical': 'Services', 'region': 'Global', 'performance': 'medium'},
            {'unit_id': 10, 'name': 'IoT Division', 'vertical': 'Hardware', 'region': 'APAC', 'performance': 'struggling'},
            {'unit_id': 11, 'name': 'Security Products', 'vertical': 'Software', 'region': 'North America', 'performance': 'medium'},
            {'unit_id': 12, 'name': 'APAC Sales', 'vertical': 'Sales', 'region': 'APAC', 'performance': 'growing'},
        ]
    
    def generate_monthly_pnl(self):
        """
        Generate monthly P&L data for all units
        
        Business Context: Core financial performance by unit
        Used for: Board reporting, unit leader accountability, variance analysis
        """
        data = []
        
        for unit in self.units:
            # Base revenue varies by unit
            if unit['performance'] == 'high':
                base_revenue = random.uniform(8_000_000, 12_000_000)
                growth_rate = random.uniform(0.03, 0.05)  # 3-5% monthly growth
                margin = random.uniform(0.65, 0.75)
            elif unit['performance'] == 'growing':
                base_revenue = random.uniform(4_000_000, 7_000_000)
                growth_rate = random.uniform(0.06, 0.10)  # 6-10% monthly growth
                margin = random.uniform(0.45, 0.55)  # Lower margins due to growth investments
            elif unit['performance'] == 'struggling':
                base_revenue = random.uniform(2_000_000, 4_000_000)
                growth_rate = random.uniform(-0.02, 0.01)  # Flat to declining
                margin = random.uniform(0.30, 0.45)
            else:  # medium
                base_revenue = random.uniform(5_000_000, 8_000_000)
                growth_rate = random.uniform(0.02, 0.04)
                margin = random.uniform(0.55, 0.65)
            
            # Generate 12 months of data
            for month in range(1, 13):
                date = datetime(2024, month, 1)
                
                # Revenue with growth trend and seasonality
                seasonality = 1 + (0.15 if month in [11, 12] else 0)  # Q4 spike
                monthly_revenue = base_revenue * (1 + growth_rate) ** month * seasonality
                monthly_revenue *= random.uniform(0.95, 1.05)  # Add noise
                
                # COGS based on margin profile
                cogs = monthly_revenue * (1 - margin)
                gross_profit = monthly_revenue - cogs
                
                # Operating expenses
                headcount = random.randint(15, 80) if unit['performance'] != 'struggling' else random.randint(8, 25)
                personnel_cost = headcount * random.uniform(8_000, 12_000)
                
                # Contractors (issue to flag in Unit 4)
                if unit['unit_id'] == 4 and month >= 7:  # Unit 4 ramps contractors in Q3
                    contractor_cost = personnel_cost * random.uniform(0.60, 0.70)  # Red flag
                else:
                    contractor_cost = personnel_cost * random.uniform(0.10, 0.20)
                
                marketing = monthly_revenue * random.uniform(0.15, 0.25)
                other_opex = monthly_revenue * random.uniform(0.08, 0.12)
                
                total_opex = personnel_cost + contractor_cost + marketing + other_opex
                operating_income = gross_profit - total_opex
                
                # Budget (set at beginning of year)
                budget_revenue = base_revenue * 1.15 * seasonality  # Assume 15% annual growth budget
                budget_operating_income = budget_revenue * 0.20  # 20% operating margin target
                
                data.append({
                    'unit_id': unit['unit_id'],
                    'unit_name': unit['name'],
                    'vertical': unit['vertical'],
                    'region': unit['region'],
                    'date': date,
                    'month': month,
                    'quarter': f"Q{(month-1)//3 + 1}",
                    'revenue': round(monthly_revenue, 2),
                    'cogs': round(cogs, 2),
                    'gross_profit': round(gross_profit, 2),
                    'gross_margin_pct': round((gross_profit / monthly_revenue) * 100, 2),
                    'personnel_cost': round(personnel_cost, 2),
                    'contractor_cost': round(contractor_cost, 2),
                    'marketing': round(marketing, 2),
                    'other_opex': round(other_opex, 2),
                    'total_opex': round(total_opex, 2),
                    'operating_income': round(operating_income, 2),
                    'operating_margin_pct': round((operating_income / monthly_revenue) * 100, 2),
                    'headcount': headcount,
                    'budget_revenue': round(budget_revenue, 2),
                    'budget_operating_income': round(budget_operating_income, 2),
                    'revenue_variance': round(monthly_revenue - budget_revenue, 2),
                    'operating_income_variance': round(operating_income - budget_operating_income, 2),
                })
        
        return pd.DataFrame(data)
    
    def generate_operational_metrics(self):
        """
        Generate key operational metrics by unit
        
        Business Context: Non-financial KPIs that drive financial performance
        Used for: Early warning indicators, operational reviews
        """
        data = []
        
        for unit in self.units:
            for month in range(1, 13):
                date = datetime(2024, month, 1)
                
                # Customer metrics
                if unit['vertical'] in ['Software', 'Infrastructure']:
                    customers = random.randint(150, 500) if unit['performance'] == 'high' else random.randint(50, 200)
                    arr = customers * random.uniform(50_000, 150_000)
                    mrr = arr / 12
                    churn_rate = random.uniform(0.01, 0.03) if unit['performance'] == 'high' else random.uniform(0.04, 0.08)
                    nrr = random.uniform(110, 125) if unit['performance'] == 'high' else random.uniform(95, 105)
                else:
                    customers = random.randint(50, 150)
                    arr = None
                    mrr = None
                    churn_rate = None
                    nrr = None
                
                # Sales metrics
                if unit['vertical'] == 'Sales':
                    pipeline = random.uniform(20_000_000, 40_000_000)
                    win_rate = random.uniform(0.25, 0.35)
                    avg_deal_size = random.uniform(75_000, 150_000)
                else:
                    pipeline = None
                    win_rate = None
                    avg_deal_size = None
                
                # Common metrics
                dso = random.uniform(35, 55) if unit['performance'] != 'struggling' else random.uniform(60, 85)
                cac = random.uniform(5_000, 15_000)
                ltv = cac * random.uniform(3, 8)
                
                # Employee metrics
                employee_satisfaction = random.uniform(7.5, 9.0) if unit['performance'] == 'high' else random.uniform(6.0, 7.5)
                
                data.append({
                    'unit_id': unit['unit_id'],
                    'unit_name': unit['name'],
                    'date': date,
                    'customers': customers,
                    'arr': arr,
                    'mrr': mrr,
                    'churn_rate_pct': round(churn_rate * 100, 2) if churn_rate else None,
                    'nrr_pct': round(nrr, 1) if nrr else None,
                    'pipeline': pipeline,
                    'win_rate_pct': round(win_rate * 100, 1) if win_rate else None,
                    'avg_deal_size': avg_deal_size,
                    'dso_days': round(dso, 1),
                    'cac': round(cac, 2),
                    'ltv': round(ltv, 2),
                    'ltv_cac_ratio': round(ltv / cac, 2),
                    'employee_satisfaction': round(employee_satisfaction, 1),
                })
        
        return pd.DataFrame(data)
    
    def generate_resource_allocation(self):
        """
        Generate resource allocation data
        
        Business Context: Shows how budget and headcount are distributed
        Used for: Strategic planning, resource optimization
        """
        data = []
        
        for unit in self.units:
            # Annual budget allocation
            if unit['performance'] == 'high':
                annual_budget = random.uniform(80_000_000, 120_000_000)
            elif unit['performance'] == 'growing':
                annual_budget = random.uniform(50_000_000, 80_000_000)
            elif unit['performance'] == 'struggling':
                annual_budget = random.uniform(25_000_000, 45_000_000)
            else:
                annual_budget = random.uniform(60_000_000, 90_000_000)
            
            # Headcount by function
            if unit['vertical'] == 'Software':
                engineering_pct = 0.50
                sales_pct = 0.20
                marketing_pct = 0.15
                ops_pct = 0.15
            elif unit['vertical'] == 'Sales':
                engineering_pct = 0.10
                sales_pct = 0.55
                marketing_pct = 0.25
                ops_pct = 0.10
            elif unit['vertical'] == 'Services':
                engineering_pct = 0.15
                sales_pct = 0.30
                marketing_pct = 0.10
                ops_pct = 0.45
            else:
                engineering_pct = 0.40
                sales_pct = 0.25
                marketing_pct = 0.20
                ops_pct = 0.15
            
            total_headcount = random.randint(40, 90) if unit['performance'] != 'struggling' else random.randint(15, 35)
            
            data.append({
                'unit_id': unit['unit_id'],
                'unit_name': unit['name'],
                'annual_budget': round(annual_budget, 2),
                'q1_spend': round(annual_budget * random.uniform(0.23, 0.25), 2),
                'q2_spend': round(annual_budget * random.uniform(0.24, 0.26), 2),
                'q3_spend': round(annual_budget * random.uniform(0.24, 0.26), 2),
                'q4_projected': round(annual_budget * random.uniform(0.25, 0.27), 2),
                'total_headcount': total_headcount,
                'engineering_headcount': int(total_headcount * engineering_pct),
                'sales_headcount': int(total_headcount * sales_pct),
                'marketing_headcount': int(total_headcount * marketing_pct),
                'ops_headcount': int(total_headcount * ops_pct),
                'contractor_fte': round(total_headcount * random.uniform(0.10, 0.20), 1),
                'avg_salary': random.uniform(95_000, 125_000),
                'open_positions': random.randint(2, 12),
            })
        
        return pd.DataFrame(data)
    
    def generate_alerts(self):
        """
        Generate executive alerts and flags
        
        Business Context: Items requiring C-suite attention
        Used for: Weekly exec reviews, Board escalations
        """
        alerts = [
            {
                'alert_id': 1,
                'unit_id': 4,
                'unit_name': 'Mobile Products',
                'severity': 'HIGH',
                'category': 'Cost Overrun',
                'title': 'Contractor Spend Exceeding Plan',
                'description': 'Unit 4 contractor costs up 67% in Q3. Now 60% of personnel budget vs 15% target.',
                'financial_impact': -180_000,
                'recommended_action': 'Convert 3 key contractors to FTE. Net annual savings: $180K',
                'owner': 'Unit 4 GM',
                'date_raised': datetime(2024, 9, 15),
                'status': 'Open'
            },
            {
                'alert_id': 2,
                'unit_id': 10,
                'unit_name': 'IoT Division',
                'severity': 'HIGH',
                'category': 'Revenue Variance',
                'title': 'Q3 Revenue 18% Below Budget',
                'description': 'IoT Division missing targets. Product-market fit concerns raised.',
                'financial_impact': -2_300_000,
                'recommended_action': 'Strategic review: pivot vs sunset decision needed',
                'owner': 'CFO / Unit 10 GM',
                'date_raised': datetime(2024, 10, 5),
                'status': 'Open'
            },
            {
                'alert_id': 3,
                'unit_id': 6,
                'unit_name': 'Data Analytics',
                'severity': 'MEDIUM',
                'category': 'Margin Pressure',
                'title': 'Revenue Growth Strong but Margins Declining',
                'description': 'Unit 6 growing 40% YoY but operating margin compressed 8pts to 15%.',
                'financial_impact': -850_000,
                'recommended_action': 'Review pricing strategy and cloud infrastructure costs',
                'owner': 'Unit 6 GM / Product',
                'date_raised': datetime(2024, 10, 20),
                'status': 'In Progress'
            },
            {
                'alert_id': 4,
                'unit_id': 8,
                'unit_name': 'EMEA Sales',
                'severity': 'MEDIUM',
                'category': 'Collections',
                'title': 'DSO Increasing - Collections Concern',
                'description': 'EMEA DSO up to 72 days vs 45 day target. $3.2M aging >60 days.',
                'financial_impact': -3_200_000,
                'recommended_action': 'Dedicated AR resource for EMEA region',
                'owner': 'Unit 8 GM / Finance',
                'date_raised': datetime(2024, 11, 1),
                'status': 'Open'
            },
            {
                'alert_id': 5,
                'unit_id': 1,
                'unit_name': 'SaaS Platform',
                'severity': 'LOW',
                'category': 'Positive Variance',
                'title': 'Q4 Revenue Tracking 12% Above Budget',
                'description': 'SaaS Platform accelerating. Enterprise deals closing faster than forecast.',
                'financial_impact': 4_500_000,
                'recommended_action': 'Consider raising FY25 guidance',
                'owner': 'CFO / Investor Relations',
                'date_raised': datetime(2024, 11, 10),
                'status': 'In Progress'
            },
        ]
        
        return pd.DataFrame(alerts)
    
    def generate_all_data(self):
        """Generate all datasets and save to CSV"""
        print("Generating Executive Operations Dashboard Sample Data...")
        print("=" * 60)
        
        # Generate datasets
        print("\n1. Generating Monthly P&L Data...")
        pnl_df = self.generate_monthly_pnl()
        pnl_df.to_csv('/home/claude/executive-ops-dashboard/data/monthly_pnl.csv', index=False)
        print(f"   ✓ Generated {len(pnl_df)} P&L records")
        
        print("\n2. Generating Operational Metrics...")
        metrics_df = self.generate_operational_metrics()
        metrics_df.to_csv('/home/claude/executive-ops-dashboard/data/operational_metrics.csv', index=False)
        print(f"   ✓ Generated {len(metrics_df)} operational records")
        
        print("\n3. Generating Resource Allocation...")
        resources_df = self.generate_resource_allocation()
        resources_df.to_csv('/home/claude/executive-ops-dashboard/data/resource_allocation.csv', index=False)
        print(f"   ✓ Generated {len(resources_df)} resource records")
        
        print("\n4. Generating Executive Alerts...")
        alerts_df = self.generate_alerts()
        alerts_df.to_csv('/home/claude/executive-ops-dashboard/data/executive_alerts.csv', index=False)
        print(f"   ✓ Generated {len(alerts_df)} alerts")
        
        # Generate business units reference
        print("\n5. Creating Business Units Reference...")
        units_df = pd.DataFrame(self.units)
        units_df.to_csv('/home/claude/executive-ops-dashboard/data/business_units.csv', index=False)
        print(f"   ✓ Generated {len(units_df)} business units")
        
        print("\n" + "=" * 60)
        print("✓ Sample Data Generation Complete!")
        print("\nFiles created in /data directory:")
        print("  - monthly_pnl.csv (144 records)")
        print("  - operational_metrics.csv (144 records)")
        print("  - resource_allocation.csv (12 records)")
        print("  - executive_alerts.csv (5 records)")
        print("  - business_units.csv (12 records)")
        print("\nReady to launch dashboard!")

if __name__ == "__main__":
    generator = SampleDataGenerator()
    generator.generate_all_data()
