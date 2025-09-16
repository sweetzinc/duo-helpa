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
    
    def set_target_language(self, language: str):
        """Update the target language for translation and grammar services"""
        if language in Config.SUPPORTED_LANGUAGES:
            self.target_language = language
        else:
            raise ValueError(f"Unsupported language: {language}. Supported languages: {Config.SUPPORTED_LANGUAGES}")
    
    def get_target_language(self) -> str:
        """Get the current target language"""
        return self.target_language
    
    def word_lookup(self, word: str, source_to_target: bool = True) -> dict:
        if source_to_target:
            prompt = f"""
            Translate the {self.source_language} word '{word}' to {self.target_language}.
            
            Return ONLY a JSON object with the following structure:
            {{
                "translation": "the translated word in target language",
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
            response_text = response.text.strip()
            if response_text[0] != "{" :
                find_start = response_text.find("{")
                find_end = response_text.find("}", find_start)
                response_text = response_text[find_start:find_end + 1]
            # Parse the JSON response
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON response: {str(e)}", "translation": "", "gender": "", "plural": "", "examples": [text]}
        except Exception as e:
            return {"error": f"Could not process word lookup: {str(e)}", "translation": "", "gender": "", "plural": "", "examples": [text]}
    
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
    
    def sentence_correction(self, text: str) -> dict:
        """Analyze sentence for grammar and return structured JSON response"""
        prompt = f"""
        Analyze this {self.target_language} sentence for grammar correctness: '{text}'
        
        Return ONLY a JSON object with the following structure:
        {{
            "grammar check": true/false (boolean indicating if grammar is correct),
            "corrected version": "the corrected sentence if applicable, or the original if correct",
            "Applicable grammar explained": "explanation of grammar rules in markdown format"
        }}
        
        Do not include any other text, only the JSON object.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response if it contains extra text
            if response_text[0] != "{":
                find_start = response_text.find("{")
                find_end = response_text.rfind("}") + 1
                if find_start != -1 and find_end != 0:
                    response_text = response_text[find_start:find_end]
            
            # Parse the JSON response
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON response: {str(e)}"}
        except Exception as e:
            return {"error": f"Could not process sentence correction: {str(e)}"}


if __name__ == "__main__":
    service = LanguageService()
    print(service.word_lookup("Haus", source_to_target=False))
    print(service.word_lookup("Cat", source_to_target=True))
    print(service.grammar_explanation("Ich gehe zu der Schule.", is_question=False))
