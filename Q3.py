from collections import defaultdict
import sys

#------------------------------------------------------------------------------

# Data Structures
knap_dict = defaultdict(lambda: []) # Mapping of calorie values to activity
values = [] # list of calorie values

# Get Data
for i, line in enumerate(sys.stdin.readlines()):
    if i == 0:
        n = int(line)
    else:
        [activity, value]= line.strip("\n").split(" ")
        value = int(value)
        knap_dict[value].append(activity)
        values.append(value)

# Basic error checking       
assert n == len(values)

# Dynamic programming problem
memo = {}
def Q(i, s):
    """Construct the dynamic programming solution by memoisation.
       Q(i, s) == True if and only if we can construct a subset of 
       items 0, 1, 2, \dots, i summing to s.
       """
    memo_key = str(i) + str( '-' ) + str(s)
    if memo_key in memo:
        return memo[memo_key]
    elif i == 0:
        val = values[0] == s
    else:
        # Dynamic programming recurrence 
        val = Q(i - 1, s) or values[i] == s or Q(i - 1, s - values[i]) # Eq. 1
    memo[memo_key] = val
    return val

def find_solution(i, cum_sum = 0, sol_so_far  = []):
    """Backtrace the solution.  
    Uses the dynamic programming recurrence above in Eq. 1"""
    if i < 0:
        # We have completed our backtrace
        pass
    elif values[i] == cum_sum:
        # Must backtrace as values[i] may be zero?
        sol_so_far.append(knap_dict[values[i]].pop())
        cum_sum = 0
        return find_solution(i - 1, cum_sum, sol_so_far)
    elif Q(i-1, cum_sum):
        # item i is not in the subset
        find_solution(i - 1, cum_sum, sol_so_far)
    elif Q(i - 1, cum_sum - values[i]):
        # item i is in the subset
        sol_so_far.append(knap_dict[values[i]].pop())
        cum_sum -= values[i]
        return find_solution(i - 1, cum_sum, sol_so_far)
    
    return sol_so_far

def main():
    "Present the solution"
    if Q(n-1, 0):
        sol = find_solution(n-1)
        for activity in sol:
            print activity
    else:
        print "no solution"

main()
