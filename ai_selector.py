#!/usr/bin/env python3
"""
ai_selector.py

Shared AI selection logic used by both the GUI (ResumeBuilder.py) and the
CLI (resume_cli.py). No tkinter dependency.
"""

import json
import urllib.request
import urllib.error


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

    def call_openrouter_with_retry(self, api_key, model, job_posting, on_progress=None):
        """
        Call the OpenRouter API, retrying up to 3 times on failure.

        on_progress: optional callable(str) for status messages.
                     GUI passes a lambda that updates a status label;
                     CLI passes print (or None to suppress).

        Returns (result_dict, None) on success, or (None, error_str) on failure.
        """
        prompt = self._build_autoselect_prompt(job_posting)
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "resume-generator-app",
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }

        last_error = None
        for attempt in range(1, 4):
            if on_progress:
                on_progress(f"Contacting AI... (attempt {attempt} of 3)")
            try:
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=60) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                raw_text = body["choices"][0]["message"]["content"].strip()

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

            except urllib.error.HTTPError as e:
                last_error = f"Attempt {attempt}: HTTP {e.code} \u2014 {e.reason}"
            except urllib.error.URLError as e:
                last_error = f"Attempt {attempt}: Network error \u2014 {e.reason}"
            except (json.JSONDecodeError, KeyError) as e:
                last_error = f"Attempt {attempt}: Could not parse AI response \u2014 {e}"
            except Exception as e:
                last_error = f"Attempt {attempt}: Unexpected error \u2014 {e}"

        return None, f"AI Auto-Select failed after 3 attempts.\n\nLast error: {last_error}"

    def build_selected_sections(self, result):
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

        selected_projects = {projects[i] for i in result["technical_project_indices"]}
        selected_comps = {competencies[i] for i in result["core_competency_indices"]}
        chosen_objective = objectives[result["objective_index"]]

        selected_sections = []
        for section in self.master_resume:
            title = section["title"]
            content = section["content"]

            if title == "Objective":
                selected_sections.append({"title": title, "content": [chosen_objective]})
            elif title == "Technical Projects":
                filtered = [p for p in content if p in selected_projects]
                if filtered:
                    selected_sections.append({"title": title, "content": filtered})
            elif title == "Core Competencies":
                filtered = [c for c in content if c in selected_comps]
                if filtered:
                    selected_sections.append({"title": title, "content": filtered})
            else:
                # Personal Information, Education, Professional Experience,
                # Certifications, and any other sections — include in full.
                selected_sections.append({"title": title, "content": content})

        return selected_sections
