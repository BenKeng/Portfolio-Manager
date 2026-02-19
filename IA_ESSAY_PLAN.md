# IB Computer Science HL — Internal Assessment Essay Plan

## Product: Investment Portfolio Analytics Dashboard
## Tech Stack: Python · Streamlit · Yahoo Finance API · Pandas · Matplotlib

---

## CRITERION A: PLANNING (6 marks | ~500 words total)

### A1 — Scenario (175–250 words)

- **Client**: Identify your real client by first name only (e.g. "My client, Ben, is a Year 13 student at [school] who actively trades equities...")
- **The problem**: Client currently tracks stock purchases in a basic spreadsheet (or on paper). No live pricing, no automatic profit calculation, no visual overview. They must manually look up each stock price on Yahoo Finance, calculate profit by hand, and have no way to compare portfolio performance over time
- **Current solution and why it is inadequate**: Spreadsheet has no API connection → prices go stale immediately; manual arithmetic is error-prone; no graphs or visual analysis capability
- **Evidence of consultation**: Reference Appendix A (Interview 1) — "We discussed...", "Ben explained that he needed...", "We agreed the main pain points were..."
- **Scope**: The product must be web-accessible (Streamlit Cloud) so the client can use it from any device without installing software

### A2 — Rationale (175–250 words)

- **Why Python**: Best ecosystem for financial data (pandas, yfinance); client has no programming experience so a scripted solution is more maintainable than a compiled language
- **Why Streamlit**: Produces a web dashboard without requiring HTML/CSS/JS knowledge; interactive widgets (data_editor, selectbox, tabs) are native; free cloud hosting via Streamlit Community Cloud; appropriate for the scenario because the client needs browser access, not a desktop app
- **Why yfinance REST API**: Free, no API key required, provides historical and real-time equity data; directly solves the client's "stale prices" problem
- **Why not alternatives**: A plain Flask/Django app would require far more boilerplate for interactive UI; a mobile app is unnecessary since the client primarily uses a laptop; Excel VBA would not support live API calls easily
- **Reference consultation**: "After presenting this technology stack to Ben (Appendix B — Interview 2), he confirmed that browser-based access was ideal and agreed with the proposed approach."

### A3 — Success Criteria (bullet points, no word count)

Write 8–10 specific, testable criteria. Each must be demonstrable in the video and evaluable in Criterion E.

1. The system authenticates users via a password before granting dashboard access
2. Users can manually enter stock positions (ticker, purchase date, quantity) through an interactive table
3. Users can alternatively upload a CSV file containing portfolio positions
4. The system validates ticker symbols against Yahoo Finance before processing
5. The system fetches live closing prices and historical buy prices via the yfinance REST API
6. Profit ($), percentage return (%), and cost per share ($) are calculated and displayed for each position
7. An executive summary displays aggregate portfolio metrics (total profit, total cost, total return %)
8. An interactive line chart shows individual stock price history from the purchase date, with a buy-date marker
9. A multi-stock comparative chart overlays all portfolio assets on one graph
10. A pie chart visualizes capital allocation across holdings
11. Users can export the full analytics table as a downloadable CSV file
12. Users can save manually entered positions to a local CSV for persistence

---

## CRITERION B: SOLUTION OVERVIEW (6 marks | no word count, diagrams only)

### B1 — Record of Tasks

Use the **official IB template**. Must cover all 5 SDLC stages in the Criterion column:

| Phase | Example entries |
|-------|-----------------|
| **Plan** | Initial client interview; agreed on requirements; chose Python + Streamlit stack |
| **Design** | Created UML class diagram; designed UI mockups; wrote test plan; designed data flow |
| **Develop** | Implemented data_loader.py (API layer); built models.py (OOP classes); built App.py (UI); integrated plotting.py |
| **Test** | Tested normal inputs (AAPL, TSLA); tested invalid tickers (XYZ123); tested empty CSV; tested boundary dates |
| **Implement** | Deployed to Streamlit Cloud; trained client on usage; gathered client feedback |

### B2 — Design Overview (diagrams, tables, mockups — NO extended writing)

**Include all of the following:**

- **DFD Context Diagram**: User ↔ Portfolio Manager System ↔ Yahoo Finance API
- **DFD Level 0**: Show data flows between: User Input → Validation → API Fetch → Analytics Engine → Display Layer
- **UML Class Diagram**: Show `StockPosition` and `Portfolio` classes with attributes, methods, and their relationship (composition — Portfolio contains 0..* StockPosition)
  - `StockPosition`: ticker, purchase_date, quantity, current_value, buy_value, profit, return_pct, cost_per_share | update_metrics(), to_dict()
  - `Portfolio`: positions[] | add_position(), refresh_all(), get_summary_df(), get_totals()
- **Module Dependency Diagram**: App.py → analytics.py → models.py → data_loader.py; App.py → plotting.py
- **Data Dictionary Table**:
  - positions.csv: ticker (string), datetime (date), quantity (integer)
  - Output DataFrame columns: Stock Ticker, Purchase Date, Quantity, Cost Per Share ($), Total Cost ($), Current Value ($), Profit ($), Percentage Return (%)
- **Annotated Screen Mockups**: Login page, data entry view, dashboard with metrics/charts (use Adobe XD or hand-drawn with annotations)
- **Flowchart / Pseudocode**: Show logic for `update_metrics()` — fetch API → calculate profit → calculate return. Show login flow with session state

### B3 — Test Plan (table format, part of design overview)

| # | What to test | Input | Expected output | Type |
|---|-------------|-------|-----------------|------|
| 1 | Valid ticker entry | AAPL, 2025-01-15, 10 | Row appears with profit/cost data | Normal |
| 2 | Invalid ticker entry | XYZFAKE, 2025-01-15, 5 | Error: "Invalid Tickers Detected" | Abnormal |
| 3 | Empty table submission | No rows entered, click Update | Warning: "Please enter at least one valid stock position" | Boundary |
| 4 | CSV upload with correct format | positions.csv with 3 valid rows | Dashboard populates with 3 rows | Normal |
| 5 | CSV upload with wrong columns | CSV missing "ticker" column | Error message displayed | Abnormal |
| 6 | Future date entry | AAPL, 2030-01-01, 5 | Graceful handling (no crash) | Extreme |
| 7 | Quantity of zero | AAPL, 2025-01-15, 0 | Error or handled division by zero | Boundary |
| 8 | Password authentication | Correct password "admin" | Dashboard loads | Normal |
| 9 | Wrong password | "wrongpassword" | "Access Denied" error shown | Abnormal |
| 10 | Save to local disk | Click Save button | File written to config/positions.csv | Normal |
| 11 | Download CSV export | Click Export button | Browser downloads portfolio_analysis.csv | Normal |
| 12 | Chart rendering | Select AAPL from dropdown | Line chart with buy-date marker appears | Normal |

---

## CRITERION C: DEVELOPMENT (12 marks | 500–1000 words)

**This is the most heavily weighted criterion. Structure the writing around techniques used.**

### Structure of the product and why it is appropriate

- 5-file modular architecture following separation of concerns:
  - `data_loader.py` — Data access layer (Yahoo Finance API calls, CSV parsing, ticker validation)
  - `models.py` — Domain model layer (OOP classes: StockPosition, Portfolio)
  - `analytics.py` — Business logic / controller (factory function, CSV→Portfolio pipeline)
  - `plotting.py` — Visualization layer (matplotlib chart generation)
  - `App.py` — Presentation layer (Streamlit UI, session state, user interaction)
- Explain this follows an MVC-like pattern: Model (models.py), View (App.py + plotting.py), Controller (analytics.py + data_loader.py)

### Techniques to highlight (with code screenshots and explanations)

**Complexity indicators:**

1. **REST API integration** (`yfinance`): `fetch_stock_value()` in data_loader.py makes HTTP calls to Yahoo Finance to retrieve real-time and historical price data. Show the code, explain the API call, explain timezone normalization (`tz_localize(None)`)
2. **Object-Oriented Programming**: `StockPosition` class encapsulates per-position data and logic; `Portfolio` class manages a collection. Show the UML and code side-by-side. Explain encapsulation (attributes + methods bundled), composition (Portfolio has-a list of StockPositions)
3. **Dynamic data structures**: Lists of objects (`self.positions`), dictionaries (`to_dict()`), pandas DataFrames throughout
4. **File I/O**: CSV reading/writing for data persistence (`pd.read_csv`, `to_csv`); `tempfile.NamedTemporaryFile` for secure intermediate file handling
5. **Complex presentation framework**: Streamlit with `st.data_editor`, `st.metric`, `st.tabs`, `st.columns`, `st.download_button`, `st.selectbox`, `st.file_uploader`
6. **Multiple visualization types**: Matplotlib line charts (single + multi-stock), pie chart for allocation — each generated programmatically with formatted axes

**Ingenuity indicators:**

7. **Input validation**: `is_valid_ticker()` queries the API to verify a symbol exists before processing; quantity/date validation with user-facing error messages; graceful empty-state handling
8. **Error handling**: try/except blocks around API calls and CSV parsing; fallback returns `(0.0, 0.0)` if data is unavailable rather than crashing
9. **Session state management**: `st.session_state` preserves login and table data across Streamlit reruns; `st.rerun()` forces immediate UI refresh
10. **Meaningful naming**: All variables, functions, and classes follow clear naming conventions (`fetch_stock_value`, `StockPosition`, `build_portfolio_from_csv`)
11. **Modular functions**: Each function does one thing — `is_valid_ticker()` validates, `fetch_stock_value()` fetches, `update_metrics()` calculates, `to_dict()` serializes
12. **Secrets management**: Password stored in `.streamlit/secrets.toml`, accessed via `st.secrets`, with a fallback default

### Existing tools / libraries used (must be acknowledged)

| Library | Purpose | Source |
|---------|---------|--------|
| streamlit | Web dashboard framework | https://streamlit.io |
| pandas | DataFrame manipulation | https://pandas.pydata.org |
| yfinance | Yahoo Finance API wrapper | https://pypi.org/project/yfinance/ |
| matplotlib | Chart generation | https://matplotlib.org |
| tempfile | Secure temporary file handling | Python standard library |

---

## CRITERION D: FUNCTIONALITY & EXTENSIBILITY (4 marks)

### D1 — Video (5–7 min, MP4)

Script the video to walk through each success criterion:

1. **0:00–0:30** — Show login screen → enter wrong password → "Access Denied" → enter correct password → dashboard loads
2. **0:30–1:30** — Manual entry: type AAPL / 2025-01-15 / 10 and TSLA / 2025-06-01 / 5 using the date picker → click "Update Portfolio View" → results table appears
3. **1:30–2:00** — Show ticker validation: enter "XYZFAKE" → click update → error message appears
4. **2:00–2:30** — Show empty submission warning
5. **2:30–3:00** — Switch toggle to CSV upload → upload positions.csv → dashboard populates
6. **3:00–3:30** — Walk through the results table: point out each column (Ticker, Quantity, Cost, Profit, Return %)
7. **3:30–4:00** — Show Executive Summary metric cards (profit delta, total cost, growth %)
8. **4:00–4:30** — Show single stock chart with buy-date red line → select different ticker → chart updates
9. **4:30–5:00** — Switch to Comparison View tab → all stocks plotted together
10. **5:00–5:15** — Switch to Capital Allocation tab → pie chart shown
11. **5:15–5:30** — Click "Export Portfolio Report" → CSV downloads
12. **5:30–5:45** — Click "Save Entry to Local Disk" → success message
13. **5:45–6:00** — Brief mention of how the product could be extended (see below)

### D2 — Extensibility (assessed through B and C documentation)

The following is evidenced by:
- **Well-structured code**: 5 modules with clear responsibilities
- **Annotated code listing in appendix**: Every function has a docstring; inline comments explain key logic
- **OOP design**: New asset types (bonds, crypto) could extend StockPosition; new analytics could be added to Portfolio
- **Consistent conventions**: snake_case for functions/variables, PascalCase for classes

---

## CRITERION E: EVALUATION (6 marks | ~500 words total)

### E1 — Evaluation (175–250 words)

- Go through **every** success criterion from A3 and state: Met / Partially Met / Not Met
- For each, reference specific evidence (video timestamp or screenshot)
- **Include client feedback**: "I presented the finished product to Ben and conducted a feedback interview (Appendix C). He stated: '...'. He confirmed criteria 1–10 were fully met. He noted that..."
- Discuss any criteria that were partially met and why
- Be honest — partial honesty scores better than false claims

### E2 — Recommendations (175–250 words)

Must be **realistic** and go **beyond** unmet criteria:

1. **Multi-currency support**: Currently all values are in USD. The API supports international exchanges — could add a currency conversion layer using a forex API
2. **User accounts with database**: Replace the single password with a proper authentication system (e.g. Streamlit's built-in auth or a SQLite/PostgreSQL backend) so multiple users can each have their own portfolio
3. **Historical portfolio tracking**: Currently shows a snapshot. Could store daily snapshots to a database and plot portfolio value over time (not just individual stocks)
4. **Dividend tracking**: yfinance provides dividend data — could extend StockPosition with a `dividends` attribute and factor it into total return calculations
5. **Automated alerts**: Email or push notification when a stock drops below a configurable threshold

Each recommendation should include 1–2 sentences explaining the **benefit to the client**.

---

## APPENDICES (not counted in 2000 word limit)

- **Appendix A**: Transcript/summary of Client Interview 1 (initial requirements gathering)
- **Appendix B**: Transcript/summary of Client Interview 2 (presenting proposed solution and success criteria; client signs off)
- **Appendix C**: Transcript/summary of Client Feedback Session (post-implementation evaluation)
- **Appendix D**: Full annotated code listing (all .py files with comments)
- **Appendix E**: Additional screenshots of the product functioning (supplement to video)

---

## WORD COUNT BUDGET

| Section | Target | Notes |
|---------|--------|-------|
| A1 Scenario | 225 words | Extended writing |
| A2 Rationale | 225 words | Extended writing |
| A3 Success Criteria | 0 (bullets) | Not counted |
| B Record of Tasks | 0 | Template, not counted |
| B Design Overview | 0 | Diagrams only, not counted |
| C Development | 900 words | Extended writing — this is where marks are won |
| D Video | 0 | No written component |
| E1 Evaluation | 225 words | Extended writing |
| E2 Recommendations | 225 words | Extended writing |
| **TOTAL** | **~1800 words** | Under the 2000 hard limit with buffer |

---

## KEY REMINDERS

- [ ] Never include your real name, school name, or teacher name — use your 6-character IB code only
- [ ] Client interviews MUST be referenced in the main text ("see Appendix A") or they receive no credit
- [ ] The Record of Tasks must use the **official IB template**
- [ ] Export all documentation as PDF with the exact filenames: Crit_A_Planning.pdf, Crit_B_Design.pdf, etc.
- [ ] Video must be MP4, max 7 minutes
- [ ] Include the product files in a /Product folder and documentation in a /Documentation folder
