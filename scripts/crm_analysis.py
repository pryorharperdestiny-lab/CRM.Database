import numpy as np
import pandas as pd


def load_and_analyze_crm_data(file_path):
  """Loads the mock Salesforce CRM database and computes core pipeline KPIs."""
  print("--- Loading CRM Dataset ---")
  try:
    df = pd.read_csv(file_path)
    print(f"Successfully loaded {len(df)} client records.\n")
  except FileNotFoundError:
    print(f"Error: Could not find file at {file_path}. Check your path.")
    return

  # Convert date columns, coercing 'N/A' strings to NaT (Not a Time)
  date_cols = ["Initiation_Date", "Active_Date", "Termed_Date"]
  for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

  # 1. Calculate Time-to-Value (TTV) in days for Active/Termed accounts
  # (Measures onboarding duration, targeting the 45-60 day window)
  df["TTV_Days"] = (df["Active_Date"] - df["Initiation_Date"]).dt.days

  # 2. Calculate Customer Lifetime Value (LTV) contract duration in days
  df["LTV_Contract_Days"] = (df["Termed_Date"] - df["Active_Date"]).dt.days

  # --- Summary Reports ---
  print("=== CRM ARCHITECTURE PERFORMANCE METRICS ===")
  print(f"• Total Client Accounts: {len(df)}")
  print(
      f"• Average Onboarding Time (TTV): {df['TTV_Days'].mean():.1f} days"
      " (Target: 45-60 days)"
  )

  cancelled_df = df[df["Account_Status"] == "Cancelled"]
  cancellation_rate = (len(cancelled_df) / len(df)) * 100
  print(
      f"• Pre-Go-Live Cancellations: {len(cancelled_df)} accounts"
      f" ({cancellation_rate:.1f}% drop-off rate)"
  )

  active_count = len(df[df["Account_Status"] == "Active"])
  print(f"• Currently Active Accounts: {active_count}")

  avg_ltv = df["LTV_Contract_Days"].mean()
  print(f"• Average Active Contract Lifespan (LTV): {avg_ltv:.1f} days")
  print("============================================\n")

# --- Agent Performance Breakdown ---
  print("=== AGENT ONBOARDING PERFORMANCE BREAKDOWN ===")
  agent_summary = (
      active_or_termed.groupby("Referring_Agent")["TTV_Days"]
      .agg(["count", "mean"])
      .reset_index()
  )
  agent_summary.columns = ["Referring_Agent", "Completed_Onboardings", "Avg_TTV_Days"]
  agent_summary["Avg_TTV_Days"] = agent_summary["Avg_TTV_Days"].round(1)

# Classify agent performance tiers
  def classify_performance(avg_days):
    if avg_days < 45:
      return "Fast / Upper-Lower (<45 days)"
    elif avg_days <= 60:
      return "On Target (45-60 days)"
    else:
      return "Slow / Upper-End (>60 days)"

  agent_summary["Performance_Tier"] = agent_summary["Avg_TTV_Days"].apply(
      classify_performance
  )

  for _, row in agent_summary.iterrows():
    print(
        f"• Agent: {row['Referring_Agent']} | Completed: "
        f"{row['Completed_Onboardings']} | Avg TTV: "
        f"{row['Avg_TTV_Days']} days | Tier: {row['Performance_Tier']}"
    )
  print("==============================================")

  return df


if __name__ == "__main__":
  # Run the function pointing to your mock database path
  dataset_path = "data/mock_crm_database.csv"
  analyzed_df = load_and_analyze_crm_data(dataset_path)
