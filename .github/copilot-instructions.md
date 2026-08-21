# AutoAI Showroom — AI-Powered Automotive Marketing & Sales Consultant Platform

## Project Summary

This project is an open-source, full-stack AI-powered automotive marketing and smart digital showroom platform. It combines automated listing ingestion, multi-model creative copy generation (Balanced & Engaging variants), high-converting social media hooks, and a **Cognitive AI Sales Consultant Chatbot** that guides prospective buyers and controls the Next.js showcase in real time.

The platform collects rich vehicle listings (including technical specs, package/trim levels, equipment lists, damage/expertise reports, and genuine photo galleries), stores structured data in PostgreSQL, and generates certified advertising assets and lead intelligence.

---

## Business Goal

Transform raw vehicle listing data into high-converting marketing copy and active sales leads.

The system:

1. Collects comprehensive vehicle information from automotive listing sources and portals.
2. Stores and organizes vehicle data in a structured PostgreSQL database (`vehicles`, `vehicle_images`, `creative_briefs`, `customer_leads`, `test_drives`).
3. Modular Architecture:
   - `backend/db/`: Database session management and SQLAlchemy ORM models.
   - `backend/scraper/`: Listing scrapers, hardware normalization and content hashing.
   - `backend/agent/`: Cognitive AI sales consultant (`ChatbotAgent`) and marketing copy generator (`MarketingAgent`).
   - `backend/web/`: FastAPI REST endpoints and `/vehicle_images` static asset mounts.
   - `frontend/`: Next.js 15 UI showroom, floating AI assistant widget, and static vehicle assets.
   - `tests/`: Modular test suite covering chatbot, NLU, API routes, and assets (85 tests).
4. Dispatches real-time page filter actions from the chatbot.

---

## Core Principle

Do not think like a static vehicle catalog. Think like an automotive marketing agency and an expert sales consultant.

When generating content or speaking in chat:
- Focus on customer benefits and emotional value propositions.
- Highlight certified inspection points, warranty coverage, and transparency.
- Provide tailored financing/credit and trade-in guidance.
- Avoid simply repeating technical specifications unless they directly support purchasing decisions.

---

## AI Sales Consultant & Chatbot Rules

1. **Role & Principle:** Cognitive Automotive AI Sales Consultant. Strictly zero-hallucination.
2. **Rule 1 (Body Type & Filtering):** Direct match to `body_type` in database. If in stock, directly present matching vehicles.
3. **Rule 2 (Context Management & Anti-Hallucination Shield):** Never generate fabricated context. Reset previous model focus when new filters are applied.
4. **Rule 3 (Cross-Recommendation Criteria):** Only cross-recommend when specific requested criteria is missing using transparent phrasing.
5. **Lead Onboarding & Memory:** Warm greeting, captures Customer Name, Phone (or respects `phone_declined`), and Budget into `customer_leads` under a single persistent `session_id`.
6. **Turkish NER & Honorifics:** 1000+ Turkish name dictionary + negative word blacklist. Inquires honorific preference for unisex names and remembers choice.
7. **Budget & Negation Parsing:** Accurately distinguishes minimum vs maximum price bounds and filters out negative criteria ("dizel olmasın", "manuel istemiyorum").
8. **New vs Used Distinction:** Evaluates true 0 KM stock for new vehicle inquiries and offers certified 12-month guaranteed alternatives.