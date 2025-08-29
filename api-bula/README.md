# API de Bulas de Medicamentos

API REST em Node.js para consulta de bulas de medicamentos. Fornece acesso completo a informações farmacêuticas detalhadas, incluindo composição, indicações, contraindicações, posologia e muito mais.

## 🚀 Instalação e Execução

```bash
# Instalar dependências
npm install

# Iniciar o servidor
npm start
```

A API rodará na porta **3001** por padrão.

## 📊 Base de Dados

- **17 medicamentos** com informações completas
- Dados estruturados com composição detalhada
- Informações regulatórias e técnicas

## 🔗 Endpoints da API

### Health Check
```
GET /health
```
Verifica se a API está funcionando.

**Resposta:**
```json
{
  "status": "OK", 
  "message": "API de Bulas funcionando"
}
```

### Buscar Todas as Bulas (com filtros)
```
GET /api/bulas
```

**Parâmetros opcionais:**
- `limit`: Número de resultados (padrão: 50, máx: 50)
- `offset`: Itens para pular na paginação (padrão: 0)
- `medicamento`: Filtrar por nome do medicamento
- `fabricante`: Filtrar por fabricante
- `principio_ativo`: Filtrar por princípio ativo
- `indicacao`: Filtrar por indicação

**Exemplo:**
```
GET /api/bulas?limit=5&medicamento=ibuprofeno
```

### Buscar Bula por ID
```
GET /api/bulas/{id}
```

**Exemplo:**
```
GET /api/bulas/0
```

### Buscar Medicamento por Nome Exato
```
GET /api/bulas/medicamento/{nome}
```

**Exemplo:**
```
GET /api/bulas/medicamento/ibuprofeno
```

### Busca Geral (Recomendado para Chatbots)
```
GET /api/search?q={termo}&field={campo}&limit={limite}
```

**Parâmetros:**
- `q`: Termo de busca (obrigatório)
- `field`: Campo de busca - `all`, `medicamento`, `indicacoes`, `principio_ativo`, `fabricante` (padrão: `all`)
- `limit`: Número de resultados (padrão: 20)

**Exemplo:**
```
GET /api/search?q=ibuprofeno&limit=1
```

**Resposta:**
```json
{
  "query": "ibuprofeno",
  "field": "all", 
  "total": 1,
  "results": [
    {
      "id": 0,
      "bula": { /* dados completos da bula */ },
      "matchedFields": ["medicamento", "principio_ativo"]
    }
  ]
}
```

### Listar Medicamentos Resumido
```
GET /api/medicamentos
```

Retorna lista com ID, nome, fabricante e princípio ativo.

## 📋 Estrutura Completa dos Dados

Cada bula contém informações detalhadas:

### Identificação
- `medicamento`: Nome do medicamento
- `fabricante`: Empresa farmacêutica
- `forma_farmaceutica`: Forma (cápsula, comprimido, etc.)
- `apresentacao`: Concentração e embalagem
- `uso`: Público alvo (adulto, pediátrico)
- `via_administracao`: Como administrar

### Composição
- `composicao.principio_ativo`: Substância ativa
- `composicao.excipientes`: Lista completa de excipientes

### Informações Clínicas
- `indicacoes`: Lista de indicações terapêuticas
- `contraindicacoes`: Quando não usar
- `advertencias_precaucoes`: Cuidados importantes
- `posologia`: Como usar (adultos/crianças)
- `reacoes_adversas`: Efeitos colaterais por frequência
- `superdose`: Sintomas e tratamento

### Informações Técnicas
- `armazenamento`: Condições de conservação
- `registro`: Número no Ministério da Saúde
- `responsavel_tecnico`: Farmacêutico responsável
- `sac`: Serviço de atendimento ao consumidor
- `tarja`: Classificação regulatória

## 💻 Integração com Chatbot

Para usar com o chatbot em `/home/mathaus/projects/mia/projects/meu_chatbot`:

```javascript
// Buscar medicamento específico
const response = await fetch('http://localhost:3001/api/search?q=ibuprofeno&limit=1');
const data = await response.json();

if (data.total > 0) {
  const bula = data.results[0].bula;
  console.log(`Medicamento: ${bula.medicamento}`);
  console.log(`Princípio ativo: ${bula.composicao.principio_ativo}`);
  console.log(`Excipientes: ${bula.composicao.excipientes.join(', ')}`);
}

// Listar medicamentos disponíveis
const medicamentos = await fetch('http://localhost:3001/api/medicamentos');
const lista = await medicamentos.json();

// Buscar em múltiplas bulas
const resultados = await fetch('http://localhost:3001/api/search?q=dor&limit=10');
```

## ⚙️ Configuração

### Porta Personalizada
```bash
PORT=8080 npm start
```

### Variáveis de Ambiente
- `PORT`: Porta do servidor (padrão: 3001)

## 🔒 CORS

A API possui CORS habilitado para todas as origens durante desenvolvimento. Para produção, considere configurar origens específicas.

## 🧪 Testes

```bash
# Testar health check
curl http://localhost:3001/health

# Testar busca
curl "http://localhost:3001/api/search?q=ibuprofeno"

# Testar listagem
curl http://localhost:3001/api/medicamentos
```

## 📖 Exemplos de Medicamentos Disponíveis

- Ibuprofeno
- Omeprazol  
- Dipirona
- Paracetamol
- Hidroclorotiazida
- Amoxicilina
- Enalapril
- E mais 10 medicamentos...

## ⚠️ Importante

Esta API fornece informações educativas. Sempre consulte profissionais de saúde para orientações médicas específicas.