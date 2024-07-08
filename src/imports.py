import configparser
import importlib
import os

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'core', 'models', 'config.ini')
config.read(config_path)

def get_llm_model():
    try:
        llm_model = config['Models']['LLM']
        module = importlib.import_module(f'core.models.llm.{llm_model.lower()}_llm')
        return getattr(module, f'{llm_model}LLM')()
    except KeyError:
        print(f"Error: 'Models' section or 'LLM' key not found in config file. Path: {config_path}")
        raise

def get_stt_model():
    stt_model = config['Models']['STT']
    module = importlib.import_module(f'core.models.stt.{stt_model.lower()}_stt')
    return getattr(module, f'{stt_model}STT')()

def get_tts_model():
    tts_model = config['Models']['TTS']
    module = importlib.import_module(f'core.models.tts.{tts_model.lower()}_tts')
    return getattr(module, f'{tts_model}TTS')()