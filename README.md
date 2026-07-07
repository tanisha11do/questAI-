# questAI- Personalized AI Learning & Knowledge Graph
Stay updated with AI by automatically converting AI news into a living knowledge graph, personalized quizzes, and learning recommendations.

## Proposed Architecture
                   ┌────────────────────────────┐
                   │        News Sources        │
                   │ OpenAI, NVIDIA, Anthropic  │
                   │ arXiv, HF, GitHub, etc.    │
                   └─────────────┬──────────────┘
                                 │
                      Daily Scheduler (Cron)
                                 │
                                 ▼
                  ┌───────────────────────────┐
                  │     News Ingestion        │
                  │ RSS/API/Web Scraper       │
                  └─────────────┬─────────────┘
                                │
                                ▼
                ┌────────────────────────────────┐
                │      LLM Information Extractor │
                │                                │
                │ Extract:                       │
                │ • Entities                     │
                │ • Relationships                │
                │ • Events                       │
                │ • Metadata                     │
                └─────────────┬──────────────────┘
                              │
                              ▼
              ┌─────────────────────────────────┐
              │ Entity Resolution Engine        │
              │                                 │
              │ Exact Match                     │
              │ Fuzzy Match                     │
              │ (Vector Search - V2)            │
              └─────────────┬───────────────────┘
                            │
                New?         │       Existing?
                  │          │            │
                  ▼          │            ▼
            Create Node      │      Update Node
                             │
                             ▼
               ┌────────────────────────────┐
               │ Relationship Builder       │
               │                            │
               │ Creates graph edges        │
               └────────────┬───────────────┘
                            │
                            ▼
               ┌────────────────────────────┐
               │ Knowledge Graph Database   │
               └────────────┬───────────────┘
                            │
          ┌─────────────────┴──────────────────┐
          │                                    │
          ▼                                    ▼
 Question Generator                 Recommendation Engine
          │                                    │
          ▼                                    ▼
    Question Bank                     User Learning Profile
          │                                    │
          └─────────────────┬──────────────────┘
                            ▼
                    Quiz Application
                            │
                            ▼
                      Dashboard

