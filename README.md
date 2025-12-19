# 📊 Painel de Relatórios BRG

Plataforma centralizada para visualização de relatórios corporativos da BRG Geradores, desenvolvida em **Streamlit**.

## 🚀 Visão Geral

O projeto visa unificar o acesso a diferentes dashboards operacionais (como Estoque em Tempo Real) sob uma única interface segura, com autenticação Microsoft e controle de permissões granular.

## ✨ Funcionalidades Principais

- **🔐 Autenticação Corporativa**: Login integrado com Microsoft Azure AD.
- **🛡️ Controle de Acesso**:
  - Painel administrativo para gerenciar quem vê o quê.
  - Ícone de configuração exclusivo para administradores.
- **📦 Relatórios Integrados**:
  - **Estoque em Tempo Real**: Visualização de KPIs e saldos de estoque.
- **🎨 UI Premium**: Design moderno com tema escuro, logo da empresa e layout responsivo.

## 🛠️ Tecnologias

- **Python 3.11+**
- **Streamlit**: Framework de interface.
- **MSAL**: Biblioteca de autenticação Microsoft.
- **Pandas**: Manipulação de dados.

## ⚙️ Instalação e Configuração

O projeto utiliza um ambiente virtual global na raiz.

1. **Clone o repositório** (ou baixe os arquivos).
2. **Crie o ambiente virtual**:
   ```powershell
   python -m venv .venv
   ```
3. **Instale as dependências**:
   ```powershell
   .\.venv\Scripts\pip install -r Estoque-Em-Tempo-Real-Streamlit/requirements.txt streamlit msal pandas openpyxl pyodbc
   ```
4. **Configure as Credenciais**:
   - Certifique-se de que o arquivo `backend/secrets.toml` (ou similar) esteja configurado com as chaves do Azure e Banco de Dados.

## ▶️ Como Rodar

Abra o terminal na pasta raiz do projeto (`.../Relatorios`) e execute:

```powershell
.\.venv\Scripts\python.exe -m streamlit run Menu/app.py
```

O sistema estará acessível em: `http://localhost:8507`

## 📂 Estrutura do Projeto

- **Menu/**: Aplicação principal (Entry point), Login, Home e Navegação.
  - `app.py`: Roteador principal.
  - `permissions.json`: Banco de dados local de permissões.
- **Estoque-Em-Tempo-Real-Streamlit/**: Módulo do relatório de estoque.
