"""
Extract text from PDF, DOCX, and TXT files
"""

import PyPDF2
import pdfplumber
import docx
import re
import os

class DocumentParser:
    """Parse resumes and job descriptions from various file formats"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt']
    
    def parse_file(self, filepath):
        """
        Parse a file and extract text
        
        Parameters:
        -----------
        filepath : str
            Path to the file
            
        Returns:
        --------
        dict
            Dictionary with filename and extracted text
        """
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        file_ext = os.path.splitext(filepath)[1].lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        if file_ext == '.pdf':
            text = self._parse_pdf(filepath)
        elif file_ext == '.docx':
            text = self._parse_docx(filepath)
        elif file_ext == '.txt':
            text = self._parse_txt(filepath)
        
        return {
            'filename': os.path.basename(filepath),
            'filepath': filepath,
            'text': text,
            'word_count': len(text.split()),
            'char_count': len(text)
        }
    
    def _parse_pdf(self, filepath):
        """Extract text from PDF using pdfplumber (better formatting)"""
        text = ""
        
        try:
            # Try pdfplumber first (better text extraction)
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"⚠ pdfplumber failed, trying PyPDF2: {e}")
            # Fallback to PyPDF2
            try:
                with open(filepath, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e2:
                print(f"❌ PyPDF2 also failed: {e2}")
                raise
        
        return text.strip()
    
    def _parse_docx(self, filepath):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(filepath)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {e}")
    
    def _parse_txt(self, filepath):
        """Extract text from TXT file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing TXT: {e}")
    
    def parse_directory(self, directory_path):
        """
        Parse all supported files in a directory
        
        Parameters:
        -----------
        directory_path : str
            Path to directory containing files
            
        Returns:
        --------
        list
            List of dictionaries with parsed documents
        """
        
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        documents = []
        failed_files = []
        
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            
            if os.path.isfile(filepath):
                file_ext = os.path.splitext(filename)[1].lower()
                
                if file_ext in self.supported_formats:
                    try:
                        doc = self.parse_file(filepath)
                        documents.append(doc)
                        print(f"✓ Parsed: {filename} ({doc['word_count']} words)")
                    except Exception as e:
                        print(f"❌ Error parsing {filename}: {e}")
                        failed_files.append(filename)
        
        if failed_files:
            print(f"\n⚠ Failed to parse {len(failed_files)} file(s):")
            for f in failed_files:
                print(f"  - {f}")
        
        return documents
    
    def get_file_info(self, filepath):
        """Get basic file information without parsing"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        file_stats = os.stat(filepath)
        
        return {
            'filename': os.path.basename(filepath),
            'filepath': filepath,
            'size_bytes': file_stats.st_size,
            'size_kb': round(file_stats.st_size / 1024, 2),
            'extension': os.path.splitext(filepath)[1]
        }


def main():
    """Test the document parser"""
    
    print("="*70)
    print("DOCUMENT PARSER - TEST")
    print("="*70)
    
    parser = DocumentParser()
    
    # Test parsing resumes
    print("\n📄 PARSING RESUMES")
    print("-"*70)
    resume_dir = 'data/sample/resumes'
    
    if os.path.exists(resume_dir):
        resumes = parser.parse_directory(resume_dir)
        print(f"\n✓ Total resumes parsed: {len(resumes)}")
        
        if resumes:
            print("\n" + "="*70)
            print("SAMPLE RESUME ANALYSIS")
            print("="*70)
            sample = resumes[0]
            print(f"Filename: {sample['filename']}")
            print(f"Word Count: {sample['word_count']:,}")
            print(f"Character Count: {sample['char_count']:,}")
            print(f"\nFirst 300 characters:")
            print("-"*70)
            print(sample['text'][:300] + "...")
    else:
        print(f"❌ Directory not found: {resume_dir}")
    
    # Test parsing job descriptions
    print("\n\n📋 PARSING JOB DESCRIPTIONS")
    print("-"*70)
    jd_dir = 'data/sample/job_descriptions'
    
    if os.path.exists(jd_dir):
        jobs = parser.parse_directory(jd_dir)
        print(f"\n✓ Total job descriptions parsed: {len(jobs)}")
        
        if jobs:
            print("\n" + "="*70)
            print("SAMPLE JOB DESCRIPTION ANALYSIS")
            print("="*70)
            sample = jobs[0]
            print(f"Filename: {sample['filename']}")
            print(f"Word Count: {sample['word_count']:,}")
            print(f"Character Count: {sample['char_count']:,}")
            print(f"\nFirst 300 characters:")
            print("-"*70)
            print(sample['text'][:300] + "...")
    else:
        print(f"❌ Directory not found: {jd_dir}")
    
    print("\n" + "="*70)
    print("PARSING TEST COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()