"""
============================================================
  Apriori Algorithm
============================================================
  The Apriori algorithm is used for Association Rule
  Learning in data mining. It identifies frequent itemsets
  in a transaction database and derives association rules.

  Key Concepts:
    - Support:    How often an itemset appears in the dataset
                  support(A) = transactions containing A / total transactions
    - Confidence: How often the rule A→B is correct
                  confidence(A→B) = support(A∪B) / support(A)
    - Lift:       How much more likely B occurs given A
                  lift(A→B) = confidence(A→B) / support(B)

  Core Property (Apriori Principle):
    If an itemset is frequent, ALL its subsets must also
    be frequent. This allows us to prune the search space.
============================================================
"""

from itertools import combinations
from collections import defaultdict


def get_frequent_itemsets(transactions, min_support):
    """Find all frequent itemsets using the Apriori algorithm."""
    item_counts = defaultdict(int)
    n = len(transactions)

    # Count individual item frequencies (1-itemsets)
    for transaction in transactions:
        for item in transaction:
            item_counts[frozenset([item])] += 1

    # Filter by min_support
    frequent = {k: v for k, v in item_counts.items()
                if v / n >= min_support}

    all_frequent = dict(frequent)
    current_frequent = list(frequent.keys())
    k = 2

    while current_frequent:
        # Generate candidate k-itemsets
        candidates = set()
        for i in range(len(current_frequent)):
            for j in range(i + 1, len(current_frequent)):
                union = current_frequent[i] | current_frequent[j]
                if len(union) == k:
                    candidates.add(union)

        # Count candidate frequencies
        candidate_counts = defaultdict(int)
        for transaction in transactions:
            t_set = frozenset(transaction)
            for candidate in candidates:
                if candidate.issubset(t_set):
                    candidate_counts[candidate] += 1

        # Filter by min_support
        new_frequent = {k_: v for k_, v in candidate_counts.items()
                        if v / n >= min_support}

        all_frequent.update(new_frequent)
        current_frequent = list(new_frequent.keys())
        k += 1

    return all_frequent, n


def generate_rules(frequent_itemsets, n_transactions, min_confidence):
    """Generate association rules from frequent itemsets."""
    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for antecedent in combinations(itemset, size):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent

                support_itemset   = frequent_itemsets[itemset] / n_transactions
                support_antecedent = frequent_itemsets[antecedent] / n_transactions
                support_consequent = frequent_itemsets[consequent] / n_transactions

                if support_antecedent == 0:
                    continue

                confidence = support_itemset / support_antecedent
                lift       = confidence / support_consequent if support_consequent else 0

                if confidence >= min_confidence:
                    rules.append({
                        "antecedent": set(antecedent),
                        "consequent": set(consequent),
                        "support":    round(support_itemset, 3),
                        "confidence": round(confidence, 3),
                        "lift":       round(lift, 3),
                    })
    return rules


# ─────────────────────────────────────────────
# EXAMPLE 1: Grocery Store Transactions
# Find what items customers buy together
# ─────────────────────────────────────────────

print("=" * 60)
print("  APRIORI ALGORITHM — EXAMPLE 1: Grocery Store Basket")
print("=" * 60)

grocery_transactions = [
    ["bread", "milk", "butter"],
    ["bread", "diapers", "beer", "eggs"],
    ["milk", "diapers", "beer", "cola"],
    ["bread", "milk", "diapers", "beer"],
    ["bread", "milk", "butter", "cola"],
    ["milk", "butter"],
    ["bread", "milk"],
    ["bread", "butter", "eggs"],
    ["milk", "diapers", "cola"],
    ["bread", "milk", "diapers"],
]

MIN_SUPPORT    = 0.3   # itemset must appear in at least 30% of transactions
MIN_CONFIDENCE = 0.6   # rule must be correct at least 60% of the time

frequent_sets, n = get_frequent_itemsets(grocery_transactions, MIN_SUPPORT)
rules = generate_rules(frequent_sets, n, MIN_CONFIDENCE)

print(f"\n  Transactions: {n}  |  Min Support: {MIN_SUPPORT}  |  Min Confidence: {MIN_CONFIDENCE}")
print(f"\n  Frequent Itemsets Found ({len(frequent_sets)}):")
for itemset, count in sorted(frequent_sets.items(), key=lambda x: -len(x[0])):
    support = round(count / n, 3)
    print(f"    {str(set(itemset)):<40}  support={support}  count={count}")

print(f"\n  Association Rules Found ({len(rules)}):")
print(f"  {'Antecedent':<25} → {'Consequent':<15}  support  confidence  lift")
print("  " + "-" * 70)
for rule in sorted(rules, key=lambda x: -x['confidence']):
    ant = str(rule['antecedent'])
    con = str(rule['consequent'])
    print(f"  {ant:<25} → {con:<15}  {rule['support']:<9} {rule['confidence']:<12} {rule['lift']}")


# ─────────────────────────────────────────────
# EXAMPLE 2: Online Course Enrollments
# Find which courses students take together
# ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("  APRIORI ALGORITHM — EXAMPLE 2: Course Enrollment Patterns")
print("=" * 60)

course_transactions = [
    ["Python", "DataScience", "MachineLearning"],
    ["Python", "WebDev", "Django"],
    ["Python", "DataScience", "SQL"],
    ["DataScience", "MachineLearning", "SQL"],
    ["Python", "MachineLearning", "SQL"],
    ["WebDev", "Django", "JavaScript"],
    ["Python", "Django", "JavaScript"],
    ["Python", "DataScience", "MachineLearning", "SQL"],
    ["DataScience", "SQL"],
    ["Python", "SQL"],
    ["Python", "DataScience"],
    ["MachineLearning", "SQL", "DataScience"],
]

MIN_SUPPORT    = 0.3
MIN_CONFIDENCE = 0.65

frequent_sets2, n2 = get_frequent_itemsets(course_transactions, MIN_SUPPORT)
rules2 = generate_rules(frequent_sets2, n2, MIN_CONFIDENCE)

print(f"\n  Transactions: {n2}  |  Min Support: {MIN_SUPPORT}  |  Min Confidence: {MIN_CONFIDENCE}")
print(f"\n  Frequent Itemsets Found ({len(frequent_sets2)}):")
for itemset, count in sorted(frequent_sets2.items(), key=lambda x: -len(x[0])):
    support = round(count / n2, 3)
    print(f"    {str(set(itemset)):<50}  support={support}  count={count}")

print(f"\n  Association Rules Found ({len(rules2)}):")
print(f"  {'Antecedent':<30} → {'Consequent':<20}  support  confidence  lift")
print("  " + "-" * 80)
for rule in sorted(rules2, key=lambda x: -x['confidence']):
    ant = str(rule['antecedent'])
    con = str(rule['consequent'])
    print(f"  {ant:<30} → {con:<20}  {rule['support']:<9} {rule['confidence']:<12} {rule['lift']}")

print("\n  Done! Apriori successfully mined association rules from both examples.")
