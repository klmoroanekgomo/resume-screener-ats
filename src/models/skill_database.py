"""
Comprehensive skills taxonomy and database for resume screening
"""

# Technical skills organized by category
TECHNICAL_SKILLS = {
    'programming_languages': [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
        'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'Perl',
        'HTML', 'CSS', 'SQL', 'Shell', 'Bash', 'PowerShell', 'Dart', 'Lua',
        'Objective-C', 'Groovy', 'Haskell', 'Elixir', 'Clojure', 'F#'
    ],
    
    'web_frameworks': [
        'Django', 'Flask', 'FastAPI', 'React', 'Angular', 'Vue', 'Vue.js', 'Node.js',
        'Express', 'Express.js', 'Spring', 'Spring Boot', 'ASP.NET', 'Laravel', 
        'Rails', 'Ruby on Rails', 'Next.js', 'Nuxt.js', 'Gatsby', 'Svelte',
        'Bootstrap', 'Tailwind', 'Tailwind CSS', 'jQuery', 'Backbone.js', 'Ember.js'
    ],
    
    'ml_ai': [
        'Machine Learning', 'Deep Learning', 'Neural Networks', 'NLP', 'CNN', 'RNN',
        'Natural Language Processing', 'Computer Vision', 'Reinforcement Learning',
        'TensorFlow', 'PyTorch', 'Keras', 'scikit-learn', 'sklearn', 'XGBoost',
        'LightGBM', 'CatBoost', 'NLTK', 'spaCy', 'Transformers', 'BERT', 'GPT',
        'YOLO', 'OpenCV', 'Hugging Face', 'MLflow', 'Weights & Biases', 'SageMaker',
        'AutoML', 'Transfer Learning', 'GANs', 'LSTM', 'GRU'
    ],
    
    'databases': [
        'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Cassandra', 'Oracle',
        'SQL Server', 'SQLite', 'DynamoDB', 'Elasticsearch', 'Neo4j',
        'Firebase', 'MariaDB', 'CouchDB', 'InfluxDB', 'Snowflake', 'BigQuery',
        'Redshift', 'DocumentDB', 'Cosmos DB', 'Memcached', 'Couchbase'
    ],
    
    'cloud_platforms': [
        'AWS', 'Azure', 'GCP', 'Google Cloud', 'Google Cloud Platform',
        'Heroku', 'DigitalOcean', 'Linode', 'IBM Cloud', 'Oracle Cloud',
        'Alibaba Cloud', 'Cloudflare'
    ],
    
    'devops_tools': [
        'Docker', 'Kubernetes', 'Jenkins', 'CI/CD', 'Terraform', 'Ansible',
        'Git', 'GitHub', 'GitLab', 'BitBucket', 'Travis CI', 'CircleCI',
        'GitHub Actions', 'ArgoCD', 'Helm', 'Vagrant', 'Puppet', 'Chef',
        'Prometheus', 'Grafana', 'ELK Stack', 'Nagios', 'Datadog', 'New Relic'
    ],
    
    'aws_services': [
        'EC2', 'S3', 'Lambda', 'ECS', 'EKS', 'RDS', 'DynamoDB', 'CloudFormation',
        'CloudWatch', 'Route 53', 'API Gateway', 'SNS', 'SQS', 'Kinesis',
        'Elastic Beanstalk', 'CloudFront', 'IAM', 'VPC', 'Athena', 'Glue'
    ],
    
    'data_tools': [
        'pandas', 'NumPy', 'Spark', 'Apache Spark', 'Hadoop', 'Kafka', 
        'Apache Kafka', 'Airflow', 'Apache Airflow', 'dbt', 'Tableau', 
        'Power BI', 'Looker', 'Matplotlib', 'Seaborn', 'Plotly', 'D3.js',
        'Excel', 'Jupyter', 'JupyterLab', 'ETL', 'Apache Flink', 'Databricks'
    ],
    
    'mobile': [
        'React Native', 'Flutter', 'Ionic', 'Android', 'iOS', 'Xamarin',
        'Swift UI', 'Jetpack Compose', 'Cordova', 'PhoneGap'
    ],
    
    'testing': [
        'Jest', 'Mocha', 'Pytest', 'Selenium', 'Cypress', 'JUnit', 'TestNG',
        'Unit Testing', 'Integration Testing', 'E2E Testing', 'TDD', 'BDD',
        'Postman', 'JMeter', 'LoadRunner', 'Cucumber', 'Jasmine', 'Karma'
    ],
    
    'api_protocols': [
        'REST', 'REST API', 'RESTful API', 'GraphQL', 'gRPC', 'WebSockets',
        'SOAP', 'OAuth', 'JWT', 'OpenAPI', 'Swagger', 'Microservices'
    ],
    
    'other_tech': [
        'Linux', 'Unix', 'Nginx', 'Apache', 'RabbitMQ', 'WebRTC',
        'Blockchain', 'Solidity', 'Web3', 'WebAssembly', 'Socket.io'
    ]
}

# Soft skills
SOFT_SKILLS = [
    'Leadership', 'Communication', 'Teamwork', 'Team Collaboration', 'Problem Solving',
    'Critical Thinking', 'Time Management', 'Adaptability', 'Creativity',
    'Collaboration', 'Project Management', 'Agile', 'Scrum', 'Analytical',
    'Detail-Oriented', 'Self-Motivated', 'Mentoring', 'Presentation Skills',
    'Public Speaking', 'Conflict Resolution', 'Decision Making', 'Strategic Thinking',
    'Customer Service', 'Stakeholder Management', 'Cross-functional Collaboration'
]

# Methodologies and practices
METHODOLOGIES = [
    'Agile', 'Scrum', 'Kanban', 'Waterfall', 'DevOps', 'CI/CD',
    'Test-Driven Development', 'TDD', 'Behavior-Driven Development', 'BDD',
    'Domain-Driven Design', 'DDD', 'Microservices Architecture',
    'Event-Driven Architecture', 'SOLID Principles', 'Design Patterns',
    'RESTful Design', 'API Design', 'Database Design', 'System Design'
]

# Create flat list of all technical skills
ALL_TECHNICAL_SKILLS = []
for category, skills in TECHNICAL_SKILLS.items():
    ALL_TECHNICAL_SKILLS.extend(skills)

# Add methodologies to technical skills
ALL_TECHNICAL_SKILLS.extend(METHODOLOGIES)

# Skill synonyms and variations
SKILL_SYNONYMS = {
    'Machine Learning': ['ML', 'Machine-Learning'],
    'Deep Learning': ['DL', 'Deep-Learning'],
    'Natural Language Processing': ['NLP'],
    'Continuous Integration': ['CI', 'CI/CD'],
    'Amazon Web Services': ['AWS'],
    'Google Cloud Platform': ['GCP', 'Google Cloud'],
    'Microsoft Azure': ['Azure'],
    'Artificial Intelligence': ['AI'],
    'PostgreSQL': ['Postgres'],
    'MongoDB': ['Mongo'],
    'JavaScript': ['JS'],
    'TypeScript': ['TS'],
    'Kubernetes': ['K8s'],
    'React.js': ['React', 'ReactJS'],
    'Vue.js': ['Vue', 'VueJS'],
    'Node.js': ['Node', 'NodeJS'],
    'Express.js': ['Express', 'ExpressJS'],
    'scikit-learn': ['sklearn'],
}

# Education levels and keywords
EDUCATION_LEVELS = {
    'phd': ['PhD', 'Ph.D', 'Ph.D.', 'Doctorate', 'Doctoral', 'Doctor of Philosophy'],
    'masters': ['Master', 'Masters', "Master's", 'M.S.', 'M.Sc', 'M.Sc.', 'MBA', 'M.A.', 'MSc', 'MS'],
    'bachelors': ['Bachelor', 'Bachelors', "Bachelor's", 'B.S.', 'B.Sc', 'B.Sc.', 'B.A.', 'B.Tech', 'B.E.', 'BSc', 'BS'],
    'associate': ['Associate', 'A.S.', 'A.A.', 'AS', 'AA'],
    'diploma': ['Diploma', 'Certificate', 'Advanced Diploma'],
    'high_school': ['High School', 'Secondary School', 'Matric']
}

# Experience levels
EXPERIENCE_KEYWORDS = {
    'senior': ['Senior', 'Lead', 'Principal', 'Staff', 'Architect', 'Chief', 'Director', 'VP', 'Head of'],
    'mid': ['Mid-level', 'Intermediate', 'Mid', 'Experienced'],
    'junior': ['Junior', 'Entry-level', 'Graduate', 'Associate', 'Assistant'],
    'intern': ['Intern', 'Internship', 'Trainee', 'Apprentice']
}

# Common certifications
CERTIFICATIONS = [
    'AWS Certified Solutions Architect',
    'AWS Certified Developer',
    'AWS Certified Machine Learning',
    'Azure Certified',
    'Google Cloud Certified',
    'PMP', 'Project Management Professional',
    'Certified Scrum Master', 'CSM',
    'CISSP',
    'CompTIA',
    'Oracle Certified',
    'Microsoft Certified',
    'Kubernetes Certified',
    'Docker Certified',
    'TensorFlow Developer Certificate',
    'Data Science Certificate',
    'Python Certificate'
]


def get_all_skills():
    """Get list of all skills (technical + soft)"""
    return list(set(ALL_TECHNICAL_SKILLS + SOFT_SKILLS))


def get_skill_category(skill):
    """Get category for a given skill"""
    skill_lower = skill.lower()
    
    for category, skills in TECHNICAL_SKILLS.items():
        if skill in skills or skill_lower in [s.lower() for s in skills]:
            return category
    
    if skill in SOFT_SKILLS or skill_lower in [s.lower() for s in SOFT_SKILLS]:
        return 'soft_skills'
    
    if skill in METHODOLOGIES or skill_lower in [s.lower() for s in METHODOLOGIES]:
        return 'methodologies'
    
    return 'unknown'


def normalize_skill(skill):
    """Normalize skill name (handle synonyms)"""
    skill = skill.strip()
    
    # Check if it's a synonym
    for main_skill, synonyms in SKILL_SYNONYMS.items():
        if skill in synonyms or skill.upper() in [s.upper() for s in synonyms]:
            return main_skill
        # Also check lowercase
        if skill.lower() in [s.lower() for s in synonyms]:
            return main_skill
    
    return skill


def get_skills_by_category(category):
    """Get all skills in a specific category"""
    if category in TECHNICAL_SKILLS:
        return TECHNICAL_SKILLS[category]
    elif category == 'soft_skills':
        return SOFT_SKILLS
    elif category == 'methodologies':
        return METHODOLOGIES
    else:
        return []


def search_skills(query):
    """Search for skills matching a query"""
    query_lower = query.lower()
    all_skills = get_all_skills()
    
    matching_skills = []
    for skill in all_skills:
        if query_lower in skill.lower():
            matching_skills.append(skill)
    
    return matching_skills


def main():
    """Test the skills database"""
    
    print("="*70)
    print("SKILLS DATABASE")
    print("="*70)
    
    # Count skills
    total_technical = len(ALL_TECHNICAL_SKILLS)
    total_soft = len(SOFT_SKILLS)
    total_all = len(get_all_skills())
    
    print(f"\n📊 SKILL COUNTS")
    print("-"*70)
    print(f"  Total technical skills: {total_technical}")
    print(f"  Total soft skills: {total_soft}")
    print(f"  Total unique skills: {total_all}")
    
    # Skills by category
    print(f"\n📁 SKILLS BY CATEGORY")
    print("-"*70)
    for category, skills in TECHNICAL_SKILLS.items():
        print(f"  {category:25s}: {len(skills):3d} skills")
    
    # Show sample skills from each category
    print(f"\n🔍 SAMPLE SKILLS FROM EACH CATEGORY")
    print("-"*70)
    for category, skills in TECHNICAL_SKILLS.items():
        sample = skills[:5]
        print(f"\n  {category.upper()}:")
        print(f"    {', '.join(sample)}")
    
    # Test synonym normalization
    print(f"\n🔄 SYNONYM NORMALIZATION TEST")
    print("-"*70)
    test_synonyms = ['ML', 'AWS', 'K8s', 'JS', 'Postgres']
    for syn in test_synonyms:
        normalized = normalize_skill(syn)
        print(f"    {syn:15s} → {normalized}")
    
    # Test skill search
    print(f"\n🔎 SKILL SEARCH TEST")
    print("-"*70)
    search_queries = ['Python', 'React', 'AWS']
    for query in search_queries:
        results = search_skills(query)
        print(f"    '{query}': Found {len(results)} match(es)")
        if results:
            print(f"      → {', '.join(results[:3])}")
    
    # Test category lookup
    print(f"\n📂 CATEGORY LOOKUP TEST")
    print("-"*70)
    test_skills = ['Python', 'Docker', 'Leadership', 'PostgreSQL']
    for skill in test_skills:
        category = get_skill_category(skill)
        print(f"    {skill:20s} → {category}")
    
    print("\n" + "="*70)
    print("SKILLS DATABASE TEST COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()