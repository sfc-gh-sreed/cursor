-- Troubleshoot Streamlit in Snowflake Permissions
-- Run these commands in Snowsight to diagnose permission issues

-- 1. Check your current role and context
SELECT CURRENT_ROLE(), CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE();

-- 2. Check if you can create databases
SHOW GRANTS TO ROLE IDENTIFIER(CURRENT_ROLE());

-- 3. Check Cortex AI availability
SELECT SYSTEM$GET_CORTEX_AI_AVAILABILITY();

-- 4. Check specific Cortex AI function permissions
SHOW GRANTS TO ROLE IDENTIFIER(CURRENT_ROLE()) ON FUNCTION SNOWFLAKE.CORTEX.SUMMARIZE;
SHOW GRANTS TO ROLE IDENTIFIER(CURRENT_ROLE()) ON FUNCTION SNOWFLAKE.CORTEX.CLASSIFY_TEXT;
SHOW GRANTS TO ROLE IDENTIFIER(CURRENT_ROLE()) ON FUNCTION SNOWFLAKE.CORTEX.COMPLETE;

-- 5. Try creating the database (this will tell us exactly what's missing)
CREATE DATABASE IF NOT EXISTS ML_HELPER_APP_TEST;

-- 6. If database creation works, try using it
USE DATABASE ML_HELPER_APP_TEST;
CREATE SCHEMA IF NOT EXISTS CORE;
USE SCHEMA CORE;

-- 7. Try creating a test table
CREATE OR REPLACE TABLE TEST_TABLE (
    id STRING,
    test_content TEXT
);

-- 8. Test Cortex AI function access
SELECT SNOWFLAKE.CORTEX.SUMMARIZE('This is a test message for summarization.');

-- Cleanup (only run if tests above worked)
-- DROP DATABASE ML_HELPER_APP_TEST; 