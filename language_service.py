import google.generativeai as genai
import json
from config import Config

class LanguageService:
    def __init__(self):
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        self.target_language = Config.TARGET_LANGUAGE
        self.source_language = Config.SOURCE_LANGUAGE
    
    def word_lookup(self, word: str, source_to_target: bool = True) -> dict:
        if source_to_target:
            prompt = f"""
            Translate the {self.source_language} word '{word}' to {self.target_language}.
            
            Return ONLY a JSON object with the following structure:
            {{
                "translation": "the translated word",
                "gender": "der/die/das or empty string if not applicable",
                "plural": "plural form or empty string if not applicable", 
                "examples": ["example sentence 1", "example sentence 2"]
            }}
            
            Do not include any other text, only the JSON object.
            """
        else:
            prompt = f"""
            For the {self.target_language} word '{word}', provide:
            
            Return ONLY a JSON object with the following structure:
            {{
                "translation": "the {self.source_language} translation",
                "gender": "der/die/das or empty string if not applicable",
                "plural": "plural form or empty string if not applicable",
                "examples": ["example sentence 1 in {self.target_language}", "example sentence 2 in {self.target_language}"]
            }}
            
            Do not include any other text, only the JSON object.
            """
        
        try:
            response = self.model.generate_content(prompt)
            # Parse the JSON response
            result = json.loads(response.text.strip())
            return result
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON response: {str(e)}", "translation": "", "gender": "", "plural": "", "examples": []}
        except Exception as e:
            return {"error": f"Could not process word lookup: {str(e)}", "translation": "", "gender": "", "plural": "", "examples": []}
    
    def grammar_explanation(self, text: str, is_question: bool = False) -> str:
        if is_question:
            prompt = f"""
            Answer this {self.target_language} grammar question: '{text}'
            
            Provide a clear, helpful explanation suitable for a language learner.
            Include examples when appropriate.
            """
        else:
            prompt = f"""
            Analyze this {self.target_language} sentence or phrase: '{text}'
            
            1. Check if the grammar is correct
            2. If incorrect, provide the corrected version
            3. Explain any grammar rules that apply
            4. Provide additional examples if helpful
            
            Format your response clearly for a language learner.
            """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: Could not process grammar explanation. {str(e)}"


if __name__ == "__main__":
    service = LanguageService()
    print(service.word_lookup("Haus", source_to_target=False))
    print(service.grammar_explanation("Ich gehe zu der Schule.", is_question=False))