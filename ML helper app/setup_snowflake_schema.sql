-- ML Helper App - Snowflake Database Setup
-- This script sets up the database schema, tables, and initial configuration

-- Create database and schema
CREATE DATABASE IF NOT EXISTS ML_HELPER_APP;
USE DATABASE ML_HELPER_APP;
CREATE SCHEMA IF NOT EXISTS CORE;
USE SCHEMA CORE;

-- Create table for storing reference knowledge base (customer stories, training materials)
CREATE OR REPLACE TABLE REFERENCE_KNOWLEDGE (
    id STRING,
    document_type STRING, -- 'customer_stories' or 'ae_training'
    title STRING,
    content TEXT,
    summary TEXT,
    key_topics ARRAY,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Create table for storing uploaded customer data
CREATE OR REPLACE TABLE CUSTOMER_UPLOADS (
    upload_id STRING,
    session_id STRING,
    file_name STRING,
    file_type STRING, -- 'pdf', 'docx', 'mp3', 'text'
    original_content TEXT,
    parsed_content TEXT,
    transcribed_content TEXT,
    upload_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Create table for customer profile data (from form inputs)
CREATE OR REPLACE TABLE CUSTOMER_PROFILES (
    session_id STRING,
    company_name STRING,
    industry STRING,
    company_size STRING,
    current_ml_maturity STRING,
    current_platforms ARRAY,
    use_cases ARRAY,
    pain_points ARRAY,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Create table for AI analysis results
CREATE OR REPLACE TABLE AI_ANALYSIS_RESULTS (
    analysis_id STRING,
    session_id STRING,
    analysis_type STRING, -- 'competitive', 'strategy', 'discovery', 'compute_upside'
    ai_response TEXT,
    confidence_score FLOAT,
    recommendations ARRAY,
    next_steps ARRAY,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Create table for final reports
CREATE OR REPLACE TABLE CUSTOMER_REPORTS (
    report_id STRING,
    session_id STRING,
    customer_name STRING,
    executive_summary TEXT,
    competitive_analysis TEXT,
    compute_upside_analysis TEXT,
    short_term_strategy TEXT,
    long_term_strategy TEXT,
    discovery_questions ARRAY,
    poc_recommendations ARRAY,
    risks_to_avoid ARRAY,
    report_generated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Create a file format for parsing documents
CREATE OR REPLACE FILE FORMAT DOCUMENT_FORMAT
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null')
    EMPTY_FIELD_AS_NULL = true;

-- Create stages for file uploads (if needed)
CREATE OR REPLACE STAGE CUSTOMER_UPLOADS_STAGE
    FILE_FORMAT = DOCUMENT_FORMAT;

-- Grant necessary permissions (adjust based on your role setup)
GRANT USAGE ON DATABASE ML_HELPER_APP TO ROLE SYSADMIN;
GRANT USAGE ON SCHEMA ML_HELPER_APP.CORE TO ROLE SYSADMIN;
GRANT ALL ON ALL TABLES IN SCHEMA ML_HELPER_APP.CORE TO ROLE SYSADMIN;
GRANT ALL ON ALL STAGES IN SCHEMA ML_HELPER_APP.CORE TO ROLE SYSADMIN;

-- Verify Cortex AI availability
SELECT SYSTEM$GET_CORTEX_AI_AVAILABILITY() AS cortex_status;

SHOW FUNCTIONS LIKE 'PARSE_DOCUMENT';
SHOW FUNCTIONS LIKE 'AI_TRANSCRIBE';
SHOW FUNCTIONS LIKE 'AI_COMPLETE';
SHOW FUNCTIONS LIKE 'AI_CLASSIFY';
SHOW FUNCTIONS LIKE 'SUMMARIZE';

SELECT 'Database schema setup complete!' AS status; 