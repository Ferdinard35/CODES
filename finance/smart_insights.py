"""
smart_insights.py
=================
AI-style spending analysis – no external API needed.
Pure Python logic that reads from the local database and produces
human-readable insights, warnings, and suggestions.
"""

from collections import defaultdict
from datetime import datetime, date
import database


# ── helpers ───────────────────────────────────────────────────────
def _current_month():
    return datetime.now().strftime("%Y-%m")


def _month_name(ym):
    import calendar
    try:
        y, m = ym.split("-")
        return f"{calendar.month_abbr[int(m)]} {y}"
    except Exception:
        return ym


def _get_all_expenses():
    with database.connect_db() as conn:
        return conn.execute("""
            SELECT date, category, amount_cents
            FROM transactions
            WHERE type = 'Expense'
            ORDER BY date DESC
        """).fetchall()


def _get_all_income():
    with database.connect_db() as conn:
        return conn.execute("""
            SELECT date, amount_cents
            FROM transactions
            WHERE type = 'Income'
            ORDER BY date DESC
        """).fetchall()


# ── public API ────────────────────────────────────────────────────
def generate_insights() -> list[dict]:
    """
    Return a list of insight dicts:
        {
          "type":    "warning" | "info" | "success" | "tip",
          "title":   str,
          "message": str,
        }
    """
    insights = []
    expenses = _get_all_expenses()
    income   = _get_all_income()

    if not expenses and not income:
        return [{
            "type": "info",
            "title": "No Data Yet",
            "message": "Add some transactions to get personalised insights."
        }]

    # ── 1. Category breakdown for current month ──
    month = _current_month()
    cat_totals = defaultdict(float)
    month_total = 0.0

    for row in expenses:
        if str(row[0]).startswith(month):
            amt = row[2] / 100
            cat_totals[row[1]] += amt
            month_total += amt

    if month_total > 0:
        for cat, amt in sorted(cat_totals.items(), key=lambda x: -x[1]):
            pct = (amt / month_total) * 100
            if pct >= 40:
                insights.append({
                    "type": "warning",
                    "title": f"High {cat} Spending",
                    "message": (
                        f"You spent GHS {amt:,.2f} on {cat} this month "
                        f"({pct:.0f}% of total expenses). "
                        f"Consider setting a category limit."
                    )
                })
            elif pct >= 25:
                insights.append({
                    "type": "info",
                    "title": f"{cat} Is Your #2 Category",
                    "message": (
                        f"GHS {amt:,.2f} on {cat} = {pct:.0f}% of your "
                        f"monthly spend."
                    )
                })

    # ── 2. Budget usage ──
    budget_cents = database.get_budget(month)
    spent_cents  = database.get_month_expenses(month)
    budget = budget_cents / 100
    spent  = spent_cents / 100

    if budget > 0:
        pct = (spent / budget) * 100
        if pct > 100:
            insights.append({
                "type": "warning",
                "title": "Budget Exceeded",
                "message": (
                    f"You've overspent by GHS {spent - budget:,.2f} "
                    f"({pct:.0f}% of your {_month_name(month)} budget)."
                )
            })
        elif pct >= 80:
            insights.append({
                "type": "warning",
                "title": f"{pct:.0f}% of Budget Used",
                "message": (
                    f"Only GHS {budget - spent:,.2f} left for the rest of "
                    f"{_month_name(month)}. Slow down spending."
                )
            })
        else:
            insights.append({
                "type": "success",
                "title": "On Track This Month",
                "message": (
                    f"You've used {pct:.0f}% of your budget. "
                    f"GHS {budget - spent:,.2f} remaining – great discipline!"
                )
            })

    # ── 3. Month-over-month expense trend ──
    monthly = defaultdict(float)
    for row in expenses:
        key = str(row[0])[:7]
        monthly[key] += row[2] / 100

    months_sorted = sorted(monthly.keys())
    if len(months_sorted) >= 2:
        prev = monthly[months_sorted[-2]]
        curr = monthly[months_sorted[-1]]
        diff_pct = ((curr - prev) / prev * 100) if prev else 0

        if diff_pct > 20:
            insights.append({
                "type": "warning",
                "title": "Spending Increased",
                "message": (
                    f"Expenses rose {diff_pct:.0f}% vs last month "
                    f"(GHS {prev:,.2f} → GHS {curr:,.2f})."
                )
            })
        elif diff_pct < -10:
            insights.append({
                "type": "success",
                "title": "Spending Decreased",
                "message": (
                    f"Great job! Expenses dropped {abs(diff_pct):.0f}% vs "
                    f"last month."
                )
            })

    # ── 4. Savings rate ──
    total_inc = sum(r[1] for r in income) / 100
    total_exp = sum(r[2] for r in expenses) / 100

    if total_inc > 0:
        savings_rate = ((total_inc - total_exp) / total_inc) * 100
        if savings_rate < 10:
            insights.append({
                "type": "warning",
                "title": "Low Savings Rate",
                "message": (
                    f"Your overall savings rate is {savings_rate:.1f}%. "
                    f"Financial advisors recommend saving at least 20%."
                )
            })
        elif savings_rate >= 30:
            insights.append({
                "type": "success",
                "title": "Excellent Savings Rate",
                "message": (
                    f"You're saving {savings_rate:.1f}% of your income. "
                    f"Keep it up!"
                )
            })
        else:
            insights.append({
                "type": "info",
                "title": f"Savings Rate: {savings_rate:.1f}%",
                "message": "Aim for 20–30% to build a solid financial cushion."
            })

    # ── 5. Top-spend day pattern ──
    day_totals = defaultdict(float)
    for row in expenses:
        try:
            d = datetime.strptime(str(row[0]), "%Y-%m-%d").strftime("%A")
            day_totals[d] += row[2] / 100
        except Exception:
            pass

    if day_totals:
        top_day = max(day_totals, key=day_totals.get)
        insights.append({
            "type": "tip",
            "title": f"You Spend Most on {top_day}s",
            "message": (
                f"GHS {day_totals[top_day]:,.2f} total spent on {top_day}s. "
                f"Plan ahead to avoid impulse purchases on this day."
            )
        })

    # ── 6. Actionable savings tip ──
    if cat_totals:
        top_cat = max(cat_totals, key=cat_totals.get)
        tips = {
            "Food":          "Meal-prepping on weekends can cut food costs by 30%.",
            "Transport":     "Combining errands into one trip saves fuel money.",
            "Entertainment": "Look for free or discounted events in your area.",
            "Shopping":      "Wait 48 hours before non-essential purchases.",
            "Bills":         "Review subscriptions – cancel ones you rarely use.",
        }
        tip = tips.get(top_cat, f"Review your {top_cat} expenses for easy savings.")
        insights.append({
            "type": "tip",
            "title": f"Tip: Reduce {top_cat} Costs",
            "message": tip
        })

    return insights
