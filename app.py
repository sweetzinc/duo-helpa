import gradio as gr
from language_service import LanguageService
from config import Config

# Initialize the language service
language_service = LanguageService()

def word_lookup_handler(word, direction):
    """Handle word lookup requests"""
    if not word.strip():
        return "", "", "", "Please enter a word to look up."
    
    source_to_target = direction == f"{Config.SOURCE_LANGUAGE} → {Config.TARGET_LANGUAGE}"
    result = language_service.word_lookup(word.strip(), source_to_target)
    
    if "error" in result:
        return "", "", "", result["error"]
    
    # Extract individual components
    translation = result.get("translation", "")
    gender = result.get("gender", "")
    plural = result.get("plural", "")
    examples = result.get("examples", [])
    examples_text = "\n".join(examples) if examples else ""
    
    return translation, gender, plural, examples_text

def grammar_explanation_handler(text, mode):
    """Handle grammar explanation requests"""
    if not text.strip():
        return "Please enter text for grammar explanation."
    
    is_question = mode == "Grammar Question"
    result = language_service.grammar_explanation(text.strip(), is_question)
    return result

def sentence_correction_handler(text):
    """Handle sentence correction requests with JSON output"""
    if not text.strip():
        return "Please enter a sentence.", "", "Please enter text for correction."
    
    result = language_service.sentence_correction(text.strip())
    
    if isinstance(result, dict) and "error" not in result:
        grammar_status = "✅ Correct" if result.get("grammar check", False) else "❌ Needs Correction"
        corrected = result.get("corrected version", "No corrections needed")
        explanation = result.get("Applicable grammar explained", "No additional explanation provided")
        return grammar_status, corrected, explanation
    elif isinstance(result, dict) and "error" in result:
        return "Error", "", result["error"]
    else:
        return "Error", "", "Could not process correction request."

# Create the Gradio interface
with gr.Blocks(title="Duo Helper", theme=gr.themes.Default()) as app:
    gr.Markdown("# 🌍 Duo Helper")
    gr.Markdown(f"A companion tool for language learning - Currently configured for {Config.TARGET_LANGUAGE}")
    
    with gr.Tabs():
        # Word Lookup Tab
        with gr.TabItem("📚 Word Lookup"):
            gr.Markdown("### Look up words and their translations")
            
            with gr.Row():
                word_input = gr.Textbox(
                    label="Enter word",
                    placeholder="Type a word to translate...",
                    scale=3
                )
                direction_dropdown = gr.Dropdown(
                    choices=[
                        f"{Config.SOURCE_LANGUAGE} → {Config.TARGET_LANGUAGE}",
                        f"{Config.TARGET_LANGUAGE} → {Config.SOURCE_LANGUAGE}"
                    ],
                    value=f"{Config.SOURCE_LANGUAGE} → {Config.TARGET_LANGUAGE}",
                    label="Translation Direction",
                    scale=2
                )
            
            lookup_button = gr.Button("🔍 Look Up", variant="primary")
            with gr.Row():
                word_translation = gr.Textbox(label="Translation", interactive=False)
                word_gender = gr.Textbox(label="Gender (if applicable)", interactive=False)
                word_plural = gr.Textbox(label="Plural (if applicable)", interactive=False)

            word_examples = gr.Textbox(
                label="Example Sentences",
                lines=4,
                interactive=False
            )

            lookup_button.click(
                fn=word_lookup_handler,
                inputs=[word_input, direction_dropdown],
                outputs=[word_translation, word_gender, word_plural, word_examples]
            )
            
            # Enable Enter key for word lookup
            word_input.submit(
                fn=word_lookup_handler,
                inputs=[word_input, direction_dropdown],
                outputs=[word_translation, word_gender, word_plural, word_examples]
            )
        
        # Grammar Questions Tab
        with gr.TabItem("❓ Grammar Questions"):
            gr.Markdown("### Ask grammar questions and get explanations")
            
            question_input = gr.Textbox(
                label="Enter your grammar question",
                placeholder="Ask a grammar question...",
                lines=3
            )
            
            question_button = gr.Button("📖 Get Answer", variant="primary")
            question_output = gr.Markdown(
                value="",
                label="Grammar Answer"
            )
            
            question_button.click(
                fn=lambda text: grammar_explanation_handler(text, "Grammar Question"),
                inputs=[question_input],
                outputs=question_output
            )
            
            # Enable Enter key for grammar questions
            question_input.submit(
                fn=lambda text: grammar_explanation_handler(text, "Grammar Question"),
                inputs=[question_input],
                outputs=question_output
            )
        
        # Sentence Correction Tab
        with gr.TabItem("✏️ Sentence Correction"):
            gr.Markdown("### Check and correct your sentences")
            
            sentence_input = gr.Textbox(
                label="Enter sentence to check",
                placeholder="Enter a sentence to check for grammar errors...",
                lines=3
            )
            
            correction_button = gr.Button("🔍 Check Grammar", variant="primary")
            
            with gr.Row():
                with gr.Column():
                    grammar_check_status = gr.Textbox(
                        label="Grammar Check Status",
                        interactive=False
                    )
                    corrected_version = gr.Textbox(
                        label="Corrected Version",
                        interactive=False,
                        lines=2
                    )
                
                with gr.Column():
                    grammar_explanation = gr.Markdown(
                        value="",
                        label="Grammar Explanation"
                    )
            
            correction_button.click(
                fn=sentence_correction_handler,
                inputs=[sentence_input],
                outputs=[grammar_check_status, corrected_version, grammar_explanation]
            )
            
            # Enable Enter key for sentence correction
            sentence_input.submit(
                fn=sentence_correction_handler,
                inputs=[sentence_input],
                outputs=[grammar_check_status, corrected_version, grammar_explanation]
            )
    
    # Footer
    gr.Markdown("---")
    gr.Markdown("💡 **Tip**: This app works great on mobile devices!")

if __name__ == "__main__":
    try:
        Config.validate()
        print(f"Starting Duo Helper - {Config.SOURCE_LANGUAGE} ↔ {Config.TARGET_LANGUAGE}")
        app.launch(share=True, server_name="0.0.0.0")
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please create a .env file with your GEMINI_API_KEY. See .env.example for reference.")