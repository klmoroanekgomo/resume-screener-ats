"""
Extract skills from resume and job description text using NLP
"""

import spacy
import re
from fuzzywuzzy import fuzz
from collections import Counter
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.skill_database import (
    get_all_skills, normalize_skill, get_skill_category,
    EDUCATION_LEVELS, EXPERIENCE_KEYWORDS, CERTIFICATIONS
)

class SkillExtractor:
    """Extract skills from text using NLP and pattern matching"""
    
    def __init__(self, use_large_model=False):
        """
        Initialize the skill extractor
        
        Parameters:
        -----------
        use_large_model : bool
            Whether to use the large spaCy model (more accurate but slower)
        """
        
        # Load spaCy model
        model_name = 'en_core_web_lg' if use_large_model else 'en_core_web_sm'
        try:
            self.nlp = spacy.load(model_name)
            print(f"✓ Loaded spaCy model: {model_name}")
        except:
            print(f"❌ Model {model_name} not found. Downloading...")
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', model_name])
            self.nlp = spacy.load(model_name)
        
        # Get skills database
        self.all_skills = get_all_skills()
        self.all_skills_lower = {skill.lower(): skill for skill in self.all_skills}
        
        # Fuzzy matching threshold (0-100)
        self.fuzzy_threshold = 85
    
    def extract_skills(self, text, use_fuzzy=True):
        """
        Extract skills from text
        
        Parameters:
        -----------
        text : str
            Text to extract skills from
        use_fuzzy : bool
            Whether to use fuzzy matching for skill extraction
            
        Returns:
        --------
        dict
            Dictionary with found skills and their details
        """
        
        if not text:
            return {'skills': [], 'skill_count': {}, 'categories': {}}
        
        found_skills = set()
        skill_positions = []
        
        # Method 1: Exact matching (case-insensitive)
        text_lower = text.lower()
        for skill_lower, skill_original in self.all_skills_lower.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            matches = re.finditer(pattern, text_lower)
            
            for match in matches:
                found_skills.add(skill_original)
                skill_positions.append({
                    'skill': skill_original,
                    'position': match.start(),
                    'method': 'exact'
                })
        
        # Method 2: Fuzzy matching (optional, slower but catches variations)
        if use_fuzzy:
            # Process text with spaCy
            doc = self.nlp(text)
            
            # Extract noun chunks and named entities
            candidates = set()
            
            # Noun chunks
            for chunk in doc.noun_chunks:
                candidates.add(chunk.text)
            
            # Named entities (especially ORG and PRODUCT)
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                    candidates.add(ent.text)
            
            # Also check individual tokens
            for token in doc:
                if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
                    candidates.add(token.text)
            
            # Fuzzy match candidates against skill database
            for candidate in candidates:
                best_match = None
                best_score = 0
                
                for skill in self.all_skills:
                    score = fuzz.ratio(candidate.lower(), skill.lower())
                    
                    if score > best_score:
                        best_score = score
                        best_match = skill
                
                # Add if score is above threshold and not already found
                if best_score >= self.fuzzy_threshold and best_match not in found_skills:
                    found_skills.add(best_match)
                    skill_positions.append({
                        'skill': best_match,
                        'position': text_lower.find(candidate.lower()),
                        'method': 'fuzzy',
                        'score': best_score
                    })
        
        # Categorize skills
        skill_categories = {}
        for skill in found_skills:
            category = get_skill_category(skill)
            if category not in skill_categories:
                skill_categories[category] = []
            skill_categories[category].append(skill)
        
        # Count skill occurrences
        skill_count = Counter([pos['skill'] for pos in skill_positions])
        
        return {
            'skills': sorted(list(found_skills)),
            'skill_count': dict(skill_count),
            'categories': skill_categories,
            'total_skills': len(found_skills),
            'skill_positions': skill_positions
        }
    
    def extract_education(self, text):
        """
        Extract education level from text
        
        Parameters:
        -----------
        text : str
            Resume text
            
        Returns:
        --------
        dict
            Dictionary with education details
        """
        
        found_degrees = []
        text_upper = text.upper()
        
        for level, keywords in EDUCATION_LEVELS.items():
            for keyword in keywords:
                if keyword.upper() in text_upper:
                    found_degrees.append({
                        'level': level,
                        'keyword': keyword
                    })
                    break  # Found this level, move to next
        
        # Get highest education level
        level_hierarchy = ['high_school', 'diploma', 'associate', 'bachelors', 'masters', 'phd']
        highest_level = None
        
        for level in reversed(level_hierarchy):
            if any(d['level'] == level for d in found_degrees):
                highest_level = level
                break
        
        return {
            'found_degrees': found_degrees,
            'highest_level': highest_level,
            'has_degree': len(found_degrees) > 0
        }
    
    def extract_experience_level(self, text):
        """
        Extract experience level from text
        
        Parameters:
        -----------
        text : str
            Resume or job description text
            
        Returns:
        --------
        str
            Experience level (senior, mid, junior, intern)
        """
        
        text_lower = text.lower()
        
        for level, keywords in EXPERIENCE_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return level
        
        return 'unknown'
    
    def extract_certifications(self, text):
        """
        Extract certifications from text
        
        Parameters:
        -----------
        text : str
            Resume text
            
        Returns:
        --------
        list
            List of found certifications
        """
        
        found_certs = []
        text_lower = text.lower()
        
        for cert in CERTIFICATIONS:
            if cert.lower() in text_lower:
                found_certs.append(cert)
        
        return found_certs
    
    def extract_complete_profile(self, text, sections=None):
        """
        Extract complete candidate/job profile
        
        Parameters:
        -----------
        text : str
            Full text
        sections : dict
            Pre-extracted sections (optional)
            
        Returns:
        --------
        dict
            Complete profile with skills, education, certifications, etc.
        """
        
        # Extract skills
        skills_data = self.extract_skills(text, use_fuzzy=True)
        
        # Extract education
        education_data = self.extract_education(text)
        
        # Extract experience level
        experience_level = self.extract_experience_level(text)
        
        # Extract certifications
        certifications = self.extract_certifications(text)
        
        # If sections provided, try to extract skills from specific sections
        section_skills = {}
        if sections:
            for section_name, section_text in sections.items():
                if section_text:
                    section_data = self.extract_skills(section_text, use_fuzzy=False)
                    section_skills[section_name] = section_data['skills']
        
        return {
            'skills': skills_data,
            'education': education_data,
            'experience_level': experience_level,
            'certifications': certifications,
            'section_skills': section_skills
        }


def main():
    """Test the skill extractor"""
    
    import json
    
    print("="*70)
    print("SKILL EXTRACTOR - TEST")
    print("="*70)
    
    # Initialize extractor
    extractor = SkillExtractor(use_large_model=False)
    
    # Load processed resumes
    with open('data/processed/processed_resumes.json', 'r', encoding='utf-8') as f:
        resumes = json.load(f)
    
    if not resumes:
        print("❌ No processed resumes found")
        return
    
    # Test on first resume
    resume = resumes[0]
    print(f"\n📄 ANALYZING RESUME: {resume['filename']}")
    print("-"*70)
    
    # Extract complete profile
    profile = extractor.extract_complete_profile(
        resume['raw_text'],
        resume.get('sections', {})
    )
    
    # Display results
    print(f"\n🔧 SKILLS EXTRACTED")
    print("-"*70)
    skills_data = profile['skills']
    print(f"  Total unique skills found: {skills_data['total_skills']}")
    
    print(f"\n  Skills by category:")
    for category, skills in skills_data['categories'].items():
        print(f"    {category:25s}: {len(skills):2d} skills")
        print(f"      → {', '.join(skills[:5])}")
        if len(skills) > 5:
            print(f"        ... and {len(skills) - 5} more")
    
    print(f"\n  Most mentioned skills:")
    top_skills = sorted(
        skills_data['skill_count'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    for skill, count in top_skills:
        print(f"    {skill:30s}: {count} mention(s)")
    
    # Education
    print(f"\n🎓 EDUCATION")
    print("-"*70)
    edu_data = profile['education']
    print(f"  Highest level: {edu_data['highest_level'] or 'Not found'}")
    print(f"  Found degrees: {len(edu_data['found_degrees'])}")
    for degree in edu_data['found_degrees']:
        print(f"    • {degree['keyword']} ({degree['level']})")
    
    # Experience level
    print(f"\n💼 EXPERIENCE LEVEL")
    print("-"*70)
    print(f"  Level: {profile['experience_level']}")
    
    # Certifications
    print(f"\n📜 CERTIFICATIONS")
    print("-"*70)
    if profile['certifications']:
        for cert in profile['certifications']:
            print(f"  • {cert}")
    else:
        print("  None found")
    
    # Section-specific skills
    if profile['section_skills']:
        print(f"\n📋 SKILLS BY SECTION")
        print("-"*70)
        for section, skills in profile['section_skills'].items():
            if skills:
                print(f"  {section.upper()}: {len(skills)} skills")
                print(f"    → {', '.join(skills[:5])}")
    
    print("\n" + "="*70)
    print("SKILL EXTRACTION TEST COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()