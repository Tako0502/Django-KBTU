from django.apps import AppConfig

class AiProcessingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_processing'
    
    def ready(self):
        import nltk
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet') 