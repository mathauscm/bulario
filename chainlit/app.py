import chainlit as cl

@cl.on_chat_start
async def start():
    await cl.Message(
        content="🤖 Olá! Bem-vindo ao seu chatbot Chainlit!\n\nDigite qualquer mensagem para começar nossa conversa!"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    # Processar a mensagem do usuário
    user_message = message.content.lower()
    
    # Criar uma resposta baseada na entrada
    if "oi" in user_message or "olá" in user_message:
        response = "Oi! Como posso ajudar você hoje?"
    elif "tchau" in user_message or "adeus" in user_message:
        response = "Até logo! Foi um prazer conversar com você! 👋"
    elif "como você está" in user_message:
        response = "Estou funcionando perfeitamente, obrigado por perguntar! E você?"
    else:
        response = f"Interessante! Você disse: '{message.content}'\n\nComo posso ajudar com isso?"
    
    # Enviar a resposta
    await cl.Message(
        content=response,
        author="Assistant"
    ).send()
