import gradio as gr
from language_service import LanguageService
from config import Config

# Initialize the language service
language_service = LanguageService()

def word_lookup_handler(word, direction):
    """Handle word lookup requests"""
    if not word.strip():
        return "", "", "", "Please enter a word to look up."
    
    source_to_target = direction == f"{Config.SOURCE_LANGUAGE} → {language_service.target_language}"
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

def language_change_handler(new_language):
    """Handle language selection changes"""
    language_service.set_target_language(new_language)
    header_text = f"A companion tool for language learning - Currently configured for {new_language}"
    direction_choices = [
        f"{Config.SOURCE_LANGUAGE} → {new_language}",
        f"{new_language} → {Config.SOURCE_LANGUAGE}"
    ]
    direction_value = f"{Config.SOURCE_LANGUAGE} → {new_language}"
    return header_text, gr.update(choices=direction_choices, value=direction_value)

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
    
    # Language selection dropdown
    with gr.Row():
        language_dropdown = gr.Dropdown(
            choices=Config.SUPPORTED_LANGUAGES,
            value=Config.DEFAULT_TARGET_LANGUAGE,
            label="Target Language",
            info="Select the language you want to learn",
            scale=1
        )
    
    # Dynamic header that updates with language selection
    header_text = gr.Markdown(f"A companion tool for language learning - Currently configured for {Config.TARGET_LANGUAGE}")
    
    with gr.Tabs():
        # Word Lookup Tab
        with gr.TabItem("📚Word"):
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

        # Sentence Correction Tab
        with gr.TabItem("✏️Sentence"):
            gr.Markdown("### Check and correct your sentences")
            
            sentence_input = gr.Textbox(
                label="Enter sentence to check",
                placeholder="Enter a sentence to check for grammar errors...",
                lines=3
            )
            
            correction_button = gr.Button("🔍 Check Grammar", variant="primary")
            

            with gr.Row():
                with gr.Column(scale=1, min_width=200):
                    grammar_check_status = gr.Textbox(
                        label="Grammar Check Status",
                        interactive=False
                    )
                with gr.Column(scale=10):
                    corrected_version = gr.Textbox(
                    label="Corrected Version",
                    interactive=False,
                    lines=1
                    )
            with gr.Accordion("Grammar Explanation", open=True):
                grammar_explanation = gr.Markdown(
                    value="",
                    label="Grammar Explanation",
                    show_copy_button=True
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
    
        # Grammar Questions Tab
        with gr.TabItem("❓Grammar"):
            gr.Markdown("### Ask grammar questions and get explanations")
            
            question_input = gr.Textbox(
                label="Enter your grammar question",
                placeholder="Ask a grammar question...",
                lines=3
            )
            
            question_button = gr.Button("📖 Get Answer", variant="primary")
            with gr.Accordion("Grammar Answer", open=True):
                question_output = gr.Markdown(
                    value="",
                    label="Grammar Answer",
                    show_copy_button=True
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
    
    # Language change event handler
    language_dropdown.change(
        fn=language_change_handler,
        inputs=[language_dropdown],
        outputs=[header_text, direction_dropdown]
    )
        

    # Footer
    gr.Markdown("---")
    gr.Markdown("💡Good Luck!")

if __name__ == "__main__":
    try:
        Config.validate()
        print(f"Starting Duo Helper - {Config.SOURCE_LANGUAGE} ↔ {Config.TARGET_LANGUAGE}")
        app.launch(share=True, server_name="0.0.0.0")
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please create a .env file with your GEMINI_API_KEY. See .env.example for reference.")