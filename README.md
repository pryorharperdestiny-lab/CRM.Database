# Comprehensive Salesforce CRM Architecture & Historical Data Lifecycle Simulation

## 📌 Project Overview
This portfolio project showcases a robust, scalable data architecture designed to model complex customer lifecycles and product entitlements within a Salesforce CRM ecosystem. The project features a synthetically generated database of **413 unique client companies**, mapping multi-product account relationships, strict sequential temporal business logic, and programmatic partner relationships. 

The objective of this case study is to demonstrate advanced data engineering principles, continuous historical trend tracking, and governance frameworks required by Salesforce Administrators, Data Architects, and CRM Consultants.

---

## 🏗️ Core Architecture & Schema Design

The foundational data asset is housed in [`data/mock_crm_database.csv`](./data/mock_crm_database.csv) and contains 413 rows engineered with zero duplicates, enforcing absolute referential integrity.

### 1. Database Fields (Data Dictionary)

| Field Name | Data Type | Salesforce Field Equivalent | Business Logic & Rules Enforced |
| :--- | :--- | :--- | :--- |
| **Client_ID** | Autonumber / Text | `Name` (Autonumber: `CLI-{0000}`) | Primary Key. Global unique identifier for the account record. |
| **Company_Name** | Text (255) | `AccountName` (Text) | Enforced 100% uniqueness across all 413 operational rows. |
| **Company_Liaison** | Text (255) | `Contact.Name` (Lookup) | The primary point of contact. Unique to each client to simulate dedicated account ownership. |
| **Liaison_Phone** | Phone | `Contact.Phone` (Phone) | Standardized direct-dial format (`###-###-####`) mapped cleanly to the liaison. |
| **Referring_Agent** | Text (255) | `User.Name` (Lookup / Lead Source) | The internal sales agent or partner responsible for the deal pipeline. |
| **Account_Status** | Picklist | `Account_Status__c` (Picklist) | Restriced Values: `Initiation`, `Active`, `Terming`, `Termed`. |
| **Client_Type** | Multi-Select Picklist | `Product_Entitlements__mru__c` | Maps individual or bundled product offerings using strict operational codes (B, P, Q, G). |
| **Initiation_Date** | Date | `Onboarding_Start_Date__c` (Date) | The entry stamp. Populated across **100%** of accounts regardless of status. |
| **Active_Date** | Date | `Go_Live_Date__c` (Date) | Populated sequentially for `Active`, `Terming`, and `Termed` records. Retains `N/A` for `Initiation`. |
| **Termed_Date** | Date | `Contract_End_Date__c` (Date) | Populated only if Status is `Termed`. Preserved continuously for downstream churn analytics. |

---

## 🏷️ Entitlement Mappings (Client_Type)
To handle real-world business models where a single corporate client subscribes to multiple service suites, the `Client_Type` column utilizes multi-select flags. 

* **B** = Benefits Management
* **P** = Core Payroll Services
* **Q** = Canada Payroll Only (Regional Compliance)
* **G** = Garnishments & Tax Levies

*System Constraint Realized:* Records display single product lines (e.g., `G`) or compound product bundles (e.g., `"B, P, Q"`) seamlessly, simulating standard Salesforce junction object capabilities or Multi-Select Picklist parameters.

---

## 📆 Strict Lifecycle Temporal Logic
A primary focus of this project is avoiding "data downtime" and establishing clean historical baselines. The chronological pipeline forces fields to populate or lock based on status transitions:

```text
  [ Initiation_Date ]
         │
         ▼
  [ Active_Date ]  ──────►  ( Terming Status )
         │
         ▼
  [ Termed_Date ] (Continuous Historical Tracking Retained)
```

1. **Initiation Stage:** Every client begins here. `Initiation_Date` is logged. `Active_Date` and `Termed_Date` must equal `N/A`.
2. **Active Stage:** Triggered once onboarding concludes (14-45 days post-initiation). `Active_Date` locks a historical stamp. `Termed_Date` remains `N/A`.
3. **Terming Stage:** Represents clients mid-severance. The historical `Active_Date` is preserved to calculate accurate lifetime values (LTV), while `Termed_Date` remains unpopulated until final legal termination.
4. **Termed Stage:** Final status. `Termed_Date` applies automatically (60–730 days post-activation). Crucially, **all prior dates remain natively in the database** to allow historical velocity reporting.

---

## 🛡️ Recommended CRM Validation Governance (Salesforce Implementation)
To prevent dirty data from compromising this structure in production, the following standard Salesforce validation logic formulas should be implemented:

### Rule 1: Enforce Active Date Presence
* **Description:** Prevents an account from moving past initiation without an onboarding Go-Live date.
* **Formula:**
  ```excel
  AND(
      ISPICKVAL(Account_Status__c, "Active"),
      ISBLANK(Active_Date__c)
  )
  ```

### Rule 2: Chronological Sequence Verification
* **Description:** Ensures time cannot move backward (Active Date cannot occur before the Onboarding Initiation Date).
* **Formula:**
  ```excel
  AND(
      NOT(ISBLANK(Active_Date__c)),
      Active_Date__c < Initiation_Date__c
  )
  ```

### Rule 3: Termed Date Integrity
* **Description:** Restricts users from entering a termination date unless the account lifecycle status is explicitly set to Termed.
* **Formula:**
  ```excel
  AND(
      NOT(ISPICKVAL(Account_Status__c, "Termed")),
      NOT(ISBLANK(Termed_Date__c))
  )
  ```

---

## 📈 Downstream Analytics Opportunities
Because this architecture retains complete temporal footprints, this dataset can be plugged directly into **Tableau, Power BI, or CRM Analytics** to calculate core business health metrics:
* **Time-to-Value (TTV):** `Active_Date` minus `Initiation_Date` (Measuring internal onboarding speed).
* **Customer Lifetime Value (LTV):** `Termed_Date` minus `Active_Date` to pinpoint historical contract duration by `Client_Type` segment.
* **Churn Velocity:** Cross-referencing `Referring_Agent` performance against account termination distributions to track agent lead quality.
