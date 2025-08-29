# 🤖 Chatbot de Medicamentos - OpenAI Version

Um chatbot inteligente especializado em informações sobre medicamentos, construído com Chainlit e OpenAI, baseado no projeto MIA original.

## Funcionalidades

- 💊 **Consulta de Medicamentos**: Informações detalhadas sobre medicamentos específicos
- **Composição Detalhada**: Princípios ativos e excipientes
- **Indicações Terapêuticas**: Para que serve cada medicamento  
- **Contraindicações**: Quando não usar o medicamento
- **Posologia**: Como administrar corretamente
- **Reações Adversas**: Efeitos colaterais organizados por frequência
- **Informações Técnicas**: Armazenamento, validade e dados regulatórios

## Como usar

### 1. Configuração do Ambiente

```bash
# Clone ou navegue até o diretório do projeto
cd /home/mathaus/projects/bulario/api-medicamentos-bulario/chainlit

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração da API Key

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua chave da OpenAI
# OPENAI_API_KEY=sk-sua_chave_aqui
```

### 3. Execução

```bash
# Execute o chatbot
chainlit run main_mybot.py --port 8001

# Ou execute diretamente o app
chainlit run app_mybot.py --port 8001
```

### 4. Acesso

Abra seu navegador em: http://localhost:8001

## 🔧 Estrutura do Projeto

```
chainlit/
├── app_mybot.py          # Aplicação principal do chatbot
├── main_mybot.py         # Arquivo de entrada com verificações
├── requirements.txt      # Dependências do projeto  
├── .env.example         # Exemplo de configuração
├── .env                 # Suas configurações (não commitado)
├── tools/               # Ferramentas e utilitários
│   └── consultar_bulas.py # Função para consultar base de medicamentos
└── README.md            # Este arquivo
```

## 💬 Exemplos de Uso

- *"Me fale sobre ibuprofeno"*
- *"Quais são os excipientes do omeprazol?"*  
- *"Contraindicações da dipirona"*
- *"Posologia do paracetamol para adultos"*
- *"Reações adversas da amoxicilina"*

## ⚠️ Importante

- As informações fornecidas são apenas para fins educativos
- Sempre consulte um profissional de saúde antes de usar qualquer medicamento
- Este chatbot não substitui consulta médica ou farmacêutica

## 🛠️ Tecnologias Utilizadas

- **Chainlit**: Framework para interface de chatbot
- **OpenAI GPT**: Inteligência artificial conversacional
- **Python**: Linguagem de programação
- **API de Medicamentos**: Base de dados especializada

## 📝 Diferenças do Projeto MIA Original

- Usa OpenAI ao invés do framework MIA
- Estrutura mais simples e direta
- Mantém a funcionalidade de consulta de medicamentos

## Migração do Projeto MIA

Este projeto foi adaptado de `/home/mathaus/projects/mia/projects/meu_chatbot`, mantendo:

- A especialização em medicamentos
- A integração com a API de bulas
- A estrutura de mensagens educativas
- Os avisos de segurança importantes