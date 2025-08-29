import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Verificar se a chave da OpenAI está configurada
if not os.getenv("OPENAI_API_KEY"):
    print("Erro: OPENAI_API_KEY não encontrada no arquivo .env")
    print("Configure sua chave da OpenAI no arquivo .env:")
    print("OPENAI_API_KEY=sua_chave_aqui")
    sys.exit(1)

print("Chave OpenAI carregada com sucesso")
print("Inicializando Chatbot de Medicamentos...")
print("Acesse: http://localhost:8001")
print("\nPara executar:")
print("chainlit run main_mybot.py --port 8001")

# Importar o app principal
from app_mybot import *

# Como executar:
# >> source chainlit_env/bin/activate
# >> chainlit run ./projects/meu_chatbot/main_meu_chatbot.py --port 8001  # Interface Chainlit