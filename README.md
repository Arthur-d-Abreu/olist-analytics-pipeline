# 📊 Projeto de Análise de Dados — Olist E-commerce

Este projeto tem como objetivo realizar um pipeline completo de **engenharia e análise de dados**, partindo de dados brutos até a construção de um **modelo dimensional (Star Schema)** pronto para consumo em ferramentas de BI.

---

## 🚀 Objetivo do Projeto

Construir uma solução completa de dados que permita:

- Organização dos dados transacionais
- Criação de um **Data Warehouse dimensional**
- Geração de insights estratégicos
- Visualização clara através de dashboards

---

## 🧱 Arquitetura do Projeto
CSV → Python (ETL) → Banco de Dados Relacional → Modelagem Dimensional (Star Schema) → Power BI

---

## ⚙️ Tecnologias Utilizadas

- Python (Pandas, SQLAlchemy)
- SQL Server
- SQL (T-SQL)
- Power BI
- Git & GitHub

---

## 🗂️ Estrutura do Repositório

├── data/
│   ├── raw/            # Arquivos CSV originais
│   └── processed/      # Dados tratados prontos para carga
│
├── scripts/
│   ├── clean_data.py   # Limpeza e tratamento dos dados
│   └── upload_base.py  # Carga automatizada para o SQL Server
│
├── sql/
│   └── views.sql       # Criação das views dimensionais e fato
│
├── powerbi/
│   └── dashboard.pbix  # Dashboard final(em construção)
│
└── README.md

---

## 🛠️ Processo ETL
O pipeline ETL foi desenvolvido em Python utilizando Pandas e SQLAlchemy, implementando práticas de engenharia de dados, incluindo:

- Padronização de nomes de colunas
- Tratamento de valores nulos
- Correção de tipos de dados
- Criação automática de tabelas no banco
- Carga incremental em chunks para alta performance

O processo de carga é totalmente automatizado, com suporte a múltiplos bancos de dados (SQL Server, PostgreSQL, MySQL e SQLite), garantindo portabilidade e escalabilidade.

---
⚙️ Como Executar o Projeto
### 1️⃣ Criar ambiente virtual (opcional)
```bash
python -m venv venv
venv\Scripts\activate
```
### 2️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```
### 3️⃣ Limpar os dados

python scripts/clean_data.py

### 4️⃣ Subir os dados no banco
```bash
python scripts/upload_base.py --db-type sqlserver
```
### 5️⃣ Criar as views dimensionais

Executar os scripts SQL localizados na pasta /sql no SQL Server.

## 🧩 Modelo Dimensional

O projeto implementa **modelagem dimensional em estrela (Star Schema)**, separando fatos e dimensões para otimizar consultas analíticas e performance em BI.


### 🔹 Tabela Fato

- `vw_fato_vendas`

### 🔹 Dimensões

- `vw_dim_cliente`
- `vw_dim_produto`
- `vw_dim_vendedores`
- `vw_dim_tempo`

---

## 📐 Regras de Negócio

### Classificação de tamanho de produto

Foi criado um critério baseado no volume do produto:


| Volume (cm³) | Classificação |
|---------------|---------------|
| ≤ 20.000      | Pequeno       |
| ≤ 100.000     | Médio         |
| > 100.000     | Grande        |

---

## 📊 Dashboard no Power BI

Construção de dashboards no **Power BI**, incluindo:

- Receita total
- Ticket médio
- Vendas por estado
- Vendas por categoria
- Distribuição logística por tamanho

---

## 👨‍💻 Autor

Arthur Abreu  
Projeto desenvolvido para fins educacionais, validação de conhecimentos em engenharia e análise de dados, e composição de portfólio profissional.

--------------------------------------------------------------------------------------------------------------------------------------------------------

EN

# 📊 Data Analytics Project — Olist E-commerce

This project aims to build a complete **data engineering and analytics pipeline**, starting from raw data ingestion to the construction of a **dimensional data warehouse (Star Schema)**, ready for consumption by BI tools.

---

## 🚀 Project Objective

To build a complete data solution that enables:

- Organization of transactional data  
- Creation of a **dimensional Data Warehouse**  
- Generation of strategic insights  
- Clear and efficient visualization through dashboards  

---

## 🧱 Project Architecture

CSV → Python (ETL) → Relational Database → Dimensional Modeling (Star Schema) → Power BI

---

## ⚙️ Technologies Used

- Python (Pandas, SQLAlchemy)  
- SQL Server  
- SQL (T-SQL)  
- Power BI  
- Git & GitHub  

---

## 🗂️ Repository Structure

├── data/
│ ├── raw/ # Original CSV files
│ └── processed/ # Cleaned data ready for loading
│
├── scripts/
│ ├── clean_data.py # Data cleaning and preprocessing
│ └── upload_base.py # Automated database loading
│
├── sql/
│ └── views.sql # Creation of fact and dimension views
│
├── powerbi/
│ └── dashboard.pbix # Final dashboard (in progress)
│
└── README.md

---

---

## 🛠️ ETL Process

The ETL pipeline was developed in Python using Pandas and SQLAlchemy, following data engineering best practices, including:

- Column name standardization  
- Missing value handling  
- Data type correction  
- Automatic table creation  
- Chunk-based incremental loading for high performance  

The loading process is fully automated and supports multiple databases (SQL Server, PostgreSQL, MySQL, and SQLite), ensuring portability and scalability.

---

## ⚙️ How to Run the Project

### 1️⃣ Create a virtual environment (optional)
```bash
python -m venv venv
venv\Scripts\activate
```
### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Clean the data

python scripts/clean_data.py

### 4️⃣ Load data into the database
```bash
python scripts/upload_base.py --db-type sqlserver
```
### 5️⃣ Create dimensional views

Executar os scripts SQL localizados na pasta /sql no SQL Server.

## 🧩 Dimensional Model

The project implements star schema dimensional modeling, separating fact and dimension tables to optimize analytical queries and BI performance.


### 🔹 Fact Table

- `vw_fato_vendas`

### 🔹 Dimensions

- `vw_dim_cliente`
- `vw_dim_produto`
- `vw_dim_vendedores`
- `vw_dim_tempo`

---

## 📐 Business Rules

Product size classification

A business rule was created based on product volume:


| Volume (cm³) | Classificação |
|---------------|---------------|
| ≤ 20.000      | Small         |
| ≤ 100.000     | Medium        |
| > 100.000     | Large         |

---

## 📊 Dashboard on Power BI

Development of dashboards in Power BI, including:

- Total revenue
- Average ticket
- Sales by state
- Sales by category
- Logistics distribution by product size

---

## 👨‍💻 Author

Arthur Abreu
Project developed for educational purposes, validation of data engineering and analytics skills, and professional portfolio composition.


