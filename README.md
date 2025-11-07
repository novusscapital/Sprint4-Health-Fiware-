# 🩺 **HealthD01 – IoT Health Monitoring System**

## 👥 **Integrantes**
| Nome | RM | Função |
|------|----|--------|
| Matheus Bispo Faria Barbosa | RM562140 | Desenvolvimento, integração e documentação |
| Henrique Keigo Nakashima Minowa | RM564091 | Configuração do FIWARE, arquitetura e testes |
| Eduardo Delorenzo Moraes | RM561749 | Desenvolvimento do data feeder e dashboard |

---

## 🧠 **Descrição do Projeto**

O **HealthD01** é um sistema de **monitoramento esportivo inteligente** baseado em **IoT**, projetado para acompanhar em tempo real os **batimentos cardíacos**, a **temperatura corporal** e a **distância percorrida** de atletas durante treinos e partidas.  

O objetivo do projeto é permitir que **médicos e treinadores** acompanhem o desempenho e a condição física das jogadoras, prevenindo situações de risco e otimizando o desempenho.

A coleta de dados é feita por meio de uma **pulseira RFID simulada**, e os valores são enviados para o **FIWARE**, onde são armazenados e exibidos em um **dashboard dinâmico desenvolvido em Python (Dash)**.

---

## 🧩 **Arquitetura Proposta**

### **Diagrama da Arquitetura**
```
+-------------------+         +----------------------+         +----------------------+
|  Pulseira RFID /  |  --->   |   IoT Agent (UL2.0)  |  --->   |   Orion Context Broker|
|  Simulador Wokwi  |         |     Porta: 7896      |         |     Porta: 1026      |
+-------------------+         +----------------------+         +----------------------+
                                    |                                       |
                                    |                                       v
                                    |                          +--------------------------+
                                    |                          |     Dashboard (Python)    |
                                    |                          |     Porta: 5000           |
                                    |                          +--------------------------+
                                    |
                                    v
                           +-------------------------+
                           |   Data Feeder (Python)  |
                           |   Envio de métricas fixas|
                           +-------------------------+
```

---

## ⚙️ **Explicação da Arquitetura**

1. **Dispositivo IoT (simulado)**  
   - Representa uma pulseira RFID posicionada em pontos de circulação sanguínea.  
   - Mede *batimentos cardíacos*, *temperatura corporal* e *distância percorrida*.  
   - Os dados são enviados via **Ultralight 2.0** para o **IoT Agent**.

2. **IoT Agent (FIWARE)**  
   - Traduz o protocolo Ultralight 2.0 para NGSIv2.  
   - Porta utilizada: **7896**  
   - Serviço: **health**

3. **Orion Context Broker**  
   - Armazena e distribui os dados em formato de contexto.  
   - Porta: **1026**

4. **Data Feeder (Python)**  
   - Script que simula o envio de dados contínuos para o FIWARE.  
   - Envia requisições POST para o IoT Agent, atualizando o Orion.

5. **Dashboard (Python Dash)**  
   - Exibe os dados do atleta em tempo real:  
     - Temperatura corporal (°C)  
     - Frequência cardíaca (bpm)  
     - Distância percorrida (km)  
   - Atualização automática a cada 5 segundos.

---

## 🧰 **Recursos Necessários**

### **Software**
- **FIWARE Generic Enablers**:
  - IoT Agent Ultralight 2.0
  - Orion Context Broker
  - STH-Comet (opcional para histórico)
- **Python 3.10+**
  - Bibliotecas: `dash`, `requests`, `plotly`
- **Postman** (para configuração e testes)
- **Git + GitHub** (para versionamento)
- **VM Azure** (para execução e deploy)
- **Wokwi** (para simulação do hardware ESP32)

### **Hardware (simulado)**
- ESP32 DevKit v1  
- Sensor de temperatura (simulado)  
- Sensor de batimentos (simulado)  
- RFID Tag / Pulseira simulada

---

## 🚀 **Instruções de Uso**

### **1. Clonar o repositório**
```bash
git clone https://github.com/<seu-usuario>/HealthD01.git
cd HealthD01
```

### **2. Instalar dependências**
```bash
pip install -r requirements.txt
```

### **3. Executar o Data Feeder**
```bash
python data_feeder.py
```
*(Simula o envio de métricas para o FIWARE.)*

### **4. Executar o Dashboard**
```bash
python dashboard.py
```
Acesse em:  
👉 `http://localhost:8050` ou `http://<IP_VM>:5000`

---

## 🧪 **Códigos-Fonte**

| Componente | Descrição |
|-------------|------------|
| `data_feeder.py` | Script que envia dados simulados para o IoT Agent |
| `dashboard.py` | Interface visual em Python Dash para exibir os dados |
| `fiware_collection.json` | Collection do Postman com todas as requisições de setup |
| `iot_device_config.json` | Estrutura de registro de dispositivos no FIWARE |
| `requirements.txt` | Dependências do Python para execução local ou na VM |

---

## 🧠 **Princípios Técnicos**

- **Protocolo Ultralight 2.0** para comunicação leve entre IoT e FIWARE.  
- **NGSIv2** para gerenciamento de contexto no Orion.  
- **Dash (Plotly)** para visualização responsiva e leve.  
- **API REST** para integração entre componentes.  
- **Simulação Wokwi** e **Postman** para validação.

---

## 🎯 **Objetivo Final**

O **HealthD01** busca demonstrar como a tecnologia IoT pode ser aplicada no **esporte feminino** para fornecer dados confiáveis e em tempo real, ajudando no **planejamento físico**, **prevenção de lesões** e **monitoramento de desempenho**.

---

## 📈 **Próximos Passos**

- Integração com sensores reais via ESP32.  
- Implementação de alertas em tempo real (notificações de risco).  
- Histórico de dados via **STH-Comet**.  
- Migração do dashboard para **deploy automático (Docker + Azure)**.

---

## 🩵 **Licença**

Este projeto foi desenvolvido como parte do curso de **Engenharia de Computação – FIAP**, no módulo de **IoT e Soluções Inteligentes**, para fins educacionais e demonstrativos.
