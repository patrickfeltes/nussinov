import sys
import copy

# Perform the following recurrence
# s[i][j] = max(
#   0                                           if i >= j                           (1)
#   s[i + 1][j]                                 if i < j                            (2)
#   s[i][j - 1]                                 if i < j                            (3)
#   s[i + 1][j - 1] + 1                         if i < j and vi matches vj          (4)
#   s[i + 1][j - 1]                             if i < j and vi does not match vj   (5)
#   max(s[i][k] + s[k+1][j]) for i < k < j      if i < j                            (6)
# )
def nussinov_alg(rna_sequence, base_pairings):
    n = len(rna_sequence)
    s = [[0] * n for x in range(n)]

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            vi = rna_sequence[i]
            vj = rna_sequence[j]

            # Assemble a list of possible values for the cell we are examining
            # Once we have all the possible values in the list, set the 
            # value of s[i][j] to the maximum value in the list
            max_lst = []

            # Cases two and three in the recurrence (see above)
            max_lst.append(s[i + 1][j])
            max_lst.append(s[i][j - 1])

            # Case four and five of the recurrence (see above)
            if (vj in base_pairings[vi]):
                max_lst.append(s[i + 1][j - 1] + 1)
            else:
                max_lst.append(s[i + 1][j - 1])

            # Case six of the recurrence (see above)
            max_skip = max([s[i][k] + s[k + 1][j] for k in range(i + 1, j)], default=0)
            max_lst.append(max_skip)

            s[i][j] = max(max_lst)

    return s

# Get each of the possible tracebacks
def traceback(s, seq, base_pairings):
    stacks = []
    traceback_lists = []
    match_lists = []
    results = []

    initial_stack = []
    initial_stack.append((0, len(s) - 1))
    stacks.append(initial_stack)
    initial_traceback = []
    initial_traceback.append((0, len(s) - 1))
    traceback_lists.append(initial_traceback)
    initial_match_list = []
    match_lists.append(initial_match_list)

    already_started_on = []
    for i in range(len(s)):
        already_started_on.append([])
        for j in range(len(s[i])):
         already_started_on[i].append([])

    # Keep iterating until we have completed all of the possible tracebacks
    while len(stacks) != 0:
        prev_stacks = stacks
        prev_traceback_lists = traceback_lists
        prev_match_lists = match_lists

        stacks = []
        traceback_lists = []
        match_lists = []

        for i in range(len(prev_stacks)):
            stack = prev_stacks[i]
            traceback_list = prev_traceback_lists[i]
            match_list = prev_match_lists[i]
            
            # If the current backtrace is complete
            # add its data to the list of results and move on to the 
            # next backtrace
            if len(stack) == 0:
                results.append((traceback_list, match_list))
                continue
            
            i, j = stack.pop()

            # If we have found a repeat backtrace
            # simply continue to the next backtracce
            # Otherwise, record  it
            if (match_list in already_started_on[i][j]):
                continue
            else:
                already_started_on[i][j].append(match_list)

            # If the indexes are invalid, move to the next backtrace
            if i >= j:
                stacks.append(stack)
                traceback_lists.append(traceback_list)
                match_lists.append(match_list)
                continue
            
            # Now, perform the core logic of the backtracing
            if s[i + 1][j] == s[i][j]:
                stack_c = copy.deepcopy(stack)
                traceback_c = copy.deepcopy(traceback_list)
                match_list_c = copy.deepcopy(match_list)
                
                stack_c.append((i + 1, j))
                traceback_c.append((i + 1, j))

                stacks.append(stack_c)
                traceback_lists.append(traceback_c)
                match_lists.append(match_list_c)

            if s[i][j - 1] == s[i][j]:
                stack_c = copy.deepcopy(stack)
                traceback_c = copy.deepcopy(traceback_list)
                match_list_c = copy.deepcopy(match_list)

                stack_c.append((i, j - 1))
                traceback_c.append((i, j - 1))

                stacks.append(stack_c)
                traceback_lists.append(traceback_c)
                match_lists.append(match_list_c)

            if s[i + 1][j - 1] + 1 == s[i][j] and seq[i] in base_pairings[seq[j]]:
                stack_c = copy.deepcopy(stack)
                traceback_c = copy.deepcopy(traceback_list)
                match_list_c = copy.deepcopy(match_list)

                stack_c.append((i + 1, j - 1))
                traceback_c.append((i + 1, j - 1))
                match_list_c.append((i, j))
                                      
                stacks.append(stack_c)
                traceback_lists.append(traceback_c)
                match_lists.append(match_list_c)

            for k in range(i + 1, j):
                if s[i][k] + s[k + 1][j] == s[i][j]:
                    stack_c = copy.deepcopy(stack)
                    traceback_c = copy.deepcopy(traceback_list)
                    match_list_c = copy.deepcopy(match_list)

                    stack_c.append((k + 1, j))
                    stack_c.append((i, k))
                    traceback_c.append((k + 1, j))
                    traceback_c.append((i, k))

                    stacks.append(stack_c)
                    traceback_lists.append(traceback_c)
                    match_lists.append(match_list_c)
                
    return results


def get_dot_parentheses_notation(s, traceback_list):
    string = ['.'] * len(s)
    for (i, j) in traceback_list:
        string[i] = '('
        string[j] = ')'
    return ''.join(string)
    