# Word Frequency Analysis App with AI Agent

A powerful document analysis tool that extracts text from PDF, DOCX, and TXT files, calculates word frequency distributions, and provides an AI-powered chat interface powered by Ollama.

## Features

- **Document Processing**: Extract text from PDF, DOCX, and TXT files
- **Word Frequency Analysis**: Calculate and visualize word frequency distributions
- **Interactive Visualizations**: Bar charts and data tables
- **AI Chat Interface**: Powered by Ollama for intelligent document analysis
- **Modern UI**: Built with Streamlit for an intuitive user experience

## Tech Stack

- **Python 3.11+**
- **Streamlit** - Web UI framework
- **PyMuPDF (fitz)** - PDF text extraction
- **python-docx** - DOCX text extraction
- **Ollama** - Local LLM backend
- **Altair** - Interactive visualizations
- **Matplotlib** - Chart generation

## Prerequisites

1. **Python 3.11 or higher**
2. **Ollama** installed and running locally

### Installing Ollama

#### Windows
```bash
# Download and install from https://ollama.ai
# Or use winget
winget install Ollama.Ollama
```

#### macOS
```bash
# Install via Homebrew
brew install ollama

# Or download from https://ollama.ai
```

#### Linux
```bash
# Install via curl
curl -fsSL https://ollama.ai/install.sh | sh
```

### Setting up Ollama

1. **Start Ollama service**:
   ```bash
   ollama serve
   ```

2. **Pull a model** (choose one):
   ```bash
   # Llama2 (recommended for this app)
   ollama pull llama2
   
   # Or other models
   ollama pull mistral
   ollama pull codellama
   ```

3. **Verify installation**:
   ```bash
   ollama list
   ```

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** to `http://localhost:8501`

4. **Upload a document** (PDF, DOCX, or TXT)

5. **Analyze and chat** with the AI about your document!

## How It Works

### Document Processing Flow

1. **File Upload**: User uploads a PDF, DOCX, or TXT file
2. **Text Extraction**: The `frequency_tool.py` extracts text using appropriate libraries
3. **Word Analysis**: Text is processed to calculate word frequency distribution
4. **Visualization**: Results are displayed as interactive charts and tables
5. **AI Chat**: Ollama provides intelligent analysis and answers about the document

### Frequency Analysis

The tool performs sophisticated text analysis:

- **Text Cleaning**: Removes special characters and normalizes case
- **Stop Word Filtering**: Removes common words (a, an, the, etc.)
- **Word Length Filtering**: Excludes very short words (1-2 characters)
- **Frequency Counting**: Uses Python's Counter for efficient counting
- **JSON Output**: Structured data for easy processing

### AI Integration

The Ollama integration provides:

- **Context-Aware Responses**: AI receives document analysis results
- **Multiple Model Support**: Choose from various Ollama models
- **Conversation History**: Maintains chat context
- **Error Handling**: Graceful fallbacks for connection issues

## File Structure

```
word-frequency-app/
├── app.py                 # Main Streamlit application
├── frequency_tool.py      # Text extraction and analysis tool
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

### Ollama Models

The app supports various Ollama models. You can change the model in the sidebar:

- `llama2` (default)
- `llama2:7b`
- `llama2:13b`
- `mistral`
- `codellama`

### Analysis Parameters

- **Top N Words**: Adjust the number of most frequent words to analyze (5-100)
- **File Types**: PDF, DOCX, TXT supported
- **Chart Types**: Interactive Altair charts and Matplotlib fallback

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**:
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is installed: `ollama list`
   - Verify the model name in the app matches your installed model

2. **File Processing Error**:
   - Ensure the file is not corrupted
   - Check file format is supported (PDF, DOCX, TXT)
   - Try with a smaller file first

3. **Dependencies Issues**:
   - Update pip: `pip install --upgrade pip`
   - Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

4. **Memory Issues**:
   - Use smaller documents for analysis
   - Reduce the "Top N Words" setting
   - Close other applications to free up memory

### Performance Tips

- **Large Documents**: For very large files, consider splitting them first
- **Model Selection**: Smaller models (like llama2:7b) are faster but less capable
- **Batch Processing**: The app processes one document at a time for optimal performance

## API Reference

### frequency_tool.py

```python
def extract_text(file_path: str) -> str:
    """Extract text from supported file formats."""

def word_frequency(text: str, top_n: int = 20) -> str:
    """Calculate word frequency and return JSON."""

def frequency_tool(file_path: str, top_n: int = 20) -> str:
    """Main function combining extraction and analysis."""
```

### Ollama Integration

```python
def query_ollama(prompt: str, model: str = "llama2") -> str:
    """Query Ollama API for AI responses."""
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Verify Ollama is properly installed and running
3. Ensure all dependencies are correctly installed
4. Check the console output for error messages

## Future Enhancements

- Support for more file formats (RTF, ODT, etc.)
- Advanced text analysis (sentiment, topics, etc.)
- Batch processing capabilities
- Export functionality for results
- Custom stop word lists
- Multi-language support


