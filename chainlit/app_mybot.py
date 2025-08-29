import chainlit as cl
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from tools.consultar_bulas import buscar_medicamento

# Carregar variáveis do .env
load_dotenv()

# Inicializar cliente OpenAI
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mensagem de apresentação do chatbot de medicamentos
introduction = (
    "🤖 **Bem-vindo ao Chatbot de Medicamentos!** 💊\n\n"
    "Sou seu assistente especializado em informações sobre medicamentos. "
    "**Com este chatbot, você pode:**\n"
    "- **Consultar medicamentos**: Informações detalhadas incluindo composição completa\n"
    "- **Composição detalhada**: Princípios ativos e lista completa de excipientes\n"
    "- **Indicações terapêuticas**: Para que serve cada medicamento\n"
    "- **Contraindicações**: Quando não usar o medicamento\n"
    "- **Posologia**: Como administrar corretamente\n"
    "- **Reações adversas**: Efeitos colaterais por frequência\n"
    "- **Informações técnicas**: Armazenamento, validade e dados regulatórios\n\n"
    "**Exemplos do que você pode perguntar:**\n"
    "- *\"Me fale sobre ibuprofeno\"*\n"
    "- *\"Quais são os excipientes do omeprazol?\"*\n"
    "- *\"Reações adversas da sepurin\"*\n"
    "- *\"Quais são os excipientes da macrodantina?\"*\n\n"
    " **Importante**: As informações fornecidas são apenas para fins educativos. "
    "Sempre consulte um profissional de saúde antes de usar qualquer medicamento.\n\n"
    "Digite sua pergunta sobre medicamentos para começar!"
)

# Instruções do sistema para o comportamento da IA
system_prompt = (
    "Você é um assistente especializado em informações sobre medicamentos. "
    "Seu foco principal é fornecer informações precisas e educativas sobre medicamentos "
    "através de consultas a uma base de dados especializada.\n\n"
    "INSTRUÇÕES IMPORTANTES:\n"
    "- Sempre forneça informações completas: composição, indicações, contraindicações, posologia, reações adversas\n"
    "- SEMPRE inclua avisos de segurança sobre consultar profissionais de saúde\n"
    "- As informações de posologia são apenas educativas - sempre oriente a consultar um profissional\n"
    "- Seja claro que suas informações são apenas para fins informativos\n"
    "- DESTAQUE informações importantes como contraindicações e reações adversas graves\n"
    "- Responda sempre em português brasileiro de forma clara e profissional\n"
    "- Seja cordial, responsável e educativo\n"
    "- Se não encontrar informações sobre um medicamento específico, sugira alternativas ou oriente a consultar um profissional\n\n"
    "Enfatize sempre a importância de consultar profissionais de saúde."
)

@cl.on_chat_start
async def start():
    await cl.Message(content=introduction).send()

@cl.on_message
async def main(message: cl.Message):
    user_message = message.content.lower()
    
    # Verificar se é uma consulta sobre medicamento
    medicamento_keywords = [
        'medicamento', 'remedio', 'comprimido', 'capsula', 'xarope', 
        'pomada', 'creme', 'gel', 'solução', 'gotas', 'injetavel',
        'ibuprofeno', 'paracetamol', 'dipirona', 'omeprazol', 'amoxicilina',
        'composição', 'indicação', 'contraindicação', 'posologia', 'dose',
        'efeito colateral', 'reação adversa', 'bula', 'princípio ativo'
    ]
    
    is_medicine_query = any(keyword in user_message for keyword in medicamento_keywords)
    
    # Mostrar que está processando
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # Se for consulta sobre medicamento, tentar buscar informações primeiro
        medicine_info = ""
        if is_medicine_query:
            try:
                # Extrair possível nome do medicamento da mensagem
                words = message.content.split()
                for word in words:
                    if len(word) > 3:  # Palavras com mais de 3 caracteres
                        result = buscar_medicamento(word.lower())
                        if result and 'erro' not in result.lower():
                            medicine_info = f"\n\nINFORMAÇÕES DA BASE DE DADOS:\n{result}\n\n"
                            break
            except Exception as e:
                print(f"Erro ao consultar medicamento: {e}")
        
        # Preparar contexto com informações do medicamento se encontradas
        context = system_prompt
        if medicine_info:
            context += f"\n\nUse as seguintes informações específicas do medicamento para complementar sua resposta:\n{medicine_info}"
        
        # Fazer chamada para OpenAI
        stream = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": message.content}
            ],
            stream=True,
            temperature=0.7
        )
        
        # Stream da resposta
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                await msg.stream_token(chunk.choices[0].delta.content)
        
        await msg.update()
        
    except Exception as e:
        await cl.Message(
            content=f"Erro ao processar sua solicitação: {str(e)}\n\n"
                   "Tente novamente ou reformule sua pergunta."
        ).send()