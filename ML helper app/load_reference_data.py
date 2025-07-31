"""
Reference Data Loader for ML Helper App
This script loads the reference knowledge base from PDF files into Snowflake
"""

import snowflake.connector
from snowflake.snowpark import Session
import uuid
import json
from datetime import datetime
import base64

class ReferenceDataLoader:
    """Load reference knowledge data into Snowflake"""
    
    def __init__(self, connection_params):
        self.session = Session.builder.configs(connection_params).create()
        self.session.sql("USE DATABASE ML_HELPER_APP").collect()
        self.session.sql("USE SCHEMA CORE").collect()
    
    def parse_pdf_with_cortex(self, file_path: str) -> str:
        """Parse PDF using Snowflake Cortex PARSE_DOCUMENT"""
        try:
            # Read and encode PDF file
            with open(file_path, 'rb') as file:
                pdf_content = file.read()
                pdf_b64 = base64.b64encode(pdf_content).decode('utf-8')
            
            # Use Cortex to parse the document
            query = f"""
            SELECT PARSE_DOCUMENT(
                to_binary('{pdf_b64}', 'BASE64'),
                'PDF'
            ) as parsed_content
            """
            
            result = self.session.sql(query).collect()
            if result and len(result) > 0:
                return result[0]['PARSED_CONTENT']
            return ""
            
        except Exception as e:
            print(f"Error parsing PDF {file_path}: {str(e)}")
            return ""
    
    def summarize_with_cortex(self, content: str) -> str:
        """Summarize content using Snowflake Cortex"""
        try:
            query = f"""
            SELECT SUMMARIZE('{content.replace("'", "''")}') as summary
            """
            
            result = self.session.sql(query).collect()
            if result and len(result) > 0:
                return result[0]['SUMMARY']
            return ""
            
        except Exception as e:
            print(f"Error summarizing content: {str(e)}")
            return ""
    
    def extract_key_topics_with_cortex(self, content: str) -> list:
        """Extract key topics using AI_CLASSIFY"""
        try:
            # Define ML/Sales related topics
            topics = [
                "Customer Success Stories", "Competitive Analysis", "Data Engineering",
                "Machine Learning", "MLOps", "Model Training", "Model Deployment",
                "Data Science", "Analytics", "Migration Strategy", "POC Strategy",
                "Technical Architecture", "Compute Optimization", "Cost Analysis",
                "Industry Use Cases", "Platform Comparison"
            ]
            
            query = f"""
            SELECT AI_CLASSIFY(
                '{content.replace("'", "''")}',
                ARRAY_CONSTRUCT({', '.join([f"'{topic}'" for topic in topics])})
            ) as classification
            """
            
            result = self.session.sql(query).collect()
            if result and len(result) > 0:
                classification = json.loads(result[0]['CLASSIFICATION'])
                # Return topics with confidence > 0.3
                return [item['label'] for item in classification if item.get('confidence', 0) > 0.3]
            return []
            
        except Exception as e:
            print(f"Error extracting topics: {str(e)}")
            return []
    
    def load_customer_stories(self, content: str):
        """Load customer stories reference data"""
        print("Processing Customer Stories document...")
        
        # Parse content into sections
        sections = self.split_content_into_sections(content, "Customer Stories")
        
        for i, section in enumerate(sections):
            if len(section.strip()) > 100:  # Only process substantial sections
                summary = self.summarize_with_cortex(section)
                key_topics = self.extract_key_topics_with_cortex(section)
                
                # Insert into database
                record_id = str(uuid.uuid4())
                query = """
                INSERT INTO REFERENCE_KNOWLEDGE 
                (id, document_type, title, content, summary, key_topics)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                
                self.session.sql(query, params=[
                    record_id,
                    'customer_stories',
                    f'Customer Story Section {i+1}',
                    section,
                    summary,
                    json.dumps(key_topics)
                ]).collect()
        
        print(f"Loaded {len(sections)} customer story sections")
    
    def load_ae_training(self, content: str):
        """Load AE training materials reference data"""
        print("Processing AE Training document...")
        
        # Parse content into sections
        sections = self.split_content_into_sections(content, "AE Training")
        
        for i, section in enumerate(sections):
            if len(section.strip()) > 100:  # Only process substantial sections
                summary = self.summarize_with_cortex(section)
                key_topics = self.extract_key_topics_with_cortex(section)
                
                # Insert into database
                record_id = str(uuid.uuid4())
                query = """
                INSERT INTO REFERENCE_KNOWLEDGE 
                (id, document_type, title, content, summary, key_topics)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                
                self.session.sql(query, params=[
                    record_id,
                    'ae_training',
                    f'AE Training Section {i+1}',
                    section,
                    summary,
                    json.dumps(key_topics)
                ]).collect()
        
        print(f"Loaded {len(sections)} AE training sections")
    
    def split_content_into_sections(self, content: str, doc_type: str) -> list:
        """Split content into logical sections for better processing"""
        # Simple section splitting - can be enhanced based on actual PDF structure
        sections = []
        
        # Split by common section markers
        section_markers = [
            "\n# ", "\n## ", "\n### ",  # Markdown headers
            "\nChapter ", "\nSection ",  # Chapter/Section markers
            "\n\n\n",  # Multiple line breaks
            "\nCustomer: ", "\nCompany: ",  # Customer story markers
            "\nUse Case: ", "\nSolution: "  # Solution markers
        ]
        
        current_section = ""
        lines = content.split('\n')
        
        for line in lines:
            # Check if line starts a new section
            is_new_section = any(marker.strip() in line for marker in section_markers)
            
            if is_new_section and current_section.strip():
                sections.append(current_section.strip())
                current_section = line + '\n'
            else:
                current_section += line + '\n'
        
        # Add the final section
        if current_section.strip():
            sections.append(current_section.strip())
        
        # Filter out very short sections
        sections = [s for s in sections if len(s) > 200]
        
        return sections
    
    def load_all_reference_data(self, customer_stories_path: str = None, 
                               ae_training_path: str = None,
                               customer_stories_text: str = None,
                               ae_training_text: str = None):
        """Load all reference data from files or provided text"""
        
        # Clear existing reference data
        self.session.sql("DELETE FROM REFERENCE_KNOWLEDGE").collect()
        print("Cleared existing reference data")
        
        # Load customer stories
        if customer_stories_text:
            self.load_customer_stories(customer_stories_text)
        elif customer_stories_path:
            customer_content = self.parse_pdf_with_cortex(customer_stories_path)
            if customer_content:
                self.load_customer_stories(customer_content)
        
        # Load AE training materials
        if ae_training_text:
            self.load_ae_training(ae_training_text)
        elif ae_training_path:
            training_content = self.parse_pdf_with_cortex(ae_training_path)
            if training_content:
                self.load_ae_training(training_content)
        
        print("Reference data loading complete!")
    
    def verify_data_load(self):
        """Verify that reference data was loaded correctly"""
        query = """
        SELECT 
            document_type,
            COUNT(*) as section_count,
            AVG(LENGTH(content)) as avg_content_length
        FROM REFERENCE_KNOWLEDGE 
        GROUP BY document_type
        """
        
        result = self.session.sql(query).collect()
        
        print("\n=== Data Load Verification ===")
        for row in result:
            print(f"{row['DOCUMENT_TYPE']}: {row['SECTION_COUNT']} sections, "
                  f"avg length: {row['AVG_CONTENT_LENGTH']:.0f} chars")
        
        # Show sample content
        sample_query = """
        SELECT document_type, title, LEFT(summary, 200) as sample_summary
        FROM REFERENCE_KNOWLEDGE 
        LIMIT 5
        """
        
        samples = self.session.sql(sample_query).collect()
        print("\n=== Sample Summaries ===")
        for sample in samples:
            print(f"\n{sample['DOCUMENT_TYPE']} - {sample['TITLE']}:")
            print(f"  {sample['SAMPLE_SUMMARY']}...")

def main():
    """Main function for running the data loader"""
    
    # Connection parameters - adjust as needed
    connection_params = {
        # Add your Snowflake connection parameters here
        # These should match your Streamlit secrets or be provided as environment variables
        "account": "YOUR_ACCOUNT",
        "user": "YOUR_USER", 
        "password": "YOUR_PASSWORD",
        "role": "YOUR_ROLE",
        "warehouse": "YOUR_WAREHOUSE",
        "database": "ML_HELPER_APP",
        "schema": "CORE"
    }
    
    # Initialize loader
    loader = ReferenceDataLoader(connection_params)
    
    # For now, we'll use placeholder text since we don't have the actual PDF content yet
    # Once you provide the PDF content, replace these with the actual text
    
    customer_stories_sample = """
    # Snowflake ML External Customer Stories - Complete Reference
    
    ## COMPETITIVE DISPLACEMENT SUCCESS STORIES
    
    ### Scene+ - 66% Processing Time Reduction with Feature Store
    - **Use Case**: ML for personalized member experiences across properties
    - **Previous Solution**: Extensive Python scripts, input files, dependency scripts
    - **Snowflake Solution**: Snowflake Feature Store with 4 blocks of code
    - **Results**: 66% reduction in processing time, simplified joining model universe with features
    - **Quote**: "Leveraging the straightforward Snowflake Feature Store drove a 66% reduction in processing time; we can join the model universe with the features with just four blocks of code." - Aasma John, Data Science Manager
    
    ### Unnamed Customer - SageMaker vs Snowflake ML Comparison
    **Developer Perspective:**
    - **Build Model**: 2 weeks setup (SageMaker) vs 0 setup (Snowflake ML)
    - **Permissions**: Time consuming multi-platform vs None needed (Snowflake RBAC)
    - **Production**: 3 weeks setup vs <1 hour
    - **Iteration**: 1 day for changes vs <1 hour
    **Admin/Governance Perspective:**
    - **Data Transfer**: Costly AWS<>Snowflake transfers vs None needed
    - **Visibility**: Difficult siloed development vs Easy governance and collaboration
    
    ### Cloudbeds - 95% Accuracy with 24x Training Speed Improvement
    - **Use Case**: Hospitality performance forecasting across 20,000 global properties
    - **Previous Challenges**: 12+ hour training cycles, only 3 experiments per week
    - **Snowflake Results**: 
      * 95% forecasting accuracy
      * 30-minute experiments (down from 12+ hours)
      * 5 experiments per day (up from 3 per week)
      * 90% efficiency gains within 6-month forecasting window
    
    ### Fidelity Investments - Massive Performance Gains
    - **Use Case**: Feature engineering with large datasets
    - **Snowflake ML Performance Results**:
      * MinMax Scaler: 77x speedup (536s to 7s) on 28M rows
      * One Hot Encoding: 50x speedup (654s to 13s) on 100M rows  
      * Pearson Correlation: 17x speedup (702s to 41s) on 162k rows
    - **Benefits**: No data duplication, scalability without operational complexity, no governance trade-offs
    
    ### CHG Healthcare - Cost-Effective GPU ML in Snowflake
    - **Use Case**: Healthcare staffing classification models
    - **Solution**: GPU-powered Snowflake Notebooks on Container Runtime
    - **Results**: Most cost-effective ML solution, parallel processing flexibility
    - **Quote**: "Using GPUs from Snowflake Notebooks on Container Runtime turned out to be the most cost-effective solution for our machine learning needs."
    
    ### IGS Energy - 75% Cost Savings, Databricks Migration
    - **Use Case**: Retail energy demand forecasting for Midwest provider
    - **Data Scale**: 40-50 billion rows, over 1 terabyte
    - **Previous Challenge**: Hundreds of thousands of individual models in Databricks
    - **Snowflake Results**: 
      * 75% cost savings in training
      * Minutes vs 30 minutes for hundreds of thousands of customer forecasts
      * One unified model replacing hundreds of thousands of individual models
    - **Quote**: "We can more easily build predictive models and mock up data products all in the Snowflake ecosystem because the data is all there." - Dan Shah, Manager of Data Science
    
    ### Swire Coca Cola - Managed Spark Migration Success
    - **Use Case**: Logistics route optimization for Coca-Cola bottler
    - **Previous Challenges**: Complex managed Spark billing, data movement costs, infrastructure management
    - **Snowflake Results**: 
      * Weeks of deployment acceleration
      * Significant cost savings
      * Seamless transition due to Snowpark/Spark syntax similarity
      * Eliminated governance and security challenges
    
    ### Spark New Zealand - 9.2x Performance Improvement
    - **Use Case**: End-to-end marketing analytics and customer understanding
    - **Previous Setup**: Virtual machines, Docker containers, unnecessary data transfers
    - **Snowflake Results**:
      * 9.2x speed improvement vs Spark
      * Lazy query execution for better performance
      * No data movement, enhanced governance
      * Eliminated complex deployment pipelines
    
    ### Decile - 9.2x Speed Improvement, Spark to Snowflake ML
    - **Use Case**: Customer Data + Analytics Platform, propensity to purchase models
    - **Previous Challenges**: Managed Spark data transfers, resource administration complexity, data sampling requirements
    - **Snowflake Results**:
      * 9.2x speedup (60 minutes to 6.5 minutes)
      * Intuitive developer experience with familiar SKLearn/XGBoost APIs
      * Enhanced backtesting, QA, and monitoring
      * Easy sharing and collaboration with Snowflake permissions
      * Model Registry for version management and SQL inference
    - **Quote**: "By bringing familiar modeling capabilities to Snowflake, Snowpark ML has enabled us to more rapidly iterate on our models, improving accuracy and operational efficiency."
    
    ### INVISTA - MLOps Transformation
    - **Use Case**: Supply chain forecasting
    - **Previous Challenges**: Multiple platforms, cross-team dependencies, no experiment structure, multiple ML/DL architectures
    - **Snowflake Results**:
      * Universal structure in experimentation → deployment
      * Deployment time from months to days/hours
      * Reduced cloud spend
      * Great visibility for business on usage & cost metrics
      * Ease in orchestrating DAGs
    - **Quote**: "Doing MLOps on Snowflake will reduce our deployment time from months to days, even hours, all while reducing development cloud spend and ensuring model tracking and visibility."
    
    ## HIGH-PERFORMANCE ML SUCCESS STORIES
    
    ### Ecolab - 71x Speed Improvement
    - **Use Case**: Sales opportunity predictions using KMeans clustering
    - **Previous Challenges**: Diverse customer base accuracy issues, limited PaaS/SaaS customization
    - **Snowflake Results**:
      * 71x speedup (15 minutes to 12.6 seconds) on 10.1GB data
      * 4 weeks development time saved
      * 7 lines of code for custom model training and registry
      * Model Registry as first-class schema-level object
    
    ### Cooke Aquaculture - Scalable Production Predictions
    - **Use Case**: World's largest private seafood company, production metrics prediction
    - **Data Scale**: 10+ years of raw data from 70+ sites
    - **Previous Challenge**: Scalability with massive historical datasets
    - **Snowflake Benefits**:
      * Unified development environment (data, pipelines, ML models)
      * On-demand compute scaling
      * No local processing constraints
      * Integrated ML capabilities for faster production
    
    ### BAMA - 35% Cash Flow Loss Reduction
    - **Use Case**: Norwegian fruit/vegetable distributor, invoice due date prediction
    - **Business Challenge**: Currency risk exposure (buy in USD/EUR/GBP, sell in NOK)
    - **Snowflake Results**: 35% reduction in cash flow-related losses
    - **Quote**: "The due date prediction model has significantly reduced our exposure to currency exchange rate risk, enhancing financial stability and forecasting accuracy" - Jarle Gjerde, Group CFO
    
    ### Classy - 11% Greater Donation Revenue
    - **Use Case**: Nonprofit giving platform, intelligent ask amounts
    - **Previous Challenges**: Small data team, modern data stack doesn't support MLOps, limited architecture support
    - **Snowflake Results**:
      * 11% greater donation revenue in testing
      * Compute and storage within Snowflake for entire model development
      * User-friendly syntax for quick training and evaluation
      * Powerful hyperparameter tuning in few lines of code
    
    ### S&P Global - 75% Time Savings
    - **Migration**: PySpark on Databricks to Snowflake ML
    - **Results**: 75% time savings
    
    ### Lessmore - 10x Cost Reduction
    - **Use Case**: Customer lifetime value forecasts
    - **Results**: 10x cost reduction, accelerated innovation cycle, enhanced efficiency
    - **Quote**: "Leveraging the Snowflake Model Registry has transformed our model development and experimentation process for our customer lifetime value forecasts. This shift has not only accelerated our innovation cycle but also reduced our costs by a factor of 10, while enhancing efficiency." - Moritz Schöne, Head of Data Science
    
    ### Paytronix - 70% Cost Reduction, Real-Time Predictions
    - **Use Case**: Personalized customer experiences
    - **Results**: 70% cost reduction, hour-long inference jobs to near real-time predictions
    - **Quote**: "We've been able to achieve a 70% cost reduction and enhanced agility by moving from running hour-long inference jobs to predictions in near real-time." - Stefan Kochi, CTO
    
    ## ML FUNCTIONS SUCCESS STORIES (SQL-Based ML)
    
    ### SpartanNash - Retail Forecasting Automation
    - **Use Case**: Year-long sales forecasts for 183 locations, 10 districts
    - **Previous Process**: Manual Excel-based, 400 hours per period, 5,200 hours per year
    - **Snowflake ML Functions Results**:
      * Fully automated process (5 minutes per week vs 400 hours per period)
      * Accuracy improved from 71% to 88%
      * Lower granularity predictions now possible
      * Data-driven vs institutional knowledge-based
    - **Quote**: "We've been using Snowflake's ML-based forecasting function for three months now and have saved hours of effort while generating more accurate forecasts."
    
    ### Snowflake Data Science - Lead Scoring Internal Success
    - **Use Case**: Prospect propensity scoring for sales team assignment
    - **Previous Challenges**: Multiple third-party tools, data movement out of Snowflake
    - **Snowflake ML Functions Results**:
      * 5x higher conversion rate with target accounts
      * 1,000 hours of development saved
      * 150,000 accounts assigned through strategic market expansion
      * 70% efficiency improvements (no third-party tools, no data movement)
    
    ## KEY COMPETITIVE ADVANTAGES DEMONSTRATED
    
    ### Cost Savings:
    - IGS Energy: 75% cost savings in training
    - Lessmore: 10x cost reduction  
    - Paytronix: 70% cost reduction
    - CHG Healthcare: Most cost-effective solution
    
    ### Performance Improvements:
    - Scene+: 66% processing time reduction
    - Cloudbeds: 24x training speed improvement (12+ hours to 30 minutes)
    - Fidelity: Up to 77x speedup
    - Decile: 9.2x speedup (60 to 6.5 minutes)
    - Spark New Zealand: 9.2x speed improvement
    - Ecolab: 71x speedup (15 minutes to 12.6 seconds)
    
    ### Accuracy & Business Impact:
    - Cloudbeds: 95% forecasting accuracy
    - SpartanNash: 88% accuracy (up from 71%)
    - BAMA: 35% reduction in cash flow losses
    - Classy: 11% greater donation revenue
    - Snowflake Internal: 5x higher conversion rate
    
    ### Time to Production:
    - INVISTA: Months to days/hours deployment
    - Ecolab: 4 weeks development time saved
    - Snowflake Internal: 1,000 hours saved
    - SpartanNash: 5,200 to 5 minutes per year
    """
    
    ae_training_sample = """
    # AI & ML 101 for AEs - Snowflake Training Material
    
    ## ML Fundamentals & Key Terms
    - Algorithm: The mathematical "recipe" that tells a computer how to learn patterns from data
    - Model: The object created once algorithm learns from data—what makes actual predictions
    - Model Training: Teaching a model using historical data for accurate predictions
    - Model Scoring/Inference: When trained model makes predictions on new, real-world data
    - Feature Engineering: Selecting and creating useful data inputs—separates good from great models
    - AutoML: Technology that automates model-building, accessible to non-experts
    - Drift: Performance degradation over time requiring retraining
    
    ## Snowflake ML Lifecycle Phases
    
    ### 1. Develop & Iterate
    - Data Scientists doing EDA, feature engineering, model building
    - Critical group to win over with high compute upside
    - Snowflake notebooks with container runtime, distributed APIs, git integration
    - Discovery Questions:
      * How much time spent moving/sampling data vs building models?
      * How do you ensure fresh, production-quality data without security risks?
      * How do you manage compute environments and package dependencies?
    
    ### 2. Orchestrate & Automate  
    - ML engineers turning code into repeatable, production-grade pipelines
    - Multi-step data preparation and model training workflows
    - High compute upside with ML Jobs on container runtime
    - Discovery Questions:
      * How do you automate model preprocessing pipeline?
      * How much engineering time spent maintaining vs building new ones?
      * How do you manage and scale compute resources for automated ML jobs?
    
    ### 3. Manage
    - Centralized way to discover, manage, govern all ML assets
    - Model Registry and ML Lineage for immediate value
    - Low compute upside but important for mindshare
    - Discovery Questions:
      * How do you manage models in production - centralized or spread across teams?
      * How do you trace lineage back to exact features and data versions?
      * How do you track model versions and authorization?
    
    ### 4. Deploy & Serve
    - Model inference step - moving to production for predictions
    - Batch (overnight predictions) or real-time serving
    - Medium compute upside owning inference location
    - Snowflake has warehouse for batch, SPCS for low latency
    - Discovery Questions:
      * Do you have models in production - what percentage batch vs real-time?
      * How do you ensure feature processing pipelines for new scoring data?
      * How do you manage underlying compute resources for deployed models?
    
    ### 5. Monitor
    - Monitor production models to ensure continued performance
    - Track accuracy metrics, detect drift, trigger retraining
    - ML Observability & ML Explainability for complete lifecycle
    - Discovery Questions:
      * How do you track model performance over time?
      * How do you detect and get alerted to model/data drift?
      * What's your process for troubleshooting and triggering retrain?
    
    ## Competitive Analysis
    
    ### AWS SageMaker
    Strengths:
    - "Mature" ML platform in capabilities and product marketing
    - No gaps in ML features or tools
    - Sticky ecosystem
    
    Weaknesses:
    - Not really a single platform - must stitch services together
    - Architecture complexity to get model off ground
    - Forced data movement & egress costs
    
    How Snowflake Wins:
    - Emphasize architecture simplicity
    - Reduce time to value by starting and ending in Snowflake
    - Land & Expand in ML pipeline
    - If predictions come back to Snowflake, use our model registry
    
    ### Databricks
    Strengths:
    - "Industry Leading" in ML mindshare
    - Robust MLOps framework/experimentation
    - Made for ML practitioners (lots of horsepower)
    
    Weaknesses:
    - Overwhelming and complex depending on ML maturity
    - Spark experience required, cluster optimization needed
    - Lack of cost transparency for ML projects start to finish
    
    How Snowflake Wins:
    - Grab attention with specific capability showcases
    - Snowflake ML jobs for remote code execution
    - Position multi-modal offerings - AI SQL + Snowflake ML
    
    ### Microsoft Azure ML
    Strengths:
    - Really good for all-in Microsoft ecosystem customers
    - Tightly integrated to Microsoft services/Databricks
    - Mature ML platform for practitioners
    
    Weaknesses:
    - Effectively single cloud when it comes to Azure ML
    - Using both Databricks ML and Azure ML creates separation confusion
    - Delta lake can add complexity and governance challenges
    
    How Snowflake Wins:
    - If delta lake users proud of "open source", challenge Azure-centric stack
    - Pitch multi-cloud capabilities
    - Find pain points/governance challenges in bronze layer
    - Land & Expand strategy
    
    ## Use Case to ML Technique Mapping
    - Customer Segmentation: Unsupervised learning
    - Customer Lifetime Value (CLV): Supervised learning
    - Customer Churn: Supervised learning
    - Demand Forecasting: Supervised learning
    - Dynamic Pricing: Supervised learning
    - Fraud Detection: Supervised learning
    - Inventory Optimization: Supervised learning
    - Anomaly Detection: Unsupervised learning
    - Ad Targeting & Click-Through Rate: Supervised learning
    - Audience Segmentation: Unsupervised learning
    
    ## Key Strategic Points
    - Unified Governance across entire ML lifecycle
    - Architecture simplicity vs complex multi-tool approaches
    - High compute upside in Develop & Iterate, Orchestrate & Automate phases
    - Medium compute upside in Deploy & Serve phase
    - Low compute upside but high strategic value in Manage and Monitor phases
    - Focus on reducing time to value and eliminating data movement
    """
    
    print("Loading reference data...")
    
    # Load the sample data (replace with actual PDF content when available)
    loader.load_all_reference_data(
        customer_stories_text=customer_stories_sample,
        ae_training_text=ae_training_sample
    )
    
    # Verify the load
    loader.verify_data_load()
    
    print("\nReference data loading complete! The ML Helper App is ready to use.")

if __name__ == "__main__":
    main() 