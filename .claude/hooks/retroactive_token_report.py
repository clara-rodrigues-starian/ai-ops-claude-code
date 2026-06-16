#!/usr/bin/env python3
"""
Claude Code — Retroactive Token & Interaction Report
Lê todos os transcripts existentes em ~/.claude/projects/ e gera
um relatório completo de tokens e interações por projeto e sessão.

Uso:
    python retroactive_token_report.py

O relatório é salvo em token_report_retroativo.json
e um resumo é exibido no terminal.
"""

import json
import os
import glob
from datetime import datetime
from pathlib import Path


PROJECTS_DIR = Path.home() / ".claude" / "projects"

# Preços Claude Sonnet 4.6 (ajuste se necessário)
INPUT_PRICE_PER_M  = 3.00   # USD por 1M tokens de input
OUTPUT_PRICE_PER_M = 15.00  # USD por 1M tokens de output


def find_transcript_files(projects_dir: Path) -> list:
    """Encontra todos os arquivos de transcript .jsonl em todos os projetos."""
    pattern = str(projects_dir / "**" / "*.jsonl")
    return glob.glob(pattern, recursive=True)


def parse_transcript(filepath: str) -> dict:
    """Lê um arquivo .jsonl e extrai tokens e interações."""
    human_turns   = 0
    tool_uses     = 0
    input_tokens  = 0
    output_tokens = 0
    first_ts = None
    last_ts  = None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                role = msg.get("role", "")
                ts   = msg.get("timestamp") or msg.get("created_at")
                if ts:
                    if first_ts is None:
                        first_ts = ts
                    last_ts = ts

                if role == "human":
                    human_turns += 1

                elif role == "assistant":
                    usage = msg.get("usage") or msg.get("message", {}).get("usage", {}) or {}
                    input_tokens  += usage.get("input_tokens", 0)
                    output_tokens += usage.get("output_tokens", 0)

                    content = msg.get("content", [])
                    if isinstance(content, list):
                        tool_uses += sum(
                            1 for b in content
                            if isinstance(b, dict) and b.get("type") == "tool_use"
                        )
    except Exception as e:
        return {"error": str(e)}

    total_tokens = input_tokens + output_tokens
    cost = round(
        (input_tokens / 1_000_000) * INPUT_PRICE_PER_M +
        (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_M,
        6
    )

    return {
        "human_turns":         human_turns,
        "tool_uses":           tool_uses,
        "input_tokens":        input_tokens,
        "output_tokens":       output_tokens,
        "total_tokens":        total_tokens,
        "estimated_cost_usd":  cost,
        "first_message":       first_ts,
        "last_message":        last_ts,
    }


def build_report(projects_dir: Path) -> dict:
    """Varre todos os projetos e consolida o relatório."""
    transcript_files = find_transcript_files(projects_dir)

    if not transcript_files:
        print(f"\n⚠️  Nenhum transcript encontrado em: {projects_dir}")
        return {}

    projects = {}

    for filepath in sorted(transcript_files):
        project_folder = Path(filepath).parent.name
        session_name   = Path(filepath).stem

        stats = parse_transcript(filepath)

        if project_folder not in projects:
            projects[project_folder] = {
                "sessions":            [],
                "total_human_turns":   0,
                "total_tool_uses":     0,
                "total_input_tokens":  0,
                "total_output_tokens": 0,
                "total_tokens":        0,
                "total_cost_usd":      0.0,
            }

        p = projects[project_folder]
        p["sessions"].append({"session": session_name, "file": filepath, **stats})

        if "error" not in stats:
            p["total_human_turns"]   += stats["human_turns"]
            p["total_tool_uses"]     += stats["tool_uses"]
            p["total_input_tokens"]  += stats["input_tokens"]
            p["total_output_tokens"] += stats["output_tokens"]
            p["total_tokens"]        += stats["total_tokens"]
            p["total_cost_usd"]       = round(p["total_cost_usd"] + stats["estimated_cost_usd"], 6)

    return projects


def print_summary(projects: dict):
    """Exibe resumo no terminal."""
    grand_tokens = sum(p["total_tokens"] for p in projects.values())
    grand_cost   = sum(p["total_cost_usd"] for p in projects.values())
    grand_sessions = sum(len(p["sessions"]) for p in projects.values())

    print("\n" + "═" * 60)
    print("  📊 Claude Code — Relatório Retroativo de Tokens")
    print("═" * 60)
    print(f"  Projetos encontrados : {len(projects)}")
    print(f"  Sessões totais       : {grand_sessions}")
    print(f"  Tokens totais        : {grand_tokens:,}")
    print(f"  Custo total estimado : ~USD {grand_cost:.4f}")
    print("─" * 60)

    for folder, data in sorted(projects.items(), key=lambda x: -x[1]["total_tokens"]):
        print(f"\n  📁 {folder}")
        print(f"     Sessões  : {len(data['sessions'])}")
        print(f"     Tokens   : {data['total_tokens']:,}")
        print(f"     Custo    : ~USD {data['total_cost_usd']:.4f}")

    print("\n" + "═" * 60)
    print(f"  Relatório completo salvo em: token_report_retroativo.json")
    print("═" * 60 + "\n")


def main():
    if not PROJECTS_DIR.exists():
        print(f"\n❌ Pasta não encontrada: {PROJECTS_DIR}")
        print("Verifique se o Claude Code já foi usado neste computador.")
        return

    print(f"\n🔍 Lendo transcripts em: {PROJECTS_DIR}")
    projects = build_report(PROJECTS_DIR)

    if not projects:
        return

    # Salva relatório completo
    report = {
        "generated_at": datetime.now().isoformat(),
        "projects_dir": str(PROJECTS_DIR),
        "projects": projects,
    }

    output_path = Path("token_report_retroativo.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print_summary(projects)


if __name__ == "__main__":
    main()
