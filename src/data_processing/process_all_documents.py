"""
Process all documents and save structured data
"""

import sys
import os
import json
import pandas as pd

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processing.pdf_parser import DocumentParser
from data_processing.text_cleaner import TextCleaner

def process_resumes(resume_dir='data/sample/resumes', output_dir='data/processed'):
    """Process all resumes and save structured data"""
    
    parser = DocumentParser()
    cleaner = TextCleaner()
    
    print("="*70)
    print("PROCESSING RESUMES")
    print("="*70)
    
    # Parse all resumes
    resumes = parser.parse_directory(resume_dir)
    
    processed_data = []
    
    for resume in resumes:
        text = resume['text']
        
        # Extract information
        contact = cleaner.extract_contact_info(text)
        name = cleaner.extract_name(text)
        years_exp = cleaner.extract_years_of_experience(text)
        sections = cleaner.extract_sections(text)
        
        # Store processed data
        processed = {
            'filename': resume['filename'],
            'name': name,
            'email': contact['email'],
            'phone': contact['phone'],
            'linkedin': contact['linkedin'],
            'github': contact['github'],
            'years_experience': years_exp,
            'raw_text': text,
            'sections': sections,
            'word_count': resume['word_count']
        }
        
        processed_data.append(processed)
        print(f"✓ Processed: {resume['filename']}")
    
    # Save to JSON
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'processed_resumes.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved {len(processed_data)} processed resumes to {output_file}")
    
    return processed_data

def process_job_descriptions(jd_dir='data/sample/job_descriptions', output_dir='data/processed'):
    """Process all job descriptions and save structured data"""
    
    parser = DocumentParser()
    cleaner = TextCleaner()
    
    print("\n" + "="*70)
    print("PROCESSING JOB DESCRIPTIONS")
    print("="*70)
    
    # Parse all job descriptions
    job_descriptions = parser.parse_directory(jd_dir)
    
    processed_data = []
    
    for jd in job_descriptions:
        text = jd['text']
        sections = cleaner.extract_sections(text)
        
        # Store processed data
        processed = {
            'filename': jd['filename'],
            'raw_text': text,
            'sections': sections,
            'word_count': jd['word_count']
        }
        
        processed_data.append(processed)
        print(f"✓ Processed: {jd['filename']}")
    
    # Save to JSON
    output_file = os.path.join(output_dir, 'processed_job_descriptions.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved {len(processed_data)} processed job descriptions to {output_file}")
    
    return processed_data

def main():
    """Main processing pipeline"""
    
    print("="*70)
    print("DOCUMENT PROCESSING PIPELINE")
    print("="*70)
    
    # Process resumes
    resumes = process_resumes()
    
    # Process job descriptions
    job_descriptions = process_job_descriptions()
    
    print("\n" + "="*70)
    print("PROCESSING COMPLETE!")
    print("="*70)
    print(f"\nProcessed Files:")
    print(f"  • {len(resumes)} resumes → data/processed/processed_resumes.json")
    print(f"  • {len(job_descriptions)} job descriptions → data/processed/processed_job_descriptions.json")
    print("\n✓ Ready for Phase 3: Skill Extraction & NLP")
    print("="*70)

if __name__ == "__main__":
    main()