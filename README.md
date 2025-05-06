# GyroAI-SAT 🛰️

## Descrição
GyroAI-SAT é um projeto que utiliza Inteligência Artificial para estabilização de satélites e mitigação do gimbal lock. O modelo de IA é treinado para prever e corrigir falhas de orientação, garantindo um controle mais eficiente.

## 📂 Estrutura do Projeto
- `docs/` → Documentação completa do projeto (LaTeX, diagramas, referências)
- `src/` → Código-fonte principal, incluindo processamento de dados, modelagem de IA e simulação
- `notebooks/` → Notebooks para análise e experimentação
- `data/` → Dados utilizados para treino e validação (não versionados)
- `tests/` → Scripts de testes automatizados
- `requirements.txt` → Dependências do projeto

## O arquivo Excel contém os seguintes dados por amostra temporal:

🛰️ Posição (km): x_km, y_km, z_km
🚀 Velocidade (km/s): vx_km_s, vy_km_s, vz_km_s
🧭 Orientação (quaternions): q0, q1, q2, q3
🔄 Ângulos de Euler (em graus): roll_deg, pitch_deg, yaw_deg
🕒 Timestamp: timestamp

## ⚡ Instalação
Para rodar o projeto localmente:
```bash
git clone https://github.com/seu-usuario/GyroAI-SAT.git
cd GyroAI-SAT
pip install -r requirements.txt
```

## 🚀 Como Usar

    Pré-processar os dados:

python src/preprocessing.py

Treinar o modelo de IA:

python src/model.py

Rodar a simulação:

    python src/simulation.py

## 📜 Licença

Este projeto está sob a licença MIT.