import re
import json
import fitz  # PyMuPDF
import docx
from collections import Counter
import sys

def extract_text(file_path: str) -> str:
    """Extract text from PDF, DOCX, or TXT files."""
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        text = " ".join([page.get_text() for page in doc])
        doc.close()
        return text
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return " ".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file format. Supported formats: PDF, DOCX, TXT")

def word_frequency(text: str, top_n: int = 20) -> str:
    """Calculate word frequency distribution and return as JSON."""
    # Clean and tokenize text
    words = re.findall(r"\b\w+\b", text.lower())
    
    # Filter out very short words (1-2 characters) and common stop words
    stop_words = {'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 
                  'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 
                  'to', 'was', 'will', 'with', 'i', 'you', 'we', 'they', 'this', 
                  'these', 'those', 'or', 'but', 'if', 'so', 'do', 'does', 'did'}
    
    # Filter words
    filtered_words = [word for word in words if len(word) > 2 and word not in stop_words]
    
    # Count frequency
    counter = Counter(filtered_words)
    freq = counter.most_common(top_n)
    
    # Convert to JSON format
    result = [{"word": word, "count": count} for word, count in freq]
    return json.dumps(result, indent=2)

def frequency_tool(file_path: str, top_n: int = 20) -> str:
    """Main function to extract text and calculate word frequency."""
    try:
        text = extract_text(file_path)
        if not text.strip():
            return json.dumps([{"error": "No text found in the document"}], indent=2)
        return word_frequency(text, top_n)
    except Exception as e:
        return json.dumps([{"error": f"Error processing file: {str(e)}"}], indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python frequency_tool.py <file_path> [top_n]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    result = frequency_tool(file_path, top_n)
    print(result)
