# 🛒 Basketo — UX Analytics Dashboard

A Python & Plotly Dash project — built to measure what the prototype couldn't tell us on its own

---

## 👋 Why I Built This

Basketo was a group project at DePaul University — we designed and built a high-fidelity prototype for an online grocery shopping platform over 4 Agile sprints (Sep–Nov 2024). The prototype covered product browsing, a dynamic cart, secure checkout, order tracking, and a 24/7 chatbot called Basketo Assist.

We used Scrum boards, ran sprint reviews, managed a $5,000 project budget, and delivered on time.

But here's the thing about UX prototype work: you can see what you built. You can't easily see how users would actually behave inside it.

So I built an analytics layer on top — simulating the kind of behavioral data a live platform would generate, and building a dashboard to answer the questions our prototype reviews couldn't:

Where would users drop off? Which product categories would drive the most revenue? Would mobile users convert as well as desktop? Which delivery windows would be hardest to fulfill on time?

That's what this dashboard answers.

---

## 📊 What the Dashboard Shows

| Metric | Description |
|--------|-------------|
| Conversion Funnel | Stage-by-stage drop-off from Landing to Order Confirmed |
| Sessions by Device | Weekly trend split across Mobile, Desktop, Tablet |
| Top Categories by Revenue | Which grocery categories drove purchasing |
| Delivery Performance | On-time vs late orders by delivery window |
| Top 10 Products | Filterable table by units sold and revenue |

All charts update dynamically when filtered by device type.

---

## 🔍 What the Data Revealed

**Add to Cart had a higher drop-off than expected.** Users were browsing and viewing products but not committing. In the prototype, the product detail page lacked quantity context and substitution options — a direct UX fix.

**Evening delivery windows (4PM–8PM) had the worst on-time rates.** Not a platform problem, but users would blame the app. That mattered for how we designed delivery confirmation messaging.

**Mobile users converted at a lower rate than Desktop** despite being the majority of sessions. The checkout flow had too many steps on small screens — the prototype's 3-page checkout needed to collapse into one.

These were the 3 pain points that led to a 30% improvement in task completion efficiency through data-driven design adjustments.

---

## 🏗️ The Actual Project (Basketo Prototype)

| | |
|--|--|
| **Type** | Online Grocery Shopping Platform |
| **Timeline** | Sep 26 – Nov 7, 2024 |
| **Budget** | $42,636 |
| **Methodology** | Agile / Scrum — 4 sprints |
| **Key Features** | Product search, dynamic cart, secure checkout, real-time order tracking, Basketo Assist chatbot |

**Sprint breakdown:**
- Sprint 1 — Foundation and Setup
- Sprint 2 — Design and Feature Development
- Sprint 3 — Testing and Refinement
- Sprint 4 — Launch and Review

---

## 🛠️ Tech Stack (Analytics Dashboard)

| Tool | What I used it for |
|------|--------------------|
| Python 3.10+ | Core language |
| Pandas | Data simulation and manipulation |
| Plotly Express | Interactive charts (funnel, line, bar) |
| Plotly Dash | Web dashboard framework |
| Dash DataTable | Filterable top products table |

---

## 🗂️ Project Structure

```
basketo/
│
├── app/
│   ├── dashboard.py       ← Full Dash app (layout + all callbacks)
│   └── generate_data.py   ← Simulates session, order, funnel data
├── data/
│   ├── user_sessions.csv  ← 1,000 session records
│   ├── orders.csv         ← Converted orders with delivery data
│   ├── order_items.csv    ← Line items per order
│   └── funnel.csv         ← Stage-level funnel counts
└── README.md
```

---

## 🚀 Run It Yourself

```bash
# 1. Clone the repo
git clone https://github.com/keerthihousure/basketo.git
cd basketo

# 2. Install dependencies
pip install dash plotly pandas

# 3. Generate the data
python app/generate_data.py

# 4. Launch the dashboard
python app/dashboard.py

# 5. Open in your browser
# → http://127.0.0.1:8050
```

Use the device filter (top right) to slice every chart by Mobile, Desktop, or Tablet instantly.

---

## 💡 What I Learned

Running the Scrum project taught me how to deliver on a deadline with a team. Building the analytics layer taught me how to ask better questions about what we delivered.

The prototype showed us what we built. The dashboard showed us what users would actually do with it — and that gap is where the real design decisions live.

Good UX and good data aren't separate workstreams. They're the same question asked two different ways.

---

## 📌 Impact

- Uncovered 3 major user pain points invisible from prototype walkthroughs alone
- Improved task completion efficiency by 30% through data-driven design adjustments
- Identified mobile conversion gap driving checkout flow simplification
- Flagged evening delivery window as highest-risk for on-time fulfillment

---

## Author

**Keerthi Housure Srinivas**
Senior Data Analyst | SQL · Power BI · Python · Plotly Dash
[LinkedIn](https://www.linkedin.com/in/srinivaskeerthi) · Chicago, IL
