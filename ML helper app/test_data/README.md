# 🧪 ML Helper App - Test Data Scenarios

This folder contains realistic synthetic customer scenarios for testing the ML Workload Discovery Assistant. Each scenario is designed to showcase different aspects of the application and help AEs practice using the tool.

## 📁 Test Scenarios

### 1. `scenario_1_sagemaker_migration.txt`
**AWS SageMaker Migration Challenge**
- **Customer**: Global Manufacturing Corp ($2.3B revenue)
- **Current Platform**: AWS SageMaker
- **Key Pain Points**: Data movement costs ($40K/month), complex setup (2-3 weeks), poor collaboration
- **Use Cases**: Predictive maintenance, quality control AI, supply chain forecasting
- **Decision Driver**: Need 50% reduction in operational overhead

**Expected App Response:**
- Should identify SageMaker displacement opportunity
- Recommend Snowflake ML unified platform
- Reference Scene+ and Cloudbeds customer stories
- Provide cost savings estimates
- Suggest POC with predictive maintenance use case

---

### 2. `scenario_2_databricks_costs.txt`
**Databricks Cost Explosion Crisis**
- **Customer**: TechStart Financial Services (Fintech startup)
- **Current Platform**: Databricks Premium on AWS
- **Key Pain Points**: Cost explosion ($45K→$180K/month), Spark complexity, unpredictable pricing
- **Use Cases**: Credit risk modeling, fraud detection, customer lifetime value
- **Decision Driver**: Board mandate to reduce infrastructure costs by 40%

**Expected App Response:**
- Should identify Databricks displacement opportunity
- Highlight Spark complexity vs. Snowflake simplicity
- Reference IGS Energy, Decile, and Spark New Zealand stories
- Emphasize cost transparency and predictability
- Suggest quick wins with ML Functions for simpler use cases

---

### 3. `scenario_3_retail_forecasting.txt`
**Simple Retail Forecasting (ML Functions Perfect Fit)**
- **Customer**: Alpine Outdoor Retail ($120M regional retailer)
- **Current Platform**: Excel spreadsheets
- **Key Pain Points**: Manual forecasting (40 hrs/week), 65% accuracy, seasonal miscalculations
- **Use Cases**: Demand forecasting, inventory optimization, weather-based adjustments
- **Decision Driver**: Need implementation in <30 days, <$50K budget

**Expected App Response:**
- Should recommend ML Functions as perfect fit
- Reference SpartanNash success story (71%→88% accuracy)
- Emphasize quick implementation and business user friendliness
- Suggest integration with existing Snowflake/Tableau setup
- Provide ROI calculations for inventory optimization

---

### 4. `audio_transcript_sample.txt`
**Healthcare AI Platform Migration (Audio Transcript)**
- **Customer**: Healthcare AI Company (medical imaging)
- **Current Platform**: Google Vertex AI
- **Key Pain Points**: High costs ($120K/month), 6-week deployment cycles, poor cost transparency
- **Use Cases**: Medical image analysis, computer vision models, HIPAA compliance
- **Decision Driver**: Need 30% cost reduction + faster deployment

**Expected App Response:**
- Should identify Google Vertex AI displacement opportunity
- Highlight governance and compliance advantages
- Reference healthcare/regulated industry examples
- Emphasize unified platform benefits
- Address HIPAA compliance requirements

## 🎯 How to Use Test Scenarios

### For AE Training:
1. **Upload each scenario** to the ML Helper App
2. **Review AI recommendations** for accuracy and relevance
3. **Practice discovery questions** suggested by the app
4. **Compare recommendations** across different customer situations

### For App Testing:
1. **Text Input**: Copy/paste scenario content directly
2. **File Upload**: Save scenarios as .txt files and upload
3. **Audio Simulation**: Use the audio transcript as sample transcribed content

### Expected Outcomes:
- ✅ **Competitive Analysis**: Accurate identification of current platform challenges
- ✅ **Customer Stories**: Relevant reference stories from knowledge base
- ✅ **Strategic Recommendations**: Appropriate next steps and discovery questions
- ✅ **ROI Projections**: Business case calculations based on customer metrics
- ✅ **Discovery Questions**: Relevant follow-up questions for each scenario

## 🧬 Scenario Design Principles

Each test scenario includes:
- **Realistic company profiles** with specific revenue, team size, and industry context
- **Detailed pain points** that map to Snowflake competitive advantages
- **Quantified business impact** to enable ROI calculations
- **Specific technical requirements** that demonstrate Snowflake ML capabilities
- **Decision timelines and criteria** to drive urgency and next steps
- **Direct customer quotes** for authenticity and emotional resonance

## 📊 Success Metrics

The app should demonstrate:
1. **Accurate Platform Identification** (SageMaker, Databricks, Vertex AI, Excel)
2. **Relevant Customer Story Matching** (based on use case and industry)
3. **Competitive Positioning** (highlighting specific advantages vs. current platform)
4. **Quantified Value Proposition** (cost savings, performance improvements)
5. **Actionable Next Steps** (discovery questions, POC suggestions, timeline)

## 🔄 Updating Test Scenarios

To add new scenarios:
1. Follow the existing format and structure
2. Include quantified pain points and success metrics
3. Map to specific Snowflake ML capabilities
4. Reference real customer stories from the knowledge base
5. Update this README with scenario details

These scenarios are designed to be comprehensive test cases that validate the full capability of the ML Helper App while providing realistic training scenarios for Snowflake AEs. 