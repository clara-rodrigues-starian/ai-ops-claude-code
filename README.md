# AI OPS — Claude Code

Workspace de referência pessoal para ferramentas de IA na Starian.

## Conteúdo

### `tetris.html`

Jogo de Tetris completo, autocontido — sem dependências externas, sem build step. Abra diretamente no navegador.

**Como jogar:**

| Tecla | Ação |
|-------|------|
| `←` `→` | Mover peça |
| `↑` | Girar |
| `↓` | Descer mais rápido (+1 ponto) |
| `Espaço` | Drop instantâneo (+2 pts por linha) |
| `P` | Pausar / retomar |

**Funcionalidades:**
- 7 peças clássicas (I, O, T, S, Z, J, L)
- Ghost piece (sombra da peça)
- Próxima peça visível
- Sistema de pontuação: 100 / 300 / 500 / 800 pts por 1–4 linhas simultâneas
- Dificuldade aumenta a cada 10 linhas (nível → velocidade)
- Tela de game over com pontuação final

---

### `time_tracking_claude_code_figma_make.html`

Guia de referência bilíngue (português) sobre métodos de rastreamento de tempo para Claude Code (CLI) e Figma Make. Requer o design system do host para renderizar corretamente (variáveis CSS e fonte Tabler Icons).

---

## Sincronização

O repositório é espelhado em [github.com/clara-rodrigues-starian/ai-ops-claude-code](https://github.com/clara-rodrigues-starian/ai-ops-claude-code).

Cada edição feita via Claude Code dispara um commit e push automático via hook `PostToolUse`.
