import chainlit as cl
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Inicializar cliente OpenAI
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@cl.on_chat_start
async def start():
    await cl.Message(
        content="🤖 Olá! Sou um chatbot conectado ao GPT da OpenAI. Como posso ajudar você?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    # Mostrar que está processando
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # Fazer chamada para OpenAI com a nova API
        stream = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil que responde em português."},
                {"role": "user", "content": message.content}
            ],
            stream=True
        )
        
        # Stream da resposta
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                await msg.stream_token(chunk.choices[0].delta.content)
        
        await msg.update()
        
    except Exception as e:
        await cl.Message(
            content=f"Erro ao conectar com OpenAI: {str(e)}"
        ).send()