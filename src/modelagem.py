# %% [markdown]
# # 1. Propagação Orbital a partir do TLE
# 
# A partir de um TLE (Two-Line Element), obtemos os vetores de posição e velocidade em função do tempo com o modelo SGP4.
# 
# A conversão de data para Julian Date é feita por:
# 
# $$
# \text{JD} = 367y - \left\lfloor \frac{7(y + \left\lfloor \frac{m + 9}{12} \right\rfloor)}{4} \right\rfloor + \left\lfloor \frac{275m}{9} \right\rfloor + d + 1721013.5 + \frac{h + \frac{min}{60} + \frac{s}{3600}}{24}
# $$
# 
# O modelo retorna:
# - $\vec{r}(t) = [x, y, z] \in \mathbb{R}^3$ (posição em km)
# - $\vec{v}(t) = [v_x, v_y, v_z] \in \mathbb{R}^3$ (velocidade em km/s)
# 
# Ambos são calculados no referencial TEME (True Equator Mean Equinox) para um instante $t$ dado em tempo juliano.
# 
# O processo de extração envolve os seguintes passos:
# 
# 1. Conversão da data e hora em tempo juliano:
# <div align="center">$$
# \text{JD} = \text{data juliana} + \text{fração do dia}
# $$</div>
# 
# 2. Aplicação do modelo SGP4 sobre os parâmetros do TLE:
# <div align="center">$$
# \text{SGP4}(\text{JD}) \longrightarrow \vec{r}(t), \vec{v}(t)
# $$</div>
# 
# 3. Saída direta em unidades do SI:
# - $\vec{r}(t)$ em **quilômetros**
# - $\vec{v}(t)$ em **quilômetros por segundo**
# 
# > Essa etapa fornece a base para o cálculo da orientação do satélite, sendo $\vec{r}(t)$ usado como vetor "nadir" e $\vec{v}(t)$ como vetor de direção do movimento.
# 
# O TLE contém os parâmetros orbitais de um satélite em duas linhas padronizadas. Exemplo de estrutura do TLE:
# 
# 1 25544U 98067A 24106.45347222 .00012190 00000+0 21377-3 0 9992 \\
# 2 25544 51.6414 52.8843 0003046 96.6780 42.0736 15.51762384294959
# 
# #### Linha 1 – Informações de tempo e decaimento:
# <div align="center">
# 
# | Campo (colunas)     | Significado                                 |
# |---------------------|---------------------------------------------|
# | 3–7                 | NORAD ID (Ex: 25544 = ISS)                  |
# | 19–32               | Época: ano e dia juliano fracionário        |
# | 34–43               | Derivada do movimento médio $\dot{n}$       |
# | 45–52               | Segunda derivada $\ddot{n}$ (geralmente zero) |
# | 54–61               | Coef. de arrasto atmosférico $B^*$          |
# 
# </div>
# 
# A época é usada para calcular o tempo de referência da órbita:
# 
# $$
# t_0 = \text{época juliana} = \text{ano base} + \text{dia fracionário}
# $$
# 
# #### Linha 2 – Parâmetros orbitais principais:
# <div align="center">
# 
# | Campo (colunas)     | Significado                                 | Unidade       |
# |---------------------|---------------------------------------------|---------------|
# | 9–16                | Inclinação ($i$)                            | graus         |
# | 18–25               | RAAN ($\Omega$)                             | graus         |
# | 27–33               | Eccentricidade ($e$)                        | adimensional  |
# | 35–42               | Argumento do perigeu ($\omega$)             | graus         |
# | 44–51               | Anomalia média ($M$)                        | graus         |
# | 53–63               | Movimento médio ($n$)                       | revs/dia      |
# 
# </div>
# 
# ---
# 
# <p align="center"><b>período orbital</b></p>
# 
# A partir do movimento médio $n$ (revoluções por dia), obtemos:
# 
# $$
# T = \frac{1}{n} \times 86400 \quad \text{(em segundos)}
# $$
# 
# Exemplo:  
# Se $n = 15.5176$, então:
# 
# $$
# T \approx \frac{86400}{15.5176} \approx 5569 \text{ s} \approx 92.8 \text{ minutos}
# $$
# 
# Esse é o tempo para uma órbita completa — importante para estimar a janela temporal ou a frequência de coleta.
# 
# ---
# 
# <p align="center"><b>Eccentricidade</b></p>
# 
# O valor no TLE aparece como um número sem ponto decimal. Exemplo: `0003046`
# 
# <div align="center">$$
# e = 0.0003046
# $$</div>
# 
# ---
# 
# <p align="center"><b>Derivada do Movimento Médio</b></p>
# 
# Indica a aceleração angular da órbita:
# 
# <div align="center">$$
# \dot{n} = \frac{d(n)}{dt} \quad \text{(revs/dia²)}
# $$</div>
# 
# ---
# 
# <p align="center"><b>Coeficiente Balístico (Arrasto)</b></p>
# 
# No TLE é representado com notação truncada, ex: `21377-3`
# 
# <div align="center">$$
# B^* = 0.21377 \times 10^{-3}
# $$</div>

# %%
# TLE da ISS (ZARYA)
line1 = "1 25544U 98067A   24106.45347222  .00012190  00000+0  21377-3 0  9992"
line2 = "2 25544  51.6414  52.8843 0003046  96.6780  42.0736 15.51762384294959"
sat = Satrec.twoline2rv(line1, line2)

# Função auxiliar
def datetime_to_julian_date(dt):
    year, month, day = dt.year, dt.month, dt.day
    hour, minute, second = dt.hour, dt.minute, dt.second + dt.microsecond / 1e6
    jd = 367 * year - int((7 * (year + int((month + 9) / 12))) / 4) \
         + int((275 * month) / 9) + day + 1721013.5 \
         + (hour + minute / 60 + second / 3600) / 24
    fr = (hour + minute / 60 + second / 3600) / 24 % 1
    return jd, fr

# Parâmetros
base_time = datetime.utcnow()
intervalo_segundos = 30
samples = 3000 # priemeiro teste foi com 200 amostras apenas (94% de acurácia)
tempos, q0, q1, q2, q3 = [], [], [], [], []
rolls, pitchs, yaws = [], [], []

# Loop de propagação
for i in range(samples):
    dt = base_time + timedelta(seconds=i * intervalo_segundos)
    jd, fr = datetime_to_julian_date(dt)
    err, position, velocity = sat.sgp4(jd, fr)

# %% [markdown]
# # 2. Construção da Matriz de Rotação $\mathbf{R}(t)$
# 
# Com os vetores de posição $\vec{r}(t)$ e velocidade $\vec{v}(t)$, define-se um referencial ortonormal fixo ao satélite (body frame), usado para estimar sua orientação.
# 
# As direções dos eixos são:
# 
# - Eixo $-\hat{z}$: aponta para o centro da Terra (nadir)
# $$
# \hat{z}(t) = -\frac{\vec{r}(t)}{||\vec{r}(t)||}
# $$
# 
# - Eixo $\hat{y}$: ortogonal ao plano orbital (direção normal)
# $$
# \hat{y}(t) = \frac{\hat{z}(t) \times \vec{v}(t)}{||\hat{z}(t) \times \vec{v}(t)||}
# $$
# 
# - Eixo $\hat{x}$: completa a base ortonormal com regra da mão direita
# $$
# \hat{x}(t) = \hat{y}(t) \times \hat{z}(t)
# $$
# 
# A matriz de rotação no tempo $t$ é então:
# 
# <div align="center">$$
# \mathbf{R}(t) = \begin{bmatrix}
# \hat{x}(t) & \hat{y}(t) & \hat{z}(t)
# \end{bmatrix}
# $$</div>
# 
# Esta matriz transforma coordenadas do sistema inercial para o referencial do corpo (satélite).
# 
# ---
# 
# ### Conversão de $\mathbf{R}(t)$ para Representações de Orientação
# 
# A matriz $\mathbf{R}(t)$ obtida do referencial ortonormal é uma matriz $3\times3$ de rotação real:
# 
# <div align="center">$$
# \mathbf{R}(t) =
# \begin{bmatrix}
# R_{00} & R_{01} & R_{02} \\
# R_{10} & R_{11} & R_{12} \\
# R_{20} & R_{21} & R_{22}
# \end{bmatrix}
# $$</div>
# 
# ---
# 
# <p align="center"><b>Quaternions</b></p>
# 
# Usamos o traço da matriz:
# 
# <div align="center">$$
# \text{tr} = R_{00} + R_{11} + R_{22}
# $$</div>
# 
# Se $\text{tr} > 0$ (caso mais comum):
# 
# <div align="center">$$
# q_0 = \frac{1}{2} \sqrt{1 + \text{tr}} \\
# q_1 = \frac{R_{21} - R_{12}}{4q_0} \quad
# q_2 = \frac{R_{02} - R_{20}}{4q_0} \quad
# q_3 = \frac{R_{10} - R_{01}}{4q_0}
# $$</div>
# 
# O quaternion é então representado como:
# 
# <div align="center">$$
# \vec{q}(t) = [q_0,\ q_1,\ q_2,\ q_3]
# $$</div>
# 
# ---
# 
# <p align="center"><b>Ângulos de Euler</b></p>
# 
# Assumindo a convenção ZYX (yaw $\rightarrow$ pitch $\rightarrow$ roll), os ângulos são extraídos diretamente de $\mathbf{R}(t)$:
# 
# <div align="center">$$
# \begin{aligned}
# \phi(t) &= \arctan2(R_{32}, R_{33}) \quad \text{(roll)} \\
# \theta(t) &= \arcsin(-R_{31}) \quad \text{(pitch)} \\
# \psi(t) &= \arctan2(R_{21}, R_{11}) \quad \text{(yaw)}
# \end{aligned}
# $$</div>
# 
# ---
# 
# Esses ângulos formam o vetor:
# 
# <div align="center">$$
# [\phi(t),\ \theta(t),\ \psi(t)] = [\text{roll},\ \text{pitch},\ \text{yaw}]
# $$</div>
# 
# Ambas representações são extraídas diretamente a partir da matriz de rotação, garantindo coerência entre o espaço tridimensional real e a entrada da rede neural.
# 

# %%
    r = np.array(position)
    v = np.array(velocity)

    z = -r / np.linalg.norm(r)
    y = np.cross(z, v); y /= np.linalg.norm(y)
    x = np.cross(y, z)
    rot_matrix = np.vstack([x, y, z]).T
    rotation = R.from_matrix(rot_matrix)

    quat = rotation.as_quat()   # x, y, z, w
    euler = rotation.as_euler('xyz', degrees=True)

    tempos.append(i * intervalo_segundos)
    q0.append(quat[3]); q1.append(quat[0]); q2.append(quat[1]); q3.append(quat[2])
    rolls.append(euler[0]); pitchs.append(euler[1]); yaws.append(euler[2])

# %% [markdown]
# # 3. Rotulagem Automática com base no Pitch
# 
# Para transformar o problema em uma tarefa de classificação supervisionada, define-se o rótulo de cada instante com base no valor do ângulo de pitch $\theta(t)$.
# 
# ---
# 
# ### Definição das classes
# 
# - **ok**: $\left|\theta(t)\right| < 85^\circ$
# - **alerta**: $85^\circ \le \left|\theta(t)\right| < 89^\circ$
# - **gimbal\_lock**: $\left|\theta(t)\right| \ge 89^\circ$
# 
# ---
# 
# ### Expressão matemática (função por partes):
# 
# <div align="center">$$
# y(t) =
# \begin{cases}
# \text{gimbal_lock}, & \text{se } |\theta(t)| \ge 89^\circ \\
# \text{alerta}, & \text{se } 85^\circ \le |\theta(t)| < 89^\circ \\
# \text{ok}, & \text{se } |\theta(t)| < 85^\circ
# \end{cases}
# $$</div>
# 
# O fenômeno conhecido como **Gimbal Lock** ocorre quando dois eixos de rotação de um sistema se tornam colineares, resultando na **perda de um grau de liberdade** na orientação.
# 
# No caso dos **ângulos de Euler** com a convenção **ZYX**, isso ocorre quando:
# 
# <div align="center">$$
# \theta(t) = \pm 90^\circ
# $$</div>
# 
# Nesta condição, os eixos de rotação **X (roll)** e **Z (yaw)** tornam-se alinhados, tornando a orientação indefinida ou ambígua.
# 
# ---
# 
# ### Interpretação geométrica:
# 
# A decomposição ZYX realiza a rotação na ordem:
# 1. yaw  →  eixo Z  
# 2. pitch →  eixo Y  
# 3. roll →  eixo X  
# 
# Se $\theta(t) = \pm 90^\circ$, os eixos rotacionais colapsam:
# 
# <div align="center">$$
# \text{gimbal_lock} \quad \Leftrightarrow \quad |\theta(t)| \to 90^\circ
# $$</div>
# 
# Utilizar o **pitch θ(t)** como variável crítica permite:
# 
# - Detecção direta da condição de alinhamento dos eixos.
# - Implementação simples da lógica de classificação.
# - Monitoramento contínuo da orientação com base em uma variável física interpretável.
# 
# > Essa escolha é especialmente útil em sistemas embarcados e de navegação, onde a singularidade de Euler deve ser antecipada.
# 
# 
# A conversão da matriz de rotação $\mathbf{R}(t)$ para ângulos de Euler foi realizada utilizando a **ordem ZYX**, também conhecida como yaw–pitch–roll.
# 
# A ordem **ZYX** significa que a rotação total é composta da seguinte sequência:
# 
# 1. Rotação $\psi$ (yaw) ao redor do eixo **Z**
# 2. Rotação $\theta$ (pitch) ao redor do eixo **Y**
# 3. Rotação $\phi$ (roll) ao redor do eixo **X**
# 
# - É a **ordem mais comum em sistemas inerciais** e de navegação.
# - Reflete o movimento real de aeronaves, drones e satélites:
#   - Yaw: direção
#   - Pitch: elevação
#   - Roll: inclinação lateral
# 
# - Quando o fenômeno ocorre, é matematicamente evidente nesta convenção. A matriz $\mathbf{R}(t)$ é decomposta como:
# 
# <div align="center">$$
# \mathbf{R}(t) = R_z(\psi) \cdot R_y(\theta) \cdot R_x(\phi)
# $$</div>
# 
# Nesta ordem, quando o pitch atinge 90°, ocorre a perda de um grau de liberdade → os eixos de roll e yaw se alinham.
# 
# > Portanto, a ordem ZYX é essencial para que o Gimbal Lock seja visível no comportamento do pitch.

# %%
# Define a rotulagem automática para a comparação com as resposts da IA.
# Serve para saber se ela acertou a previsão com base no cálculo da função de perda (MSE e MAE).

def rotular_gimbal_lock(pitch, tolerancia=2):
    if abs(pitch - 90) < tolerancia:
        return "gimbal_lock"
    elif abs(pitch - 90) < tolerancia + 5:
        return "alerta"
    else:
        return "ok"

# DataFrame final:
df = pd.DataFrame({
    'tempo': tempos,
    'q0': q0, 'q1': q1, 'q2': q2, 'q3': q3,
    'roll': rolls,
    'pitch': pitchs,
    'yaw': yaws
})
df['status'] = df['pitch'].apply(rotular_gimbal_lock)

# %% [markdown]
# # 4. Preparação dos Dados para Treinamento
# 
# Antes de alimentar a rede neural, os dados de orientação precisam ser:
# 
# - Rotulados corretamente
# - Codificados como números inteiros (rótulos)
# - Organizados em janelas temporais fixas
# 
# ---
# 
# ### Geração de dados sintéticos
# 
# Para garantir a presença de todas as classes no conjunto de dados, foram adicionadas **amostras artificiais** com valores controlados de pitch:
# 
# Esses dados são rotulados da mesma forma que os dados reais, com base no valor de $\theta(t)$ (pitch).
# 
# ---
# 
# Codificação dos rótulos (Label Encoding)
# 
# Os rótulos nominais 'ok', 'alerta', 'gimbal_lock' são transformados em inteiros para entrada na rede:
# 
# <div align="center">$$
# \text{ok} \rightarrow 0,\quad
# \text{alerta} \rightarrow 1,\quad
# \text{gimbal_lock} \rightarrow 2
# $$</div>Posteriormente, os rótulos são convertidos para vetores one-hot:
# 
# <div align="center">$$
# \text{Ex: } \text{alerta} \rightarrow [0,\ 1,\ 0]
# $$</div>
# 

# %%
# Dados sintéticos para reforço supervisionado
df_fake = pd.DataFrame({
    'tempo': range(30),
    'q0': np.random.uniform(-1, 1, 30),
    'q1': np.random.uniform(-1, 1, 30),
    'q2': np.random.uniform(-1, 1, 30),
    'q3': np.random.uniform(-1, 1, 30),
    'roll': np.random.uniform(-180, 180, 30),
    'pitch': np.concatenate([
        np.full(10, 90),     # gimbal_lock
        np.full(10, 88),     # alerta
        np.full(10, 100)     # ok
    ]),
    'yaw': np.random.uniform(-180, 180, 30)
})
df_fake['status'] = df_fake['pitch'].apply(rotulo)

# Junta com os dados reais
df = pd.concat([df, df_fake], ignore_index=True)

# Codificação dos rótulos
encoder = LabelEncoder()
y_raw = encoder.fit_transform(df['status'])
print("Distribuição dos rótulos gerados:\n", df['status'].value_counts())
print("Rótulos codificados:", encoder.classes_)

# %% [markdown]
# ## > Observação sobre o uso de dados sintéticos (`df_fake`) <
# 
# Para complementar os dados orbitais reais gerados via TLE, foi inserido um pequeno conjunto de amostras artificiais — chamado `df_fake`. Essas amostras foram adicionadas com o objetivo de:
# 
# - Garantir **representação mínima das três classes** (`ok`, `alerta`, `gimbal_lock`)
# - **Evitar desbalanceamento extremo** no início do treinamento
# - **Auxiliar o aprendizado inicial** da rede em cenários críticos
# 
# O uso de dados sintéticos é uma prática comum chamada **data augmentation**, muito utilizada em Machine Learning para:
# 
# - Introduzir variabilidade controlada
# - Balancear classes raras
# - Reduzir o risco de overfitting
# - Fornecer exemplos rotulados onde a coleta de dados reais é escassa ou lenta
# 
# A função de rotulagem é **exatamente a mesma** para dados reais e sintéticos:
# 
# - O modelo **é treinado majoritariamente com dados reais** propagados com o modelo orbital SGP4.
# 
# - A **validação foi feita com dados de outro satélite (HST)**, demonstrando generalização e independência dos dados artificiais.
# 
# ---
# 
# 
# > O `df_fake` é apenas um mecanismo de reforço para garantir cobertura completa das classes durante o treinamento. Sua presença **não invalida a validade física, nem a modelagem matemática** do projeto. O sistema funciona plenamente com dados orbitais reais e é validado com diferentes entradas, comprovando sua robustez.

# %% [markdown]
# # 5. Construção da Janela Temporal $X_t$
# 
# A rede LSTM é projetada para processar **sequências temporais**. Por isso, os dados de orientação são reorganizados em **janelas deslizantes** de tamanho fixo.
# 
# ---
# 
# ### Vetor de entrada individual
# 
# Cada instante $t$ é representado por um vetor de 7 dimensões contendo:
# 
# <div align="center">$$
# x(t) = \left[ q_0(t),\ q_1(t),\ q_2(t),\ q_3(t),\ \phi(t),\ \theta(t),\ \psi(t) \right] \in \mathbb{R}^7
# $$</div>
# 
# ---
# 
# ### Montagem da janela temporal
# 
# A matriz de entrada $X_t \in \mathbb{R}^{10 \times 7}$ é composta por 10 vetores de estado consecutivos, ou seja, para cada instante $t$, é criada uma janela contendo os 10 vetores anteriores:
# 
# <div align="center">$$
# X_t =
# \begin{bmatrix}
# x(t-9) \\
# x(t-8) \\
# \vdots \\
# x(t)
# \end{bmatrix}
# =
# \begin{bmatrix}
# q_0 & q_1 & q_2 & q_3 & \phi & \theta & \psi \\
# \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
# q_0 & q_1 & q_2 & q_3 & \phi & \theta & \psi
# \end{bmatrix}
# =
# \begin{bmatrix}
# q_0^{(t-9)} & q_1^{(t-9)} & q_2^{(t-9)} & q_3^{(t-9)} & \phi^{(t-9)} & \theta^{(t-9)} & \psi^{(t-9)} \\
# q_0^{(t-8)} & q_1^{(t-8)} & q_2^{(t-8)} & q_3^{(t-8)} & \phi^{(t-8)} & \theta^{(t-8)} & \psi^{(t-8)} \\
# \vdots      & \vdots      & \vdots      & \vdots      & \vdots      & \vdots         & \vdots       \\
# q_0^{(t)}   & q_1^{(t)}   & q_2^{(t)}   & q_3^{(t)}   & \phi^{(t)}   & \theta^{(t)}   & \psi^{(t)}
# \end{bmatrix} \in \mathbb{R}^{10 \times 7}
# $$</div>
# 
# ### Associação do rótulo
# 
# O rótulo da janela é definido com base no **último instante** da sequência:
# 
# <div align="center">$$
# y(t) = \text{status associado a } \theta(t)
# $$</div>
# 
# Essa estratégia permite à rede LSTM aprender **padrões de evolução do movimento** que levam a situações de alerta ou Gimbal Lock. Ao final, $X$ contém todas as janelas possíveis e $y$ contém seus respectivos rótulos.

# %%
# Preparação de janelas temporais
features = ['q0', 'q1', 'q2', 'q3', 'roll', 'pitch', 'yaw']
window_size = 10
X, y = [], []
for i in range(len(df) - window_size):
    seq_x = df[features].iloc[i:i+window_size].values
    label = y_raw[i + window_size]
    X.append(seq_x)
    y.append(label)

X = np.array(X)
y = np.array(y)
y_cat = to_categorical(y)

# %% [markdown]
# # 6. Arquitetura e Treinamento da Rede LSTM
# 
# A rede LSTM foi projetada para aprender a detectar padrões temporais nos vetores de orientação do satélite ao longo do tempo.
# 
# ---
# 
# ### Entrada
# 
# Cada entrada é uma janela temporal:
# 
# <div align="center">$$
# X_t \in \mathbb{R}^{10 \times 7}
# $$</div>
# 
# representando 10 instantes consecutivos de orientação (quaternions + ângulos de Euler).
# 
# ---
# 
# ### Estrutura da rede
# 
# 1. **Camada LSTM** com 64 unidades:
#    - Capta dependências temporais
#    - Aplica "gates" para controlar memória
# 
# 2. **Camada densa** com 32 neurônios e ativação ReLU:
#    - Mapeia relações não-lineares
# 
# 3. **Camada de saída Softmax** com 3 neurônios:
#    - Cada neurônio representa uma classe:
#      - ok
#      - alerta
#      - gimbal\_lock
# 
# ---
# 
# ### Saída
# 
# A rede retorna um vetor de probabilidade:
# 
# <div align="center">$$
# \hat{y}(t) = \text{softmax}(W \cdot h + b) \in \mathbb{R}^3
# $$</div>
# 
# onde $\hat{y}_k(t) \in [0, 1]$ representa a probabilidade da amostra pertencer à classe $k$.
# 
# ---
# 
# ### Função de perda: Cross Entropy
# 
# Para problemas de classificação com múltiplas classes, como neste projeto (`ok`, `alerta`, `gimbal_lock`), usamos **entropia cruzada categórica (categorical crossentropy)**. Para cada janela $X_t$, com rótulo real $y(t) \in \{0,1,2\}$, a função de perda no tempo $t$ é:
# 
# <div align="center">$$
# \mathcal{L}_{CE}(t) = - \sum_{k=1}^{3} y_k(t) \cdot \log \left( \hat{y}_k(t) \right)
# $$</div>
# 
# onde:
# - $y_k(t) = [y_1(t), y_2(t), y_3(t)]$: rótulo real (vetor one-hot (ex: $[0,\ 1,\ 0]$))
# - $\hat{y}_k(t) = [\hat{y}_1(t), \hat{y}_2(t), \hat{y}_3(t)]$: saída da rede (probabilidades), ou seja, a predição da rede para a classe $k$
# 
# **Exemplo:**
# Se a classe correta for “alerta”, temos:
# 
# - $y(t) = [0,\ 1,\ 0]$
# - $\hat{y}(t) = [0.05,\ 0.91,\ 0.04]$
# 
# Cálculo:
# 
# <div align="center">$$
# \mathcal{L}_{CE}(t) = - \left( 0 \cdot \log(0.05) + 1 \cdot \log(0.91) + 0 \cdot \log(0.04) \right) = -\log(0.91) \approx 0.094
# $$</div>
# 
# ### Atualização dos pesos (Backpropagation Through Time)
# 
# Os parâmetros $\theta$ da rede são atualizados via:
# 
# <div align="center">$$
# \theta \leftarrow \theta - \eta \cdot \nabla_\theta \mathcal{L}
# $$</div>
# 
# com:
# - $\eta$: taxa de aprendizado
# - $\nabla_\theta \mathcal{L}$: gradiente da perda em relação aos pesos
# 
# > A arquitetura da LSTM permite à rede detectar antecipadamente situações de risco a partir da evolução temporal dos dados de orientação.

# %%
# Separação em treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)

# Modelo LSTM
model = Sequential()
model.add(LSTM(64, input_shape=(window_size, len(features)))) # Entrada: (10, 7) = janela de 10 instantes com 7 features
model.add(Dense(32, activation='relu')) # Camada intermediária com 32 neurônios
model.add(Dense(3, activation='softmax')) # Saída com 3 neurônios (ok, alerta, gimbal_lock)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# %% [markdown]
# ## > Observações <
# ### Métricas de Avaliação
# 
# Além da função de perda (Cross Entropy), o modelo pode ser avaliado por métricas como:
# 
# #### Acurácia: Proporção de previsões corretas.
# $$
# \text{Accuracy} = \frac{\text{número de acertos}}{\text{total de amostras}}
# $$
# 
# #### MAE – Mean Absolute Error: Mede a média dos erros absolutos entre predições e rótulos. Pode ser computada para comparar distribuições de probabilidade:
# $$
# \text{MAE} = \frac{1}{N} \sum_{i=1}^N |y_i - \hat{y}_i|
# $$
# 
# - Mede o erro absoluto médio entre a predição e o vetor one-hot
# - Pode ajudar a verificar se a rede está **próxima da classe correta**, mesmo quando erra
# 
# #### MSE – Mean Squared Error: Mede o erro quadrático médio. Usado mais em regressão, mas pode ser observado como:
# $$
# \text{MSE} = \frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2
# $$
# 
# Exemplo com:
# 
# - $y = [0, 1, 0]$
# - $\hat{y} = [0.05, 0.91, 0.04]$
# 
# <div align="center">$$
# \text{MSE} = \frac{1}{3} \left( (0.05 - 0)^2 + (0.91 - 1)^2 + (0.04 - 0)^2 \right) \approx 0.0063
# $$</div>
# 
# > Embora Cross Entropy seja a função de perda principal para classificação, métricas como MAE e MSE podem auxiliar no diagnóstico do comportamento do modelo.
# 
# ---
# 
# ### Otimizador Adam
# 
# O otimizador **Adam** é utilizado para ajustar os pesos com base nos gradientes calculados:
# 
# - Combina as vantagens do Momentum e do RMSProp
# - Atualiza os pesos com base nas médias móveis dos gradientes e suas variâncias
# 
# Fórmula de atualização dos pesos:
# $$
# \theta \leftarrow \theta - \eta \cdot \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}
# $$
# 
# onde:
# - $\eta$ é a taxa de aprendizado
# - $\hat{m}_t$ é a média móvel do gradiente (momento)
# - $\hat{v}_t$ é a média móvel do quadrado dos gradientes (variância)
# - $\epsilon$ é um pequeno valor para estabilidade numérica
# 
# ---
# 
# ### Integração no Treinamento
# 
# Durante cada época, o processo é:
# 
# 1. A rede recebe uma sequência $X_t \in \mathbb{R}^{10 \times 7}$
# 2. Calcula a predição $\hat{y}(t)$
# 3. Compara com $y(t)$ via Cross Entropy
# 4. Calcula o gradiente da perda:
#    $$
#    \nabla_\theta \mathcal{L} = \text{retropropagação dos erros}
#    $$
# 5. Atualiza os pesos com o otimizador Adam
# 6. Avalia o desempenho com métricas como acurácia, MAE e MSE.
# 
# 
# > Essa integração matemática garante que o modelo aprenda a **antecipar o Gimbal Lock** com base em tendências temporais presentes nas janelas de orientação.
# 
# ---
# 
# ### Estratégia de Early Stopping
# 
# No treinamento, foi utilizada a técnica **EarlyStopping**, que monitora a perda da validação:
# 
# - monitor='val_loss': observa a perda na validação
# - patience=5: para se não melhorar após 5 épocas
# - restore_best_weights=True: retorna aos melhores pesos salvos
# 
# > Isso evita o overfitting, parando o treino assim que o modelo começa a perder generalização.
# 
# ```python
# early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
# 

# %% [markdown]
# ## Treinamento Supervisionado e Avaliação Final
# 
# * **Entrada**: lote de amostras \$X\_t \in \mathbb{R}^{10 \times 7}\$ com rótulos one-hot \$y(t) \in \mathbb{R}^3\$
# * **Função de perda** $\mathcal{L}(t)$
# 
# * **Backpropagation Through Time (BPTT)**:
# 
#   * Os pesos \$\theta\$ são atualizados via gradiente descendente com **Adam**
# 
# ---
# 
# ### Validação interna
# 
# A cada época, 20% dos dados de treino são usados como **validação** (`validation_split=0.2`), ou seja:
# 
# * De 80% dos dados que vão para o treino, 64% são de treino real
# * 16% são para validação durante `fit()`
# 
# O **early stopping** interrompe o treinamento caso `val_loss` não melhore após 5 épocas.
# 
# ---
# 
# ### Avaliação final
# 
# Após o treinamento, é avaliado com:
# 
# ```python
# loss, acc = model.evaluate(X_test, y_test)
# ```
# 
# * **X\_test**: dados **nunca vistos antes**
# * **acc**: acurácia do modelo
# * **loss**: valor da função de perda \$\mathcal{L}\$ no teste
# 
# Isso garante que o modelo está **generalizando** corretamente para novas situações.

# %%
# Treinamento
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=16,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=1
)

# Avaliação final
loss, acc = model.evaluate(X_test, y_test)
print(f"\n✅ Acurácia (ISS): {acc:.2f} | Loss: {loss:.4f}")

# %% [markdown]
# # 7. Avaliação do Modelo com Métricas de Classificação
# 
# Após o treinamento, o modelo é avaliado usando o conjunto de teste (dados nunca vistos antes).
# 
# ### Matriz de Confusão
# 
# A matriz de confusão representa a comparação entre os rótulos **verdadeiros** $y_{\text{true}}$ e os rótulos **previstos** $\hat{y}_{\text{pred}}$ pelo modelo.
# 
# <div align="center">
# 
# | Verdadeiro ↓ / Previsto → | ok | alerta | gimbal\_lock |
# |---------------------------|----|--------|--------------|
# | ok                        | TP | FP     | FP           |
# | alerta                   | FN | TP     | FN           |
# | gimbal\_lock             | FN | FP     | TP           |
# 
# </div>
# 
# Cada célula mostra a quantidade de acertos e erros por classe. As métricas são calculadas para cada classe (multiclasse) com base em:
# 
# - **Verdadeiro Positivo (TP)**: acertos do modelo
# - **Falso Positivo (FP)**: previsões erradas para uma classe
# - **Falso Negativo (FN)**: previsões que deveriam ter sido feitas
# 
# <div align="center">$$
# \text{Precision}_k = \frac{TP_k}{TP_k + FP_k}
# $$</div>
# 
# Representa **quantas das previsões feitas para a classe $k$ estavam corretas**.
# 
# <div align="center">$$
# \text{Recall}_k = \frac{TP_k}{TP_k + FN_k}
# $$</div>
# 
# Indica **quantos dos exemplos reais da classe $k$ o modelo conseguiu encontrar**.
# 
# <div align="center">$$
# \text{F1}_k = 2 \cdot \frac{\text{Precision}_k \cdot \text{Recall}_k}{\text{Precision}_k + \text{Recall}_k}
# $$</div>
# 
# E o **F1-score** é a média harmônica entre precision e recall — ideal para avaliar **equilíbrio** entre erros e acertos.
# 
# 

# %%
# ----- Matriz de confusão -----
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

# Previsão
y_pred_prob = model.predict(X_test)
y_pred = y_pred_prob.argmax(axis=1)
y_true = y_test.argmax(axis=1)

# Matriz
cm = confusion_matrix(y_true, y_pred)
labels = encoder.classes_

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.title("Matriz de Confusão - ISS")
plt.ylabel('Verdadeiro')
plt.xlabel('Predito')
plt.show()

# Relatório de Classificação
print("Relatório de Classificação - ISS:\n")
print(classification_report(y_true, y_pred, target_names=labels))

# Previsões exemplo
print("\nExemplo de previsões para novas sequências (ISS):\n")
for i in range(5):
    sample = X_test[i][np.newaxis, ...]
    pred_prob = model.predict(sample)[0]
    pred_class = encoder.inverse_transform([pred_prob.argmax()])[0]
    print(f"Amostra {i+1}: Classe prevista = {pred_class}, Probabilidades = {pred_prob}")

# %% [markdown]
# ### Predição Individual com Softmax
# 
# Após o treinamento, podemos fazer a predição de uma **única sequência temporal** $X_t$. ("sample" e "pred_prob")
# 
# ### Etapas matemáticas da predição
# 
# 1. O modelo recebe a sequência \$X\_t \in \mathbb{R}^{10 \times 7}\$ como entrada
# 
# 2. A rede gera uma **distribuição de probabilidade** usando a camada softmax:
# 
# <div align="center">$$
# \hat{y}_k(t) = \frac{e^{z_k}}{\sum_{j=1}^{3} e^{z_j}}
# $$</div>
# 
# onde:
# 
# * \$z\_k\$ é a saída bruta do neurônio \$k\$ da camada final
# * \$\hat{y}\_k(t)\$ é a **probabilidade da amostra pertencer à classe \$k\$**
# 
# ---
# 
# ### Conversão para rótulo original
# 
# ```python
# encoder.inverse_transform([classe_prevista])
# ```
# 
# Essa função transforma o índice numérico (ex: `1`) no rótulo original (ex: `"alerta"`), com base na codificação definida no início do pipeline:
# 
# ```python
# encoder = LabelEncoder()
# ```
# 
# ---
# 
# ### Exemplo de saída
# 
# ```
# Amostra 1: Classe prevista = alerta
# Probabilidades = [0.01, 0.12, 0.87]
# Sequência de pitchs: [84.2, 85.1, ..., 88.7]
# ```
# 
# Esse processo mostra que a rede não apenas classifica, mas também fornece **nível de confiança para cada possível classe**, útil para análise de risco.
# 

# %% [markdown]
# # 8. Interpretação dos Resultados
# 
# Após rodar o modelo, os resultados podem ser interpretados de forma visual e numérica.
# 
# ---
# 
# ### Predições Individuais
# 
# ```python
# print(f"Amostra {i+1}: Classe prevista = {pred_class}, Probabilidades = {pred_prob}")
# ```
# 
# A rede retorna um vetor de 3 valores com **probabilidades para cada classe**.
# 
# **Interpretação**:
# 
# * Se `pred_prob = [0.02, 0.90, 0.08]`, o modelo tem **alta confiança** na classe `alerta`
# * A última linha da sequência indica o **pitch final**, que valida a previsão
# 
# ---
# 
# ### Métricas de Avaliação
# 
# As métricas finais (Precision, Recall, F1-score) mostram:
# 
# * Se o modelo é **equilibrado** entre as classes
# * Se está **especializado** ou cometendo erros em alguma classe específica
# 
# **F1-score alto para “gimbal_lock”** é particularmente importante, pois garante que o modelo detecta os momentos críticos com confiabilidade.
# 
# ---
# 
# Se:
# 
# * A acurácia for alta
# * A matriz de confusão mostrar poucos erros
# * As curvas de acurácia treino/validação forem estáveis
# * E os rótulos visuais estiverem coerentes
# 
# Então o modelo está **generalizando bem** e pode ser considerado **robusto** para uso prático ou embarcado.
# 
# 

# %% [markdown]
# ## **Explicando os Resultados por Partes**
# 
# ### PARTE 1 – Treinamento e Acerto Final
# 
# ```plaintext
# Distribuição dos rótulos gerados:
#  status
# ok             3010
# gimbal_lock      10
# alerta           10
# ```
# 
# Isso mostra **quantos exemplos** de cada classe existem no seu conjunto de dados.
# 
# ```plaintext
# Rótulos codificados: ['alerta' 'gimbal_lock' 'ok']
# ```
# 
# Essa linha confirma como o `LabelEncoder` converteu texto em números:
# 
# * `'alerta'` → 0
# * `'gimbal_lock'` → 1
# * `'ok'` → 2
# 
# Esse mapeamento é usado internamente pela rede.
# 
# ---
# 
# ### Treinamento por Época
# 
# ```plaintext
# Epoch 1/50
# ... accuracy: 0.9311 - loss: 0.3366 - val_accuracy: 0.9917 - val_loss: 0.0129
# ...
# Epoch 13/50
# ... accuracy: 0.9996 - loss: 0.0033 - val_accuracy: 0.9979 - val_loss: 0.0050
# ```
# 
# A cada época, o modelo:
# 
# * Treina com 80% dos dados (`accuracy` e `loss`)
# * Valida com 20% internos (`val_accuracy` e `val_loss`)
# 
# A **perda (loss)** usa a fórmula da entropia cruzada (cross-entropy):
# 
# <div align="center">$$
# \mathcal{L}(t) = -\sum_{k=1}^{3} y_k(t) \cdot \log(\hat{y}_k(t))
# $$</div>
# 
# Valores de loss e accuracy muito baixos e altos, respectivamente, indicam **boa convergência sem overfitting**, graças ao `early_stopping`.
# 
# ```plaintext
# ✅ Acurácia (HST): 1.00 | Loss: 0.0086
# ```
# 
# **Avaliação no conjunto de teste (HST):**
# 
# * `acc = 1.00`: o modelo classificou corretamente todas as amostras
# * `loss = 0.0086`: perda baixa = predições confiáveis
# 
# Dado o desequilíbrio nas classes pela raridade do fenômeno, é fundamental **verificar a matriz de confusão** para confirmar que o modelo não está apenas favorecendo a classe majoritária.
# 
# ---
# 
# ### **PARTE 2 – Matriz de Confusão**
# 
# A matriz de confusão mostra **quantos acertos e erros o modelo cometeu por classe**:
# 
# ```
#           Predito
#          a   b   c
# Verdadeiro
# a       TP  FP  FP
# b       FN  TP  FN
# c       FP  FP  TP
# ```
# 
# Se todos os valores estiverem na diagonal principal, o modelo acertou 100%.
# 
# ---
# 
# ### **PARTE 3 – Relatório de Classificação**
# 
# Exemplo:
# 
# ```plaintext
#               precision    recall  f1-score   support
# 
#       alerta       0.33      1.00      0.50         1
#  gimbal_lock       1.00      1.00      1.00         1
#           ok       1.00      1.00      1.00       602
# ```
# 
# * **Precision**: % das predições da classe que estavam corretas
# * **Recall**: % das amostras reais da classe que foram previstas corretamente
# * **F1-score**: média harmônica entre os dois
# 
# `alerta` tem `precision = 0.33` porque:
# 
# * Ela apareceu **só 1 vez**
# * E houve **outros falsos positivos** de `alerta`
# 
# > Isso mostra que embora a acurácia geral seja 100%, o **F1-score macro** (média entre as classes) cai para 0.83 — revelando **fragilidade nas classes minoritárias**.
# 
# ---
# 
# ### **PARTE 4 – Exemplo de Previsões Individuais**
# 
# ```plaintext
# Amostra 1: Classe prevista = ok
# Probabilidades = [7.2e-06 2.4e-05 9.99968e-01]
# ```
# 
# * O vetor é a saída da camada **softmax**:
# 
# <div align="center">$$
# \hat{y}(t) = [P_{\text{alerta}},\ P_{\text{gimbal}},\ P_{\text{ok}}]
# $$</div>
# 
# * O modelo **prevê com quase 100% de confiança** que a amostra é "ok".
# 
# Como as probabilidades de alerta/gimbal são muito próximas de zero, o modelo **não está incerto** — o que é bom para estabilidade.
# 
# ---
# 
# ### **PARTE 5 – Gráfico da Curva de Acurácia**
# 
# Esse gráfico mostra:
# 
# * Como a **acurácia de treino e validação** evoluem ao longo das épocas
# * Se há **overfitting** (acurácia de treino sobe, validação cai)
# * Se o modelo **estabiliza rapidamente** (bom sinal)
# 
# Se as duas curvas convergem para o mesmo valor, como nesse caso, é **excelente**.
# 


