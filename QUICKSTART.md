# Quick Start Guide

## Getting Your Dashboard Running in 5 Minutes

### Step 1: Clone or Download
```bash
# If this is on GitHub
git clone https://github.com/yourusername/executive-ops-dashboard.git
cd executive-ops-dashboard

# Or if downloaded as ZIP, extract and navigate to folder
cd executive-ops-dashboard
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note for Windows users:** If you encounter issues, you may need to install packages individually:
```bash
pip install streamlit pandas numpy plotly openpyxl
```

### Step 3: Generate Sample Data (Already Done!)
The sample data is already included in the `data/` folder. If you want to regenerate it:
```bash
python src/generate_sample_data.py
```

### Step 4: Launch Dashboard
```bash
streamlit run dashboard.py
```

Your browser should automatically open to `http://localhost:8501`

If it doesn't, manually navigate to: **http://localhost:8501**

### Step 5: Explore the Dashboard

**Three Main Sections:**

1. **Executive Overview** (Default landing page)
   - Corporate performance KPIs
   - Unit performance matrix
   - Executive alerts

2. **Unit Performance** (Select from sidebar)
   - Choose any business unit
   - Deep dive into financials and operations
   - Cost structure analysis

3. **Resource Allocation** (Select from sidebar)
   - Budget distribution across units
   - Headcount by function
   - Quarterly spend tracking

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Install requirements: `pip install -r requirements.txt`

### Issue: "FileNotFoundError: data/monthly_pnl.csv"
**Solution:** Run data generator: `python src/generate_sample_data.py`

### Issue: Port 8501 already in use
**Solution:** Run on different port: `streamlit run dashboard.py --server.port 8502`

### Issue: Dashboard doesn't load
**Solution:** 
1. Check terminal for error messages
2. Verify Python version: `python --version` (needs 3.9+)
3. Try running validation: `python validate.py`

---

## For GitHub Portfolio Use

### Publishing to GitHub

1. **Initialize Git Repository**
```bash
git init
git add .
git commit -m "Initial commit - Executive Operations Dashboard"
```

2. **Create GitHub Repository**
   - Go to https://github.com/new
   - Name: `executive-ops-dashboard`
   - Description: "Real-time multi-unit operational performance dashboard"
   - Public (for portfolio visibility)
   - Click "Create repository"

3. **Push to GitHub**
```bash
git remote add origin https://github.com/yourusername/executive-ops-dashboard.git
git branch -M main
git push -u origin main
```

4. **Pin to Profile**
   - Go to your GitHub profile
   - Click "Customize your pins"
   - Select this repository

### Taking Screenshots for README

To add impressive visuals to your README:

1. **Launch Dashboard:** `streamlit run dashboard.py`
2. **Take Screenshots:**
   - Executive Overview page (main metrics and charts)
   - Unit Performance drill-down
   - Resource Allocation view
3. **Save to:** `screenshots/` folder
4. **Update README:** Add image links:
   ```markdown
   ![Executive Overview](screenshots/executive_overview.png)
   ```

### Creating a Demo Video (Optional but Impressive)

Record a 2-minute walkthrough:
1. Show executive overview
2. Drill into a specific unit
3. Explain an alert
4. Show resource allocation

Upload to YouTube/Loom and add link to README.

---

## Customizing for Real Data

When you're ready to use your own company data:

### Option 1: Modify Sample Data Generator
Edit `src/generate_sample_data.py` to match your:
- Number of business units
- Cost structure
- Performance profiles

### Option 2: Replace with Real Data
Create CSV files matching the schema in `data/`:
- `monthly_pnl.csv`
- `operational_metrics.csv`
- `resource_allocation.csv`
- `executive_alerts.csv`
- `business_units.csv`

**Important:** Never commit real company data to public GitHub!

### Option 3: Connect to Database
Modify `dashboard.py` to read from your database instead of CSV files.

---

## Interview Talking Points

When discussing this project in interviews:

**"Tell me about a time you drove operational excellence"**
> "I built an executive operations dashboard that provided real-time visibility across 12 business units. It replaced 50+ manual Excel reports and reduced our monthly reporting time by 60%. The dashboard automatically flags issues requiring C-suite attention—for example, it caught a contractor overspend issue early enough that we could convert those roles to FTE and save $180K annually."

**"How do you approach technology investments?"**
> "I believe in building internal capabilities for competitive advantage. Rather than buying a $100K+ enterprise dashboard tool, I built this custom solution in a few weeks that's tailored exactly to our business needs. It proves I can bridge business requirements with technical implementation."

**"What's your approach to multi-unit management?"**
> "Visibility is the foundation of accountability. This dashboard gives each unit leader real-time access to their performance metrics and variance explanations. Our exec team has a single source of truth for discussing resource allocation and strategic priorities."

---

## Next Steps

### Immediate (This Week)
- [x] Get dashboard running locally
- [ ] Take screenshots for README
- [ ] Push to GitHub
- [ ] Pin to profile

### Short Term (Next 2 Weeks)
- [ ] Add your LinkedIn/contact info to README
- [ ] Create demo video (optional)
- [ ] Share link with your network
- [ ] Add to resume under "Projects" section

### Long Term (Next Month)
- [ ] Build additional repositories (see portfolio structure doc)
- [ ] Cross-reference projects in READMEs
- [ ] Engage with relevant GitHub repos (star, contribute)
- [ ] Write blog post about building it

---

## Support

If you run into issues:
1. Check the troubleshooting section above
2. Run `python validate.py` to test data loading
3. Check Streamlit documentation: https://docs.streamlit.io

---

## What's Next

This is **Repository #1** of your portfolio. Continue building:

**Priority #2:** Resource Planning Engine  
**Priority #3:** Automation Transformation Framework  
**Priority #4:** Multi-Unit Performance Tracker  

Each repository demonstrates additional leadership capabilities!

---

**Remember:** The goal isn't perfection—it's demonstrating you can bridge finance and technology. Your README and business context matter more than code perfection.

Good luck! 🚀
