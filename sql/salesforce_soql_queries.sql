/* =====================================================================
   Salesforce CRM Architecture - Portfolio SOQL Query Suite
   Target Environment: Salesforce Developer Console / Bulk REST API
   ================================================================     */

-- 1. Query Active Accounts with Product Entitlements
-- Retrieves all live corporate accounts ordered by their onboarding start date.
SELECT 
    Id, 
    Name, 
    Account_Status__c, 
    Product_Entitlements__mru__c, 
    Onboarding_Start_Date__c, 
    Go_Live_Date__c 
FROM 
    Account 
WHERE 
    Account_Status__c = 'Active' 
ORDER BY 
    Onboarding_Start_Date__c DESC;


-- 2. Pipeline Drop-off Analysis: Pre-Go-Live Cancellations
-- Tracks accounts that dropped out during the 45-60 day onboarding window.
SELECT 
    Id, 
    Name, 
    Referring_Agent__c, 
    Onboarding_Start_Date__c, 
    Contract_End_Date__c 
FROM 
    Account 
WHERE 
    Account_Status__c = 'Cancelled'
ORDER BY 
    Onboarding_Start_Date__c ASC;


-- 3. Product Entitlement Filter (Multi-Select Picklist)
-- Queries accounts subscribed to Core Payroll Services ('P') bundled with Benefits Management ('B').
SELECT 
    Id, 
    Name, 
    Account_Status__c, 
    Product_Entitlements__mru__c 
FROM 
    Account 
WHERE 
    Product_Entitlements__mru__c INCLUDES ('P', 'B');


-- 4. Churn Velocity & Lifetime Value (LTV) Reporting
-- Pulls termed accounts to audit contract longevity post-activation.
SELECT 
    Id, 
    Name, 
    Product_Entitlements__mru__c, 
    Go_Live_Date__c, 
    Contract_End_Date__c 
FROM 
    Account 
WHERE 
    Account_Status__c = 'Termed';
