# 🏔️ Streamlit in Snowflake Deployment Guide

## ML Workload Discovery Assistant - Snowflake Native Version

This guide shows how to deploy the ML Helper App as a **Streamlit in Snowflake** application, eliminating all local environment issues and running natively where your data lives.

## 🎯 **Benefits of Streamlit in Snowflake**

✅ **No local setup issues** - Runs natively in Snowflake  
✅ **Built-in Cortex AI access** - Direct access to all AI functions  
✅ **Automatic scaling** - Snowflake handles all infrastructure  
✅ **Enterprise security** - Built-in governance and access controls  
✅ **Zero data movement** - Analysis happens where data lives  

## 📋 **Prerequisites**

### **Required Snowflake Edition:**
- **Enterprise** or higher (for Cortex AI functions)
- **Streamlit in Snowflake** enabled in your account

### **Required Permissions:**
```sql
-- Database and schema creation
GRANT CREATE DATABASE ON ACCOUNT TO ROLE YOUR_ROLE;
GRANT CREATE SCHEMA ON DATABASE TO ROLE YOUR_ROLE;

-- Cortex AI functions (if not already granted)
GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.SUMMARIZE TO ROLE YOUR_ROLE;
GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.CLASSIFY_TEXT TO ROLE YOUR_ROLE;
GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.COMPLETE TO ROLE YOUR_ROLE;
GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.PARSE_DOCUMENT TO ROLE YOUR_ROLE;

-- Streamlit app creation
GRANT CREATE STREAMLIT ON SCHEMA TO ROLE YOUR_ROLE;
```

### **Check Cortex AI Availability:**
```sql
-- Verify Cortex AI is available in your account
SELECT SYSTEM$GET_CORTEX_AI_AVAILABILITY();

-- List available models
SHOW FUNCTIONS LIKE 'SNOWFLAKE.CORTEX.%';
```

## 🚀 **Deployment Steps**

### **Step 1: Create the Streamlit App**

1. **Open Snowsight** in your browser
2. **Navigate to** Projects → Streamlit
3. **Click "Create Streamlit App"**
4. **Name your app:** `ML_WORKLOAD_DISCOVERY_ASSISTANT`
5. **Choose location:** Database and schema where you want to deploy
6. **Click "Create"**

### **Step 2: Upload the Application Code**

1. **Copy the content** from `streamlit_app.py` (created above)
2. **Paste it into** the Streamlit editor in Snowsight
3. **Click "Run"** to test the initial deployment

### **Step 3: Load Reference Data**

The app includes sample reference data, but to load the full customer stories and AE training data, run this SQL script:

```sql
-- Switch to app database
USE DATABASE ML_HELPER_APP;
USE SCHEMA CORE;

-- Load customer stories (sample - replace with full data)
INSERT INTO REFERENCE_KNOWLEDGE VALUES
('scene_plus', 'customer_stories', 'Scene+ - 66% Processing Time Reduction',
 'Scene+ leverages machine learning to deliver relevant member experiences across our properties. This requires working with a vast amount of data. Leveraging the straightforward Snowflake Feature Store drove a 66% reduction in processing time; we can join the model universe with the features with just four blocks of code. Previous methods required writing extensive Python scripts, input files and additional dependency scripts.',
 'Feature Store reduced processing time by 66% with 4 blocks of code vs extensive scripts',
 PARSE_JSON('["Feature Store", "Performance", "Member Experience", "Python Simplification"]'),
 CURRENT_TIMESTAMP()),

('cloudbeds', 'customer_stories', 'Cloudbeds - 95% Accuracy with 24x Training Speed',
 'Cloudbeds is a global hospitality management platform that uses ML to forecast performance across 20,000 global properties. Difficulty scaling forecasting across a large dataset with 20k properties. Long 12+ hour training cycles, reducing experiments the team could run each week. Accelerated experimentation cycles, achieving 95% accuracy and efficiency gains of over 90% within a six-month forecasting window. Experiments that took 12+ hours were reduced to 30 minutes.',
 '95% accuracy, 24x training speed improvement (12+ hours to 30 minutes)',
 PARSE_JSON('["Performance", "Hospitality", "Training Speed", "Forecasting", "Experimentation"]'),
 CURRENT_TIMESTAMP()),

('fidelity', 'customer_stories', 'Fidelity - Massive Performance Gains',
 'Feature Engineering with Snowflake ML. Language of Choice on a Single Platform. Data is not duplicated nor transferred across the network. Scalability without Operational Complexity. Handles large data volumes. Scales both vertically and horizontally. Simple to use. Lazy evaluation. No Governance and Security Trade-offs. Leverages extensive RBAC controls, enabling tightly managed security.',
 'Up to 77x speedup on feature engineering tasks',
 PARSE_JSON('["Feature Engineering", "Performance", "Scalability", "Security", "RBAC"]'),
 CURRENT_TIMESTAMP());

-- Load AE training materials (sample - replace with full data)
INSERT INTO REFERENCE_KNOWLEDGE VALUES
('sagemaker_competitive', 'ae_training', 'Competitive Analysis - AWS SageMaker',
 'SageMaker Strengths: "Mature" ML platform in capabilities and product marketing. No gaps in ML features or tools. Sticky ecosystem. Weaknesses: Not really a single platform - must stitch services together. Architecture complexity to get model off ground. Forced data movement & egress costs. How Snowflake Wins: Emphasize architecture simplicity. Reduce time to value by starting and ending in Snowflake. Land & Expand in ML pipeline. If predictions come back to Snowflake, use our model registry.',
 'SageMaker competitive positioning and how Snowflake wins',
 PARSE_JSON('["SageMaker", "Competitive Analysis", "Architecture", "Data Movement", "Time to Value"]'),
 CURRENT_TIMESTAMP()),

('databricks_competitive', 'ae_training', 'Competitive Analysis - Databricks',
 'Databricks Strengths: "Industry Leading" in ML mindshare. Robust MLOps framework/experimentation. Made for ML practitioners (lots of horsepower). Weaknesses: Overwhelming and complex depending on ML maturity. Spark experience required, cluster optimization needed. Lack of cost transparency for ML projects start to finish. How Snowflake Wins: Grab attention with specific capability showcases. Snowflake ML jobs for remote code execution. Position multi-modal offerings - AI SQL + Snowflake ML.',
 'Databricks competitive positioning and how Snowflake wins',
 PARSE_JSON('["Databricks", "Competitive Analysis", "Spark", "Cost Transparency", "MLOps"]'),
 CURRENT_TIMESTAMP());
```

### **Step 4: Test the Application**

1. **Click "Run"** in the Streamlit editor
2. **Navigate to "Upload Content"** page
3. **Test with sample content:**

```
Customer Discovery Call - TechCorp Inc.
Current setup: AWS SageMaker for ML training
Pain points: High data movement costs ($50K/month), complex setup taking weeks
Use cases: Fraud detection, customer segmentation, predictive analytics
Team: 15 data scientists, 5 ML engineers
Timeline: Evaluating alternatives by Q2 2025
```

4. **Click "Analyze Content"** to test Cortex AI integration
5. **Check "Analysis Dashboard"** for results

## ⚙️ **Configuration Options**

### **Customize for Your Organization:**

1. **Update branding** in the CSS section:
```python
# Change colors to match your organization
primaryColor = "#YOUR_BRAND_COLOR"
backgroundColor = "#YOUR_BACKGROUND_COLOR"
```

2. **Add your specific customer stories** to the reference data loading
3. **Customize competitive analysis** based on your market positioning
4. **Add organization-specific discovery questions**

### **Enable Additional Cortex Functions:**

```sql
-- For document parsing (if not already enabled)
GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.PARSE_DOCUMENT TO ROLE YOUR_ROLE;

-- For sentiment analysis
GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.SENTIMENT TO ROLE YOUR_ROLE;

-- For translation (if needed)
GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.TRANSLATE TO ROLE YOUR_ROLE;
```

## 🔒 **Security & Governance**

### **Access Control:**
```sql
-- Grant app access to specific roles
GRANT USAGE ON STREAMLIT ML_WORKLOAD_DISCOVERY_ASSISTANT TO ROLE AE_ROLE;
GRANT USAGE ON STREAMLIT ML_WORKLOAD_DISCOVERY_ASSISTANT TO ROLE SALES_MANAGER_ROLE;

-- Restrict sensitive data access
GRANT SELECT ON TABLE REFERENCE_KNOWLEDGE TO ROLE AE_ROLE;
-- Don't grant access to raw customer uploads for broader roles
```

### **Data Privacy:**
- Customer content is processed in your Snowflake account
- No data leaves your environment
- Built-in Snowflake governance and encryption
- Audit trails for all analysis activities

## 📊 **Monitoring & Analytics**

### **Track App Usage:**
```sql
-- Monitor app usage
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.STREAMLIT_USAGE_HISTORY 
WHERE STREAMLIT_NAME = 'ML_WORKLOAD_DISCOVERY_ASSISTANT'
ORDER BY START_TIME DESC;

-- Monitor Cortex AI usage
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY 
WHERE QUERY_TEXT ILIKE '%CORTEX%'
AND START_TIME >= CURRENT_DATE() - 7;
```

### **Performance Optimization:**
- Use appropriate warehouse sizes for Cortex AI workloads
- Consider caching for frequently accessed reference data
- Monitor compute usage and optimize as needed

## 🔧 **Troubleshooting**

### **Common Issues:**

**1. Cortex AI Functions Not Available:**
```sql
-- Check if Cortex is enabled
SELECT SYSTEM$GET_CORTEX_AI_AVAILABILITY();
-- Contact Snowflake support if not available
```

**2. Permission Errors:**
```sql
-- Verify role permissions
SHOW GRANTS TO ROLE YOUR_ROLE;
-- Ensure you have USAGE on required functions
```

**3. App Won't Load:**
- Check warehouse is running
- Verify database and schema exist
- Ensure role has necessary permissions

### **Support:**
- Check Snowflake documentation for Streamlit in Snowflake
- Review Cortex AI documentation for function usage
- Contact Snowflake support for platform-specific issues

## 🎯 **Next Steps**

1. **Deploy the basic app** using the steps above
2. **Load your full reference data** (customer stories, competitive intelligence)
3. **Customize branding and content** for your organization
4. **Train your AE team** on how to use the application
5. **Monitor usage and gather feedback** for improvements
6. **Expand with additional features** as needed

## 📈 **Advanced Features** (Future Enhancements)

- **Historical trend analysis** of customer ML workloads
- **Automated competitive intelligence** updates
- **Integration with CRM systems** (Salesforce, HubSpot)
- **Predictive lead scoring** based on analysis patterns
- **Custom reporting** and executive dashboards

Your ML Workload Discovery Assistant is now ready to help Snowflake AEs discover and win ML opportunities! 🚀 