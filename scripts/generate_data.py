import os
import numpy as np
import pandas as pd


def generate_mock_crm_data(
    num_records=413, output_path="data/mock_crm_database.csv"
):
  print(f"Generating synthetic dataset with {num_records} records...")

  # Set random seed for reproducibility
  np.random.seed(42)

  company_prefixes = [
      "Apex",
      "Vanguard",
      "Summit",
      "Nexus",
      "Pioneer",
      "Global",
      "Sterling",
      "Dynamic",
      "Omni",
      "Veridian",
      "Atlas",
      "Quantum",
      "Meridian",
      "Zenith",
  ]
  company_suffixes = [
      "Logistics",
      "Technologies",
      "Holdings",
      "Solutions",
      "Group",
      "Partners",
      "Industries",
      "Consulting",
      "Enterprise",
      "Systems",
  ]
  first_names = [
      "Sarah",
      "Michael",
      "David",
      "Jessica",
      "James",
      "Emily",
      "Robert",
      "Amanda",
      "John",
      "Ashley",
      "Brian",
      "Megan",
      "Kevin",
      "Rachel",
  ]
  last_names = [
      "Smith",
      "Johnson",
      "Williams",
      "Brown",
      "Jones",
      "Miller",
      "Davis",
      "Garcia",
      "Rodriguez",
      "Wilson",
      "Martinez",
      "Anderson",
      "Taylor",
      "Thomas",
  ]

  # Agents mapped to specific onboarding speed profiles (in days)
  agent_profiles = {
      "Alex Mercer": {"profile": "fast", "range": (35, 45)},
      "Jordan Lee": {"profile": "target", "range": (45, 60)},
      "Taylor Swift": {"profile": "slow", "range": (60, 75)},
      "Morgan Vance": {"profile": "target", "range": (42, 58)},
      "Casey Sterling": {"profile": "fast", "range": (38, 48)},
      "Samira Khan": {"profile": "slow", "range": (58, 72)},
      "Devon Brooks": {"profile": "target", "range": (45, 60)},
  }
  agents = list(agent_profiles.keys())

  products = ["B", "P", "Q", "G", "B, P", "P, G", "B, P, Q", "B, G"]
  statuses = ["Initiation", "Active", "Cancelled", "Terming", "Termed"]
  status_weights = [0.10, 0.45, 0.10, 0.10, 0.25]

  # Generate unique company names
  company_names = set()
  while len(company_names) < num_records:
    name = f"{np.random.choice(company_prefixes)} {np.random.choice(company_suffixes)} {np.random.randint(100, 999)}"
    company_names.add(name)
  company_names = list(company_names)

  data = []
  start_date_base = pd.to_datetime("2023-01-01")

  for i in range(num_records):
    client_id = f"CLI-{i+1:04d}"
    comp_name = company_names[i]
    liaison = f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
    phone = f"{np.random.randint(200, 999)}-{np.random.randint(100, 999)}-{np.random.randint(1000, 9999)}"

    agent = np.random.choice(agents)
    status = np.random.choice(statuses, p=status_weights)
    client_type = np.random.choice(products)

    # Initiation Date spread over 700 days
    init_days_offset = np.random.randint(0, 700)
    init_date = start_date_base + pd.Timedelta(days=init_days_offset)

    active_date = "N/A"
    termed_date = "N/A"

    if status == "Initiation":
      pass
    elif status == "Cancelled":
      # Pre-Go-Live Cancellation strictly within the first 30 days
      cancel_offset = np.random.randint(1, 31)
      termed_date = (
          init_date + pd.Timedelta(days=cancel_offset)
      ).strftime("%Y-%m-%d")
    else:
      # Active, Terming, or Termed: pull onboarding days based on agent profile (35-75 day bounds)
      min_day, max_day = agent_profiles[agent]["range"]
      onboard_days = np.random.randint(min_day, max_day + 1)
      active_dt = init_date + pd.Timedelta(days=onboard_days)
      active_date = active_dt.strftime("%Y-%m-%d")

      if status in ["Terming", "Termed"]:
        contract_days = np.random.randint(60, 730)
        termed_dt = active_dt + pd.Timedelta(days=contract_days)
        termed_date = termed_dt.strftime("%Y-%m-%d")

    data.append({
        "Client_ID": client_id,
        "Company_Name": comp_name,
        "Company_Liaison": liaison,
        "Liaison_Phone": phone,
        "Referring_Agent": agent,
        "Account_Status": status,
        "Client_Type": client_type,
        "Initiation_Date": init_date.strftime("%Y-%m-%d"),
        "Active_Date": active_date,
        "Termed_Date": termed_date,
    })

  df = pd.DataFrame(data)

  # Ensure directory exists and save
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  df.to_csv(output_path, index=False)
  print(f"Successfully generated database at: {output_path}")


if __name__ == "__main__":
  generate_mock_crm_data()
