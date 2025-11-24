import os
from django.apps import AppConfig
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.staticfiles import finders

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        font_uri = 'fonts/Gacor.ttf' 
        path = finders.find(font_uri)
        
        if path:
            if isinstance(path, (list, tuple)):
                path = path[0]

            if 'Gacor' not in pdfmetrics.getRegisteredFontNames():
                try:
                    pdfmetrics.registerFont(TTFont('Gacor', path))
                    pdfmetrics.registerFontFamily('Gacor', normal='Gacor')
                except Exception as e:
                    print(f"ERRO CRÍTICO NA FONTE: Falha ao registrar Gacor: {e}")