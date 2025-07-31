# 🤖 ML Workload Discovery Assistant

A powerful Streamlit application built for Snowflake Account Executives to discover and analyze customer ML workloads, providing AI-powered recommendations for capturing ML opportunities.

## 🎯 Overview

This application helps Snowflake AEs:
- **Discover** ML workloads customers run outside Snowflake
- **Analyze** competitive positioning and opportunities
- **Generate** strategic recommendations and next steps
- **Create** compelling POC proposals and migration strategies

## 🚀 Features

### Core Functionality
- **Multi-format Upload**: PDFs, Word docs, MP3 audio files, and text input
- **AI-Powered Analysis**: Uses Snowflake Cortex AI for document parsing, transcription, and analysis
- **Competitive Intelligence**: Compares current platforms against Snowflake advantages
- **Strategic Recommendations**: Short-term and long-term strategies tailored to customer profile
- **POC Suggestions**: Specific proof-of-concept ideas based on customer needs

### Technical Capabilities
- **Document Processing**: PARSE_DOCUMENT for PDFs and Word docs
- **Audio Transcription**: AI_TRANSCRIBE for customer call recordings
- **Content Analysis**: AI_CLASSIFY and SUMMARIZE for intelligent content processing
- **Report Generation**: AI_COMPLETE for comprehensive recommendations

### User Experience
- **Interactive UI**: Streamlit Pills for navigation, Lottie animations
- **Professional Reports**: Structured output with executive summary, competitive analysis, and action items
- **Session Management**: Track multiple customer analyses
- **Export Options**: PDF and PowerPoint export capabilities (planned)

## 📋 Prerequisites

### Snowflake Requirements
- Snowflake account with Cortex AI enabled
- Access to the following Cortex functions:
  - `PARSE_DOCUMENT`
  - `AI_TRANSCRIBE` (preview feature)
  - `AI_COMPLETE`
  - `AI_CLASSIFY`
  - `SUMMARIZE`
- Appropriate role with permissions to create databases and tables

### Development Environment
- Python 3.8+
- Streamlit
- Snowflake Connector for Python
- Snowpark Python

## 🛠️ Installation & Setup

### 1. Clone and Install Dependencies

```bash
# Clone the repository
git clone <repository_url>
cd ml-helper-app

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Set Up Snowflake Environment

```sql
-- Run the setup script in your Snowflake environment
-- This creates the database, schema, and tables
@setup_snowflake_schema.sql
```

### 3. Configure Snowflake Connection

Create `.streamlit/secrets.toml` with your Snowflake credentials:

```toml
[snowflake]
account = "your_account.region"
user = "your_username"
password = "your_password"
role = "SYSADMIN"
warehouse = "COMPUTE_WH"
database = "ML_HELPER_APP"
schema = "CORE"
```

### 4. Load Reference Knowledge Base

```bash
# Run the data loader to populate reference materials
python load_reference_data.py
```

**Note**: Update the data loader with actual content from your PDF files.

### 5. Launch the Application

```bash
streamlit run ml_helper_app.py
```

## 📖 Usage Guide

### Step 1: Customer Profile Setup
1. Open the application
2. Navigate to "📁 Upload & Input" 
3. Fill out the customer profile form:
   - Company information
   - Industry and size
   - Current ML maturity level
   - Existing platforms and use cases

### Step 2: Upload Customer Data
Choose from multiple input methods:
- **Documents**: Upload PDFs or Word documents (meeting notes, technical docs)
- **Audio**: Upload MP3 files of customer calls for transcription
- **Text**: Paste meeting notes or customer information directly
- **URLs**: Analyze customer websites or technical documentation (coming soon)

### Step 3: AI Analysis
1. Navigate to "🔍 Analysis"
2. Click "🚀 Run Complete Analysis"
3. The system will:
   - Parse and transcribe uploaded content
   - Classify ML workload types
   - Generate competitive analysis
   - Create strategic recommendations

### Step 4: Review Report
1. Navigate to "📊 Report" 
2. Review the comprehensive analysis including:
   - **Executive Summary**: High-level opportunity assessment
   - **Competitive Analysis**: Current platforms vs. Snowflake advantages
   - **Compute Upside**: Potential revenue opportunity
   - **Strategy**: Short-term and long-term recommendations
   - **Discovery Questions**: Key questions for next customer conversation
   - **POC Recommendations**: Specific proof-of-concept ideas
   - **Risk Mitigation**: Things to avoid or be careful about

## 🏗️ Architecture

### Data Flow
1. **Input Processing**: Documents parsed via PARSE_DOCUMENT, audio via AI_TRANSCRIBE
2. **Content Analysis**: AI_CLASSIFY identifies ML workload types, SUMMARIZE extracts key insights
3. **Recommendation Engine**: AI_COMPLETE generates structured recommendations using reference knowledge
4. **Report Generation**: Structured output with actionable insights

### Database Schema
- **REFERENCE_KNOWLEDGE**: Customer success stories and AE training materials
- **CUSTOMER_UPLOADS**: Uploaded documents and transcriptions
- **CUSTOMER_PROFILES**: Customer information and characteristics
- **AI_ANALYSIS_RESULTS**: AI-generated analysis and recommendations
- **CUSTOMER_REPORTS**: Final structured reports

### AI Integration
- **Model**: Uses Llama 3-8b for analysis (configurable)
- **Temperature**: 0.3 for consistent, focused responses
- **Context**: Combines customer data with reference knowledge for accurate recommendations

## 🎛️ Configuration

### AI Model Settings
- Adjust model choice in Settings section
- Configure response creativity (temperature)
- Customize analysis focus areas

### Reference Knowledge Base
- Update customer success stories
- Modify competitive analysis templates
- Add new industry-specific use cases

## 🔧 Customization

### Adding New Document Types
1. Extend `DocumentProcessor` class
2. Add new file type handling in upload section
3. Update UI to support new formats

### Enhancing AI Analysis
1. Modify prompts in `AIAnalyzer.generate_recommendations()`
2. Add new analysis types (e.g., technical feasibility)
3. Customize output structure for specific needs

### UI Enhancements
1. Add new Streamlit components
2. Customize CSS styling
3. Integrate additional Lottie animations

## 📊 Sample Output

The application generates structured reports with:

```
📋 Executive Summary
Brief assessment of ML opportunity and strategic fit

🏆 Competitive Analysis  
• Current Platforms: AWS SageMaker, Databricks
• Snowflake Advantages: Unified platform, better governance
• Competitive Risks: Existing investments, team expertise

💰 Compute Upside Analysis
• Estimated Workloads: Data engineering + ML training
• Potential Increase: 30-50% compute growth
• Revenue Opportunity: High - enterprise ML expansion

🎯 Strategy & Next Steps
Short-term (30-90 days):
🔥 Schedule technical deep-dive on current architecture
🔥 Propose data consolidation POC

Long-term (6-12 months):
🚀 Full ML pipeline migration
🚀 Cortex AI adoption for new use cases

❓ Discovery Questions
• What's your current ML model deployment process?
• How do you handle data governance across platforms?
• What are your biggest ML infrastructure pain points?

🧪 POC Recommendations
POC 1: Data consolidation from multiple sources
POC 2: Cortex AI for existing model enhancement
POC 3: Real-time inference pipeline migration

⚠️ Risks to Avoid
⚠️ Don't undersell existing team expertise
⚠️ Address data migration concerns early
⚠️ Ensure competitive pricing discussion
```

## 🔍 Troubleshooting

### Common Issues

**Connection Errors**
- Verify Snowflake credentials in secrets.toml
- Check network connectivity and firewall settings
- Ensure proper role permissions

**Cortex AI Function Errors**
- Verify Cortex AI is enabled in your Snowflake account
- Check function availability: `SELECT SYSTEM$GET_CORTEX_AI_AVAILABILITY()`
- Ensure you have proper permissions to use AI functions

**Upload/Processing Issues**
- Check file size limits (recommend <10MB per file)
- Verify supported file formats (PDF, DOCX, MP3)
- Review error logs in Streamlit interface

**Performance Issues**
- Use appropriate warehouse size for AI processing
- Consider splitting large documents into smaller sections
- Monitor Snowflake credits usage

## 🛡️ Security & Privacy

- All data is processed within your Snowflake environment
- No external API calls for AI processing
- Customer data remains in your secure Snowflake account
- Follow your organization's data governance policies

## 🚀 Future Enhancements

### Planned Features
- **Export Capabilities**: PDF and PowerPoint report generation
- **Email Integration**: Direct report sharing
- **Advanced Analytics**: ROI calculators and timeline predictions
- **Integration APIs**: CRM and sales tool connectivity
- **Mobile Optimization**: Responsive design for mobile access

### Potential Additions
- **Real-time Collaboration**: Multi-user session support
- **Advanced Visualizations**: Interactive charts and graphs
- **Template Library**: Industry-specific analysis templates
- **Automated Follow-up**: Scheduled reminder and progress tracking

## 📞 Support

For technical support or feature requests:
1. Check the troubleshooting section above
2. Review Snowflake Cortex AI documentation
3. Contact your Snowflake support team for account-specific issues

## 📄 License

This project is proprietary software for Snowflake internal use.

---

**Built with ❄️ Snowflake Cortex AI and ⚡ Streamlit** 