# ============================================================
# MSDS 501 – Day 2 Exercise  |  Partner B
# ============================================================
# SCENARIO: A grading script reads student quiz scores from a
# list. Some entries are corrupt (non-numeric). The script tries
# to convert every entry to an int so we can compute the total.
#
# YOUR TASK (Task 2): Run this script and read the error.
#   - What type of error is it?
#   - Which line causes it?
#   - Write a comment below explaining the cause.
#
# YOUR TASK (Task 3): Wrap the risky conversion in try/except.
#   - Catch the specific error type (not bare except:)
#   - When a bad value is caught, print a message that includes
#     the index and the bad value — e.g.:
#         [index 2] Skipped bad score: 'absent'
#   - The script should complete without crashing.
#
# EXPECTED OUTPUT (after your fix):
#   Score [0]: 88
#   Score [1]: 95
#   [index 2] Skipped bad score: 'absent'
#   Score [3]: 72
#   [index 4] Skipped bad score: 'n/a'
#   Score [5]: 84
#   Total of valid scores: 339
#   Count of valid scores: 4
# ============================================================

scores = ['88', '95', 'absent', '72', 'n/a', '84']


valid = []


for i, s in enumerate(scores):
    try:
        score = int(s)            # <-- this line crashes on bad strings
        # line 37 crashes on third score which can't be changed to an int; this is a TypeError
        print(f'Score [{i}]: {score}')
        valid.append(score)
    except ValueError:
        print(f"[index {i}] Skipped bad score: '{s}'")
              
print(f'Total of valid scores: {sum(valid)}')
print(f'Count of valid scores: {len(valid)}')
