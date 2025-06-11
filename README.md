<h1 align="center">GyroAI-SAT 🛰️<p></h1>

<div align="center">
  <strong>Detecção de Gimbal Lock em Satélites com IA:<p>Uma abordagem baseada em TLE e Quaternions para previsão de anomalias de atitude<p></strong><br> 
</div>

## 🔭 Overview

GyroAI-SAT é um projeto de inteligência artificial voltado para a detecção antecipada de Gimbal Lock em satélites. Utilizando dados orbitais reais (TLE), o sistema gera automaticamente representações de orientação (quaternions e ângulos de Euler) e classifica o estado de risco via rede neural LSTM.

    Objetivo: Antecipar falhas críticas de orientação em tempo real, melhorando a estabilidade e controle de satélites.

## 💻 Technologies

- Python (.py)
- Jupyter (.ipynb)
- MATLAB (.m)

[![Tec](https://skillicons.dev/icons?i=py,sklearn,tensorflow,matlab)](https://skillicons.dev)

## Dados: o arquivo Excel(.xlsx) contém os seguintes dados por amostra temporal:

| Coluna   | Significado                                                    |
| -------- | -------------------------------------------------------------- |
| `tempo`  | Instante da amostra                                            |
| `q0..q3` | Componentes do quaternion                                      |
| `roll`   | Ângulo em torno do eixo X                                      |
| `pitch`  | Ângulo em torno do eixo Y (**principal causa do Gimbal Lock**) |
| `yaw`    | Ângulo em torno do eixo Z                                      |
| `status` | Rótulo (ok, alerta, gimbal\_lock) gerado automaticamente       |

## Pipeline:

- Carrega os dados de orientação (quaternions e ângulos de Euler);
- Pré-processa esses dados (normaliza, cria janelas temporais);
- Usa os dados para treinar uma IA (LSTM);
- Retorna previsões de risco de Gimbal Lock (ok, alerta, gimbal_lock).

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

## 📘 Estudo Completo
Para os interessados em entender a fundo o funcionamento do sistema, incluindo toda a base matemática por trás das decisões de modelagem, o notebook [`modelagem.ipynb`](https://colab.research.google.com/drive/14xkAJb2e-92LwjhuEXTaQgWPzdYtDk8e#scrollTo=Sch4abQETB08) apresenta um estudo completo:

- Derivações matemáticas e físicas
- Cálculo de funções de transferência
- Conversões entre TLE, quaternions e ângulos de Euler
- Justificativas técnicas para o uso de redes LSTM

## 📜 Licença

Este projeto está sob a licença MIT.
