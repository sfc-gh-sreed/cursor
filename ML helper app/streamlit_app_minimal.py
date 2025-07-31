import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
import json
from typing import Dict, List

# Get the active Snowflake session
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
    }
    .recommendation-box {
        background-color: #f8f9fa;
        border-left: 5px solid #1f4e79;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
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

def check_permissions():
    """Check if we have necessary permissions"""
    try:
        # Test basic session access
        result = session.sql("SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE()").collect()
        
        # Test Cortex AI access
        cortex_test = session.sql("""
            SELECT SNOWFLAKE.CORTEX.SUMMARIZE('This is a simple test for Cortex AI access.')
        """).collect()
        
        return True, "All permissions OK"
    except Exception as e:
        return False, str(e)

def analyze_with_cortex(content: str) -> Dict:
    """Analyze content using Snowflake Cortex AI - simplified version"""
    try:
        # Simple content analysis without database dependencies
        if len(content) < 50:
            return {
                'summary': "Content too short for analysis",
                'platform_classification': "Unknown",
                'recommendations': "Please provide more detailed customer information"
            }
        
        # Use Cortex AI for basic analysis
        summary_result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SUMMARIZE('{content.replace("'", "''")}') as summary
        """).collect()
        
        # Simple keyword-based platform detection
        content_lower = content.lower()
        platform = "Unknown"
        if "sagemaker" in content_lower or "aws" in content_lower:
            platform = "AWS SageMaker"
        elif "databricks" in content_lower:
            platform = "Databricks"
        elif "azure ml" in content_lower or "azure" in content_lower:
            platform = "Azure ML"
        elif "vertex ai" in content_lower or "google cloud" in content_lower:
            platform = "Google Vertex AI"
        elif "excel" in content_lower or "spreadsheet" in content_lower:
            platform = "Excel/Manual"
        
        # Generate basic recommendations
        recommendations = f"""
        Based on the analysis, this customer appears to be using {platform} and could benefit from:
        
        1. **Unified Platform Approach**: Consolidate ML workloads in Snowflake to eliminate data movement
        2. **Cost Optimization**: Leverage Snowflake's transparent, predictable pricing model
        3. **Simplified Architecture**: Reduce operational complexity with Snowflake ML
        4. **Governance Improvements**: Built-in data governance and lineage tracking
        
        **Next Steps:**
        - Schedule technical deep-dive on Snowflake ML capabilities
        - Conduct POC with their primary use case
        - Provide cost comparison analysis vs current platform
        """
        
        return {
            'summary': summary_result[0]['SUMMARY'] if summary_result else "Analysis completed",
            'platform_classification': platform,
            'recommendations': recommendations
        }
    except Exception as e:
        return {
            'summary': f"Analysis error: {str(e)}",
            'platform_classification': "Unknown",
            'recommendations': "Unable to generate recommendations due to permission or configuration issues"
        }

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 ML Workload Discovery Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Simplified version - AI-powered tool for Snowflake AEs</p>', unsafe_allow_html=True)
    
    # Check permissions first
    permissions_ok, perm_message = check_permissions()
    
    if not permissions_ok:
        st.error(f"Permission Issue: {perm_message}")
        st.markdown("""
        ### 🔧 **Troubleshooting Steps:**
        
        1. **Check your role permissions** by running the SQL in `troubleshoot_permissions.sql`
        2. **Contact your Snowflake admin** to grant necessary permissions:
           - `USAGE` on Cortex AI functions
           - `CREATE SCHEMA` permissions (if using full version)
        3. **Try the minimal version** by using this simplified app
        
        ### 📋 **Required Permissions:**
        ```sql
        -- Minimum required for this app
        GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.SUMMARIZE TO ROLE YOUR_ROLE;
        GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.CLASSIFY_TEXT TO ROLE YOUR_ROLE;
        GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.COMPLETE TO ROLE YOUR_ROLE;
        ```
        """)
        return
    
    st.success("✅ Permissions check passed! App is ready to use.")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["📊 Quick Analysis", "ℹ️ About"]
    )
    
    if page == "📊 Quick Analysis":
        st.markdown("### 📝 Customer Content Analysis")
        
        # Input area
        customer_content = st.text_area(
            "Paste customer discovery notes, meeting transcripts, or pain points:",
            height=300,
            placeholder="""Example:
Customer: TechCorp Inc.
Current ML Platform: AWS SageMaker  
Pain Points: High data movement costs ($50K/month), complex setup
Use Cases: Fraud detection, customer segmentation
Team Size: 15 data scientists, 5 ML engineers
Timeline: Evaluating alternatives by Q2 2025
            """)
        
        # Analysis button
        if st.button("🔍 Analyze with Cortex AI", type="primary"):
            if customer_content and len(customer_content.strip()) > 10:
                with st.spinner("Analyzing content with Snowflake Cortex AI..."):
                    analysis = analyze_with_cortex(customer_content)
                    
                    # Display results
                    st.markdown("### 📋 Analysis Results")
                    
                    # Executive Summary
                    st.markdown("#### Executive Summary")
                    st.markdown(f'<div class="recommendation-box">{analysis["summary"]}</div>', unsafe_allow_html=True)
                    
                    # Platform Identification
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Platform Identified", analysis["platform_classification"])
                    with col2:
                        st.metric("Analysis Status", "✅ Complete")
                    
                    # Strategic Recommendations
                    st.markdown("#### 🚀 Strategic Recommendations")
                    st.markdown(f'<div class="recommendation-box">{analysis["recommendations"]}</div>', unsafe_allow_html=True)
                    
                    # Sample Customer Stories
                    st.markdown("#### 🎯 Relevant Customer Success Stories")
                    
                    if "sagemaker" in analysis["platform_classification"].lower():
                        st.markdown("""
                        <div class="success-story">
                        <h4>Scene+ - 66% Processing Time Reduction</h4>
                        <p>Migrated from complex Python scripts to Snowflake Feature Store, achieving 66% reduction in processing time with just 4 blocks of code.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    elif "databricks" in analysis["platform_classification"].lower():
                        st.markdown("""
                        <div class="success-story">
                        <h4>IGS Energy - 75% Cost Savings</h4>
                        <p>Migrated from Databricks to Snowflake ML, achieving 75% cost savings and reducing training time from 30 minutes to minutes for hundreds of thousands of customer forecasts.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    else:
                        st.markdown("""
                        <div class="success-story">
                        <h4>Cloudbeds - 95% Accuracy with 24x Speed</h4>
                        <p>Achieved 95% forecasting accuracy across 20,000 properties with 24x training speed improvement using Snowflake ML.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Next Steps
                    st.markdown("#### 📋 Recommended Next Steps")
                    st.markdown("""
                    1. **Schedule technical deep-dive** on Snowflake ML capabilities
                    2. **Identify POC use case** for quick win demonstration  
                    3. **Prepare cost comparison** analysis vs current platform
                    4. **Plan migration strategy** with timeline and milestones
                    """)
            else:
                st.warning("Please provide customer content to analyze.")
    
    elif page == "ℹ️ About":
        st.markdown("### About ML Workload Discovery Assistant")
        
        st.markdown("""
        This **simplified version** helps Snowflake Account Executives analyze customer ML workloads using Snowflake Cortex AI.
        
        #### 🔧 **Current Capabilities:**
        - ✅ **Content Analysis** using Cortex AI SUMMARIZE
        - ✅ **Platform Identification** based on customer notes
        - ✅ **Strategic Recommendations** for Snowflake positioning
        - ✅ **Customer Success Stories** for competitive intelligence
        
        #### 📈 **Full Version Features** (requires additional permissions):
        - Customer data storage and history
        - Advanced competitive analysis
        - Detailed reporting and analytics
        - Multi-file upload capabilities
        
        #### 🎯 **Perfect For:**
        - Quick customer discovery analysis
        - Competitive platform assessment
        - Strategic account planning
        - POC opportunity identification
        
        ---
        
        **Need the full version?** Contact your Snowflake admin to grant database creation permissions and deploy the complete application.
        """)

if __name__ == "__main__":
    main() 