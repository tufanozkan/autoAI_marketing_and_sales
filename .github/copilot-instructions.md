# Automotive AI Marketing Platform

## Project Summary

This project is an AI-powered automotive marketing platform focused on used vehicle advertising and creative generation for Arkas 2. El.

The platform collects vehicle listings from the Arkas live catalog, extracts and stores structured vehicle information in PostgreSQL 17, and uses that data to generate marketing-focused visuals, banners, posters, ad creatives, social media content, and promotional materials, along with an interactive **Cognitive AI Sales Consultant Chatbot** that guides customers and controls frontend search in real time.

---

## Business Goal

Transform raw vehicle listing data into high-converting marketing assets and active sales leads.

The system should:

1. Collect vehicle information from external listing sources (`https://www.arkasotomotiv2.com`).
2. Store and organize vehicle data in a structured PostgreSQL 17 database (`vehicles`, `customer_leads`, `marketing_copies`, `creative_briefs`, `posters`).
3. Enrich vehicle records with marketing context and brand archetypes.
4. Generate persuasive advertising content (Safe & Bold copy variants, Instagram Stories).
5. Render Quiet Luxury visual posters and 16:9 banners using genuine catalog photography.
6. Provide an intelligent, human-like **Cognitive AI Sales Consultant** (`ChatbotAgent`) with session deduplication, direct equipment Q&A, budget expansion, and dynamic cross-vehicle recommendations (e.g. switching to Volvo XC40 for heated steering requests).
7. Dispatch real-time page filter actions from the chatbot.

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

# Brand Marketing Guidelines

## Volvo
Focus on: Safety, Family protection, Reliability, Premium comfort, Scandinavian quality, Long-term trust, Winter Package (Heated steering wheel & heated seats).
Target customer: Families, Professionals, Safety-conscious buyers, Premium SUV buyers.

## Skoda
Focus on: Simply Clever practicality, Space efficiency, High fuel economy (1.0 TSI), Low maintenance, Everyday convenience.
Target customer: Modern families, Value-conscious commuters, Smart budget planners.

## Ford
Focus on: Dependability, Practical performance, Commercial utility, Versatility, Everyday usability, Strong value proposition.
Target customer: Business fleets, Tradespeople, Active lifestyle families.

---

# AI Sales Consultant & Chatbot Rules

1. **Lead Onboarding & Memory:** Warm greeting, captures Customer Name, Phone, and Budget into `customer_leads` under a single persistent `session_id`.
2. **Direct Q&A:** Direct and concise responses regarding Transmission (DSG Otomatik), Mileage (KM), Price, Fuel Economy, and Equipment without generic repetitive templates.
3. **Cross-Vehicle Recommendations:** If a user asks for an unavailable feature (e.g. steering heating on a Skoda Kamiq Elite), the agent automatically scans the entire inventory and suggests the **Volvo XC40 Plus Dark** with its winter package and updates the page filter synchronously.
4. **Budget Expansion:** When a user asks to expand the budget ("fiyat aralığını 5m kadar çıkart"), updates `budget_max` and compares all available models.

---

# Mandatory Documentation Rule

Every major change must be documented in:
- `PROJECT_MEMORY.md`
- `.antigravity_rules.md`
- `.cursorrules.md`
- `.github/copilot-instructions.md`
- `README.md`
- `docs/YYYY-MM-DD_konu.md`