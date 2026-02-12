import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO

# --- 1. FUNCIÓN PARA INYECTAR ESTILO (CSS) ---
def inyectar_css_footer():
    """Llama a esto al principio de tu App para fijar el micrófono abajo."""
    st.markdown("""
        <style>
        /* BARRA FIJA INFERIOR */
        .fixed-footer-container {
            position: fixed; bottom: 0; left: 0; width: 100%;
            background-color: #0E1117; /* Color de fondo igual a la App */
            padding: 10px 10px 0px 10px; z-index: 9999;
            border-top: 1px solid #30363D;
        }
        /* Ajuste para que el contenido no quede oculto */
        .block-container { padding-bottom: 150px; }
        
        /* Ocultar el reproductor de audio de salida visualmente si se desea */
        /* audio { display: none; } */
        </style>
        """, unsafe_allow_html=True)

# --- 2. FUNCIÓN OÍDO (Escuchar) ---
def escuchar_usuario(widget_audio):
    """
    Recibe el objeto del widget st.audio_input.
    Retorna: Texto transcrito (str) o None.
    """
    if not widget_audio: return None
    
    r = sr.Recognizer()
    try:
        with sr.AudioFile(widget_audio) as source:
            r.adjust_for_ambient_noise(source)
            audio_data = r.record(source)
            texto = r.recognize_google(audio_data, language="es-MX")
            return texto
    except Exception as e:
        # st.error(f"Error de audio: {e}") # Descomentar para debug
        return None

# --- 3. FUNCIÓN HABLA (Reproducir) ---
def hablar_respuesta(texto_ia):
    """
    Recibe el texto de la IA.
    Genera y reproduce el audio automáticamente.
    """
    if not texto_ia: return
    
    try:
        tts = gTTS(text=texto_ia, lang='es')
        fp = BytesIO()
        tts.write_to_fp(fp)
        audio_bytes = fp.getvalue()
        
        # Reproducir automáticamente (autoplay=True)
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    except Exception:
        pass # Si falla el audio, no rompemos la App, solo no habla.
