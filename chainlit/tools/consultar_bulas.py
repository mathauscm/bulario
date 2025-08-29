import requests
import json


def buscar_medicamento(nome_medicamento: str) -> str:
    """Busca informações completas sobre um medicamento específico"""
    try:
        if not nome_medicamento:
            return "Nome do medicamento é obrigatório."
        
        # Normaliza o nome do medicamento
        nome_medicamento = nome_medicamento.lower().strip()
        
        # Consulta a API
        api_base_url = "http://localhost:3001"
        url = f"{api_base_url}/api/search"
        response = requests.get(url, params={"q": nome_medicamento, "limit": 1}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('total', 0) > 0:
                bula = data['results'][0]['bula']
                return _formatar_resposta_medicamento(bula)
            else:
                return _medicamento_nao_encontrado(nome_medicamento)
        else:
            return f"Erro HTTP {response.status_code}: Não foi possível consultar a API de medicamentos."
            
    except requests.exceptions.ConnectionError:
        return _erro_conexao_api()
    except requests.exceptions.Timeout:
        return "Timeout: A API de medicamentos está demorando para responder. Tente novamente em alguns segundos."
    except Exception as e:
        return f"Erro inesperado ao consultar medicamento: {str(e)}"


def _formatar_resposta_medicamento(bula_data):
    """Formata a resposta com informações completas do medicamento"""
    try:
        # Informações básicas
        nome = bula_data.get('medicamento', 'N/A')
        fabricante = bula_data.get('fabricante', 'N/A')
        forma_farmaceutica = bula_data.get('forma_farmaceutica', 'N/A')
        apresentacao = bula_data.get('apresentacao', 'N/A')
        via_administracao = bula_data.get('via_administracao', 'N/A')
        uso = bula_data.get('uso', [])
        
        # Composição detalhada
        composicao = bula_data.get('composicao', {})
        principio_ativo = composicao.get('principio_ativo', 'N/A')
        excipientes = composicao.get('excipientes', [])
        
        # Indicações detalhadas
        indicacoes = bula_data.get('indicacoes', [])
        if isinstance(indicacoes, list) and indicacoes:
            indicacoes_str = '\n'.join([f"• {ind}" for ind in indicacoes])
        else:
            indicacoes_str = str(indicacoes) if indicacoes else 'N/A'
        
        # Contraindicações detalhadas
        contraindicacoes = bula_data.get('contraindicacoes', [])
        if isinstance(contraindicacoes, list) and contraindicacoes:
            contra_str = '\n'.join([f"• {contra}" for contra in contraindicacoes[:3]])
            if len(contraindicacoes) > 3:
                contra_str += f"\n• ... e mais {len(contraindicacoes) - 3} contraindicações"
        else:
            contra_str = str(contraindicacoes) if contraindicacoes else 'N/A'
        
        # Advertências e precauções
        advertencias = bula_data.get('advertencias_precaucoes', [])
        if isinstance(advertencias, list) and advertencias:
            adv_str = '\n'.join([f"• {adv}" for adv in advertencias[:2]])
            if len(advertencias) > 2:
                adv_str += f"\n• ... e mais {len(advertencias) - 2} advertências"
        else:
            adv_str = str(advertencias) if advertencias else 'N/A'
        
        # Uso (público alvo)
        if isinstance(uso, list) and uso:
            uso_str = ', '.join(uso)
        else:
            uso_str = str(uso) if uso else 'N/A'
        
        resposta = f"**{nome}**\n\n**COMPOSIÇÃO:**\n• **Princípio Ativo:** {principio_ativo}"
        
        # Adiciona excipientes se disponíveis
        if excipientes and isinstance(excipientes, list):
            excipientes_str = ', '.join(excipientes)
            resposta += f"\n• **Excipientes:** {excipientes_str}"
        
        resposta += f"""\n\n**INFORMAÇÕES GERAIS:**\n• **Fabricante:** {fabricante}\n• **Forma Farmacêutica:** {forma_farmaceutica}\n• **Apresentação:** {apresentacao}\n• **Via de Administração:** {via_administracao}\n• **Uso:** {uso_str}\n\n**INDICAÇÕES:**\n{indicacoes_str}\n\n**CONTRAINDICAÇÕES:**\n{contra_str}\n\n**ADVERTÊNCIAS E PRECAUÇÕES:**\n{adv_str}"""
        
        # Adiciona posologia se disponível
        posologia = bula_data.get('posologia')
        if posologia:
            resposta += "\n\n**POSOLOGIA:**"
            if isinstance(posologia, dict):
                for grupo, dose in posologia.items():
                    resposta += f"\n• **{grupo.title()}:** {dose}"
            else:
                resposta += f"\n{posologia}"
        
        # Adiciona reações adversas se disponíveis
        reacoes = bula_data.get('reações_adversas', {})
        if reacoes and isinstance(reacoes, dict):
            resposta += "\n\n**PRINCIPAIS REAÇÕES ADVERSAS:**"
            for categoria, lista_reacoes in reacoes.items():
                if lista_reacoes and isinstance(lista_reacoes, list):
                    reacoes_str = ', '.join(lista_reacoes[:3])
                    if len(lista_reacoes) > 3:
                        reacoes_str += f" (e mais {len(lista_reacoes) - 3})"
                    resposta += f"\n• **{categoria.title()}:** {reacoes_str}"
        
        # Adiciona armazenamento se disponível
        armazenamento = bula_data.get('armazenamento', {})
        if armazenamento:
            resposta += "\n\n**ARMAZENAMENTO:**"
            if armazenamento.get('temperatura'):
                resposta += f"\n• **Temperatura:** {armazenamento['temperatura']}"
            if armazenamento.get('protecao'):
                resposta += f"\n• **Proteção:** {armazenamento['protecao']}"
            if armazenamento.get('validade'):
                resposta += f"\n• **Validade:** {armazenamento['validade']}"
        
        # Adiciona informações de registro se disponíveis
        registro = bula_data.get('registro')
        tarja = bula_data.get('tarja')
        if registro and registro != 'não informado na bula':
            resposta += f"\n\n**Registro:** {registro}"
        if tarja:
            resposta += f"\n**Classificação:** {tarja}"
        
        resposta += "\n\n**IMPORTANTE:** Sempre consulte um médico ou farmacêutico antes de usar qualquer medicamento. Esta é apenas uma consulta informativa."
        
        return resposta
        
    except Exception as e:
        return f"Erro ao processar dados do medicamento: {str(e)}"


def _medicamento_nao_encontrado(nome_medicamento):
    """Resposta quando medicamento não é encontrado na API"""
    return f"""**Medicamento '{nome_medicamento}' não encontrado**\n\n**Medicamentos disponíveis na base de dados:**\n• Dipirona (Dipirona Monoidratada)\n• Paracetamol\n\n**Sugestões:**\n- Verifique a grafia do medicamento\n- Use apenas o nome do princípio ativo\n- Experimente nomes similares ou sinônimos\n\n**Nota:** A base de dados atual possui um número limitado de medicamentos cadastrados."""


def _erro_conexao_api():
    """Resposta quando há erro de conexão com a API"""
    api_base_url = "http://localhost:3001"
    return f"""**Erro de Conexão com a API de Medicamentos**\n\nA API de medicamentos parece estar indisponível no momento.\n\n**Para resolver:**\n1. Verifique se a API está rodando:\n   ```\n   cd /home/mathaus/projects/bulario/api-medicamentos-bulario/api-bula\n   npm start\n   ```\n\n2. Confirme se está acessível em: {api_base_url}\n\n3. Aguarde alguns segundos e tente novamente\n\n**A API deve estar rodando na porta 3001.**"""


