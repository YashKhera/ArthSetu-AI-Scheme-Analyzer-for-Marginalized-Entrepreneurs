"""AI service for generating explanations using Claude API"""
import os
import json
from typing import Dict, List, Optional
from anthropic import Anthropic

from app.config import settings


class AIService:

    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL
        self.client = None

        if self.api_key:
            try:
                self.client = Anthropic(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize Anthropic client: {e}")

    # ------------------------------------------------------------------
    # Explanation generation (v2 scheme model)
    # ------------------------------------------------------------------
    def generate_explanation_v2(
        self,
        profile_data: Dict,
        scheme,
        matched_criteria: List[str],
        score: float,
    ) -> str:
        """Generate why this scheme matches this entrepreneur (v2 scheme object)."""
        if not self.client or not self.api_key:
            return self._generate_fallback_explanation_v2(scheme, matched_criteria, score)

        prompt = f"""Generate a brief, helpful explanation (2-3 sentences) of why this government scheme matches this entrepreneur's profile.

Entrepreneur Profile:
- Business sector: {profile_data.get('sector')}
- Location: {profile_data.get('state')}
- Stage: {profile_data.get('stage')}

Government Scheme:
- Name: {scheme.name}
- Ministry: {scheme.ministry}
- Primary sector: {scheme.primary_sector}
- Scheme type: {scheme.scheme_type}
- Benefits: {scheme.benefit_description}

Match Score: {score}/100
Matched Criteria: {', '.join(matched_criteria)}

Write a clear, encouraging explanation focusing on:
1. Why this scheme is a good fit
2. What specific benefits align with their needs
3. Keep it simple and actionable

Explanation:"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text.strip()
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_fallback_explanation_v2(scheme, matched_criteria, score)

    def _generate_fallback_explanation_v2(
        self,
        scheme,
        matched_criteria: List[str],
        score: float,
    ) -> str:
        """Rule-based explanation when AI is unavailable (v2 scheme object)."""
        parts = []

        if score >= 85:
            parts.append(f"{scheme.name} is an excellent match for your business.")
        elif score >= 70:
            parts.append(f"{scheme.name} is a strong match for your business.")
        elif score >= 55:
            parts.append(f"{scheme.name} could be a good fit for your business.")
        else:
            parts.append(f"{scheme.name} may have some relevance to your business.")

        criteria_details = []
        for c in matched_criteria:
            if c == "sector":
                criteria_details.append(f"your sector ({scheme.primary_sector}) matches")
            if c == "location":
                criteria_details.append("it is available in your state")
            if c == "purpose":
                criteria_details.append("it supports your stated needs")
            if c == "stage":
                criteria_details.append("it suits your business stage")

        if criteria_details:
            parts.append(f"It aligns because {', '.join(criteria_details[:3])}.")

        if scheme.benefit_description:
            parts.append(f"Key benefits: {scheme.benefit_description}")

        return " ".join(parts)

    # ------------------------------------------------------------------
    # Legacy explanation generation (v1 scheme model, kept for compat)
    # ------------------------------------------------------------------
    def generate_explanation(
        self,
        profile,
        scheme,
        matched_criteria: List[str],
        score: int,
    ) -> str:
        """Legacy signature: accepts v1 profile/scheme OR dict-like objects."""
        return self.generate_explanation_v2(
            profile_data={
                "sector": getattr(profile, "business_sector", ""),
                "state": getattr(profile, "state", ""),
                "stage": getattr(profile, "business_stage", ""),
            },
            scheme=scheme,
            matched_criteria=matched_criteria,
            score=score,
        )

    def _generate_fallback_explanation(self, profile, scheme, matched_criteria, score):
        """Legacy fallback that mirrors the v2 fallback."""
        return self._generate_fallback_explanation_v2(scheme, matched_criteria, score)

    # ------------------------------------------------------------------
    # Free-text profile extraction
    # ------------------------------------------------------------------
    def extract_profile_from_text(self, text: str) -> Dict:
        """Extract structured profile info from free-text description."""
        if not self.client or not self.api_key:
            return {}

        prompt = f"""Extract structured business information from this entrepreneur's description. Return ONLY a valid JSON object, no other text.

Text: "{text}"

Return JSON with these fields (use null if not identifiable):
{{
    "sector": "...",
    "location": "...",
    "business_stage": "...",
    "support_needs": [...],
    "intent": "..."
}}

JSON:"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )
            response_text = message.content[0].text.strip()
            return self._parse_json(response_text)
        except Exception as e:
            print(f"AI extraction failed: {e}")
            return {}

    def _parse_json(self, text: str) -> Dict:
        """Safely parse JSON from LLM response."""
        try:
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            return json.loads(text)
        except Exception as e:
            print(f"JSON parsing failed: {e}")
            return {}