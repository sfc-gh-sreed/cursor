# 📋 ML Helper App - Deployment Checklist

## Prerequisites ✅

### Snowflake Environment
- [ ] Snowflake account with Cortex AI enabled
- [ ] Verify Cortex AI functions are available:
  ```sql
  SELECT SYSTEM$GET_CORTEX_AI_AVAILABILITY();
  SHOW FUNCTIONS LIKE 'PARSE_DOCUMENT';
  SHOW FUNCTIONS LIKE 'AI_TRANSCRIBE';
  SHOW FUNCTIONS LIKE 'AI_COMPLETE';
  ```
- [ ] Appropriate role with database creation permissions
- [ ] Warehouse for compute (recommend MEDIUM or larger for AI processing)

### Development Environment
- [ ] Python 3.8+ installed
- [ ] Git access to repository
- [ ] Text editor/IDE for configuration

## Setup Steps 🛠️

### 1. Application Files
- [ ] Clone/download application files
- [ ] Verify all required files are present:
  - `ml_helper_app.py` (main application)
  - `setup_snowflake_schema.sql` (database setup)
  - `load_reference_data.py` (data loader)
  - `requirements.txt` (Python dependencies)
  - `.streamlit/secrets.toml.template` (configuration template)

### 2. Python Environment
- [ ] Create virtual environment:
  ```bash
  python -m venv ml_helper_env
  source ml_helper_env/bin/activate  # On Windows: ml_helper_env\Scripts\activate
  ```
- [ ] Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### 3. Snowflake Database Setup
- [ ] Connect to Snowflake (SnowSQL, Worksheet, or client)
- [ ] Run database setup script:
  ```sql
  @setup_snowflake_schema.sql
  ```
- [ ] Verify tables were created:
  ```sql
  USE DATABASE ML_HELPER_APP;
  USE SCHEMA CORE;
  SHOW TABLES;
  ```

### 4. Configuration
- [ ] Copy secrets template:
  ```bash
  cp .streamlit/secrets.toml.template .streamlit/secrets.toml
  ```
- [ ] Update `.streamlit/secrets.toml` with your Snowflake credentials:
  - Account identifier
  - Username and password
  - Role (e.g., SYSADMIN)
  - Warehouse name
  - Database: ML_HELPER_APP
  - Schema: CORE

### 5. Reference Data Loading
- [ ] Update `load_reference_data.py` with your Snowflake connection details
- [ ] **IMPORTANT**: Replace sample data with actual PDF content:
  - Update `customer_stories_sample` with content from "Snowflake ML - External Customer Stories.pdf"
  - Update `ae_training_sample` with content from "AI ML 101 for AEs.pdf"
- [ ] Run data loader:
  ```bash
  python load_reference_data.py
  ```
- [ ] Verify data was loaded:
  ```sql
  SELECT document_type, COUNT(*) FROM REFERENCE_KNOWLEDGE GROUP BY document_type;
  ```

## Testing & Validation 🧪

### 1. Application Launch
- [ ] Start the application:
  ```bash
  streamlit run ml_helper_app.py
  ```
- [ ] Verify application opens in browser (typically http://localhost:8501)
- [ ] Check Snowflake connection status in the app

### 2. Core Functionality Test
- [ ] **Upload Test**: Upload a sample PDF document
- [ ] **Text Input Test**: Paste sample customer information
- [ ] **Customer Profile**: Fill out and save a customer profile
- [ ] **AI Analysis**: Run complete analysis (verify no errors)
- [ ] **Report Generation**: Check that report displays correctly

### 3. Database Verification
- [ ] Check that data is being saved:
  ```sql
  SELECT COUNT(*) FROM CUSTOMER_UPLOADS;
  SELECT COUNT(*) FROM CUSTOMER_PROFILES;
  SELECT COUNT(*) FROM AI_ANALYSIS_RESULTS;
  ```

## Production Deployment 🚀

### Option 1: Snowflake Streamlit (Recommended)
- [ ] Upload application files to Snowflake stage
- [ ] Create Streamlit app in Snowflake:
  ```sql
  CREATE STREAMLIT ML_HELPER_APP
  ROOT_LOCATION = '@your_stage/ml_helper_app'
  MAIN_FILE = 'ml_helper_app.py';
  ```
- [ ] Grant appropriate permissions to users
- [ ] Test application access

### Option 2: External Streamlit Cloud
- [ ] Deploy to Streamlit Cloud or other hosting platform
- [ ] Configure environment variables/secrets
- [ ] Ensure Snowflake connectivity from external platform
- [ ] Set up authentication if required

### Option 3: Internal Server
- [ ] Set up application server
- [ ] Configure reverse proxy if needed
- [ ] Set up SSL certificates
- [ ] Configure authentication/authorization

## Security & Access 🔒

### User Access
- [ ] Create appropriate Snowflake roles for app users
- [ ] Grant necessary permissions:
  ```sql
  GRANT USAGE ON DATABASE ML_HELPER_APP TO ROLE AE_USER_ROLE;
  GRANT USAGE ON SCHEMA ML_HELPER_APP.CORE TO ROLE AE_USER_ROLE;
  GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA ML_HELPER_APP.CORE TO ROLE AE_USER_ROLE;
  ```
- [ ] Test user access with non-admin account

### Data Governance
- [ ] Review data retention policies
- [ ] Set up data classification if required
- [ ] Configure access logging
- [ ] Document data flow for compliance

## Post-Deployment 📊

### Monitoring
- [ ] Set up Snowflake query monitoring
- [ ] Monitor credit usage for Cortex AI functions
- [ ] Track application usage metrics
- [ ] Set up alerting for errors or performance issues

### User Training
- [ ] Create user training materials
- [ ] Schedule training sessions for AEs
- [ ] Provide quick reference guide
- [ ] Set up support process

### Maintenance
- [ ] Plan regular reference data updates
- [ ] Schedule application updates
- [ ] Monitor and optimize AI prompts
- [ ] Review and improve based on user feedback

## Troubleshooting 🔧

### Common Issues and Solutions

**Connection Errors**
- Verify Snowflake credentials
- Check network connectivity
- Confirm role permissions

**AI Function Errors**
- Verify Cortex AI is enabled
- Check function permissions
- Review warehouse size (recommend MEDIUM+)

**Upload Issues**
- Check file size limits
- Verify supported formats
- Review file content structure

**Performance Issues**
- Increase warehouse size
- Optimize content chunking
- Review prompt complexity

## Support Resources 📚

- [Snowflake Cortex AI Documentation](https://docs.snowflake.com/user-guide/snowflake-cortex)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Application README](README.md)
- Internal Snowflake support channels

---

## Final Checklist Summary ✅

Before going live:
- [ ] All tests pass
- [ ] Reference data is loaded with actual PDF content
- [ ] User access is configured
- [ ] Security requirements are met
- [ ] Monitoring is in place
- [ ] Users are trained
- [ ] Support process is defined

**Status**: Ready for production deployment! 🎉 