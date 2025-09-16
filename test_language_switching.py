#!/usr/bin/env python3
"""
Test script for language switching functionality
"""

from app import word_lookup_handler, language_service
from language_service import LanguageService

def test_language_switching():
    """Test the language switching functionality"""
    
    print("🧪 Testing Language Switching Functionality")
    print("=" * 50)
    
    # Test word lookup with different languages
    test_word = "cat"
    
    languages = ["German", "French", "Spanish", "Italian"]
    
    for lang in languages:
        print(f"\n=== Testing {lang} ===")
        language_service.set_target_language(lang)
        
        # Test English to target language
        direction = f"English → {lang}"
        result = word_lookup_handler(test_word, direction)
        
        print(f"Word: {test_word}")
        print(f"Direction: {direction}")
        print(f"Translation: {result[0]}")
        print(f"Gender: {result[1]}")
        print(f"Plural: {result[2]}")
        
        if result[3]:  # Examples
            print(f"Examples: {result[3][:100]}...")
        
        # Check if translation is actually in target language
        if result[0] and result[0] != test_word:
            print("✅ Translation successful")
        else:
            print("❌ Translation failed or returned source word")

def test_language_service_directly():
    """Test the language service methods directly"""
    
    print("\n\n🔧 Testing Language Service Directly")
    print("=" * 50)
    
    service = LanguageService()
    
    for lang in ["German", "French", "Spanish", "Italian"]:
        print(f"\n--- Testing {lang} ---")
        service.set_target_language(lang)
        print(f"Current target language: {service.get_target_language()}")
        
        result = service.word_lookup("hello", source_to_target=True)
        print(f"'hello' → {result.get('translation', 'ERROR')}")

if __name__ == "__main__":
    test_language_switching()
    test_language_service_directly()
    print("\n🎉 Testing complete!")