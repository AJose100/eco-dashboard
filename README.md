# ⚡ EcoDashboard

O **EcoDashboard** é uma aplicação completa para monitoramento de consumo de energia elétrica residencial. Com ele, é possível cadastrar seus aparelhos, visualizar o consumo mensal, calcular custos baseados em diferentes bandeiras tarifárias e receber dicas personalizadas para economizar na conta de luz.

## 🚀 Funcionalidades

- **Cálculo Inteligente:** Conversão de potência (Watts) e horas de uso em custo estimado (R$).
- **Bandeira Tarifária:** Seletor dinâmico para ajustar os cálculos de acordo com a bandeira tarifária vigente (Verde, Amarela, Vermelha 1 e 2).
- **Dashboard Responsivo:** Design moderno com modo escuro e interface otimizada para Desktop e Mobile.
- **Instalável (PWA):** Funciona como um aplicativo nativo no seu celular.
- **Relatórios:** Geração de PDF com o resumo do consumo.
- **Persistência de Dados:** Banco de dados SQLite integrado.

## 🛠 Tecnologias Utilizadas

**Backend:**
- Python 3
- FastAPI
- SQLAlchemy (SQLite)

**Frontend:**
- Vue.js 3
- Vite
- Tailwind CSS

## 📋 Como Rodar o Projeto

### Pré-requisitos
- Python 3.10+
- Node.js (v18+)
- npm ou yarn

### 1. Backend
1. Entre na pasta `backend`: `cd backend`
2. Instale as dependências: `pip install fastapi uvicorn sqlalchemy`
3. Inicie o servidor: `python -m uvicorn main:app --reload`
4. O servidor estará rodando em `http://127.0.0.1:8000`

### 2. Frontend
1. Entre na pasta `frontend`: `cd frontend`
2. Instale as dependências: `npm install`
3. Rode o projeto: `npm run dev`
4. O frontend estará disponível em `http://localhost:5173`

## 📱 Transformando em App (PWA)
Este projeto está configurado como PWA. Ao acessar o link do projeto pelo navegador do seu celular (Chrome/Safari), procure a opção **"Adicionar à tela de início"** no menu do navegador para instalar o EcoDashboard como um app nativo.

## 🤝 Contribuição
Sinta-se à vontade para abrir *Issues* ou enviar *Pull Requests* para melhorias, novas funcionalidades ou correções de bugs.

---
Desenvolvido com foco em sustentabilidade e economia doméstica. 🌿
