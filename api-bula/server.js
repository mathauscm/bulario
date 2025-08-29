const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(helmet());
app.use(cors());
app.use(express.json());

let bulasData = null;

async function loadBulasData() {
  try {
    const data = await fs.readFile(path.join(__dirname, 'db', 'bulas.json'), 'utf8');
    bulasData = JSON.parse(data);
    console.log(`Carregadas ${bulasData.length} bulas`);
  } catch (error) {
    console.error('Erro ao carregar dados das bulas:', error);
    process.exit(1);
  }
}

app.get('/health', (req, res) => {
  res.json({ status: 'OK', message: 'API de Bulas funcionando' });
});

app.get('/api/bulas', (req, res) => {
  try {
    const { 
      medicamento, 
      fabricante, 
      principio_ativo, 
      indicacao,
      limit = 50,
      offset = 0 
    } = req.query;

    let filteredBulas = [...bulasData];

    if (medicamento) {
      const searchTerm = medicamento.toLowerCase();
      filteredBulas = filteredBulas.filter(bula => 
        bula.medicamento.toLowerCase().includes(searchTerm)
      );
    }

    if (fabricante) {
      const searchTerm = fabricante.toLowerCase();
      filteredBulas = filteredBulas.filter(bula => 
        bula.fabricante.toLowerCase().includes(searchTerm)
      );
    }

    if (principio_ativo) {
      const searchTerm = principio_ativo.toLowerCase();
      filteredBulas = filteredBulas.filter(bula => 
        bula.composicao?.principio_ativo && 
        typeof bula.composicao.principio_ativo === 'string' &&
        bula.composicao.principio_ativo.toLowerCase().includes(searchTerm)
      );
    }

    if (indicacao) {
      const searchTerm = indicacao.toLowerCase();
      filteredBulas = filteredBulas.filter(bula => 
        bula.indicacoes?.some(ind => ind.toLowerCase().includes(searchTerm))
      );
    }

    const startIndex = parseInt(offset);
    const endIndex = startIndex + parseInt(limit);
    const paginatedBulas = filteredBulas.slice(startIndex, endIndex);

    res.json({
      total: filteredBulas.length,
      limit: parseInt(limit),
      offset: parseInt(offset),
      data: paginatedBulas
    });
  } catch (error) {
    console.error('Erro ao buscar bulas:', error);
    res.status(500).json({ error: 'Erro interno do servidor' });
  }
});

app.get('/api/bulas/:id', (req, res) => {
  try {
    const id = parseInt(req.params.id);
    
    if (isNaN(id) || id < 0 || id >= bulasData.length) {
      return res.status(404).json({ error: 'Bula não encontrada' });
    }

    res.json(bulasData[id]);
  } catch (error) {
    console.error('Erro ao buscar bula:', error);
    res.status(500).json({ error: 'Erro interno do servidor' });
  }
});

app.get('/api/bulas/medicamento/:nome', (req, res) => {
  try {
    const nome = req.params.nome.toLowerCase();
    const bula = bulasData.find(b => 
      b.medicamento.toLowerCase() === nome
    );

    if (!bula) {
      return res.status(404).json({ error: 'Medicamento não encontrado' });
    }

    res.json(bula);
  } catch (error) {
    console.error('Erro ao buscar medicamento:', error);
    res.status(500).json({ error: 'Erro interno do servidor' });
  }
});

app.get('/api/search', (req, res) => {
  try {
    const { q, field = 'all', limit = 20 } = req.query;

    if (!q) {
      return res.status(400).json({ error: 'Parâmetro de busca "q" é obrigatório' });
    }

    const searchTerm = q.toLowerCase();
    let results = [];

    bulasData.forEach((bula, index) => {
      let matches = false;
      let matchedFields = [];

      if (field === 'all' || field === 'medicamento') {
        if (bula.medicamento.toLowerCase().includes(searchTerm)) {
          matches = true;
          matchedFields.push('medicamento');
        }
      }

      if (field === 'all' || field === 'indicacoes') {
        if (bula.indicacoes?.some(ind => ind.toLowerCase().includes(searchTerm))) {
          matches = true;
          matchedFields.push('indicacoes');
        }
      }

      if (field === 'all' || field === 'principio_ativo') {
        if (bula.composicao?.principio_ativo && 
            typeof bula.composicao.principio_ativo === 'string' &&
            bula.composicao.principio_ativo.toLowerCase().includes(searchTerm)) {
          matches = true;
          matchedFields.push('principio_ativo');
        }
      }

      if (field === 'all' || field === 'fabricante') {
        if (bula.fabricante.toLowerCase().includes(searchTerm)) {
          matches = true;
          matchedFields.push('fabricante');
        }
      }

      if (matches) {
        results.push({
          id: index,
          bula: bula,
          matchedFields: matchedFields
        });
      }
    });

    results = results.slice(0, parseInt(limit));

    res.json({
      query: q,
      field: field,
      total: results.length,
      results: results
    });
  } catch (error) {
    console.error('Erro na busca:', error);
    res.status(500).json({ error: 'Erro interno do servidor' });
  }
});

app.get('/api/medicamentos', (req, res) => {
  try {
    const medicamentos = bulasData.map((bula, index) => ({
      id: index,
      medicamento: bula.medicamento,
      fabricante: bula.fabricante,
      principio_ativo: bula.composicao?.principio_ativo
    }));

    res.json(medicamentos);
  } catch (error) {
    console.error('Erro ao listar medicamentos:', error);
    res.status(500).json({ error: 'Erro interno do servidor' });
  }
});

app.use('*', (req, res) => {
  res.status(404).json({ error: 'Endpoint não encontrado' });
});

async function startServer() {
  await loadBulasData();
  
  app.listen(PORT, () => {
    console.log(`API de Bulas rodando na porta ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
    console.log(`Buscar todas as bulas: http://localhost:${PORT}/api/bulas`);
    console.log(`Buscar medicamentos: http://localhost:${PORT}/api/medicamentos`);
    console.log(`Busca geral: http://localhost:${PORT}/api/search?q=ibuprofeno`);
  });
}

startServer().catch(console.error);