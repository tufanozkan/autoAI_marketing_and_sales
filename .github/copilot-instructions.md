# Automotive AI Marketing Platform

## Project Summary

This project is an AI-powered automotive marketing platform focused on used vehicle advertising, creative copy generation, and dynamic AI sales assistance for Arkas 2. El.

The platform collects rich vehicle listings (including full technical specs, package/trim levels, equipment lists, damage/expertise reports, and genuine photo galleries), stores structured vehicle information in PostgreSQL 17, and uses that data to generate high-converting marketing copies (Safe & Bold variants), social media content, and promotional materials, accompanied by a **Cognitive AI Sales Consultant Chatbot** that guides users and controls the Next.js showcase in real time.

---

## Business Goal

Transform raw vehicle listing data into high-converting marketing copy and active sales leads.

The system:

1. Collects comprehensive vehicle information from external listing sources.
2. Stores and organizes vehicle data in a structured PostgreSQL 17 database (`vehicles`, `vehicle_images`, `creative_briefs`, `customer_leads`).
3. Modular Architecture:
   - `backend/db/`: Database session management and SQLAlchemy ORM models.
   - `backend/scraper/`: Listing scrapers, hardware normalization and content hashing.
   - `backend/agent/`: Cognitive AI sales consultant (`ChatbotAgent`) and marketing copy generator (`MarketingAgent`).
   - `backend/web/`: FastAPI REST endpoints and `/vehicle_images` static asset mounts.
   - `frontend/`: Next.js 15 UI showroom, floating AI assistant widget, and static vehicle assets (`frontend/public/vehicle_images/`).
   - `tests/`: Modular test suite covering chatbot, NLU, API routes, and assets.
4. Dispatches real-time page filter actions from the chatbot.

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

1. **Lead Onboarding & Memory:** Warm greeting, captures Customer Name, Phone (or respects `phone_declined`), and Budget into `customer_leads` under a single persistent `session_id`.
2. **Turkish NER & Honorifics:** 1000+ Turkish name dictionary + negative word blacklist. Inquires honorific preference for unisex names (Deniz, Derya, Ege, Özgür, etc.) and remembers choice.
3. **Zero Hallucination:** Strict adherence to PostgreSQL 17 database as single source of truth for price, mileage, specs, and stock.
4. **Budget & Negation Parsing:** Accurately distinguishes "1.5m üstü" (`min_price`) vs "1.5m altı" (`max_price`) and filters out negative criteria ("dizel olmasın", "manuel istemiyorum").
5. **New vs Used Distinction:** Evaluates true 0 KM stock for new vehicle inquiries and honestly offers 12-month guaranteed alternatives.
6. **Cross-Vehicle Recommendations & UI Sync:** If a feature is absent on the focused vehicle, suggests alternatives and synchronizes the Next.js showcase via `filter_action`.

---

# Mandatory Documentation Rule

Every major change must be documented in:
- `PROJECT_MEMORY.md`
- `.antigravity_rules.md`
- `.cursorrules.md`
- `.github/copilot-instructions.md`
- `README.md`
- `docs/YYYY-MM-DD_konu.md`