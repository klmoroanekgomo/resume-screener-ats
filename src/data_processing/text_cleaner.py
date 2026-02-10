"""
Clean and preprocess extracted text
"""

import re
import string

class TextCleaner:
    """Clean and normalize text from resumes and job descriptions"""
    
    def __init__(self):
        # Regex patterns
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
        self.url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        self.github_pattern = r'github\.com/[\w-]+'
    
    def clean_text(self, text, preserve_structure=True):
        """
        Clean text while preserving important information
        
        Parameters:
        -----------
        text : str
            Raw text to clean
        preserve_structure : bool
            Whether to preserve line breaks and structure
            
        Returns:
        --------
        str
            Cleaned text
        """
        
        if not text:
            return ""
        
        # Remove extra whitespace but preserve line breaks if needed
        if preserve_structure:
            text = re.sub(r' +', ' ', text)  # Multiple spaces to single
            text = re.sub(r'\n+', '\n', text)  # Multiple newlines to single
            text = re.sub(r'\t+', ' ', text)  # Tabs to spaces
        else:
            text = re.sub(r'\s+', ' ', text)  # All whitespace to single space
        
        # Remove bullet points and special characters but keep important ones
        # Keep: alphanumeric, spaces, newlines, periods, commas, hyphens, +, #, (), /
        text = re.sub(r'[•●◦▪▫]', '', text)  # Remove bullet points
        
        return text.strip()
    
    def extract_contact_info(self, text):
        """
        Extract contact information from text
        
        Parameters:
        -----------
        text : str
            Resume text
            
        Returns:
        --------
        dict
            Dictionary with email, phone, and URLs
        """
        
        # Extract email
        emails = re.findall(self.email_pattern, text)
        
        # Extract phone
        phones = re.findall(self.phone_pattern, text)
        
        # Extract LinkedIn
        linkedin = re.findall(self.linkedin_pattern, text, re.IGNORECASE)
        
        # Extract GitHub
        github = re.findall(self.github_pattern, text, re.IGNORECASE)
        
        # Extract generic URLs
        urls = re.findall(self.url_pattern, text)
        
        return {
            'email': emails[0] if emails else None,
            'phone': phones[0] if phones else None,
            'linkedin': linkedin[0] if linkedin else None,
            'github': github[0] if github else None,
            'urls': urls
        }
    
    def extract_name(self, text):
        """
        Extract candidate name (usually first line or before email)
        
        Parameters:
        -----------
        text : str
            Resume text
            
        Returns:
        --------
        str
            Candidate name
        """
        
        lines = text.strip().split('\n')
        
        # Check first few lines for name
        for line in lines[:5]:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip lines with email or phone
            if re.search(self.email_pattern, line) or re.search(self.phone_pattern, line):
                continue
            
            # Skip lines with URLs
            if re.search(self.url_pattern, line):
                continue
            
            # Check if line looks like a name (2-4 words, each capitalized)
            words = line.split()
            if 2 <= len(words) <= 4:
                if all(word[0].isupper() for word in words if word):
                    return line
        
        return None
    
    def extract_sections(self, text):
        """
        Extract common resume sections
        
        Parameters:
        -----------
        text : str
            Resume text
            
        Returns:
        --------
        dict
            Dictionary with different sections
        """
        
        text_upper = text.upper()
        sections = {}
        
        # Common section headers and their variations
        section_keywords = {
            'summary': ['SUMMARY', 'PROFILE', 'OBJECTIVE', 'ABOUT', 'PROFESSIONAL SUMMARY'],
            'experience': ['EXPERIENCE', 'WORK HISTORY', 'EMPLOYMENT', 'PROFESSIONAL EXPERIENCE', 'WORK EXPERIENCE'],
            'education': ['EDUCATION', 'ACADEMIC', 'QUALIFICATIONS', 'ACADEMIC BACKGROUND'],
            'skills': ['SKILLS', 'TECHNICAL SKILLS', 'CORE COMPETENCIES', 'EXPERTISE', 'TECHNICAL EXPERTISE'],
            'certifications': ['CERTIFICATIONS', 'CERTIFICATES', 'LICENSES', 'PROFESSIONAL CERTIFICATIONS'],
            'projects': ['PROJECTS', 'KEY PROJECTS', 'NOTABLE PROJECTS'],
            'awards': ['AWARDS', 'HONORS', 'ACHIEVEMENTS', 'RECOGNITION'],
            'publications': ['PUBLICATIONS', 'PAPERS', 'RESEARCH']
        }
        
        # Find all section positions
        section_positions = []
        for section_name, keywords in section_keywords.items():
            for keyword in keywords:
                pos = text_upper.find(keyword)
                if pos != -1:
                    # Make sure it's at the start of a line (or near start)
                    # Check characters before to ensure it's a header
                    start_of_line = text_upper.rfind('\n', 0, pos)
                    if start_of_line == -1 or pos - start_of_line < 5:
                        section_positions.append((pos, section_name, keyword))
                        break  # Found this section, move to next
        
        # Sort by position
        section_positions.sort()
        
        # Extract text for each section
        for i, (pos, section_name, keyword) in enumerate(section_positions):
            # Find end position (start of next section or end of text)
            if i < len(section_positions) - 1:
                end_pos = section_positions[i + 1][0]
            else:
                end_pos = len(text)
            
            # Extract section text
            section_text = text[pos:end_pos].strip()
            
            # Remove the section header from the text
            section_text = re.sub(f'^{re.escape(keyword)}[:\s]*', '', section_text, flags=re.IGNORECASE)
            
            sections[section_name] = section_text.strip()
        
        return sections
    
    def normalize_text(self, text):
        """
        Normalize text for comparison (lowercase, remove extra chars)
        
        Parameters:
        -----------
        text : str
            Text to normalize
            
        Returns:
        --------
        str
            Normalized text
        """
        
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_years_of_experience(self, text):
        """
        Extract years of experience from text
        
        Parameters:
        -----------
        text : str
            Resume text
            
        Returns:
        --------
        int
            Estimated years of experience
        """
        
        # Look for patterns like "5 years", "5+ years", "5-7 years"
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
            r'(\d+)\s*-\s*\d+\s*years?\s*(?:of\s*)?experience'
        ]
        
        max_years = 0
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                years = int(match)
                max_years = max(max_years, years)
        
        # Also try to estimate from work experience dates
        # Look for year patterns (e.g., 2020 - 2023, 2019 - Present)
        date_patterns = [
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*-\s*(?:present|current)',
        ]
        
        current_year = 2024
        total_experience = 0
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                start_year = int(match[0])
                if len(match) > 1 and match[1].isdigit():
                    end_year = int(match[1])
                else:
                    end_year = current_year
                
                duration = end_year - start_year
                if 0 < duration < 50:  # Sanity check
                    total_experience += duration
        
        return max(max_years, total_experience)


def main():
    """Test the text cleaner"""
    
    import sys
    import os
    
    # Add parent directory to path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from data_processing.pdf_parser import DocumentParser
    
    print("="*70)
    print("TEXT CLEANER - TEST")
    print("="*70)
    
    # Parse a sample resume
    parser = DocumentParser()
    resumes = parser.parse_directory('data/sample/resumes')
    
    if not resumes:
        print("❌ No resumes found to test")
        return
    
    cleaner = TextCleaner()
    resume_text = resumes[0]['text']
    
    print("\n1️⃣  CONTACT INFORMATION EXTRACTION")
    print("-"*70)
    contact_info = cleaner.extract_contact_info(resume_text)
    for key, value in contact_info.items():
        print(f"  {key.capitalize()}: {value}")
    
    print("\n2️⃣  NAME EXTRACTION")
    print("-"*70)
    name = cleaner.extract_name(resume_text)
    print(f"  Candidate Name: {name}")
    
    print("\n3️⃣  YEARS OF EXPERIENCE")
    print("-"*70)
    years = cleaner.extract_years_of_experience(resume_text)
    print(f"  Estimated Experience: {years} years")
    
    print("\n4️⃣  SECTION EXTRACTION")
    print("-"*70)
    sections = cleaner.extract_sections(resume_text)
    print(f"  Found {len(sections)} sections:")
    for section_name in sections.keys():
        print(f"    • {section_name.upper()}")
    
    # Show a sample section
    if 'skills' in sections:
        print(f"\n  SKILLS SECTION (first 200 chars):")
        print(f"  {'-'*66}")
        print(f"  {sections['skills'][:200]}...")
    
    print("\n5️⃣  TEXT CLEANING")
    print("-"*70)
    cleaned = cleaner.clean_text(resume_text, preserve_structure=False)
    print(f"  Original length: {len(resume_text):,} characters")
    print(f"  Cleaned length: {len(cleaned):,} characters")
    print(f"  Reduction: {((len(resume_text) - len(cleaned)) / len(resume_text) * 100):.1f}%")
    
    print("\n6️⃣  TEXT NORMALIZATION")
    print("-"*70)
    sample_text = "Python, Django, and AWS Experience!"
    normalized = cleaner.normalize_text(sample_text)
    print(f"  Original: {sample_text}")
    print(f"  Normalized: {normalized}")
    
    print("\n" + "="*70)
    print("TEXT CLEANING TEST COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()