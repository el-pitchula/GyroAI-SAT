<h1 align="center">GyroAI-SAT 🛰️<p></h1>


<div align="center">
  <strong>Detecção de Gimbal Lock em Satélites com IA: Uma Abordagem Baseada em TLE e Quaternions (Proposta de pipeline de monitoramento e previsão de anomalias de atitude)</strong>
</div>

## 🔭 Overview

GyroAI-SAT é um projeto que utiliza Inteligência Artificial para estabilização de satélites e mitigação do gimbal lock. O modelo de IA é treinado para prever e corrigir falhas de orientação, garantindo um controle mais eficiente.

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

## Como Usar

Pré-processar os dados:

    python src/preprocessing.py

Treinar o modelo de IA:

    python src/model.py

Rodar a simulação:

    python src/simulation.py

## 📜 Licença

Este projeto está sob a licença MIT.