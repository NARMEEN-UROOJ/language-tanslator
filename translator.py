from deep_translator import GoogleTranslator

class LanguageTranslator:
    def __init__(self):
        # We fetch languages from deep-translator instead of googletrans
        self.languages = GoogleTranslator().get_supported_languages(as_dict=True)
    
    def get_language_codes(self):
        return {lang.title(): code for lang, code in self.languages.items()}
    
    def translate_text(self, text, source_lang='auto', target_lang='en'):
        try:
            # deep-translator uses 'auto' for source but doesn't like it for target
            # target must be a language code
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            result = translator.translate(text)
            return {
                'translated_text': result,
                'source_lang': source_lang,
                'confidence': 'High'
            }
        except Exception as e:
            return {'error': str(e)}

# Test
if __name__ == "__main__":
    translator = LanguageTranslator()
    result = translator.translate_text("Hello, how are you?", target_lang='es')
    print(result)