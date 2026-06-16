#!/usr/bin/env python3
"""
Claude Code — Session Token & Interaction Tracker
Salva log por sessão e acumulado por projeto.

Instalação:
  1. Coloque este arquivo em .claude/hooks/session_tracker.py
  2. Adicione o hook em .claude/settings.json (veja settings_hook.json)
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


def read_transcript(transcript_path: str) -> list:
    """Lê o transcript da sessão."""
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def count_interactions_and_tokens(messages: list) -> dict:
    """
    Conta interações (turnos humano→assistente) e soma tokens.
    O transcript do Claude Code é uma lista de mensagens com papel e usage.
    """
    human_turns = 0
    assistant_turns = 0
    input_tokens = 0
    output_tokens = 0
    tool_uses = 0

    for msg in messages:
        role = msg.get("role", "")

        if role == "human":
            human_turns += 1

        elif role == "assistant":
            assistant_turns += 1
            # Tokens ficam em usage dentro da mensagem ou no nível raiz
            usage = msg.get("usage") or msg.get("message", {}).get("usage", {})
            if usage:
                input_tokens += usage.get("input_tokens", 0)
                output_tokens += usage.get("output_tokens", 0)

            # Conta tool uses dentro do conteúdo
            content = msg.get("content", [])
            if isinstance(content, list):
                tool_uses += sum(1 for block in content if isinstance(block, dict) and block.get("type") == "tool_use")

    return {
        "human_turns": human_turns,
        "assistant_turns": assistant_turns,
        "tool_uses": tool_uses,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }


def estimate_cost_usd(input_tokens: int, output_tokens: int) -> float:
    """
    Estimativa de custo baseada nos preços do Claude Sonnet 4.6.
    Ajuste se usar outro modelo.
    Input:  $3.00 / 1M tokens
    Output: $15.00 / 1M tokens
    """
    input_cost = (input_tokens / 1_000_000) * 3.00
    output_cost = (output_tokens / 1_000_000) * 15.00
    return round(input_cost + output_cost, 6)


def load_project_log(log_path: Path) -> dict:
    """Carrega o log acumulado do projeto, ou cria um novo."""
    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "project": os.path.basename(os.getcwd()),
        "created_at": datetime.now().isoformat(),
        "totals": {
            "sessions": 0,
            "human_turns": 0,
            "assistant_turns": 0,
            "tool_uses": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "estimated_cost_usd": 0.0,
        },
        "sessions": [],
    }


def save_project_log(log_path: Path, data: dict):
    """Salva o log do projeto."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def print_summary(session_data: dict, project_totals: dict, session_id: str):
    """Imprime resumo no terminal."""
    cost = estimate_cost_usd(session_data["input_tokens"], session_data["output_tokens"])
    total_cost = project_totals["estimated_cost_usd"]

    print("\n" + "═" * 52, file=sys.stderr)
    print("  📊 Claude Code — Resumo da Sessão", file=sys.stderr)
    print("═" * 52, file=sys.stderr)
    print(f"  ID da sessão  : {session_id[:16]}...", file=sys.stderr)
    print(f"  Encerrada em  : {datetime.now().strftime('%d/%m/%Y %H:%M')}", file=sys.stderr)
    print("─" * 52, file=sys.stderr)
    print("  ESTA SESSÃO", file=sys.stderr)
    print(f"  Interações    : {session_data['human_turns']} turnos humanos", file=sys.stderr)
    print(f"  Tool uses     : {session_data['tool_uses']}", file=sys.stderr)
    print(f"  Tokens input  : {session_data['input_tokens']:,}", file=sys.stderr)
    print(f"  Tokens output : {session_data['output_tokens']:,}", file=sys.stderr)
    print(f"  Total tokens  : {session_data['total_tokens']:,}", file=sys.stderr)
    print(f"  Custo estimado: ~USD {cost:.4f}", file=sys.stderr)
    print("─" * 52, file=sys.stderr)
    print("  ACUMULADO DO PROJETO", file=sys.stderr)
    print(f"  Sessões       : {project_totals['sessions']}", file=sys.stderr)
    print(f"  Total tokens  : {project_totals['total_tokens']:,}", file=sys.stderr)
    print(f"  Custo total   : ~USD {total_cost:.4f}", file=sys.stderr)
    print("═" * 52 + "\n", file=sys.stderr)


def main():
    # Lê o payload do hook via stdin
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        payload = {}

    session_id = payload.get("session_id", "unknown")
    transcript_path = payload.get("transcript_path", "")

    # Lê e analisa o transcript
    messages = read_transcript(transcript_path) if transcript_path else []
    stats = count_interactions_and_tokens(messages)
    cost = estimate_cost_usd(stats["input_tokens"], stats["output_tokens"])

    # Registro desta sessão
    session_record = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "transcript_path": transcript_path,
        **stats,
        "estimated_cost_usd": cost,
    }

    # Carrega e atualiza o log do projeto
    log_path = Path(".claude/logs/token_usage.json")
    project_log = load_project_log(log_path)

    project_log["sessions"].append(session_record)

    totals = project_log["totals"]
    totals["sessions"] += 1
    totals["human_turns"] += stats["human_turns"]
    totals["assistant_turns"] += stats["assistant_turns"]
    totals["tool_uses"] += stats["tool_uses"]
    totals["input_tokens"] += stats["input_tokens"]
    totals["output_tokens"] += stats["output_tokens"]
    totals["total_tokens"] += stats["total_tokens"]
    totals["estimated_cost_usd"] = round(totals["estimated_cost_usd"] + cost, 6)
    totals["last_updated"] = datetime.now().isoformat()

    save_project_log(log_path, project_log)

    # Mostra resumo no terminal
    print_summary(stats, totals, session_id)


if __name__ == "__main__":
    main()
