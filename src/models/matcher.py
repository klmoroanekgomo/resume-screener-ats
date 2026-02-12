"""
Match resumes to job descriptions and calculate fit scores
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.skill_extractor import SkillExtractor

class ResumeJobMatcher:
    """Match resumes to job descriptions using multiple techniques"""
    
    def __init__(self, use_transformers=True):
        """
        Initialize the matcher
        
        Parameters:
        -----------
        use_transformers : bool
            Whether to use transformer models for semantic matching
        """
        
        self.skill_extractor = SkillExtractor(use_large_model=False)
        self.use_transformers = use_transformers
        
        # Initialize transformer model if requested
        if use_transformers:
            print("Loading transformer model (this may take a moment)...")
            self.transformer = SentenceTransformer('all-MiniLM-L6-v2')
            print("✓ Transformer model loaded")
        else:
            self.transformer = None
    
    def calculate_skill_match(self, resume_skills, job_skills):
        """
        Calculate skill match percentage
        
        Parameters:
        -----------
        resume_skills : list
            List of skills from resume
        job_skills : list
            List of required skills from job
            
        Returns:
        --------
        dict
            Dictionary with match details
        """
        
        if not job_skills:
            return {
                'match_percentage': 0,
                'matched_skills': [],
                'missing_skills': [],
                'extra_skills': []
            }
        
        resume_skills_set = set([s.lower() for s in resume_skills])
        job_skills_set = set([s.lower() for s in job_skills])
        
        # Find matches
        matched = resume_skills_set.intersection(job_skills_set)
        missing = job_skills_set.difference(resume_skills_set)
        extra = resume_skills_set.difference(job_skills_set)
        
        # Calculate percentage
        match_percentage = (len(matched) / len(job_skills_set)) * 100 if job_skills_set else 0
        
        # Convert back to original case
        matched_skills = [s for s in job_skills if s.lower() in matched]
        missing_skills = [s for s in job_skills if s.lower() in missing]
        extra_skills = [s for s in resume_skills if s.lower() in extra]
        
        return {
            'match_percentage': round(match_percentage, 2),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'extra_skills': extra_skills,
            'total_required': len(job_skills),
            'total_matched': len(matched)
        }
    
    def calculate_text_similarity(self, resume_text, job_text):
        """
        Calculate text similarity using TF-IDF and cosine similarity
        
        Parameters:
        -----------
        resume_text : str
            Resume text
        job_text : str
            Job description text
            
        Returns:
        --------
        float
            Similarity score (0-100)
        """
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return round(similarity * 100, 2)
        except:
            return 0.0
    
    def calculate_semantic_similarity(self, resume_text, job_text):
        """
        Calculate semantic similarity using transformers
        
        Parameters:
        -----------
        resume_text : str
            Resume text
        job_text : str
            Job description text
            
        Returns:
        --------
        float
            Similarity score (0-100)
        """
        
        if not self.transformer:
            return 0.0
        
        try:
            # Generate embeddings
            embeddings = self.transformer.encode([resume_text, job_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return round(similarity * 100, 2)
        except:
            return 0.0
    
    def calculate_experience_match(self, resume_years, job_required_years):
        """
        Calculate experience match score
        
        Parameters:
        -----------
        resume_years : int
            Years of experience from resume
        job_required_years : int
            Required years from job description
            
        Returns:
        --------
        dict
            Experience match details
        """
        
        if job_required_years == 0:
            return {
                'score': 100,
                'meets_requirement': True,
                'difference': 0
            }
        
        if resume_years >= job_required_years:
            score = 100
            meets_requirement = True
        else:
            # Partial credit for being close
            score = (resume_years / job_required_years) * 100
            meets_requirement = False
        
        return {
            'score': round(score, 2),
            'meets_requirement': meets_requirement,
            'difference': resume_years - job_required_years
        }
    
    def calculate_education_match(self, resume_education, job_education):
        """
        Calculate education match score
        
        Parameters:
        -----------
        resume_education : str
            Education level from resume
        job_education : str
            Required education from job
            
        Returns:
        --------
        dict
            Education match details
        """
        
        education_hierarchy = {
            'high_school': 1,
            'diploma': 2,
            'associate': 3,
            'bachelors': 4,
            'masters': 5,
            'phd': 6
        }
        
        resume_level = education_hierarchy.get(resume_education, 0)
        job_level = education_hierarchy.get(job_education, 0)
        
        if job_level == 0:
            return {
                'score': 100,
                'meets_requirement': True
            }
        
        if resume_level >= job_level:
            score = 100
            meets_requirement = True
        else:
            # Partial credit
            score = (resume_level / job_level) * 70  # Max 70% if under-qualified
            meets_requirement = False
        
        return {
            'score': round(score, 2),
            'meets_requirement': meets_requirement
        }
    
    def calculate_overall_fit_score(self, resume_data, job_data, weights=None):
        """
        Calculate overall fit score combining multiple factors
        
        Parameters:
        -----------
        resume_data : dict
            Resume profile data
        job_data : dict
            Job description data
        weights : dict
            Weights for different factors
            
        Returns:
        --------
        dict
            Complete matching results
        """
        
        # Default weights
        if weights is None:
            weights = {
                'skills': 0.40,
                'experience': 0.20,
                'education': 0.15,
                'text_similarity': 0.15,
                'semantic_similarity': 0.10
            }
        
        # Extract skills
        resume_skills = resume_data.get('skills', {}).get('skills', [])
        job_skills = job_data.get('skills', {}).get('skills', [])
        
        # Calculate skill match
        skill_match = self.calculate_skill_match(resume_skills, job_skills)
        
        # Calculate experience match
        resume_years = resume_data.get('years_experience', 0)
        job_years = 0  # Extract from job description if needed
        experience_match = self.calculate_experience_match(resume_years, job_years)
        
        # Calculate education match
        resume_edu = resume_data.get('education', {}).get('highest_level', 'unknown')
        job_edu = job_data.get('education', {}).get('highest_level', 'unknown')
        education_match = self.calculate_education_match(resume_edu, job_edu)
        
        # Calculate text similarity
        resume_text = resume_data.get('raw_text', '')
        job_text = job_data.get('raw_text', '')
        text_sim = self.calculate_text_similarity(resume_text, job_text)
        
        # Calculate semantic similarity (if enabled)
        semantic_sim = 0
        if self.use_transformers:
            semantic_sim = self.calculate_semantic_similarity(resume_text, job_text)
        
        # Calculate weighted overall score
        overall_score = (
            skill_match['match_percentage'] * weights['skills'] +
            experience_match['score'] * weights['experience'] +
            education_match['score'] * weights['education'] +
            text_sim * weights['text_similarity'] +
            semantic_sim * weights['semantic_similarity']
        )
        
        # Determine fit level
        if overall_score >= 80:
            fit_level = 'Excellent'
        elif overall_score >= 60:
            fit_level = 'Good'
        elif overall_score >= 40:
            fit_level = 'Fair'
        else:
            fit_level = 'Poor'
        
        return {
            'overall_score': round(overall_score, 2),
            'fit_level': fit_level,
            'skill_match': skill_match,
            'experience_match': experience_match,
            'education_match': education_match,
            'text_similarity': text_sim,
            'semantic_similarity': semantic_sim,
            'weights_used': weights
        }


def main():
    """Test the matcher"""
    
    import json
    
    print("="*70)
    print("RESUME-JOB MATCHER - TEST")
    print("="*70)
    
    # Load processed data
    with open('data/processed/processed_resumes.json', 'r', encoding='utf-8') as f:
        resumes = json.load(f)
    
    with open('data/processed/processed_job_descriptions.json', 'r', encoding='utf-8') as f:
        jobs = json.load(f)
    
    # Initialize matcher
    matcher = ResumeJobMatcher(use_transformers=True)
    
    # Extract profiles
    print("\n📊 EXTRACTING PROFILES...")
    print("-"*70)
    
    resume_profiles = []
    for resume in resumes:
        profile = matcher.skill_extractor.extract_complete_profile(
            resume['raw_text'],
            resume.get('sections', {})
        )
        profile['filename'] = resume['filename']
        profile['name'] = resume.get('name')
        profile['years_experience'] = resume.get('years_experience', 0)
        profile['raw_text'] = resume['raw_text']
        resume_profiles.append(profile)
        print(f"  ✓ {resume['filename']}")
    
    job_profiles = []
    for job in jobs:
        profile = matcher.skill_extractor.extract_complete_profile(
            job['raw_text'],
            job.get('sections', {})
        )
        profile['filename'] = job['filename']
        profile['raw_text'] = job['raw_text']
        job_profiles.append(profile)
        print(f"  ✓ {job['filename']}")
    
    # Test matching
    print("\n" + "="*70)
    print("MATCHING RESULTS")
    print("="*70)
    
    # Match each resume to each job
    for job in job_profiles:
        print(f"\n📋 JOB: {job['filename']}")
        print("-"*70)
        print(f"Required skills: {len(job['skills']['skills'])} skills")
        
        candidate_scores = []
        
        for resume in resume_profiles:
            result = matcher.calculate_overall_fit_score(resume, job)
            candidate_scores.append({
                'name': resume.get('name', 'Unknown'),
                'filename': resume['filename'],
                'score': result['overall_score'],
                'fit_level': result['fit_level'],
                'details': result
            })
        
        # Sort by score
        candidate_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Display top candidates
        print(f"\n  🏆 TOP CANDIDATES:")
        for i, candidate in enumerate(candidate_scores, 1):
            print(f"\n  {i}. {candidate['name']} ({candidate['filename']})")
            print(f"     Overall Score: {candidate['score']:.1f}% - {candidate['fit_level']}")
            
            details = candidate['details']
            print(f"     Skills Match: {details['skill_match']['match_percentage']:.1f}% " +
                  f"({details['skill_match']['total_matched']}/{details['skill_match']['total_required']})")
            print(f"     Text Similarity: {details['text_similarity']:.1f}%")
            
            if details['semantic_similarity'] > 0:
                print(f"     Semantic Similarity: {details['semantic_similarity']:.1f}%")
            
            # Show missing skills
            if details['skill_match']['missing_skills']:
                missing = details['skill_match']['missing_skills'][:5]
                print(f"     Missing Skills: {', '.join(missing)}")
                if len(details['skill_match']['missing_skills']) > 5:
                    print(f"       ... and {len(details['skill_match']['missing_skills']) - 5} more")
    
    print("\n" + "="*70)
    print("MATCHING TEST COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()