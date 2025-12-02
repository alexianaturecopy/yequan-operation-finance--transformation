"""
Validation script to test dashboard data loading and calculations
"""
import pandas as pd
import sys

def validate_dashboard():
    """Test that all data loads correctly and basic calculations work"""
    
    print("=" * 70)
    print("EXECUTIVE OPERATIONS DASHBOARD - VALIDATION")
    print("=" * 70)
    
    try:
        # Test 1: Load all data files
        print("\n✓ Test 1: Loading Data Files")
        pnl = pd.read_csv('data/monthly_pnl.csv')
        metrics = pd.read_csv('data/operational_metrics.csv')
        resources = pd.read_csv('data/resource_allocation.csv')
        alerts = pd.read_csv('data/executive_alerts.csv')
        units = pd.read_csv('data/business_units.csv')
        
        print(f"  - monthly_pnl.csv: {len(pnl)} records loaded")
        print(f"  - operational_metrics.csv: {len(metrics)} records loaded")
        print(f"  - resource_allocation.csv: {len(resources)} records loaded")
        print(f"  - executive_alerts.csv: {len(alerts)} records loaded")
        print(f"  - business_units.csv: {len(units)} records loaded")
        
        # Test 2: Calculate corporate KPIs
        print("\n✓ Test 2: Corporate Performance Calculations")
        pnl['date'] = pd.to_datetime(pnl['date'])
        latest_month = pnl['month'].max()
        current_data = pnl[pnl['month'] == latest_month]
        
        total_revenue = current_data['revenue'].sum()
        total_operating_income = current_data['operating_income'].sum()
        operating_margin = (total_operating_income / total_revenue) * 100
        total_headcount = current_data['headcount'].sum()
        
        print(f"  - Total Revenue (Current Month): ${total_revenue/1_000_000:.1f}M")
        print(f"  - Operating Income: ${total_operating_income/1_000_000:.1f}M")
        print(f"  - Operating Margin: {operating_margin:.1f}%")
        print(f"  - Total Headcount: {total_headcount}")
        
        # Test 3: Unit performance summary
        print("\n✓ Test 3: Unit Performance Summary")
        print(f"  - Number of business units: {len(current_data)}")
        top_performer = current_data.loc[current_data['operating_margin_pct'].idxmax()]
        print(f"  - Top performer: {top_performer['unit_name']} ({top_performer['operating_margin_pct']:.1f}% margin)")
        
        # Test 4: Alerts validation
        print("\n✓ Test 4: Executive Alerts")
        print(f"  - Total alerts: {len(alerts)}")
        high_severity = len(alerts[alerts['severity'] == 'HIGH'])
        print(f"  - High severity alerts: {high_severity}")
        
        total_financial_impact = alerts['financial_impact'].sum()
        print(f"  - Total financial impact: ${total_financial_impact/1_000_000:.1f}M")
        
        # Test 5: Resource allocation
        print("\n✓ Test 5: Resource Allocation")
        total_budget = resources['annual_budget'].sum()
        print(f"  - Total corporate budget: ${total_budget/1_000_000:.1f}M")
        print(f"  - Total headcount across units: {resources['total_headcount'].sum()}")
        
        print("\n" + "=" * 70)
        print("✅ ALL VALIDATION TESTS PASSED!")
        print("=" * 70)
        print("\nDashboard is ready to launch!")
        print("\nTo run the dashboard:")
        print("  streamlit run dashboard.py")
        print("\nThen navigate to: http://localhost:8501")
        
        return True
        
    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = validate_dashboard()
    sys.exit(0 if success else 1)
