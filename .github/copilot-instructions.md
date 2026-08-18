# Automotive AI Marketing Platform

## Project Summary

This project is an AI-powered automotive marketing platform focused on used vehicle advertising, creative copy generation, and dynamic AI sales assistance for Arkas 2. El.

The platform collects rich vehicle listings (including full technical specs, package/trim levels, equipment lists, damage/expertise reports, and genuine photo galleries), stores structured vehicle information in PostgreSQL 17, and uses that data to generate high-converting marketing copies (Safe & Bold variants), social media content, and promotional materials, accompanied by a **Cognitive AI Sales Consultant Chatbot** that guides users and controls the Next.js showcase in real time.

---

## Business Goal

Transform raw vehicle listing data into high-converting marketing copy and active sales leads.

The system:

1. Collects comprehensive vehicle information from external listing sources.
2. Stores and organizes vehicle data in a structured PostgreSQL 17 database (`vehicles`, `customer_leads`, `marketing_copies`, `creative_briefs`).
3. Enriches vehicle records with marketing context and brand archetypes.
4. Generates persuasive advertising content (Safe / Kurumsal & Bold / Tutkulu copy variants, Instagram Stories).
5. Provides an intelligent, human-like **Cognitive AI Sales Consultant** (`ChatbotAgent`) with Turkish NER (Hanım/Bey/Sayın), session deduplication, direct equipment Q&A, budget expansion, and dynamic cross-vehicle recommendations.
6. Dispatches real-time page filter actions from the chatbot.

---

## Core Principle

Do not think like a vehicle catalog.

Think like an automotive marketing agency and an expert sales consultant.

When generating content or speaking in chat:
- Focus on customer benefits.
- Focus on emotional appeal.
- Focus on purchase motivation.
- Focus on brand perception.
- Focus on sales potential.

Avoid simply repeating technical specifications unless they directly support marketing objectives.

---

# AI Sales Consultant & Chatbot Rules

1. **Lead Onboarding & Memory:** Warm greeting, captures Customer Name, Phone, and Budget into `customer_leads` under a single persistent `session_id`.
2. **Turkish NER:** Accurately recognizes Turkish female/male names and attaches polite honorifics (Ceren Hanım / Tufan Bey / Sayın ...). Respects negative phone intent.
3. **Direct Q&A:** Direct and concise responses regarding Transmission, Mileage (KM), Price, Fuel Economy, and Equipment.
4. **Cross-Vehicle Recommendations:** If a user asks for an unavailable feature on the focused vehicle, the agent automatically scans the entire inventory and suggests matching models (e.g. Volvo XC40 for heated steering) and updates the page filter synchronously.
5. **Budget Expansion:** When a user asks to expand the budget, updates `budget_max` and compares available options.

---

# Mandatory Documentation Rule

Every major change must be documented in:
- `PROJECT_MEMORY.md`
- `.antigravity_rules.md`
- `.cursorrules.md`
- `.github/copilot-instructions.md`
- `README.md`
- `docs/YYYY-MM-DD_konu.md`