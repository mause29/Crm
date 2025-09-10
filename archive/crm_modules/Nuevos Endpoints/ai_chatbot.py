from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Cargar modelo LLaMA o similar
tokenizer = AutoTokenizer.from_pretrained("TheBloke/LLaMA-7B-GPTQ") 
model = AutoModelForCausalLM.from_pretrained("TheBloke/LLaMA-7B-GPTQ", torch_dtype=torch.float16, device_map="auto")

# Analizador de sentimiento simple
def sentiment_analysis(text):
    text = text.lower()
    if any(word in text for word in ["triste", "malo", "enojado", "frustrado"]):
        return "negativo"
    elif any(word in text for word in ["feliz", "bueno", "excelente", "gracias"]):
        return "positivo"
    return "neutral"

def generate_response(message, client_id=None):
    sentiment = sentiment_analysis(message)
    
    # Prompt dinámico basado en sentimiento
    prompt = f"Cliente: {message}\nSentimiento: {sentiment}\nResponde como un asistente profesional:"
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=150)
    reply = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return reply
