#!/usr/bin/env python3
"""
ai_selector.py

Shared AI selection logic used by both the GUI (ResumeBuilder.py) and the
CLI (resume_cli.py). Uses the Claude Agent SDK with subscription auth.
"""

import asyncio
import json


class AISelector:
    def __init__(self, master_resume: list):
        self.master_resume = master_resume

    def _get_section_content(self, title):
        for section in self.master_resume:
            if section.get("title") == title:
                return section.get("content", [])
        return []

    def _build_autoselect_prompt(self, job_posting):
        objectives = self._get_section_content("Objective")
        projects = self._get_section_content("Technical Projects")
        competencies = self._get_section_content("Core Competencies")

        numbered = lambda items: "\n".join(f"{i}: {v}" for i, v in enumerate(items))

        return f"""You are a resume optimization assistant. Given a job posting and a candidate's resume data, select the best matching items by their index numbers.

JOB POSTING:
{job_posting}

CANDIDATE DATA:
Objective options (select exactly ONE — provide its index):
{numbered(objectives)}

Technical Project options (select 2 to 4 — provide their indices):
{numbered(projects)}

Core Competency options (select all that are relevant — provide their indices):
{numbered(competencies)}

INSTRUCTIONS:
- Return ONLY valid JSON with no markdown, no code fences, no explanation.
- Use the integer index numbers shown above — do not include the text.
- Select exactly one objective (a single integer).
- Select between 2 and 4 technical projects (a list of integers).
- Select all relevant core competencies (a list of integers).

Return this exact JSON structure:
{{
  "objective_index": 0,
  "technical_project_indices": [0, 1],
  "core_competency_indices": [0, 1, 2]
}}"""

    def _build_reorder_prompt(self, job_posting, selected_projects, selected_competencies):
        numbered = lambda items: "\n".join(f"{i}: {v}" for i, v in enumerate(items))

        return f"""You are a resume optimization assistant. Given a job posting and already-selected resume items, determine the best ordering so the most relevant items appear first.

JOB POSTING:
{job_posting}

SELECTED TECHNICAL PROJECTS (reorder these):
{numbered(selected_projects)}

SELECTED CORE COMPETENCIES (reorder these):
{numbered(selected_competencies)}

INSTRUCTIONS:
- Return ONLY valid JSON with no markdown, no code fences, no explanation.
- Each list must contain ALL of the indices shown above, rearranged into the best order (most relevant to the job posting first).
- Do not add or remove any indices — just reorder them.

Return this exact JSON structure:
{{
  "technical_project_order": [0, 1],
  "core_competency_order": [0, 1, 2]
}}"""

    def _validate_reorder_response(self, parsed, num_projects, num_competencies):
        if not isinstance(parsed, dict):
            return "Response is not a JSON object."

        for key, expected_len in [
            ("technical_project_order", num_projects),
            ("core_competency_order", num_competencies),
        ]:
            if key not in parsed or not isinstance(parsed[key], list):
                return f"'{key}' must be a list."
            if len(parsed[key]) != expected_len:
                return f"'{key}' must have exactly {expected_len} items (got {len(parsed[key])})."
            if sorted(parsed[key]) != list(range(expected_len)):
                return f"'{key}' must be a permutation of 0\u2013{expected_len - 1}."

        return None  # valid

    def _validate_ai_response(self, parsed):
        if not isinstance(parsed, dict):
            return "Response is not a JSON object."

        # objective_index
        if "objective_index" not in parsed or not isinstance(parsed["objective_index"], int):
            return "'objective_index' must be an integer."
        objectives = self._get_section_content("Objective")
        if not (0 <= parsed["objective_index"] < len(objectives)):
            return f"'objective_index' {parsed['objective_index']} is out of range (0\u2013{len(objectives)-1})."

        # technical_project_indices
        if "technical_project_indices" not in parsed or not isinstance(parsed["technical_project_indices"], list):
            return "'technical_project_indices' must be a list."
        if not (2 <= len(parsed["technical_project_indices"]) <= 4):
            return f"'technical_project_indices' must have 2\u20134 items (got {len(parsed['technical_project_indices'])})."
        projects = self._get_section_content("Technical Projects")
        for idx in parsed["technical_project_indices"]:
            if not isinstance(idx, int) or not (0 <= idx < len(projects)):
                return f"technical_project_indices contains invalid index: {idx}"

        # core_competency_indices
        if "core_competency_indices" not in parsed or not isinstance(parsed["core_competency_indices"], list):
            return "'core_competency_indices' must be a list."
        if len(parsed["core_competency_indices"]) == 0:
            return "'core_competency_indices' must not be empty."
        competencies = self._get_section_content("Core Competencies")
        for idx in parsed["core_competency_indices"]:
            if not isinstance(idx, int) or not (0 <= idx < len(competencies)):
                return f"core_competency_indices contains invalid index: {idx}"

        return None  # valid

    async def _call_claude(self, prompt, model=None):
        """Call Claude via the Agent SDK using subscription auth."""
        from claude_agent_sdk import query, ClaudeAgentOptions
        result = ""
        async for msg in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                allowed_tools=[],
                thinking={"type": "adaptive"},
                model=model,
            ),
        ):
            if hasattr(msg, "result"):
                result = msg.result
        return result

    def _call_claude_sync(self, prompt, model=None):
        """Sync wrapper around the async Agent SDK call."""
        return asyncio.run(self._call_claude(prompt, model=model))

    def call_with_retry(self, job_posting, model=None, on_progress=None):
        """
        Call Claude via the Agent SDK, retrying up to 3 times on failure.

        on_progress: optional callable(str) for status messages.
                     GUI passes a lambda that updates a status label;
                     CLI passes print (or None to suppress).

        Returns (result_dict, None) on success, or (None, error_str) on failure.
        """
        prompt = self._build_autoselect_prompt(job_posting)

        last_error = None
        for attempt in range(1, 4):
            if on_progress:
                on_progress(f"Contacting AI... (attempt {attempt} of 3)")
            try:
                raw_text = self._call_claude_sync(prompt, model=model)

                # Strip markdown code fences if present
                if raw_text.startswith("```"):
                    raw_text = raw_text.split("```")[1]
                    if raw_text.startswith("json"):
                        raw_text = raw_text[4:]
                    raw_text = raw_text.strip()

                parsed = json.loads(raw_text)
                validation_error = self._validate_ai_response(parsed)
                if validation_error:
                    last_error = f"Attempt {attempt}: Invalid response \u2014 {validation_error}"
                    continue
                return parsed, None

            except (json.JSONDecodeError, KeyError) as e:
                last_error = f"Attempt {attempt}: Could not parse AI response \u2014 {e}"
            except Exception as e:
                last_error = f"Attempt {attempt}: Unexpected error \u2014 {e}"

        return None, f"AI Auto-Select failed after 3 attempts.\n\nLast error: {last_error}"

    def call_reorder(self, job_posting, selected_projects, selected_competencies, model=None, on_progress=None):
        """
        Second-round call: reorder already-selected projects and competencies.

        Returns (reorder_dict, None) on success, or (None, error_str) on failure.
        """
        prompt = self._build_reorder_prompt(job_posting, selected_projects, selected_competencies)

        last_error = None
        for attempt in range(1, 4):
            if on_progress:
                on_progress(f"Reordering selections... (attempt {attempt} of 3)")
            try:
                raw_text = self._call_claude_sync(prompt, model=model)

                if raw_text.startswith("```"):
                    raw_text = raw_text.split("```")[1]
                    if raw_text.startswith("json"):
                        raw_text = raw_text[4:]
                    raw_text = raw_text.strip()

                parsed = json.loads(raw_text)
                validation_error = self._validate_reorder_response(
                    parsed, len(selected_projects), len(selected_competencies)
                )
                if validation_error:
                    last_error = f"Attempt {attempt}: Invalid response \u2014 {validation_error}"
                    continue
                return parsed, None

            except (json.JSONDecodeError, KeyError) as e:
                last_error = f"Attempt {attempt}: Could not parse AI response \u2014 {e}"
            except Exception as e:
                last_error = f"Attempt {attempt}: Unexpected error \u2014 {e}"

        return None, f"AI reorder failed after 3 attempts.\n\nLast error: {last_error}"

    def build_selected_sections(self, result, reorder=None):
        """
        Convert an AI result dict (with index fields) into a selected_sections
        list ready to pass to Generator.

        Sections not controlled by AI (Personal Information, Education,
        Professional Experience, Certifications, etc.) are included in full.
        Objective, Technical Projects, and Core Competencies are filtered by
        the AI's choices.
        """
        objectives = self._get_section_content("Objective")
        projects = self._get_section_content("Technical Projects")
        competencies = self._get_section_content("Core Competencies")

        selected_project_list = [projects[i] for i in result["technical_project_indices"]]
        selected_comp_list = [competencies[i] for i in result["core_competency_indices"]]
        chosen_objective = objectives[result["objective_index"]]

        # Apply reorder if provided
        if reorder:
            selected_project_list = [selected_project_list[i] for i in reorder["technical_project_order"]]
            selected_comp_list = [selected_comp_list[i] for i in reorder["core_competency_order"]]

        selected_sections = []
        for section in self.master_resume:
            title = section["title"]
            content = section["content"]

            if title == "Objective":
                selected_sections.append({"title": title, "content": chosen_objective})
            elif title == "Technical Projects":
                if selected_project_list:
                    selected_sections.append({"title": title, "content": selected_project_list})
            elif title == "Core Competencies":
                if selected_comp_list:
                    selected_sections.append({"title": title, "content": selected_comp_list})
            else:
                selected_sections.append({"title": title, "content": content})

        return selected_sections
