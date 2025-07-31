import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import call_builtin
from snowflake.snowpark.types import BinaryType
import json
from typing import Dict, List
import base64
import time
import uuid
import tempfile
import os

# Get the active Snowflake session
session = get_active_session()

# Page configuration
st.set_page_config(
    page_title="ML Workload Discovery Assistant",
    page_icon="🤖",
    layout="wide"
)

# Simplified CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .content-box {
        background-color: #f8f9fa;
        border-left: 4px solid #1f4e79;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 6px;
    }
    .story-box {
        background-color: #e8f5e8;
        border: 1px solid #52c788;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    .platform-tag {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Reference data from AI & ML 101 and Customer Stories
CUSTOMER_STORIES = {
    "sagemaker": [
        {
            "title": "Scene+ - 66% Processing Time Reduction",
            "metrics": "66% processing time reduction, 4 blocks of code vs extensive Python scripts",
            "quote": "Leveraging the straightforward Snowflake Feature Store drove a 66% reduction in processing time"
        }
    ],
    "databricks": [
        {
            "title": "IGS Energy - 75% Cost Savings", 
            "metrics": "75% cost savings in training, minutes vs 30-minute training cycles",
            "quote": "We can more easily build predictive models and mock up data products all in the Snowflake ecosystem"
        },
        {
            "title": "Decile - 9.2x Speed Improvement",
            "metrics": "9.2x speedup (60 minutes to 6.5 minutes)",
            "quote": "Snowpark ML has enabled us to more rapidly iterate on our models, improving accuracy and operational efficiency"
        }
    ],
    "excel": [
        {
            "title": "SpartanNash - Retail Forecasting Automation",
            "metrics": "Accuracy improved 71% → 88%, 5,200 hours/year → 5 minutes/week",
            "quote": "We've saved hours of effort while generating more accurate forecasts"
        }
    ],
    "general": [
        {
            "title": "Cloudbeds - 95% Accuracy with 24x Speed", 
            "metrics": "95% accuracy, 30-minute experiments (down from 12+ hours)",
            "quote": "Achieving 95% accuracy and efficiency gains of over 90% within a six-month forecasting window"
        }
    ]
}

def check_permissions():
    """Check basic permissions"""
    try:
        session.sql("SELECT CURRENT_ROLE()").collect()
        session.sql("SELECT SNOWFLAKE.CORTEX.SUMMARIZE('test')").collect()
        return True, "OK"
    except Exception as e:
        return False, str(e)

def process_uploaded_file(uploaded_file):
    """Process uploaded files using proper Snowflake PARSE_DOCUMENT approach"""
    try:
        # Debug: show file type
        file_type = uploaded_file.type
        file_name = uploaded_file.name
        
        # Handle text files
        if file_type == "text/plain" or file_name.lower().endswith('.txt'):
            content = str(uploaded_file.read(), "utf-8")
            return content
        
        # Handle PDF and DOCX files - Note: Limited support in Streamlit in Snowflake
        elif (file_type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"] 
              or file_name.lower().endswith(('.pdf', '.docx'))):
            
            # Streamlit in Snowflake has restrictions on file operations and stages
            return f"""📄 **PDF/DOCX Upload Not Supported in This Environment**

**File detected:** {file_name} ({file_type})

**Streamlit in Snowflake has limitations on:**
• File stage operations
• PARSE_DOCUMENT function access  
• Temporary file processing

**✅ What you can do instead:**

**Option 1: Copy & Paste Text**
1. Open your PDF/DOCX file 
2. Select and copy the text content
3. Switch to "Text Input" mode
4. Paste the content for analysis

**Option 2: Convert to Text**
1. Save your document as a .txt file
2. Upload the .txt version instead

**Option 3: Use Full Snowflake Environment**  
1. Deploy this app in a full Snowflake environment
2. PARSE_DOCUMENT will work with proper permissions

The **AI analysis features work perfectly** with text input! 🤖✨"""
        
        else:
            # Try reading as text for other file types
            try:
                content = str(uploaded_file.read(), "utf-8")
                if len(content.strip()) > 10:
                    return content
                else:
                    return f"File read as text but content was too short. File type: {file_type}"
            except Exception as text_error:
                return f"Could not process file type '{file_type}'. Error: {str(text_error)}. Please try copy/paste instead."
                
    except Exception as e:
        return f"Error processing file: {str(e)}"

def detect_platforms(content: str) -> List[str]:
    """Detect ML platforms in content"""
    content_lower = content.lower()
    platforms = []
    
    if any(term in content_lower for term in ["sagemaker", "aws sagemaker"]):
        platforms.append("AWS SageMaker")
    if any(term in content_lower for term in ["databricks", "spark", "delta lake"]):
        platforms.append("Databricks")
    if any(term in content_lower for term in ["azure ml", "azure machine learning"]):
        platforms.append("Azure ML")
    if any(term in content_lower for term in ["vertex ai", "google cloud", "gcp"]):
        platforms.append("Google Vertex AI")
    if any(term in content_lower for term in ["excel", "spreadsheet", "manual"]):
        platforms.append("Excel/Manual")
    
    return platforms if platforms else ["Unknown"]

def analyze_content(content: str) -> Dict:
    """Analyze content with Cortex AI"""
    try:
        if len(content) < 50:
            return {
                'summary': "Content too short for analysis",
                'platforms': ["Unknown"],
                'recommendations': "Please provide more detailed information",
                'takeaways': ["Insufficient content"]
            }
        
        # Get summary
        summary_result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SUMMARIZE('{content.replace("'", "''")}') as summary
        """).collect()
        
        # Detect platforms
        platforms = detect_platforms(content)
        
        # Generate recommendations based on platforms
        recommendations = []
        for platform in platforms[:2]:  # Limit to avoid clutter
            if platform == "AWS SageMaker":
                recommendations.extend([
                    "Emphasize unified platform vs stitching AWS services together",
                    "Highlight elimination of data movement costs",
                    "Demo Scene+ success story (66% time reduction)"
                ])
            elif platform == "Databricks":
                recommendations.extend([
                    "Position as Spark-free alternative with predictable pricing", 
                    "Address cluster management complexity",
                    "Share IGS Energy migration success (75% cost savings)"
                ])
            elif platform == "Excel/Manual":
                recommendations.extend([
                    "Recommend ML Functions for easy SQL-based ML",
                    "Show SpartanNash automation success",
                    "Emphasize accuracy improvements (71% → 88%)"
                ])
        
        if not recommendations:
            recommendations = [
                "Conduct platform assessment and use case mapping",
                "Design POC based on highest-impact opportunity",
                "Prepare cost-benefit analysis vs current approach"
            ]
        
        # Generate key takeaways
        takeaways = []
        content_lower = content.lower()
        if "cost" in content_lower or "$" in content:
            takeaways.append("Cost optimization opportunity identified")
        if any(term in content_lower for term in ["complex", "difficult", "challenge"]):
            takeaways.append("Complexity reduction potential")
        if any(term in content_lower for term in ["data movement", "transfer"]):
            takeaways.append("Data movement elimination opportunity")
        
        return {
            'summary': summary_result[0]['SUMMARY'] if summary_result else "Analysis completed",
            'platforms': platforms,
            'recommendations': recommendations,
            'takeaways': takeaways if takeaways else ["ML modernization opportunity"]
        }
        
    except Exception as e:
        return {
            'summary': f"Analysis error: {str(e)}",
            'platforms': ["Unknown"],
            'recommendations': ["Unable to generate recommendations"],
            'takeaways': ["Analysis failed"]
        }

def get_stories(platforms: List[str]) -> List[Dict]:
    """Get relevant customer stories"""
    stories = []
    
    for platform in platforms:
        if "sagemaker" in platform.lower():
            stories.extend(CUSTOMER_STORIES.get("sagemaker", []))
        elif "databricks" in platform.lower():
            stories.extend(CUSTOMER_STORIES.get("databricks", []))
        elif "excel" in platform.lower():
            stories.extend(CUSTOMER_STORIES.get("excel", []))
    
    if not stories:
        stories.extend(CUSTOMER_STORIES.get("general", []))
    
    return stories[:2]  # Limit to 2 stories to reduce clutter

def main():
    # Simple header
    st.markdown('<h1 class="main-header">🤖 ML Workload Discovery Assistant</h1>', unsafe_allow_html=True)
    
    # Check permissions
    permissions_ok, perm_message = check_permissions()
    if not permissions_ok:
        st.error(f"Permission issue: {perm_message}")
        st.info("Contact your Snowflake admin to grant Cortex AI permissions")
        return
    
    # Simple input section
    st.markdown("## 📝 Customer Information")
    
    # Input method selection
    input_method = st.radio("Input method:", ["Text Input", "File Upload"], horizontal=True)
    
    customer_content = ""
    
    if input_method == "Text Input":
        customer_content = st.text_area(
            "Paste customer discovery notes:",
            height=250,
            placeholder="""Example:
Customer: TechCorp Inc.
Current Platform: Databricks on AWS  
Pain Points: $180K/month costs (up from $45K), complex Spark management
Use Cases: Credit risk modeling, fraud detection
Team: 40-person data team, 2 full-time on infrastructure
Timeline: Evaluating alternatives by Q1 2025"""
        )
    
    else:  # File Upload
        uploaded_file = st.file_uploader(
            "Upload document (PDF, TXT, DOCX):",
            type=['txt', 'pdf', 'docx']
        )
        
        if uploaded_file is not None:
            with st.spinner("Processing file..."):
                customer_content = process_uploaded_file(uploaded_file)
                if customer_content and len(customer_content) > 50:
                    st.success(f"✅ Processed: {uploaded_file.name}")
                    # Show first 200 chars as preview
                    st.text(f"Preview: {customer_content[:200]}...")
                else:
                    st.warning("File processed but content may be incomplete")
    
    # Analysis button
    if st.button("🔍 Analyze", type="primary"):
        if customer_content and len(customer_content.strip()) > 10:
            with st.spinner("Analyzing with Cortex AI..."):
                analysis = analyze_content(customer_content)
                
                # Results section
                st.markdown("## 📊 Analysis Results")
                
                # Platform detection
                if analysis["platforms"] != ["Unknown"]:
                    st.markdown("**Platforms Detected:**")
                    platform_html = ""
                    for platform in analysis["platforms"]:
                        platform_html += f'<span class="platform-tag">{platform}</span>'
                    st.markdown(platform_html, unsafe_allow_html=True)
                
                # Key insights
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Key Takeaways:**")
                    for takeaway in analysis["takeaways"]:
                        st.markdown(f"• {takeaway}")
                
                with col2:
                    st.markdown("**Summary:**")
                    st.markdown(f'<div class="content-box">{analysis["summary"]}</div>', unsafe_allow_html=True)
                
                # Recommendations
                st.markdown("**Strategic Recommendations:**")
                for i, rec in enumerate(analysis["recommendations"][:4], 1):
                    st.markdown(f"{i}. {rec}")
                
                # Customer stories
                stories = get_stories(analysis["platforms"])
                if stories:
                    st.markdown("**Success Stories:**")
                    for story in stories:
                        st.markdown(f"""
                        <div class="story-box">
                        <strong>{story["title"]}</strong><br>
                        <em>{story["metrics"]}</em><br>
                        "{story["quote"]}"
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("Please provide customer information to analyze")

if __name__ == "__main__":
    main() 