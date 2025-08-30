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
        
        # Grammar Explanation Tab
        with gr.TabItem("📝 Grammar Help"):
            gr.Markdown("### Get grammar explanations and corrections")
            
            grammar_mode = gr.Radio(
                choices=["Grammar Question", "Sentence Correction"],
                value="Grammar Question",
                label="Mode"
            )
            
            grammar_input = gr.Textbox(
                label="Enter your text",
                placeholder="Ask a grammar question or enter a sentence to check...",
                lines=3
            )
            
            # grammar_button = gr.Button("📖 Get Explanation", variant="primary")
            # grammar_output = gr.Textbox(
            #     label="Grammar Explanation",
            #     lines=10,
            #     interactive=False
            # )
            grammar_button = gr.Button("📖 Get Explanation", variant="primary")
            grammar_output = gr.Markdown(
                value="",
                label="Grammar Explanation"
            )
            
            grammar_button.click(
                fn=grammar_explanation_handler,
                inputs=[grammar_input, grammar_mode],
                outputs=grammar_output
            )
            
            # Enable Enter key for grammar explanation
            grammar_input.submit(
                fn=grammar_explanation_handler,
                inputs=[grammar_input, grammar_mode],
                outputs=grammar_output
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