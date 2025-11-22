# core/apps.py
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

            # 1. Tenta registrar a fonte GACOR globalmente no ReportLab
            if 'Gacor' not in pdfmetrics.getRegisteredFontNames():
                try:
                    pdfmetrics.registerFont(TTFont('Gacor', path))
                    # 2. Registra a família para que o CSS consiga usar 'Gacor'
                    pdfmetrics.registerFontFamily('Gacor', normal='Gacor')
                    # print("--- Fonte Gacor registrada com sucesso! ---")
                except Exception as e:
                    # Este erro deve ser silencioso, mas crítico
                    print(f"ERRO CRÍTICO NA FONTE: Falha ao registrar Gacor: {e}")