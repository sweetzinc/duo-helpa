# Setup Instructions

## Prerequisites
- Python 3.8 or higher
- A Google Gemini API key

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   TARGET_LANGUAGE=German
   SOURCE_LANGUAGE=English
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

## Getting a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key and paste it into your `.env` file

## Deployment to HuggingFace Spaces

1. Create a new Space on [HuggingFace](https://huggingface.co/new-space)
2. Choose "Gradio" as the SDK
3. Upload all files except `.env`
4. Add your `GEMINI_API_KEY` as a Space secret in the Settings tab
5. The app will automatically deploy

## Usage

- **Word Lookup**: Enter a word and select translation direction
- **Grammar Help**: Ask questions or check sentence grammar
- **Mobile Friendly**: Works well on smartphones and tablets