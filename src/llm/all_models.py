from ollama import chat
from src.llm.hf_inference_endpoint import HFInferenceEndpointModel
from src.llm.hf_tf_inference import HFTFInferenceModel
from src.llm.openai import OpenAIModel
from src.llm.ollama_model import OllamaModel


def initiate_model(model_id: str, run_option: str):
    if run_option == 'hf_api':
        client = HFInferenceEndpointModel(model_id=model_id)
    elif run_option == 'hf_tf':
        client = HFTFInferenceModel(model_id=model_id)
    elif run_option == 'gpt_api':
        client = OpenAIModel(model_id=model_id)
    elif run_option == 'ollama':
        client = OllamaModel(model_id=model_id)
    else:
        raise Exception('Invalid run option.')
    return client