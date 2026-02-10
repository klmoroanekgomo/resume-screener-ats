# 📄 Smart Resume Screening System (ATS)

An AI-powered Applicant Tracking System that analyzes resumes and job descriptions to find the best candidate matches.

## 🎯 Features

- Parse resumes from PDF, DOCX, and TXT formats
- Extract skills, experience, and education
- Match resumes to job descriptions
- Rank candidates by fit score
- Identify skill gaps
- RESTful API with FastAPI
- Interactive web interface

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **NLP**: spaCy, Transformers
- **ML**: scikit-learn, sentence-transformers
- **API**: FastAPI, Uvicorn
- **Data Processing**: pandas, numpy
- **PDF Processing**: PyPDF2, pdfplumber

## 📁 Project Structure
```
resume-screener-ats/
├── data/
│   ├── raw/                    # Uploaded resumes
│   ├── processed/              # Processed data
│   └── sample/                 # Sample data for testing
├── notebooks/                  # Jupyter notebooks for analysis
├── src/
│   ├── data_processing/        # PDF parsing and text extraction
│   ├── models/                 # ML models and matching logic
│   └── api/                    # FastAPI application
├── models/                     # Trained models
└── tests/                      # Unit tests
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/resume-screener-ats.git
cd resume-screener-ats
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg
```

4. Generate sample data
```bash
python data/sample/create_sample_data.py
```

## 📖 Usage

(Will be updated as we build the project)

## 👤 Author

**[Kgaiso Moroane-Kgomo]**
- BSc Computer Science Graduate
- GitHub: [@klmoroanekgomo](https://github.com/klmoroanekgomo)

## 📝 License

MIT License