#!/usr/bin/env python3
"""
prompt-scaffolder.py — Generates prompt scaffolds from specs.

Usage:
    python prompt-scaffolder.py --domain "fitness coaching" --platform claude-project
    python prompt-scaffolder.py --domain "data analysis" --platform custom-gpt --language es
    python prompt-scaffolder.py --domain "code review" --platform api --output my-prompt.md

Generates a complete Playbook scaffold pre-filled with domain-specific
section placeholders, ready to be customized.
"""

import argparse
import sys
import textwrap
from datetime import datetime

PLATFORMS = {
    "claude-project": {
        "name": "Claude Project",
        "model": "Claude (Sonnet / Opus)",
        "notes": "Uses Project Instructions + Knowledge files. Supports XML tags.",
        "max_chars": "~8,000 characters for instructions",
    },
    "custom-gpt": {
        "name": "ChatGPT Custom GPT",
        "model": "GPT-4o / GPT-4o-mini",
        "notes": "Uses Instructions field + uploaded Knowledge files + Actions (API).",
        "max_chars": "~8,000 characters for instructions",
    },
    "gemini-gem": {
        "name": "Gemini Gem",
        "model": "Gemini Pro / Ultra",
        "notes": "Uses System Instructions + connected Google Docs. More compact format needed.",
        "max_chars": "~4,000 characters for instructions",
    },
    "api": {
        "name": "API / Programmatic",
        "model": "Any (specify in parameters)",
        "notes": "Full control over context stack. Optimize for token density.",
        "max_chars": "No hard limit, but optimize for cost",
    },
}

LABELS = {
    "en": {
        "role_title": "Role & Archetype",
        "role_body": "[Domain expertise in {domain}] + [Methodology/Framework] + [Communication style]\n\nYou are a [specific archetype] who specializes in {domain}, applies [methodology] frameworks, and communicates like [style reference — e.g., senior consultant, experienced coach, technical lead].",
        "objective_title": "Objective",
        "objective_body": "[Action verb] + [what the user achieves] + [success criteria]\n\nExample: Generate [deliverable type] that [measurable outcome] for [target audience].",
        "parameters_title": "Parameters",
        "flow_title": "Interaction Flow",
        "phase1_title": "Phase 1: Discovery",
        "phase1_body": "**Entry:** User initiates conversation.\n**Behavior:**\n- Analyze input to infer context, goal, and constraints for {domain}\n- Ask maximum 2 targeted questions if critical information is missing\n- Use proactive inference — guess intelligently, confirm quickly\n**Exit:** Enough context to produce a useful first output.",
        "phase2_title": "Phase 2: Execution",
        "phase2_body": "**Entry:** Context confirmed or inferred.\n**Behavior:**\n- Generate complete output using the Output Template below\n- Apply [specific {domain} methodology] for analysis/generation\n- Flag any assumptions made\n**Exit:** Complete deliverable presented to user.",
        "phase3_title": "Phase 3: Delivery & Iteration",
        "phase3_body": "**Entry:** First draft delivered.\n**Behavior:**\n- Present output with brief summary of key decisions\n- Invite targeted feedback: \"Want me to adjust [specific aspect]?\"\n- Apply modifications atomically\n**Exit:** User approves OR 3 iterations completed.",
        "constraints_title": "Constraints",
        "constraints_body": "- DO NOT [specific prohibited behavior in {domain} context]\n- ALWAYS [specific required behavior]\n- Maximum [X] [units] per [output section]\n- Out of scope: [topics to refuse]. Redirect to: [alternative resource]\n- When uncertain about [domain-specific element], [specific action — e.g., ask, flag, use conservative default]",
        "questions_title": "Key Questions",
        "questions_body": "1. [Most critical question for {domain} — blocks all progress if unknown]\n2. [Important question — significantly affects output quality]\n3. [Nice-to-have — improves personalization]",
        "output_title": "Output Template",
        "output_body": "[Define the exact format of the deliverable for {domain}]\n\n```\n# [Title]\n\n## [Section 1 — primary content]\n[Description]\n\n## [Section 2 — supporting content]\n[Description]\n\n## [Summary / Next Steps]\n[How to close the deliverable]\n```",
        "correction_title": "Self-Correction Triggers",
        "correction_body": "- If user says \"that's not what I meant\" → Return to Discovery phase\n- If output exceeds expected length → Compress to key points, offer detailed version\n- If confidence on any claim < 70% → Flag with \"[Unverified]\" label\n- If [domain-specific failure for {domain}] → [specific recovery action]",
    },
    "es": {
        "role_title": "Rol y Arquetipo",
        "role_body": "[Experiencia en {domain}] + [Metodología/Framework] + [Estilo de comunicación]\n\nEres un [arquetipo específico] especializado en {domain}, que aplica frameworks de [metodología] y se comunica como [referencia de estilo — ej., consultor senior, coach experimentado, líder técnico].",
        "objective_title": "Objetivo",
        "objective_body": "[Verbo de acción] + [qué logra el usuario] + [criterios de éxito]\n\nEjemplo: Generar [tipo de entregable] que [resultado medible] para [audiencia objetivo].",
        "parameters_title": "Parámetros",
        "flow_title": "Flujo de Interacción",
        "phase1_title": "Fase 1: Descubrimiento",
        "phase1_body": "**Entrada:** El usuario inicia la conversación.\n**Comportamiento:**\n- Analizar el input para inferir contexto, objetivo y restricciones de {domain}\n- Hacer máximo 2 preguntas específicas si falta información crítica\n- Inferencia proactiva — adivinar inteligentemente, confirmar rápido\n**Salida:** Contexto suficiente para producir un primer output útil.",
        "phase2_title": "Fase 2: Ejecución",
        "phase2_body": "**Entrada:** Contexto confirmado o inferido.\n**Comportamiento:**\n- Generar output completo usando la Plantilla de Output\n- Aplicar [metodología específica de {domain}]\n- Señalar cualquier suposición\n**Salida:** Entregable completo presentado al usuario.",
        "phase3_title": "Fase 3: Entrega e Iteración",
        "phase3_body": "**Entrada:** Primer borrador entregado.\n**Comportamiento:**\n- Presentar output con resumen de decisiones clave\n- Invitar feedback específico: \"¿Quieres que ajuste [aspecto específico]?\"\n- Aplicar modificaciones atómicas\n**Salida:** Usuario aprueba O 3 iteraciones completadas.",
        "constraints_title": "Restricciones",
        "constraints_body": "- NO [comportamiento prohibido específico en contexto de {domain}]\n- SIEMPRE [comportamiento requerido específico]\n- Máximo [X] [unidades] por [sección del output]\n- Fuera de alcance: [temas a rechazar]. Redirigir a: [recurso alternativo]\n- Ante incertidumbre sobre [elemento de {domain}], [acción específica]",
        "questions_title": "Preguntas Clave",
        "questions_body": "1. [Pregunta más crítica para {domain} — bloquea el progreso si no se sabe]\n2. [Pregunta importante — afecta significativamente la calidad]\n3. [Nice-to-have — mejora la personalización]",
        "output_title": "Plantilla de Output",
        "output_body": "[Definir el formato exacto del entregable para {domain}]\n\n```\n# [Título]\n\n## [Sección 1 — contenido principal]\n[Descripción]\n\n## [Sección 2 — contenido de soporte]\n[Descripción]\n\n## [Resumen / Próximos Pasos]\n[Cómo cerrar el entregable]\n```",
        "correction_title": "Disparadores de Auto-Corrección",
        "correction_body": "- Si el usuario dice \"no era eso\" → Volver a fase de Descubrimiento\n- Si el output excede la longitud esperada → Comprimir a puntos clave\n- Si la confianza en algún dato < 70% → Marcar con \"[Sin verificar]\"\n- Si [falla específica de {domain}] → [acción de recuperación]",
    },
}


def generate_scaffold(domain: str, platform: str, language: str, mode: str) -> str:
    """Generate a Playbook scaffold for the given domain and platform."""
    plat = PLATFORMS.get(platform, PLATFORMS["claude-project"])
    labels = LABELS.get(language, LABELS["en"])
    now = datetime.now().strftime("%Y-%m-%d")

    def fmt(text: str) -> str:
        return text.format(domain=domain)

    lines = []
    lines.append(f"# [{domain.title()} Assistant] — v0.1")
    lines.append(f"")
    lines.append(f"<!-- Generated by prompt-scaffolder.py | {now} -->")
    lines.append(f"<!-- Platform: {plat['name']} | {plat['max_chars']} -->")
    lines.append(f"<!-- Mode: {mode} | Language: {language} -->")
    lines.append(f"")

    # Role & Archetype
    lines.append(f"## {labels['role_title']}")
    lines.append(f"")
    lines.append(fmt(labels["role_body"]))
    lines.append(f"")

    # Objective
    lines.append(f"## {labels['objective_title']}")
    lines.append(f"")
    lines.append(fmt(labels["objective_body"]))
    lines.append(f"")

    # Parameters
    lines.append(f"## {labels['parameters_title']}")
    lines.append(f"")
    lines.append(f"- Model: {plat['model']}")
    lines.append(f"- Temperature: 0.5 (adjust based on task type)")
    lines.append(f"- Platform notes: {plat['notes']}")
    lines.append(f"")

    # Interaction Flow
    lines.append(f"## {labels['flow_title']}")
    lines.append(f"")
    lines.append(f"### {labels['phase1_title']}")
    lines.append(f"")
    lines.append(fmt(labels["phase1_body"]))
    lines.append(f"")
    lines.append(f"### {labels['phase2_title']}")
    lines.append(f"")
    lines.append(fmt(labels["phase2_body"]))
    lines.append(f"")
    lines.append(f"### {labels['phase3_title']}")
    lines.append(f"")
    lines.append(fmt(labels["phase3_body"]))
    lines.append(f"")

    # Constraints
    lines.append(f"## {labels['constraints_title']}")
    lines.append(f"")
    lines.append(fmt(labels["constraints_body"]))
    lines.append(f"")

    # Key Questions
    lines.append(f"## {labels['questions_title']}")
    lines.append(f"")
    lines.append(fmt(labels["questions_body"]))
    lines.append(f"")

    # Output Template
    lines.append(f"## {labels['output_title']}")
    lines.append(f"")
    lines.append(fmt(labels["output_body"]))
    lines.append(f"")

    # Self-Correction Triggers
    lines.append(f"## {labels['correction_title']}")
    lines.append(f"")
    lines.append(fmt(labels["correction_body"]))
    lines.append(f"")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a prompt scaffold from a domain spec"
    )
    parser.add_argument(
        "--domain", required=True,
        help="Description of the assistant's domain (e.g., 'fitness coaching')"
    )
    parser.add_argument(
        "--platform", default="claude-project",
        choices=list(PLATFORMS.keys()),
        help="Target platform (default: claude-project)"
    )
    parser.add_argument(
        "--mode", default="create",
        choices=["create", "review", "evolve", "repair"],
        help="Operation mode (default: create)"
    )
    parser.add_argument(
        "--language", default="en",
        choices=["en", "es"],
        help="Output language (default: en)"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Output file path (default: stdout)"
    )

    args = parser.parse_args()

    scaffold = generate_scaffold(args.domain, args.platform, args.language, args.mode)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(scaffold)
        print(f"Scaffold written to: {args.output}", file=sys.stderr)
    else:
        print(scaffold)


if __name__ == "__main__":
    main()
