# Guia Completo de Banco de Dados - ProjectCare

## Índice
1. [Introdução](#introdução)
2. [Conceitos Fundamentais](#conceitos-fundamentais)
3. [As 4 Integridades do Banco de Dados](#as-4-integridades-do-banco-de-dados)
4. [Análise das Tabelas do Sistema](#análise-das-tabelas-do-sistema)
5. [Scripts DDL Completos](#scripts-ddl-completos)
6. [Diagrama de Entidade e Relacionamento](#diagrama-de-entidade-e-relacionamento)
7. [Relacionamentos entre Tabelas](#relacionamentos-entre-tabelas)
8. [Exemplos Práticos](#exemplos-práticos)
9. [Considerações para Apresentação](#considerações-para-apresentação)

---

## Introdução

O **ProjectCare** é um sistema de gerenciamento de cuidadores para idosos, desenvolvido em Python com Flask e SQLAlchemy. Este documento apresenta uma análise completa da estrutura de banco de dados do sistema, explicando todos os conceitos necessários para compreender e apresentar o projeto em uma avaliação acadêmica.

O sistema permite que usuários se cadastrem como **responsáveis** por idosos ou como **cuidadores profissionais**, facilitando a criação de contratos entre eles. A arquitetura do banco de dados reflete essa lógica de negócio através de 5 tabelas principais interconectadas.

---

## Conceitos Fundamentais

### O que é um Banco de Dados Relacional?

Um banco de dados relacional é um sistema de armazenamento de dados organizados em **tabelas** (também chamadas de relações), onde:

- **Tabela**: Estrutura que armazena dados em linhas e colunas
- **Linha (Registro/Tupla)**: Uma entrada individual na tabela
- **Coluna (Atributo/Campo)**: Uma característica específica dos dados
- **Chave Primária (PK)**: Identificador único de cada linha
- **Chave Estrangeira (FK)**: Referência a uma chave primária de outra tabela

### DDL (Data Definition Language)

DDL é a linguagem usada para **definir a estrutura** do banco de dados. Os principais comandos são:

- **CREATE TABLE**: Cria uma nova tabela
- **ALTER TABLE**: Modifica uma tabela existente
- **DROP TABLE**: Remove uma tabela
- **CREATE INDEX**: Cria índices para otimizar consultas

### Por que usar DDL?

- **Padronização**: Define estruturas consistentes
- **Controle**: Especifica regras de integridade
- **Documentação**: Serve como documentação técnica
- **Migração**: Facilita a recriação do banco em diferentes ambientes

---

## As 4 Integridades do Banco de Dados

### 1. Integridade de Entidade

**Conceito**: Cada tabela deve ter uma chave primária única e não nula.

**Por que é importante?**: Garante que cada registro seja único e identificável.

**Implementação no ProjectCare**:
```sql
-- Cada tabela tem sua chave primária
id INTEGER PRIMARY KEY NOT NULL
```

**Exemplo Prático**:
- Não podem existir dois usuários com o mesmo ID
- Todo registro deve ter um identificador válido

### 2. Integridade Referencial

**Conceito**: As chaves estrangeiras devem referenciar chaves primárias válidas.

**Por que é importante?**: Mantém a consistência entre tabelas relacionadas.

**Implementação no ProjectCare**:
```sql
-- Chave estrangeira com referência obrigatória
user_id INTEGER NOT NULL REFERENCES users(id)
responsible_id INTEGER NOT NULL REFERENCES responsible(id)
```

**Exemplo Prático**:
- Um idoso só pode ser cadastrado se houver um responsável válido
- Um contrato só pode existir entre cuidador e responsável existentes

### 3. Integridade de Domínio

**Conceito**: Os valores das colunas devem respeitar os tipos e restrições definidos.

**Por que é importante?**: Garante que os dados estejam no formato correto.

**Implementação no ProjectCare**:
```sql
-- Restrições de tipo e tamanho
email VARCHAR(100) UNIQUE NOT NULL,
rating FLOAT DEFAULT 0.0 CHECK (rating >= 0 AND rating <= 5),
gender VARCHAR(20) NOT NULL,
status VARCHAR(20) DEFAULT 'active'
```

**Exemplo Prático**:
- Email deve ser único no sistema
- Avaliação (rating) deve estar entre 0 e 5
- Campos obrigatórios não podem ser nulos

### 4. Integridade Definida pelo Usuário (Regras de Negócio)

**Conceito**: Regras específicas do sistema que devem ser respeitadas.

**Por que é importante?**: Garante que a lógica de negócio seja mantida no banco.

**Implementação no ProjectCare**:
```sql
-- Regras de negócio específicas
CHECK (start_date < end_date),  -- Data fim deve ser posterior à data início
CHECK (experience >= 0),        -- Experiência não pode ser negativa
CHECK (birthdate < CURRENT_DATE) -- Data de nascimento deve ser no passado
```

**Exemplo Prático**:
- Contrato não pode terminar antes de começar
- Pessoa não pode ter nascido no futuro
- Experiência profissional deve ser um valor positivo

---

## Análise das Tabelas do Sistema

### Tabela USERS (Usuários Base)

**Propósito**: Armazena informações básicas de todos os usuários do sistema.

**Características**:
- Tabela central do sistema
- Usa hash Argon2 para senhas (alta segurança)
- Campos únicos impedem duplicação (email, CPF, telefone)

**Campos Importantes**:
- `id`: Identificador único (chave primária)
- `cpf`: CPF único para cada usuário
- `email`: Email único para login
- `password_hash`: Senha criptografada com Argon2
- `created_at`: Timestamp de criação

### Tabela CAREGIVER (Cuidadores)

**Propósito**: Estende a tabela users com informações profissionais específicas de cuidadores.

**Características**:
- Relacionamento 1:1 com users
- Armazena competências e disponibilidade
- Sistema de avaliação (rating)

**Campos Específicos**:
- `specialty`: Especialidade do cuidador
- `experience`: Anos de experiência
- `skills`: Habilidades detalhadas (texto de até 500 caracteres)
- `rating`: Avaliação média (0.0 a 5.0)
- `pretensao_salarial`: Expectativa salarial

### Tabela RESPONSIBLE (Responsáveis)

**Propósito**: Estende a tabela users com informações específicas de responsáveis por idosos.

**Características**:
- Relacionamento 1:1 com users
- Pode ter múltiplos idosos associados
- Informações sobre necessidades de cuidado

**Campos Específicos**:
- `relationship_with_elderly`: Tipo de parentesco
- `primary_need_description`: Descrição das necessidades principais
- `preferred_contact_method`: Forma preferida de contato

### Tabela ELDERLY (Idosos)

**Propósito**: Armazena informações detalhadas sobre os idosos que precisam de cuidados.

**Características**:
- Relacionamento N:1 com responsible
- Informações médicas e de emergência
- Dados específicos de saúde

**Campos Importantes**:
- `medical_conditions`: Condições médicas (campo texto)
- `allergies`: Alergias conhecidas
- `medications_in_use`: Medicamentos em uso
- `emergency_contact_*`: Dados de contato de emergência
- `health_plan_*`: Informações do plano de saúde

### Tabela CONTRACT (Contratos)

**Propósito**: Gerencia contratos entre cuidadores e responsáveis.

**Características**:
- Relacionamento N:1 com caregiver e responsible
- Informações financeiras e contratuais
- Sistema de status e versionamento

**Campos Específicos**:
- `hourly_rate`: Valor por hora (decimal)
- `monthly_salary`: Salário mensal
- `payment_frequency`: Frequência de pagamento
- `status`: Status do contrato (active, completed, cancelled)
- `work_schedule`: Horários detalhados

---

## Scripts DDL Completos

### 1. Tabela USERS

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    cpf VARCHAR(17) UNIQUE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    birthdate DATE NOT NULL CHECK (birthdate < CURRENT_DATE),
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_cpf_unique UNIQUE (cpf),
    CONSTRAINT users_email_unique UNIQUE (email),
    CONSTRAINT users_phone_unique UNIQUE (phone),
    CONSTRAINT users_birthdate_check CHECK (birthdate < CURRENT_DATE)
);
```

### 2. Tabela CAREGIVER

```sql
CREATE TABLE caregiver (
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    experience INTEGER NOT NULL CHECK (experience >= 0),
    education VARCHAR(100) NOT NULL,
    expertise_area VARCHAR(100) NOT NULL,
    skills VARCHAR(500) NOT NULL,
    rating FLOAT DEFAULT 0.0 CHECK (rating >= 0.0 AND rating <= 5.0),
    dias_disponiveis VARCHAR(100),
    periodos_disponiveis VARCHAR(100),
    inicio_imediato BOOLEAN,
    pretensao_salarial DECIMAL(10,2) CHECK (pretensao_salarial >= 0),
    
    CONSTRAINT caregiver_pk PRIMARY KEY (id),
    CONSTRAINT caregiver_user_fk FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT caregiver_experience_check CHECK (experience >= 0),
    CONSTRAINT caregiver_rating_check CHECK (rating >= 0.0 AND rating <= 5.0),
    CONSTRAINT caregiver_salary_check CHECK (pretensao_salarial >= 0)
);
```

### 3. Tabela RESPONSIBLE

```sql
CREATE TABLE responsible (
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    relationship_with_elderly VARCHAR(50),
    primary_need_description VARCHAR(255),
    preferred_contact_method VARCHAR(30),
    
    CONSTRAINT responsible_pk PRIMARY KEY (id),
    CONSTRAINT responsible_user_fk FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);
```

### 4. Tabela ELDERLY

```sql
CREATE TABLE elderly (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    cpf VARCHAR(20),
    birthdate DATE NOT NULL CHECK (birthdate < CURRENT_DATE),
    gender VARCHAR(10) NOT NULL,
    address_elderly VARCHAR(255),
    city_elderly VARCHAR(100),
    state_elderly VARCHAR(100),
    photo_url VARCHAR(255),
    medical_conditions TEXT,
    allergies TEXT,
    medications_in_use TEXT,
    mobility_level VARCHAR(40),
    specific_care_needs TEXT,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(30),
    emergency_contact_relationship VARCHAR(50),
    health_plan_name VARCHAR(100),
    health_plan_number VARCHAR(50),
    additional_notes TEXT,
    responsible_id INTEGER NOT NULL,
    
    CONSTRAINT elderly_pk PRIMARY KEY (id),
    CONSTRAINT elderly_responsible_fk FOREIGN KEY (responsible_id) REFERENCES responsible(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT elderly_birthdate_check CHECK (birthdate < CURRENT_DATE)
);
```

### 5. Tabela CONTRACT

```sql
CREATE TABLE contract (
    id INTEGER PRIMARY KEY NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    hourly_rate DECIMAL(10,2) CHECK (hourly_rate >= 0),
    monthly_salary DECIMAL(10,2) CHECK (monthly_salary >= 0),
    payment_frequency VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active' NOT NULL 
        CHECK (status IN ('active', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    work_schedule TEXT,
    special_conditions TEXT,
    notes TEXT,
    responsible_id INTEGER NOT NULL,
    caregiver_id INTEGER NOT NULL,
    
    CONSTRAINT contract_pk PRIMARY KEY (id),
    CONSTRAINT contract_responsible_fk FOREIGN KEY (responsible_id) REFERENCES responsible(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT contract_caregiver_fk FOREIGN KEY (caregiver_id) REFERENCES caregiver(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT contract_dates_check CHECK (start_date < end_date OR end_date IS NULL),
    CONSTRAINT contract_hourly_rate_check CHECK (hourly_rate >= 0),
    CONSTRAINT contract_salary_check CHECK (monthly_salary >= 0),
    CONSTRAINT contract_status_check CHECK (status IN ('active', 'completed', 'cancelled'))
);
```

---

## Diagrama de Entidade e Relacionamento

### Representação Textual do DER

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│      USERS      │────→│   CAREGIVER     │────→│    CONTRACT     │
│                 │ 1:1 │                 │ 1:N │                 │
│ • id (PK)       │     │ • id (PK)       │     │ • id (PK)       │
│ • name          │     │ • user_id (FK)  │     │ • caregiver_id  │
│ • cpf (UNIQUE)  │     │ • specialty     │     │ • responsible_id│
│ • email (UNIQUE)│     │ • experience    │     │ • start_date    │
│ • password_hash │     │ • skills        │     │ • end_date      │
│ • phone         │     │ • rating        │     │ • hourly_rate   │
│ • address       │     │ • pretensao     │     │ • status        │
│ • birthdate     │     │ • disponibilid. │     └─────────────────┘
│ • created_at    │     └─────────────────┘              ↑
└─────────────────┘                                      │ N:1
         │ 1:1                                           │
         ↓                                               │
┌─────────────────┐     ┌─────────────────┐              │
│   RESPONSIBLE   │────→│     ELDERLY     │              │
│                 │ 1:N │                 │              │
│ • id (PK)       │     │ • id (PK)       │              │
│ • user_id (FK)  │     │ • name          │              │
│ • relationship  │     │ • cpf           │              │
│ • need_descrip. │     │ • birthdate     │              │
│ • contact_method│     │ • medical_cond. │              │
└─────────────────┘     │ • allergies     │              │
         │               │ • medications   │              │
         └─────────────→ │ • emergency_*   │              │
                    1:N  │ • responsible_id│──────────────┘
                         └─────────────────┘
```

### Explicação dos Relacionamentos

1. **USERS ↔ CAREGIVER (1:1)**
   - Um usuário pode ter no máximo um perfil de cuidador
   - Um cuidador pertence a exatamente um usuário

2. **USERS ↔ RESPONSIBLE (1:1)**
   - Um usuário pode ter no máximo um perfil de responsável
   - Um responsável pertence a exatamente um usuário

3. **RESPONSIBLE ↔ ELDERLY (1:N)**
   - Um responsável pode cuidar de múltiplos idosos
   - Cada idoso tem exatamente um responsável

4. **CAREGIVER ↔ CONTRACT (1:N)**
   - Um cuidador pode ter múltiplos contratos
   - Cada contrato tem exatamente um cuidador

5. **RESPONSIBLE ↔ CONTRACT (1:N)**
   - Um responsável pode criar múltiplos contratos
   - Cada contrato tem exatamente um responsável

---

## Relacionamentos entre Tabelas

### Tipos de Relacionamento Implementados

#### 1. Um para Um (1:1)
**Exemplo**: USERS ↔ CAREGIVER

**Características**:
- Chave estrangeira com restrição de unicidade
- `uselist=False` no SQLAlchemy
- Cascata de exclusão opcional

**Implementação**:
```sql
-- Em CAREGIVER
user_id INTEGER UNIQUE NOT NULL REFERENCES users(id)
```

#### 2. Um para Muitos (1:N)
**Exemplo**: RESPONSIBLE ↔ ELDERLY

**Características**:
- Chave estrangeira no lado "muitos"
- `uselist=True` no SQLAlchemy (padrão)
- Cascata de exclusão recomendada

**Implementação**:
```sql
-- Em ELDERLY
responsible_id INTEGER NOT NULL REFERENCES responsible(id)
```

#### 3. Muitos para Muitos (M:N)
**Nota**: Não implementado diretamente, mas pode ser modelado através de CONTRACT

**Como seria implementado**:
```sql
-- Tabela de relacionamento
CREATE TABLE caregiver_responsible (
    caregiver_id INTEGER REFERENCES caregiver(id),
    responsible_id INTEGER REFERENCES responsible(id),
    PRIMARY KEY (caregiver_id, responsible_id)
);
```

### Regras de Cascata Implementadas

#### ON DELETE CASCADE
**Quando usar**: Quando a exclusão do pai deve excluir os filhos

**Exemplos no sistema**:
- Excluir USER → exclui CAREGIVER e RESPONSIBLE
- Excluir RESPONSIBLE → exclui ELDERLY associados
- Excluir CAREGIVER → exclui CONTRACTS associados

#### ON UPDATE CASCADE
**Quando usar**: Quando mudanças na chave primária devem se propagar

**Implementação**:
```sql
FOREIGN KEY (user_id) REFERENCES users(id) 
    ON DELETE CASCADE ON UPDATE CASCADE
```

---

## Exemplos Práticos

### Inserção de Dados Respeitando Integridades

#### 1. Criando um Usuário Base
```sql
-- Primeiro, criar o usuário base
INSERT INTO users (name, cpf, gender, birthdate, phone, email, password_hash, address, city, state)
VALUES (
    'João Silva',
    '123.456.789-00',
    'Masculino',
    '1980-05-15',
    '(11) 99999-1234',
    'joao@email.com',
    '$argon2id$v=19$m=131072,t=5,p=10$...', -- Hash gerado
    'Rua das Flores, 123',
    'São Paulo',
    'SP'
);
```

#### 2. Criando um Perfil de Responsável
```sql
-- Usar o ID do usuário criado
INSERT INTO responsible (user_id, relationship_with_elderly, primary_need_description, preferred_contact_method)
VALUES (
    1, -- ID do usuário João Silva
    'Filho',
    'Cuidados básicos diários e acompanhamento médico',
    'WhatsApp'
);
```

#### 3. Cadastrando um Idoso
```sql
-- Associar ao responsável
INSERT INTO elderly (name, cpf, birthdate, gender, medical_conditions, responsible_id)
VALUES (
    'Maria Silva',
    '987.654.321-00',
    '1940-03-20',
    'Feminino',
    'Diabetes, Hipertensão',
    1 -- ID do responsável
);
```

### Consultas Demonstrando Integridades

#### Verificando Integridade Referencial
```sql
-- Esta consulta mostra todos os idosos com seus responsáveis
-- Demonstra que não existem "órfãos" no sistema
SELECT 
    e.name AS idoso_nome,
    u.name AS responsavel_nome,
    u.email AS responsavel_email
FROM elderly e
INNER JOIN responsible r ON e.responsible_id = r.id
INNER JOIN users u ON r.user_id = u.id;
```

#### Verificando Integridade de Domínio
```sql
-- Esta consulta verifica se todos os ratings estão no range correto
SELECT 
    c.id,
    u.name,
    c.rating
FROM caregiver c
INNER JOIN users u ON c.user_id = u.id
WHERE c.rating < 0 OR c.rating > 5; -- Deveria retornar 0 registros
```

---

## Considerações para Apresentação

### Pontos Importantes a Destacar

#### 1. Arquitetura do Sistema
- **Separação de Responsabilidades**: Tabela users centraliza dados básicos, tabelas específicas armazenam informações especializadas
- **Flexibilidade**: Usuário pode ser apenas caregiver, apenas responsável, ou ambos
- **Escalabilidade**: Estrutura permite crescimento do sistema

#### 2. Implementação das Integridades
- **Integridade de Entidade**: Todas as tabelas têm chaves primárias auto-incrementais
- **Integridade Referencial**: Todas as FKs têm cascatas apropriadas
- **Integridade de Domínio**: CHECKs, UNIQUEs e NOT NULLs bem definidos
- **Regras de Negócio**: Implementadas através de constraints personalizadas

#### 3. Decisões de Design
- **Uso de TEXT vs VARCHAR**: Campos como observações médicas usam TEXT para permitir descrições detalhadas
- **Campos Opcionais**: Informações como CPF do idoso são opcionais para flexibilidade
- **Sistema de Status**: Contratos têm status para controle de ciclo de vida

### Scripts para Demonstração

#### Para gerar o DER no DBeaver:
1. Conecte-se ao banco de dados
2. Clique com botão direito no schema
3. Selecione "View Diagram"
4. O DBeaver gerará automaticamente o diagrama ER

#### Para demonstrar as integridades:
```sql
-- Teste de Integridade Referencial (deve falhar)
INSERT INTO elderly (name, responsible_id) VALUES ('Teste', 999);

-- Teste de Integridade de Domínio (deve falhar)  
INSERT INTO caregiver (rating) VALUES (-1);

-- Teste de Integridade de Entidade (deve falhar)
INSERT INTO users (name) VALUES ('Teste Sem Campos Obrigatórios');
```

### Estrutura Sugerida para Apresentação

1. **Introdução** (2-3 minutos)
   - Apresentar o sistema ProjectCare
   - Explicar a importância do banco de dados

2. **Conceitos Teóricos** (3-4 minutos)
   - As 4 integridades
   - DDL e sua importância

3. **Demonstração Prática** (5-6 minutos)
   - Mostrar o diagrama ER no DBeaver
   - Executar alguns DDLs
   - Demonstrar integridades funcionando

4. **Análise das Tabelas** (3-4 minutos)
   - Explicar cada tabela e seus relacionamentos
   - Destacar decisões de design

5. **Conclusão** (1-2 minutos)
   - Resumir benefícios da estrutura implementada
   - Responder perguntas

### Possíveis Perguntas e Respostas

**P: Por que separar users de caregiver/responsible?**
**R**: Para permitir que um usuário possa ter ambos os perfis e evitar duplicação de dados básicos.

**P: Como garantir que email seja único?**
**R**: Através da constraint UNIQUE na coluna email da tabela users.

**P: O que acontece se excluir um responsável?**
**R**: Devido ao CASCADE, todos os idosos e contratos associados também são excluídos, mantendo a integridade referencial.

**P: Por que usar Argon2 para senhas?**
**R**: É um algoritmo moderno de hash, vencedor da Password Hashing Competition, oferecendo alta segurança contra ataques.

---

**Este documento foi criado para apoiar sua apresentação sobre banco de dados. Ele cobre todos os aspectos necessários para demonstrar conhecimento sobre DDL, integridades e design de banco de dados relacionais.**
