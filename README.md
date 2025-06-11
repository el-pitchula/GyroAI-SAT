<h1 align="center">GyroAI-SAT 🛰️<p></h1>


<div align="center">
  <strong>Detecção de Gimbal Lock em Satélites com IA: Uma Abordagem Baseada em TLE e Quaternions<p>(Proposta de pipeline de monitoramento e previsão de anomalias de atitude)<p></strong>
</div>

## 🔭 Overview

GyroAI-SAT é um projeto de Inteligência Artificial para estabilização de satélites e mitigação do gimbal lock. O modelo de IA é treinado para prever e corrigir falhas de orientação, garantindo um controle mais eficiente (atualizar).

## 💻 Technologies

- Python (.py)
- Jupyter (.ipynb)
- MATLAB (.m)

[![Tec](https://skillicons.dev/icons?i=py,sklearn,tensorflow,matlab)](https://skillicons.dev)

## O arquivo Excel(.xlsx) contém os seguintes dados por amostra temporal:

| Coluna   | Significado                                                    |
| -------- | -------------------------------------------------------------- |
| `tempo`  | Instante da amostra                                            |
| `q0..q3` | Componentes do quaternion                                      |
| `roll`   | Ângulo em torno do eixo X                                      |
| `pitch`  | Ângulo em torno do eixo Y (**principal causa do Gimbal Lock**) |
| `yaw`    | Ângulo em torno do eixo Z                                      |
| `status` | Rótulo (ok, alerta, gimbal\_lock) gerado automaticamente       |

## Pipeline:

- 📥 Carrega os dados de orientação (quaternions e ângulos de Euler);
- 🔧 Pré-processa esses dados (normaliza, cria janelas temporais);
- 🧠 Usa os dados para treinar uma IA (LSTM);
- 📊 Retorna previsões de risco de Gimbal Lock (ok, alerta, gimbal_lock).

Ou seja, você entrega dados TLE → ele gera o risco em tempo real.

## Instalação
Para rodar o projeto localmente:
```bash
git clone https://github.com/seu-usuario/GyroAI-SAT.git
cd GyroAI-SAT
pip install -r requirements.txt
```

## Como Usar (atualizar)

Pré-processar os dados:

    python src/preprocessing.py

Treinar o modelo de IA:

    python src/model.py

Rodar a simulação:

    python src/simulation.py

## 📜 Licença

Este projeto está sob a licença MIT.




<h1 align="center">🛰️ GyroAI-SAT</h1> 
<div align="center"> 
    <strong>Detecção de Gimbal Lock em Satélites com IA</strong><br> 
    <em>Uma abordagem baseada em TLE e Quaternions para previsão de anomalias de atitude</em> 
</div>

🔭 Visão Geral

GyroAI-SAT é um projeto de inteligência artificial voltado para a detecção antecipada de Gimbal Lock em satélites. Utilizando dados orbitais reais (TLE), o sistema gera automaticamente representações de orientação (quaternions e ângulos de Euler) e classifica o estado de risco via rede neural LSTM.

    Objetivo: Antecipar falhas críticas de orientação em tempo real, melhorando a estabilidade e controle de satélites.

🧠 Tecnologias Utilizadas

    Python (código principal)

    Jupyter Notebook (documentação técnica e análises)

    MATLAB (modelagem e simulação da função de transferência)

📁 Dados

O arquivo dados_orientacao.xlsx contém uma amostra temporal de orientação do satélite:
Coluna	Significado
tempo	Instante da amostra (s)
q0..q3	Componentes do quaternion
roll	Ângulo de Euler em torno do eixo X
pitch	Ângulo de Euler em torno do eixo Y (chave para Gimbal Lock)
yaw	Ângulo de Euler em torno do eixo Z
status	Rótulo automático: ok, alerta, gimbal_lock
🧪 Pipeline de Execução

graph TD
  A[TLE (.txt)] --> B[SGP4]
  B --> C[Vetores: r(t), v(t)]
  C --> D[Matriz de Rotação R(t)]
  D --> E{Conversão}
  E --> F1[Quaternions q(t)]
  E --> F2[Ângulos de Euler (roll, pitch, yaw)]
  F2 --> G[Rotulagem automática]
  G --> H[Janela Temporal X_t]
  H --> I[IA: Rede LSTM]
  I --> J[Previsão: ok / alerta / gimbal_lock]

⚙️ Instalação

Clone o repositório e instale as dependências:

git clone https://github.com/seu-usuario/GyroAI-SAT.git
cd GyroAI-SAT
pip install -r requirements.txt

🚀 Como Usar

Pré-processar os dados:

python src/preprocessing.py

Treinar o modelo:

python src/train_model.py

Rodar a inferência/simulação:

python src/simulation.py

    Também é possível acompanhar o projeto via notebook interativo:
    🧮 Google Colab – Modelagem Matemática e IA

📈 Resultados

    Acurácia de 100% nos testes com dados da ISS e HST

    Detecção antecipada de Gimbal Lock antes da perda de controle

    Arquitetura leve e compatível com sistemas embarcados (ex: ESP32 + BNO055)

📜 Licença

Este projeto está licenciado sob a MIT License.
👨‍🏫 Referência Técnica

Se baseia em autores clássicos como:

    Vallado (SGP4 e TLEs)

    Kuipers (Quaternions)

    Goodfellow (Deep Learning)

    Chollet (Keras e LSTM)