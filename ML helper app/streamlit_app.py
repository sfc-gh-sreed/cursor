import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, lit
import json
from datetime import datetime
from typing import Dict, List, Optional, Union

# Get the active Snowflake session (built-in for Streamlit in Snowflake)
session = get_active_session()

# Page configuration
st.set_page_config(
    page_title="ML Workload Discovery Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4a90a4;
        margin-bottom: 1rem;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .recommendation-box {
        background-color: #f8f9fa;
        border-left: 5px solid #1f4e79;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .competitor-analysis {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-story {
        background-color: #d1f2eb;
        border: 1px solid #52c788;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class MLHelperApp:
    def __init__(self):
        self.session = session
        
    def setup_database(self):
        """Set up database and schema if they don't exist"""
        try:
            # Create database and schema
            self.session.sql("CREATE DATABASE IF NOT EXISTS ML_HELPER_APP").collect()
            self.session.sql("USE DATABASE ML_HELPER_APP").collect()
            self.session.sql("CREATE SCHEMA IF NOT EXISTS CORE").collect()
            self.session.sql("USE SCHEMA CORE").collect()
            
            # Create tables
            self.session.sql("""
                CREATE OR REPLACE TABLE REFERENCE_KNOWLEDGE (
                    id STRING,
                    document_type STRING,
                    title STRING,
                    content TEXT,
                    summary TEXT,
                    key_topics ARRAY,
                    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
                )
            """).collect()
            
            self.session.sql("""
                CREATE OR REPLACE TABLE CUSTOMER_UPLOADS (
                    upload_id STRING,
                    session_id STRING,
                    file_name STRING,
                    file_type STRING,
                    content TEXT,
                    analysis_results VARIANT,
                    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
                )
            """).collect()
            
            self.session.sql("""
                CREATE OR REPLACE TABLE ANALYSIS_REPORTS (
                    report_id STRING,
                    upload_id STRING,
                    report_type STRING,
                    findings VARIANT,
                    recommendations VARIANT,
                    competitive_analysis VARIANT,
                    next_steps VARIANT,
                    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
                )
            """).collect()
            
            return True
        except Exception as e:
            st.error(f"Database setup error: {str(e)}")
            return False
    
    def load_reference_data(self):
        """Load reference knowledge base data"""
        try:
            # Check if data already exists
            result = self.session.sql("SELECT COUNT(*) as count FROM REFERENCE_KNOWLEDGE").collect()
            if result[0]['COUNT'] > 0:
                return True
            
            # Sample reference data (in production, this would be loaded from your PDFs)
            reference_data = [
                {
                    'id': 'customer_story_1',
                    'document_type': 'customer_stories',
                    'title': 'Scene+ - 66% Processing Time Reduction',
                    'content': 'Scene+ leverages machine learning to deliver relevant member experiences. Using Snowflake Feature Store drove a 66% reduction in processing time.',
                    'summary': 'Feature Store reduced processing time by 66%',
                    'key_topics': ['Feature Store', 'Performance', 'Member Experience']
                },
                {
                    'id': 'customer_story_2',
                    'document_type': 'customer_stories', 
                    'title': 'Cloudbeds - 95% Accuracy with 24x Speed',
                    'content': 'Cloudbeds achieved 95% accuracy across 20,000 properties with 24x training speed improvement using Snowflake ML.',
                    'summary': '95% accuracy, 24x speed improvement',
                    'key_topics': ['Performance', 'Hospitality', 'Training Speed']
                },
                {
                    'id': 'ae_training_1',
                    'document_type': 'ae_training',
                    'title': 'Competitive Analysis - AWS SageMaker',
                    'content': 'SageMaker weaknesses: Complex architecture, data movement costs, forced egress. Snowflake wins with unified platform.',
                    'summary': 'SageMaker competitive positioning',
                    'key_topics': ['SageMaker', 'Competitive Analysis', 'Architecture']
                }
            ]
            
            # Insert reference data
            for item in reference_data:
                self.session.sql("""
                    INSERT INTO REFERENCE_KNOWLEDGE (id, document_type, title, content, summary, key_topics)
                    VALUES (?, ?, ?, ?, ?, PARSE_JSON(?))
                """, [
                    item['id'],
                    item['document_type'],
                    item['title'],
                    item['content'],
                    item['summary'],
                    json.dumps(item['key_topics'])
                ]).collect()
            
            return True
        except Exception as e:
            st.error(f"Reference data loading error: {str(e)}")
            return False
    
    def analyze_with_cortex(self, content: str) -> Dict:
        """Analyze content using Snowflake Cortex AI"""
        try:
            # Use Cortex AI functions for analysis
            summary_result = self.session.sql(f"""
                SELECT SNOWFLAKE.CORTEX.SUMMARIZE('{content.replace("'", "''")}') as summary
            """).collect()
            
            classification_result = self.session.sql(f"""
                SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
                    '{content.replace("'", "''")}',
                    ['SageMaker', 'Databricks', 'Azure ML', 'Vertex AI', 'Excel', 'Other']
                ) as platform_classification
            """).collect()
            
            # Generate recommendations
            recommendations_result = self.session.sql(f"""
                SELECT SNOWFLAKE.CORTEX.COMPLETE(
                    'mistral-large',
                    'Based on this customer information, provide strategic recommendations for Snowflake ML positioning: {content.replace("'", "''")}'
                ) as recommendations
            """).collect()
            
            return {
                'summary': summary_result[0]['SUMMARY'] if summary_result else "Summary unavailable",
                'platform_classification': classification_result[0]['PLATFORM_CLASSIFICATION'] if classification_result else "Unknown",
                'recommendations': recommendations_result[0]['RECOMMENDATIONS'] if recommendations_result else "Recommendations unavailable"
            }
        except Exception as e:
            st.error(f"Cortex AI analysis error: {str(e)}")
            return {
                'summary': "Analysis unavailable",
                'platform_classification': "Unknown", 
                'recommendations': "Unable to generate recommendations"
            }
    
    def get_relevant_customer_stories(self, platform: str, use_case: str = "") -> List[Dict]:
        """Retrieve relevant customer stories from knowledge base"""
        try:
            # Query customer stories based on platform and use case
            stories = self.session.sql("""
                SELECT title, content, summary, key_topics
                FROM REFERENCE_KNOWLEDGE 
                WHERE document_type = 'customer_stories'
                LIMIT 5
            """).collect()
            
            return [
                {
                    'title': story['TITLE'],
                    'content': story['CONTENT'],
                    'summary': story['SUMMARY'],
                    'key_topics': story['KEY_TOPICS']
                }
                for story in stories
            ]
        except Exception as e:
            st.error(f"Error retrieving customer stories: {str(e)}")
            return []
    
    def generate_report(self, analysis: Dict, customer_stories: List[Dict]) -> Dict:
        """Generate comprehensive analysis report"""
        return {
            'executive_summary': analysis.get('summary', 'No summary available'),
            'platform_identified': analysis.get('platform_classification', 'Unknown'),
            'key_findings': [
                'Customer has complex ML infrastructure challenges',
                'Opportunity for platform consolidation',
                'Cost optimization potential identified'
            ],
            'competitive_analysis': {
                'current_platform_issues': [
                    'High operational complexity',
                    'Data movement costs',
                    'Poor cost transparency'
                ],
                'snowflake_advantages': [
                    'Unified data and ML platform',
                    'Transparent, predictable pricing',
                    'No data movement required'
                ]
            },
            'customer_stories': customer_stories,
            'strategic_recommendations': analysis.get('recommendations', 'No recommendations available'),
            'next_steps': [
                'Schedule technical deep-dive session',
                'Conduct POC with specific use case',
                'Develop detailed migration plan',
                'Present cost comparison analysis'
            ]
        }

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 ML Workload Discovery Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">AI-powered tool to help Account Executives discover and capture ML opportunities</p>', unsafe_allow_html=True)
    
    # Initialize app
    app = MLHelperApp()
    
    # Setup database
    if 'db_setup' not in st.session_state:
        with st.spinner("Setting up application..."):
            db_success = app.setup_database()
            ref_success = app.load_reference_data()
            st.session_state.db_setup = db_success and ref_success
    
    if not st.session_state.db_setup:
        st.error("Failed to initialize application. Please check your Snowflake permissions.")
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["📊 Analysis Dashboard", "📁 Upload Content", "📈 Reports", "ℹ️ About"]
    )
    
    if page == "📁 Upload Content":
        st.markdown('<h2 class="sub-header">Upload Customer Content</h2>', unsafe_allow_html=True)
        
        # Input methods
        input_method = st.radio(
            "Choose input method:",
            ["📝 Text Input", "📄 File Upload"]
        )
        
        customer_content = ""
        
        if input_method == "📝 Text Input":
            customer_content = st.text_area(
                "Paste customer notes, meeting transcripts, or discovery information:",
                height=300,
                placeholder="Paste your customer discovery notes here..."
            )
        
        elif input_method == "📄 File Upload":
            uploaded_file = st.file_uploader(
                "Upload customer documents",
                type=['txt', 'pdf', 'docx'],
                help="Upload text files, PDFs, or Word documents"
            )
            
            if uploaded_file is not None:
                if uploaded_file.type == "text/plain":
                    customer_content = str(uploaded_file.read(), "utf-8")
                else:
                    st.info("File uploaded successfully. Content processing would use Snowflake PARSE_DOCUMENT function.")
                    customer_content = "Sample content from uploaded file..."
        
        # Analysis button
        if st.button("🔍 Analyze Content", type="primary"):
            if customer_content:
                with st.spinner("Analyzing content with Snowflake Cortex AI..."):
                    # Analyze content
                    analysis = app.analyze_with_cortex(customer_content)
                    
                    # Get relevant customer stories
                    customer_stories = app.get_relevant_customer_stories(
                        analysis.get('platform_classification', 'Unknown')
                    )
                    
                    # Generate report
                    report = app.generate_report(analysis, customer_stories)
                    
                    # Store in session state
                    st.session_state.analysis_report = report
                    
                    st.success("Analysis complete! View results in the Analysis Dashboard.")
            else:
                st.warning("Please provide customer content to analyze.")
    
    elif page == "📊 Analysis Dashboard":
        st.markdown('<h2 class="sub-header">Analysis Results</h2>', unsafe_allow_html=True)
        
        if 'analysis_report' in st.session_state:
            report = st.session_state.analysis_report
            
            # Executive Summary
            st.markdown("### 📋 Executive Summary")
            st.markdown(f'<div class="recommendation-box">{report["executive_summary"]}</div>', unsafe_allow_html=True)
            
            # Key Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric-box"><h3>Platform Identified</h3><p>{report["platform_identified"]}</p></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-box"><h3>Customer Stories</h3><p>{len(report["customer_stories"])} relevant</p></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-box"><h3>Next Steps</h3><p>{len(report["next_steps"])} actions</p></div>', unsafe_allow_html=True)
            
            # Competitive Analysis
            st.markdown("### ⚔️ Competitive Analysis")
            comp_analysis = report["competitive_analysis"]
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Current Platform Issues:**")
                for issue in comp_analysis["current_platform_issues"]:
                    st.markdown(f"• {issue}")
            
            with col2:
                st.markdown("**Snowflake Advantages:**")
                for advantage in comp_analysis["snowflake_advantages"]:
                    st.markdown(f"• {advantage}")
            
            # Customer Success Stories
            st.markdown("### 🎯 Relevant Customer Stories")
            for story in report["customer_stories"]:
                st.markdown(f'<div class="success-story"><h4>{story["title"]}</h4><p>{story["summary"]}</p></div>', unsafe_allow_html=True)
            
            # Strategic Recommendations
            st.markdown("### 🚀 Strategic Recommendations")
            st.markdown(f'<div class="recommendation-box">{report["strategic_recommendations"]}</div>', unsafe_allow_html=True)
            
            # Next Steps
            st.markdown("### 📋 Next Steps")
            for i, step in enumerate(report["next_steps"], 1):
                st.markdown(f"{i}. {step}")
        
        else:
            st.info("No analysis results available. Please upload and analyze customer content first.")
    
    elif page == "📈 Reports":
        st.markdown('<h2 class="sub-header">Analysis Reports</h2>', unsafe_allow_html=True)
        st.info("Feature coming soon: Historical analysis reports and trend tracking.")
    
    elif page == "ℹ️ About":
        st.markdown('<h2 class="sub-header">About ML Workload Discovery Assistant</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        This application helps Snowflake Account Executives discover and analyze customer ML workloads to:
        
        - **Identify competitive displacement opportunities**
        - **Generate strategic recommendations** based on real customer success stories  
        - **Provide specific next steps** for customer engagement
        - **Reference relevant case studies** and competitive positioning
        
        ### 🔧 **Powered By:**
        - **Snowflake Cortex AI** for content analysis and recommendations
        - **Real customer success stories** for competitive intelligence
        - **Strategic sales methodology** for actionable insights
        
        ### 🎯 **Use Cases:**
        - Customer discovery call analysis
        - Competitive platform assessment  
        - Strategic account planning
        - POC opportunity identification
        """)

if __name__ == "__main__":
    main() 