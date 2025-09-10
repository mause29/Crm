def respond_to_message(message):
    greetings = ["hola", "buenos días", "hi", "hello"]
    if any(g in message.lower() for g in greetings):
        return "¡Hola! ¿Cómo puedo ayudarte hoy?"
    return "Lo siento, no entendí tu mensaje."
