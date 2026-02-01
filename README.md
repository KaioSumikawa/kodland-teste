# README - Kodland Teste

Este é o meu projeto de jogo 2D desenvolvido em Python usando Pygame Zero (pgzero). 

Criado para controlar um pinguim em uma aventura coletando moedas e desviando de inimigos.

---

## About

Este projeto foi criado para praticar:

- Desenvolvimento de jogos 2D com Pygame Zero

- Implementação de sistema de colisões usando pygame.Rect

- Criação de IA básica para inimigos

- Sistema de animação para personagens

- Controle de som e música no jogo

- Interface HUD com informações visíveis

---

## IMPORTANTE - Versão do Python

Este jogo funciona apenas com Python 3.12.8. 
Versões mais recentes (como 3.13+) podem não funcionar corretamente devido a incompatibilidades.

---

## Configuração Inicial

### 1. Clone o repositorio
```bash
git clone https://github.com/seu-usuario/kodland-teste.git
cd kodland-teste
```

### 2. Instale Python 3.12.8
Baixe e instale especificamente o Python 3.12.8 do site oficial. Durante a instalação, marque a opção "Add Python to PATH".

### 3. Instale o Pygame Zero
```bash
pip install pgzero
```

### 4. Execute o jogo

```bash
pgzrun main.py
```

---

## Controles do Jogo

### Menu Principal

- Botão START → Inicia o jogo

- Botão SOUND → Liga/desliga o som

- Botão EXIT → Sai do jogo

### Durante o Jogo

- Clique do Mouse → Move o pinguim para a posição clicada

- Tecla ESC → Volta ao menu principals

---

## Estrutura do Código

O projeto está organizado em classes principais:

- Button → Botões interativos do menu

- SoundButton → Botão especializado para controle de som

- Coin → Sistema de moedas coletáveis

- Character → Classe base para personagens

- Hero → Personagem controlado pelo jogador

- Enemy → Inimigos com IA de movimentação

--- 

## Uso do Pygame

O jogo utiliza apenas a classe Rect do Pygame para:

- Detecção de colisões entre personagens

- Áreas de hitbox para colisões

- Verificação de cliques nos botões

- Definição da área de movimentação dos inimigos

---

## Solução de Problemas

### Problema: "Python 3.13+ não roda o jogo"

Solução: Instale especificamente o Python 3.12.8.

### Problema: "ModuleNotFoundError: No module named 'pgzero'"

Solução:

```bash
pip install pgzero
```

--- 

## Personalização

Você pode modificar facilmente:

- Número de inimigos: Altere a linha com [Enemy(enemy_area) for _ in range(4)]

- Número de moedas: Modifique a constante COIN_COUNT no início do código

- Velocidade dos personagens: Ajuste os parâmetros speed nas classes

- Cores do HUD: Modifique as cores RGB nos comandos screen.draw.text()

--- 

## Licença

Este projeto está sob a licença MIT.


























