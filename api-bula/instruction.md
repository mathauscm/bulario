# 🔄 **Fluxo de Decisão e Processamento do Chatbot de Medicamentos**

## **Como funciona a conexão com GPT e a decisão de usar a base de dados da API**

### **1. Recepção da Mensagem** (`app_mybot.py:57-58`)
- Usuário envia uma mensagem
- Sistema converte para minúsculas: `user_message = message.content.lower()`

### **2. Detecção de Consulta sobre Medicamentos** (`app_mybot.py:61-69`)
O sistema verifica se a mensagem contém palavras-chave relacionadas a medicamentos:
```python
medicamento_keywords = [
    'medicamento', 'remedio', 'comprimido', 'capsula', 'xarope', 
    'pomada', 'creme', 'gel', 'solução', 'gotas', 'injetavel',
    'ibuprofeno', 'paracetamol', 'dipirona', 'omeprazol', 'amoxicilina',
    'composição', 'indicação', 'contraindicação', 'posologia', 'dose',
    'efeito colateral', 'reação adversa', 'bula', 'princípio ativo'
]
```

### **3. Decisão de Consultar a API** (`app_mybot.py:76-90`)
**SE** a mensagem contém palavras-chave de medicamentos:
- Extrai palavras com mais de 3 caracteres da mensagem
- Para cada palavra, tenta buscar na API local
- Chama `buscar_medicamento()` que consulta `http://localhost:3001/api/search`

### **4. Consulta à API de Medicamentos** (`tools/consultar_bulas.py:14-27`)
- Normaliza o nome do medicamento
- Faz requisição GET para a API local: `http://localhost:3001/api/search`
- Parâmetros: `{"q": nome_medicamento, "limit": 1}`
- **SE** encontrar resultados → formata as informações completas
- **SE NÃO** encontrar → retorna mensagem de medicamento não encontrado

### **5. Preparação do Contexto para GPT** (`app_mybot.py:91-94`)
- Usa sempre o `system_prompt` base
- **SE** encontrou informações na API → adiciona ao contexto:
```python
context += f"\n\nUse as seguintes informações específicas do medicamento para complementar sua resposta:\n{medicine_info}"
```

### **6. Chamada para GPT** (`app_mybot.py:97-105`)
```python
stream = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": context},  # Inclui dados da API se encontrados
        {"role": "user", "content": message.content}
    ],
    stream=True,
    temperature=0.7
)
```

## 📋 **Resumo da Lógica de Decisão**

1. **Sempre conecta com GPT** - independente do tipo de pergunta
2. **Decide usar a API** baseado nas palavras-chave da mensagem
3. **Prioridade da informação**: API local → GPT complementa/responde
4. **Fallback**: Se API falha, GPT responde sozinho com conhecimento geral

**Resultado**: O GPT **sempre** recebe informações específicas da API quando disponíveis, usando-as como fonte primária e complementando com seu conhecimento.

## 🔧 **Componentes Técnicos**

### **Conexão OpenAI**
- Cliente: `AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))`
- Modelo: `gpt-4o-mini`
- Temperatura: `0.7`
- Streaming: `True`

### **API Local de Medicamentos**
- URL Base: `http://localhost:3001`
- Endpoint: `/api/search`
- Método: GET
- Timeout: 10 segundos

### **Tratamento de Erros**
- ConnectionError → Mensagem de erro de conexão com instruções
- Timeout → Mensagem de timeout
- HTTP Status != 200 → Erro HTTP específico
- Exception genérica → Erro inesperado