import streamlit as st
import pandas as pd
import snowflake.connector
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit
import uuid
import json
import base64
from datetime import datetime
from typing import Dict, List, Optional, Union
import streamlit_lottie
from streamlit_pills import pills
import requests

# Page configuration
st.set_page_config(
    page_title="ML Workload Discovery Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
        color: #2c5aa0;
        margin-bottom: 1rem;
    }
    .highlight-box {
        background-color: #f0f7ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #29b5e8;
        margin: 20px 0;
    }
    .metric-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .recommendation-box {
        background-color: #f8fff0;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #52c41a;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff7e6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #fa8c16;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class SnowflakeConnection:
    """Handle Snowflake connection and queries"""
    
    def __init__(self):
        self.session = None
        self.connect()
    
    def connect(self):
        """Establish Snowflake connection"""
        try:
            # Use Snowflake connection from secrets or environment
            connection_params = st.secrets.get("snowflake", {})
            if connection_params:
                self.session = Session.builder.configs(connection_params).create()
            else:
                st.error("❄️ Snowflake connection not configured. Please check your secrets.")
                return None
            
            # Set context
            self.session.sql("USE DATABASE ML_HELPER_APP").collect()
            self.session.sql("USE SCHEMA CORE").collect()
            
        except Exception as e:
            st.error(f"❄️ Failed to connect to Snowflake: {str(e)}")
            return None
    
    def execute_query(self, query: str, params: Dict = None):
        """Execute a Snowflake query"""
        try:
            if params:
                # Handle parameterized queries
                for key, value in params.items():
                    if isinstance(value, str):
                        query = query.replace(f":{key}", f"'{value}'")
                    else:
                        query = query.replace(f":{key}", str(value))
            
            result = self.session.sql(query).collect()
            return result
        except Exception as e:
            st.error(f"Query execution failed: {str(e)}")
            return None

class DocumentProcessor:
    """Handle document parsing and AI processing"""
    
    def __init__(self, snowflake_session):
        self.session = snowflake_session
    
    def parse_document(self, file_content: bytes, file_type: str) -> str:
        """Parse document using Snowflake Cortex PARSE_DOCUMENT"""
        try:
            # Convert file to base64 for Snowflake
            file_b64 = base64.b64encode(file_content).decode('utf-8')
            
            query = f"""
            SELECT PARSE_DOCUMENT(
                to_binary('{file_b64}', 'BASE64'),
                '{file_type.upper()}'
            ) as parsed_content
            """
            
            result = self.session.execute_query(query)
            if result and len(result) > 0:
                return result[0]['PARSED_CONTENT']
            return ""
            
        except Exception as e:
            st.error(f"Document parsing failed: {str(e)}")
            return ""
    
    def transcribe_audio(self, audio_content: bytes) -> str:
        """Transcribe audio using Snowflake Cortex AI_TRANSCRIBE"""
        try:
            # Convert audio to base64
            audio_b64 = base64.b64encode(audio_content).decode('utf-8')
            
            query = f"""
            SELECT AI_TRANSCRIBE(
                to_binary('{audio_b64}', 'BASE64')
            ) as transcribed_content
            """
            
            result = self.session.execute_query(query)
            if result and len(result) > 0:
                return result[0]['TRANSCRIBED_CONTENT']
            return ""
            
        except Exception as e:
            st.error(f"Audio transcription failed: {str(e)}")
            return ""

class AIAnalyzer:
    """Generate AI analysis and recommendations"""
    
    def __init__(self, snowflake_session):
        self.session = snowflake_session
    
    def classify_content(self, content: str) -> Dict:
        """Classify content to understand ML workload types"""
        try:
            classes = [
                "Data Engineering", "Machine Learning Training", "Model Inference", 
                "MLOps", "Data Science", "Analytics", "Real-time Processing",
                "Computer Vision", "NLP", "Recommendation Systems"
            ]
            
            query = f"""
            SELECT AI_CLASSIFY(
                '{content.replace("'", "''")}',
                ARRAY_CONSTRUCT({', '.join([f"'{c}'" for c in classes])})
            ) as classification
            """
            
            result = self.session.execute_query(query)
            if result and len(result) > 0:
                return json.loads(result[0]['CLASSIFICATION'])
            return {}
            
        except Exception as e:
            st.error(f"Content classification failed: {str(e)}")
            return {}
    
    def summarize_content(self, content: str) -> str:
        """Summarize content using Snowflake Cortex"""
        try:
            query = f"""
            SELECT SUMMARIZE('{content.replace("'", "''")}') as summary
            """
            
            result = self.session.execute_query(query)
            if result and len(result) > 0:
                return result[0]['SUMMARY']
            return ""
            
        except Exception as e:
            st.error(f"Content summarization failed: {str(e)}")
            return ""
    
    def generate_recommendations(self, customer_data: Dict, reference_knowledge: str) -> Dict:
        """Generate comprehensive recommendations using AI_COMPLETE"""
        
        prompt = f"""
        You are an expert Snowflake sales consultant helping an Account Executive win ML workloads.
        
        CUSTOMER INFORMATION:
        {json.dumps(customer_data, indent=2)}
        
        REFERENCE KNOWLEDGE (Success Stories & Best Practices):
        {reference_knowledge}
        
        Based on this information, provide a comprehensive analysis in the following JSON format:
        {{
            "executive_summary": "Brief 3-sentence summary of the opportunity",
            "competitive_analysis": {{
                "current_platforms": ["list of identified competing platforms"],
                "snowflake_advantages": ["specific advantages Snowflake offers"],
                "competitive_risks": ["potential obstacles or risks"]
            }},
            "compute_upside": {{
                "estimated_workloads": "Description of ML workloads that could move to Snowflake",
                "potential_compute_increase": "Estimated percentage increase in compute usage",
                "revenue_opportunity": "Qualitative assessment of revenue potential"
            }},
            "strategy": {{
                "short_term": ["immediate next steps (30-90 days)"],
                "long_term": ["strategic initiatives (6-12 months)"]
            }},
            "discovery_questions": ["key questions to ask in next customer conversation"],
            "poc_recommendations": ["specific proof-of-concept ideas"],
            "risks_to_avoid": ["things to be careful about or avoid"]
        }}
        
        Be specific, actionable, and grounded in Snowflake's ML capabilities. Reference similar customer success stories where relevant.
        """
        
        try:
            query = f"""
            SELECT AI_COMPLETE(
                'llama3-8b',
                '{prompt.replace("'", "''")}',
                {{
                    'temperature': 0.3,
                    'max_tokens': 2000
                }}
            ) as recommendations
            """
            
            result = self.session.execute_query(query)
            if result and len(result) > 0:
                response = result[0]['RECOMMENDATIONS']
                try:
                    return json.loads(response)
                except:
                    # If JSON parsing fails, return structured text
                    return {"raw_response": response}
            return {}
            
        except Exception as e:
            st.error(f"AI recommendation generation failed: {str(e)}")
            return {}

def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def main():
    """Main application function"""
    
    # Initialize session state
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    
    # Header with Lottie animation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🤖 ML Workload Discovery Assistant</h1>', 
                   unsafe_allow_html=True)
        
        # Load Lottie animation
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"
        lottie_json = load_lottie_url(lottie_url)
        if lottie_json:
            streamlit_lottie.st_lottie(lottie_json, height=150, key="header_animation")
    
    st.markdown("### Help Account Executives discover and capture ML workloads 🎯")
    
    # Initialize Snowflake connection
    snowflake_conn = SnowflakeConnection()
    if not snowflake_conn.session:
        st.stop()
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("### 📋 Navigation")
        
        # Use pills for navigation
        nav_options = ["📁 Upload & Input", "🔍 Analysis", "📊 Report", "⚙️ Settings"]
        selected_nav = pills("Select Section:", nav_options, ["📁", "🔍", "📊", "⚙️"])
        
        st.markdown("---")
        st.markdown("### 📈 Session Info")
        st.info(f"**Session ID:** `{st.session_state.session_id[:8]}...`")
        st.info(f"**Started:** {datetime.now().strftime('%H:%M:%S')}")
    
    # Main content based on navigation
    if selected_nav == "📁 Upload & Input":
        show_upload_section(snowflake_conn)
    elif selected_nav == "🔍 Analysis":
        show_analysis_section(snowflake_conn)
    elif selected_nav == "📊 Report":
        show_report_section(snowflake_conn)
    elif selected_nav == "⚙️ Settings":
        show_settings_section()

def show_upload_section(snowflake_conn):
    """Display the upload and input section"""
    
    st.markdown('<h2 class="sub-header">📁 Upload Customer Information</h2>', 
               unsafe_allow_html=True)
    
    # Customer profile form
    with st.expander("🏢 Customer Profile Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name", placeholder="e.g., Acme Corp")
            industry = st.selectbox("Industry", [
                "Technology", "Financial Services", "Healthcare", "Retail", 
                "Manufacturing", "Media & Entertainment", "Transportation", "Other"
            ])
            company_size = st.selectbox("Company Size", [
                "Startup (1-50)", "Small (51-200)", "Medium (201-1000)", 
                "Large (1001-5000)", "Enterprise (5000+)"
            ])
        
        with col2:
            ml_maturity = st.selectbox("ML Maturity Level", [
                "Just Starting", "Experimenting", "Production Pilots", 
                "Scaled Production", "ML-First Organization"
            ])
            
            # Multi-select for current platforms
            current_platforms = st.multiselect("Current ML/Data Platforms", [
                "AWS SageMaker", "Azure ML", "Google Cloud AI", "Databricks",
                "DataRobot", "H2O.ai", "Apache Spark", "Kubernetes", "On-Premise"
            ])
            
            use_cases = st.multiselect("Primary ML Use Cases", [
                "Fraud Detection", "Recommendation Systems", "Predictive Analytics",
                "Computer Vision", "NLP/Text Analytics", "Forecasting",
                "Customer Segmentation", "Risk Assessment", "Real-time Inference"
            ])
    
    # File upload section
    st.markdown('<h3 class="sub-header">📄 Upload Customer Documents/Notes</h3>', 
               unsafe_allow_html=True)
    
    # Upload tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Documents", "🎵 Audio", "📝 Text Input", "🔗 URLs"])
    
    with tab1:
        uploaded_files = st.file_uploader(
            "Upload PDFs or Word Documents",
            type=['pdf', 'docx'],
            accept_multiple_files=True,
            help="Upload customer meeting notes, technical documents, or proposals"
        )
        
        if uploaded_files:
            process_uploaded_files(uploaded_files, snowflake_conn)
    
    with tab2:
        audio_file = st.file_uploader(
            "Upload Audio Recording",
            type=['mp3'],
            help="Upload customer call recordings for transcription"
        )
        
        if audio_file:
            process_audio_file(audio_file, snowflake_conn)
    
    with tab3:
        text_input = st.text_area(
            "Paste Meeting Notes or Customer Information",
            height=200,
            placeholder="Paste any relevant customer information, meeting notes, or technical discussions here..."
        )
        
        if text_input and st.button("Process Text Input"):
            process_text_input(text_input, snowflake_conn)
    
    with tab4:
        url_input = st.text_input(
            "Customer Website or Documentation URLs",
            placeholder="https://example.com/technical-docs"
        )
        if url_input and st.button("Analyze URL"):
            st.info("URL analysis feature coming soon!")
    
    # Save customer profile
    if st.button("💾 Save Customer Profile", type="primary"):
        save_customer_profile(snowflake_conn, {
            'company_name': company_name,
            'industry': industry,
            'company_size': company_size,
            'ml_maturity': ml_maturity,
            'current_platforms': current_platforms,
            'use_cases': use_cases
        })

def process_uploaded_files(files, snowflake_conn):
    """Process uploaded document files"""
    processor = DocumentProcessor(snowflake_conn)
    
    for file in files:
        with st.spinner(f"Processing {file.name}..."):
            # Read file content
            file_content = file.read()
            file_type = file.type.split('/')[-1]
            
            # Parse document
            parsed_content = processor.parse_document(file_content, file_type)
            
            if parsed_content:
                # Save to database
                upload_id = str(uuid.uuid4())
                query = """
                INSERT INTO CUSTOMER_UPLOADS 
                (upload_id, session_id, file_name, file_type, original_content, parsed_content)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                snowflake_conn.execute_query(query, {
                    'upload_id': upload_id,
                    'session_id': st.session_state.session_id,
                    'file_name': file.name,
                    'file_type': file_type,
                    'original_content': str(file_content),
                    'parsed_content': parsed_content
                })
                
                st.success(f"✅ Successfully processed {file.name}")
                
                # Show preview
                with st.expander(f"Preview: {file.name}"):
                    st.text_area("Parsed Content", parsed_content[:1000] + "...", height=150)
            else:
                st.error(f"❌ Failed to process {file.name}")

def process_audio_file(audio_file, snowflake_conn):
    """Process uploaded audio file"""
    processor = DocumentProcessor(snowflake_conn)
    
    with st.spinner(f"Transcribing {audio_file.name}..."):
        # Read audio content
        audio_content = audio_file.read()
        
        # Transcribe audio
        transcribed_content = processor.transcribe_audio(audio_content)
        
        if transcribed_content:
            # Save to database
            upload_id = str(uuid.uuid4())
            query = """
            INSERT INTO CUSTOMER_UPLOADS 
            (upload_id, session_id, file_name, file_type, transcribed_content)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            snowflake_conn.execute_query(query, {
                'upload_id': upload_id,
                'session_id': st.session_state.session_id,
                'file_name': audio_file.name,
                'file_type': 'mp3',
                'transcribed_content': transcribed_content
            })
            
            st.success(f"✅ Successfully transcribed {audio_file.name}")
            
            # Show preview
            with st.expander(f"Transcription: {audio_file.name}"):
                st.text_area("Transcribed Content", transcribed_content[:1000] + "...", height=150)
        else:
            st.error(f"❌ Failed to transcribe {audio_file.name}")

def process_text_input(text, snowflake_conn):
    """Process text input"""
    upload_id = str(uuid.uuid4())
    query = """
    INSERT INTO CUSTOMER_UPLOADS 
    (upload_id, session_id, file_name, file_type, parsed_content)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    snowflake_conn.execute_query(query, {
        'upload_id': upload_id,
        'session_id': st.session_state.session_id,
        'file_name': 'Text Input',
        'file_type': 'text',
        'parsed_content': text
    })
    
    st.success("✅ Text input saved successfully!")

def save_customer_profile(snowflake_conn, profile_data):
    """Save customer profile to database"""
    query = """
    INSERT INTO CUSTOMER_PROFILES 
    (session_id, company_name, industry, company_size, current_ml_maturity, 
     current_platforms, use_cases, pain_points)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    snowflake_conn.execute_query(query, {
        'session_id': st.session_state.session_id,
        **profile_data,
        'pain_points': []  # Will be extracted from content analysis
    })
    
    st.success("✅ Customer profile saved successfully!")

def show_analysis_section(snowflake_conn):
    """Display the AI analysis section"""
    st.markdown('<h2 class="sub-header">🔍 AI Analysis & Insights</h2>', 
               unsafe_allow_html=True)
    
    if st.button("🚀 Run Complete Analysis", type="primary"):
        run_complete_analysis(snowflake_conn)

def run_complete_analysis(snowflake_conn):
    """Run the complete AI analysis pipeline"""
    analyzer = AIAnalyzer(snowflake_conn)
    
    # Get customer data
    customer_query = f"""
    SELECT * FROM CUSTOMER_PROFILES 
    WHERE session_id = '{st.session_state.session_id}'
    ORDER BY created_at DESC LIMIT 1
    """
    customer_data = snowflake_conn.execute_query(customer_query)
    
    # Get uploaded content
    content_query = f"""
    SELECT parsed_content, transcribed_content 
    FROM CUSTOMER_UPLOADS 
    WHERE session_id = '{st.session_state.session_id}'
    """
    content_data = snowflake_conn.execute_query(content_query)
    
    if not customer_data or not content_data:
        st.warning("⚠️ Please upload customer information and documents first.")
        return
    
    # Combine all content
    all_content = ""
    for row in content_data:
        if row['PARSED_CONTENT']:
            all_content += row['PARSED_CONTENT'] + "\n"
        if row['TRANSCRIBED_CONTENT']:
            all_content += row['TRANSCRIBED_CONTENT'] + "\n"
    
    # Get reference knowledge (this would be loaded from the PDF files you'll provide)
    reference_knowledge = get_reference_knowledge(snowflake_conn)
    
    with st.spinner("🤖 Analyzing customer data and generating recommendations..."):
        # Classify content
        classification = analyzer.classify_content(all_content)
        
        # Summarize content
        summary = analyzer.summarize_content(all_content)
        
        # Generate recommendations
        customer_info = {
            'profile': customer_data[0] if customer_data else {},
            'content_summary': summary,
            'content_classification': classification,
            'full_content': all_content[:2000]  # Truncate for token limits
        }
        
        recommendations = analyzer.generate_recommendations(customer_info, reference_knowledge)
        
        # Save analysis results
        save_analysis_results(snowflake_conn, recommendations)
        
        st.session_state.analysis_complete = True
        st.success("✅ Analysis complete! Check the Report section for detailed recommendations.")

def get_reference_knowledge(snowflake_conn):
    """Get reference knowledge from database"""
    query = """
    SELECT content FROM REFERENCE_KNOWLEDGE 
    WHERE document_type IN ('customer_stories', 'ae_training')
    """
    
    result = snowflake_conn.execute_query(query)
    if result:
        return "\n".join([row['CONTENT'] for row in result])
    return "Reference knowledge not yet loaded."

def save_analysis_results(snowflake_conn, recommendations):
    """Save analysis results to database"""
    analysis_id = str(uuid.uuid4())
    
    query = """
    INSERT INTO AI_ANALYSIS_RESULTS 
    (analysis_id, session_id, analysis_type, ai_response)
    VALUES (%s, %s, %s, %s)
    """
    
    snowflake_conn.execute_query(query, {
        'analysis_id': analysis_id,
        'session_id': st.session_state.session_id,
        'analysis_type': 'complete_analysis',
        'ai_response': json.dumps(recommendations)
    })

def show_report_section(snowflake_conn):
    """Display the generated report"""
    st.markdown('<h2 class="sub-header">📊 Customer Analysis Report</h2>', 
               unsafe_allow_html=True)
    
    if not st.session_state.analysis_complete:
        st.info("📋 Please complete the analysis first in the Analysis section.")
        return
    
    # Get analysis results
    query = f"""
    SELECT ai_response FROM AI_ANALYSIS_RESULTS 
    WHERE session_id = '{st.session_state.session_id}'
    ORDER BY created_at DESC LIMIT 1
    """
    
    result = snowflake_conn.execute_query(query)
    if not result:
        st.error("No analysis results found.")
        return
    
    try:
        recommendations = json.loads(result[0]['AI_RESPONSE'])
        display_comprehensive_report(recommendations)
    except:
        st.error("Error parsing analysis results.")

def display_comprehensive_report(recommendations):
    """Display the comprehensive analysis report"""
    
    # Executive Summary
    if 'executive_summary' in recommendations:
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.markdown("### 📋 Executive Summary")
        st.markdown(recommendations['executive_summary'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Metrics overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📈 Compute Upside",
            value="High Potential",
            delta="Est. 30-50% increase"
        )
    
    with col2:
        st.metric(
            label="🎯 Win Probability",
            value="75%",
            delta="With proper strategy"
        )
    
    with col3:
        st.metric(
            label="⏱️ Timeline",
            value="6-9 months",
            delta="To full adoption"
        )
    
    # Detailed sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Competitive Analysis
        if 'competitive_analysis' in recommendations:
            st.markdown("### 🏆 Competitive Analysis")
            comp_analysis = recommendations['competitive_analysis']
            
            if 'current_platforms' in comp_analysis:
                st.markdown("**Current Platforms:**")
                for platform in comp_analysis['current_platforms']:
                    st.markdown(f"• {platform}")
            
            if 'snowflake_advantages' in comp_analysis:
                st.markdown("**Snowflake Advantages:**")
                for advantage in comp_analysis['snowflake_advantages']:
                    st.markdown(f"✅ {advantage}")
        
        # Strategy
        if 'strategy' in recommendations:
            st.markdown("### 🎯 Strategy & Next Steps")
            strategy = recommendations['strategy']
            
            if 'short_term' in strategy:
                st.markdown("**Short-term (30-90 days):**")
                for step in strategy['short_term']:
                    st.markdown(f"🔥 {step}")
            
            if 'long_term' in strategy:
                st.markdown("**Long-term (6-12 months):**")
                for step in strategy['long_term']:
                    st.markdown(f"🚀 {step}")
    
    with col2:
        # Compute Upside
        if 'compute_upside' in recommendations:
            st.markdown("### 💰 Compute Upside Analysis")
            compute = recommendations['compute_upside']
            
            for key, value in compute.items():
                st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
        
        # Discovery Questions
        if 'discovery_questions' in recommendations:
            st.markdown("### ❓ Discovery Questions")
            for question in recommendations['discovery_questions']:
                st.markdown(f"• {question}")
    
    # POC Recommendations
    if 'poc_recommendations' in recommendations:
        st.markdown("### 🧪 POC Recommendations")
        for i, poc in enumerate(recommendations['poc_recommendations'], 1):
            st.markdown(f'<div class="recommendation-box">', unsafe_allow_html=True)
            st.markdown(f"**POC {i}:** {poc}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Risks to Avoid
    if 'risks_to_avoid' in recommendations:
        st.markdown("### ⚠️ Risks to Avoid")
        for risk in recommendations['risks_to_avoid']:
            st.markdown(f'<div class="warning-box">', unsafe_allow_html=True)
            st.markdown(f"⚠️ {risk}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Export options
    st.markdown("### 📤 Export Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export as PDF"):
            st.info("PDF export feature coming soon!")
    
    with col2:
        if st.button("📊 Export to PowerPoint"):
            st.info("PowerPoint export feature coming soon!")
    
    with col3:
        if st.button("📧 Email Report"):
            st.info("Email feature coming soon!")

def show_settings_section():
    """Display settings and configuration"""
    st.markdown('<h2 class="sub-header">⚙️ Settings & Configuration</h2>', 
               unsafe_allow_html=True)
    
    st.markdown("### 🔧 Application Settings")
    
    # AI Model Settings
    with st.expander("🤖 AI Model Configuration"):
        model_choice = st.selectbox(
            "AI Model for Analysis",
            ["llama3-8b", "llama3-70b", "mistral-large"]
        )
        
        temperature = st.slider(
            "Response Creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1
        )
    
    # Data Management
    with st.expander("🗄️ Data Management"):
        if st.button("🗑️ Clear Session Data"):
            st.session_state.clear()
            st.success("Session data cleared!")
        
        if st.button("📊 View Database Stats"):
            st.info("Database statistics feature coming soon!")
    
    # About
    with st.expander("ℹ️ About this Application"):
        st.markdown("""
        **ML Workload Discovery Assistant** v1.0
        
        This application helps Snowflake Account Executives discover and analyze 
        customer ML workloads to identify opportunities for Snowflake adoption.
        
        **Features:**
        - Document parsing and audio transcription
        - AI-powered analysis using Snowflake Cortex
        - Competitive analysis and strategy recommendations
        - Comprehensive reporting
        
        **Built with:**
        - Streamlit
        - Snowflake Cortex AI
        - Snowpark Python
        """)

if __name__ == "__main__":
    main() 