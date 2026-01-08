# Tax_estimator_app.py

import streamlit as st
import pandas as pd

from federal_tax import estimate_tax
from illinois_tax import apply_pso_credit, compute_illinois_tax

st.title("💸 IRA Conversion & Tax Estimator")

df = st.data_editor(pd.DataFrame({
'Taxpayer 1':[66,15000,10000,12500,0,0,1500,500,2500,10000,20000],
'Taxpayer 2':[64,15000,10000,12500,0,0,1500,0,2500,10000,20000]
},
index=["age","IRA Withdrawals","Roth Conversions","Pension","Thrift Savings Plan","Annuity",
"Interest","Ordinary Dividends","Qualified Dividends","Capital Gains","Social Security",]),
width="content",height="content",disabled=["_index"])

# age_1 = st.number_input("Age of Taxpayer 1", value=64)
# age_2 = st.number_input("Age of Taxpayer 2", value=60)

age_1 = df.loc["age"]["Taxpayer 1"]
age_2 = df.loc["age"]["Taxpayer 2"]

income_sources = {
    "IRA Withdrawals": df.loc["IRA Withdrawals"]["Taxpayer 1"]+df.loc["IRA Withdrawals"]["Taxpayer 2"],
    "Roth Conversions": df.loc["Roth Conversions"]["Taxpayer 1"]+df.loc["Roth Conversions"]["Taxpayer 2"],
    "Pension": df.loc["Pension"]["Taxpayer 1"]+df.loc["Pension"]["Taxpayer 2"],
    "TSP": df.loc["Thrift Savings Plan"]["Taxpayer 1"]+df.loc["Thrift Savings Plan"]["Taxpayer 2"],
    "Annuity": df.loc["Annuity"]["Taxpayer 1"]+df.loc["Annuity"]["Taxpayer 2"],
    "Interest": df.loc["Interest"]["Taxpayer 1"]+df.loc["Interest"]["Taxpayer 2"],
    "Ordinary Dividends": df.loc["Ordinary Dividends"]["Taxpayer 1"]+df.loc["Ordinary Dividends"]["Taxpayer 2"],
    "Qualified Dividends": df.loc["Qualified Dividends"]["Taxpayer 1"]+df.loc["Qualified Dividends"]["Taxpayer 2"],
    "Capital Gains": df.loc["Capital Gains"]["Taxpayer 1"]+df.loc["Capital Gains"]["Taxpayer 2"],
    "Social Security": df.loc["Social Security"]["Taxpayer 1"]+df.loc["Social Security"]["Taxpayer 2"]
}

# capital_loss_carryover = st.number_input("Capital Loss Carryover", value=0)
# resident_tax_credit = float(st.number_input("Resident Tax Credit", value=0))
is_pso_eligible = st.checkbox("Eligible for Public Safety Officer Credit")
is_illinois_resident = st.checkbox("Illinois Resident")
# real_estate_tax_paid = st.number_input("Real Estate Taxes Paid", value=0)

df2 = st.data_editor(pd.DataFrame({
'Capital Loss Carryover':[0],
'Resident Tax Credit':[0],
'Real Estate Taxes Paid':[0]
},
index=["amount"]),width="content",disabled=["_index"])

capital_loss_carryover = df2.loc["amount"]["Capital Loss Carryover"]
resident_tax_credit = df2.loc["amount"]["Resident Tax Credit"]
real_estate_tax_paid = df2.loc["amount"]["Resident Tax Credit"]
resident_tax_credit = real_estate_tax_paid * 0.05


# Scoped copies

adjusted_income_fed = income_sources.copy()
adjusted_income_il = apply_pso_credit(income_sources.copy(), is_pso_eligible)

# Compute taxes

fed_results = estimate_tax(adjusted_income_fed, age_1, age_2, min(capital_loss_carryover, 3000))
fed_taxed_retirement = (
    income_sources.get("Social Security", 0) +
    income_sources.get("Pension", 0) +
    income_sources.get("IRA Withdrawals", 0) +
    income_sources.get("Annuity", 0) +
    income_sources.get("Roth Conversions", 0) +
    income_sources.get("TSP", 0)
)

if is_illinois_resident:
	il_results = compute_illinois_tax(
    	income_sources,
	    fed_taxable_income=fed_results["Taxable Income"],
    	fed_taxed_retirement=fed_taxed_retirement,
	    taxable_social_security=fed_results["Taxed Social Security"],
    	capital_loss_carryover=capital_loss_carryover,
	    resident_tax_credit=resident_tax_credit
	)

# Display

st.subheader("📊 Federal Tax Summary")
st.caption(f"For Married Filing Jointly | Ages ${age_1} & ${age_2}")

for k, v in fed_results.items():
    if k not in ["Bracket Breakdown", "CG Breakdown"]:
        st.write(f"**{k}:** ${v:,.2f}" if isinstance(v, (int, float)) else f"**{k}:** {v}")

st.write(f"Federally Taxed Retirement (excluded by IL): ${fed_taxed_retirement:,.2f}")
if is_illinois_resident:
	st.subheader("Illinois Income Tax")
	st.write(f"IL Taxable Income: ${il_results['IL Taxable Income']:,.2f}")
	st.write(f"IL Tax Due: ${il_results['Illinois Tax']:,.2f}")
