"""
Generate sample resumes and job descriptions for testing
"""

import os

# Sample job descriptions
job_descriptions = [
    {
        "title": "Senior_Python_Developer",
        "company": "TechCorp",
        "description": """Job Title: Senior Python Developer
Company: TechCorp

We are seeking a Senior Python Developer with 5+ years of experience.

Required Skills:
- Python, Django, FastAPI
- PostgreSQL, MongoDB
- AWS, Docker, Kubernetes
- RESTful APIs, Microservices
- Git, CI/CD

Experience:
- 5+ years in software development
- 3+ years with Python
- Experience with cloud platforms
- Strong problem-solving skills

Education:
- Bachelor's degree in Computer Science or related field

Responsibilities:
- Design and develop scalable backend services
- Build and maintain RESTful APIs
- Collaborate with frontend team
- Write clean, maintainable code
- Mentor junior developers
- Participate in code reviews
        """
    },
    {
        "title": "Data_Scientist",
        "company": "DataMinds AI",
        "description": """Job Title: Data Scientist
Company: DataMinds AI

Looking for a Data Scientist to join our ML team.

Required Skills:
- Python, R
- Machine Learning (scikit-learn, TensorFlow, PyTorch)
- SQL, NoSQL databases
- Data visualization (Matplotlib, Plotly)
- Statistical analysis
- NLP, Computer Vision (preferred)

Experience:
- 3+ years in data science or ML
- Strong mathematical background
- Experience with production ML models
- A/B testing and experimentation

Education:
- Master's degree in Computer Science, Statistics, or related field

Responsibilities:
- Develop and deploy machine learning models
- Perform statistical analysis
- Create data visualizations
- Collaborate with engineering team
- Present findings to stakeholders
        """
    },
    {
        "title": "Frontend_Developer",
        "company": "WebTech Solutions",
        "description": """Job Title: Frontend Developer
Company: WebTech Solutions

Seeking a creative Frontend Developer with modern web expertise.

Required Skills:
- JavaScript, TypeScript
- React, Vue.js or Angular
- HTML5, CSS3, Sass
- Responsive design
- Git, npm, webpack
- RESTful APIs

Experience:
- 3+ years frontend development
- Portfolio of web applications
- Experience with modern frameworks
- Understanding of UX principles

Education:
- Bachelor's degree in Computer Science or related field

Responsibilities:
- Build responsive web applications
- Implement pixel-perfect designs
- Optimize for performance
- Write unit tests
- Collaborate with designers and backend team
        """
    }
]

# Sample resumes
resumes = [
    {
        "name": "John_Doe",
        "content": """JOHN DOE
Senior Software Engineer
Email: john.doe@email.com | Phone: +27 123 456 789
LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe

SUMMARY
Experienced software engineer with 6 years of expertise in Python development,
cloud infrastructure, and building scalable applications. Passionate about clean
code and mentoring junior developers.

SKILLS
Programming Languages: Python, JavaScript, SQL, Bash
Frameworks & Libraries: Django, FastAPI, React, Flask
Databases: PostgreSQL, MongoDB, Redis, MySQL
Cloud & DevOps: AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes, Jenkins
Tools & Technologies: Git, CI/CD, Terraform, Nginx, Linux
Methodologies: Agile, Scrum, Test-Driven Development

PROFESSIONAL EXPERIENCE

Senior Python Developer | TechStart Inc. | Johannesburg, SA | 2021 - Present
- Built microservices architecture serving 1M+ users using FastAPI and Docker
- Implemented RESTful APIs with 99.9% uptime and <100ms response time
- Deployed applications on AWS using ECS, reducing infrastructure costs by 30%
- Reduced API response time by 40% through database optimization and caching
- Led team of 3 developers on core platform features
- Implemented CI/CD pipelines using Jenkins and GitHub Actions

Python Developer | SoftwareCo | Cape Town, SA | 2019 - 2021
- Developed web applications using Django and PostgreSQL
- Integrated third-party payment gateways (Stripe, PayPal)
- Wrote comprehensive unit tests achieving 90% code coverage
- Mentored 2 junior developers and conducted code reviews
- Improved application performance by 25% through optimization
- Collaborated with product team on feature development

Junior Developer | StartupXYZ | Pretoria, SA | 2018 - 2019
- Built features for e-commerce platform using Python and Django
- Fixed bugs and improved application performance
- Participated in daily standups and sprint planning
- Learned Docker and containerization

EDUCATION
Bachelor of Science in Computer Science
University of Cape Town | 2014 - 2017
GPA: 3.7/4.0

CERTIFICATIONS
- AWS Certified Solutions Architect - Associate (2022)
- Python Professional Certificate - DataCamp (2020)
- Docker Certified Associate (2021)

PROJECTS
- E-commerce API: Built scalable REST API handling 10K requests/min
- Traffic Predictor: ML system predicting traffic congestion (Python, XGBoost)
- Chat Application: Real-time chat using WebSockets and Redis
        """
    },
    {
        "name": "Sarah_Johnson",
        "content": """SARAH JOHNSON
Data Scientist & ML Engineer
Email: sarah.j@email.com | Phone: +27 987 654 321
Portfolio: sarahjohnson.com | GitHub: github.com/sarahj

PROFESSIONAL SUMMARY
Data scientist with 4 years of experience in machine learning, statistical
modeling, and deploying ML solutions in production. Specialized in NLP and
computer vision with proven track record of delivering business impact.

TECHNICAL SKILLS
Programming: Python, R, SQL, Scala
ML/AI: scikit-learn, TensorFlow, PyTorch, Keras, XGBoost
NLP: spaCy, NLTK, Transformers, BERT, Hugging Face
Computer Vision: OpenCV, YOLO, CNNs
Data Processing: pandas, NumPy, Spark, Airflow
Visualization: Matplotlib, Seaborn, Plotly, Tableau, Power BI
Cloud: AWS (SageMaker, EC2), GCP, Azure
Databases: PostgreSQL, MongoDB, Redis
Tools: Docker, Git, Jupyter, MLflow

PROFESSIONAL EXPERIENCE

Senior Data Scientist | AI Solutions Ltd. | Johannesburg, SA | 2021 - Present
- Developed NLP sentiment analysis model achieving 92% accuracy for customer feedback
- Built recommendation system that increased user engagement by 35%
- Deployed ML models to production using Docker and Kubernetes
- Conducted A/B tests and statistical analysis for product features
- Reduced model inference time by 60% through optimization
- Presented findings to C-level executives and stakeholders
- Mentored 2 junior data scientists

Machine Learning Engineer | DataCorp | Durban, SA | 2020 - 2021
- Created predictive models for customer churn with 85% accuracy
- Implemented computer vision solution for quality control in manufacturing
- Optimized model training pipelines reducing training time by 40%
- Collaborated with engineering team on API integration
- Built data pipelines using Apache Airflow
- Improved model performance through hyperparameter tuning

Data Analyst | Analytics Pro | Cape Town, SA | 2019 - 2020
- Performed statistical analysis on business metrics
- Created interactive dashboards for stakeholders using Tableau
- Cleaned and processed large datasets (100M+ records)
- Automated reporting reducing manual work by 50%
- Conducted exploratory data analysis

EDUCATION
Master of Science in Data Science
Stellenbosch University | 2017 - 2019
Thesis: "Deep Learning Approaches for Text Classification"

Bachelor of Science in Mathematics
University of Pretoria | 2013 - 2016
Graduated with Distinction

PUBLICATIONS & PRESENTATIONS
- "Advanced NLP Techniques for Text Classification" - ML Conference 2022
- "Building Scalable ML Pipelines" - PyConZA 2021

CERTIFICATIONS
- TensorFlow Developer Certificate (2022)
- AWS Machine Learning Specialty (2021)
- Deep Learning Specialization - Coursera (2020)

AWARDS
- Best Data Science Project - DataHack 2021
- Top 5% Kaggle Competitor
        """
    },
    {
        "name": "Michael_Chen",
        "content": """MICHAEL CHEN
Frontend Developer
Email: michael.chen@email.com | Phone: +27 555 123 456
Portfolio: michaelchen.dev | GitHub: github.com/mchen

SUMMARY
Creative frontend developer with 4 years of experience building modern,
responsive web applications. Expertise in React ecosystem and pixel-perfect
implementation of designs.

SKILLS
Languages: JavaScript, TypeScript, HTML5, CSS3
Frameworks: React, Next.js, Vue.js, Angular
Styling: Tailwind CSS, Sass, Bootstrap, Material-UI
State Management: Redux, Context API, Zustand
Testing: Jest, React Testing Library, Cypress
Tools: Git, npm, Webpack, Vite, Figma
APIs: REST, GraphQL, WebSockets

EXPERIENCE

Frontend Developer | WebTech Solutions | Johannesburg, SA | 2021 - Present
- Built responsive web applications using React and TypeScript
- Implemented pixel-perfect designs from Figma mockups
- Optimized application performance achieving 95+ Lighthouse scores
- Reduced bundle size by 40% through code splitting and lazy loading
- Wrote comprehensive unit tests with 85% code coverage
- Collaborated with UX designers and backend developers
- Mentored junior developers on React best practices

Junior Frontend Developer | DigitalCraft | Pretoria, SA | 2020 - 2021
- Developed features for e-commerce platform using Vue.js
- Implemented responsive designs for mobile and desktop
- Integrated RESTful APIs and handled state management
- Fixed bugs and improved user experience
- Participated in code reviews and sprint planning

Frontend Intern | StartupHub | Cape Town, SA | 2019 - 2020
- Built landing pages and marketing websites
- Learned React and modern JavaScript (ES6+)
- Assisted senior developers with feature development

EDUCATION
Bachelor of Science in Computer Science
University of the Witwatersrand | 2015 - 2018

CERTIFICATIONS
- React Developer Certificate - Meta (2022)
- JavaScript Algorithms and Data Structures - freeCodeCamp (2020)

PROJECTS
- E-commerce Dashboard: Admin panel with charts and analytics (React, TypeScript)
- Portfolio CMS: Content management system for portfolios (Next.js, Tailwind)
- Weather App: Real-time weather application (React, OpenWeather API)
        """
    }
]

def create_sample_files():
    """Create sample text files for job descriptions and resumes"""
    
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create directories if they don't exist
    jd_dir = os.path.join(script_dir, 'job_descriptions')
    resume_dir = os.path.join(script_dir, 'resumes')
    
    os.makedirs(jd_dir, exist_ok=True)
    os.makedirs(resume_dir, exist_ok=True)
    
    print("="*60)
    print("CREATING SAMPLE DATA")
    print("="*60)
    
    # Create job description files
    print("\nCreating Job Descriptions...")
    for jd in job_descriptions:
        filename = os.path.join(jd_dir, f"{jd['title']}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(jd['description'])
        print(f"✓ Created: {jd['title']}.txt")
    
    # Create resume files
    print("\nCreating Resumes...")
    for resume in resumes:
        filename = os.path.join(resume_dir, f"{resume['name']}_Resume.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(resume['content'])
        print(f"✓ Created: {resume['name']}_Resume.txt")
    
    print("\n" + "="*60)
    print("SAMPLE DATA CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"\nJob Descriptions: {len(job_descriptions)} files in {jd_dir}")
    print(f"Resumes: {len(resumes)} files in {resume_dir}")
    print("\nYou can now use these files for testing the resume screener.")
    print("="*60)

if __name__ == "__main__":
    create_sample_files()