import matplotlib.pyplot as plt

def nussinov(rna_sequence, base_pairings):
    n = len(rna_sequence)

    s = [[0] * n for x in range(n)]

    for i in range(n - 1, -1, -1):
        for j in range(n):

            vi = rna_sequence[i]
            vj = rna_sequence[j]

            if i >= j:
                0
            else:
                max_lst = []

                if (vj in base_pairings[vi]):
                    max_lst.append(s[i + 1][j - 1] + 1)
                else:
                    max_lst.append(s[i + 1][j - 1])

                max_lst.append(s[i + 1][j])
                max_lst.append(s[i][j - 1])

                max_skip = max([s[i][k] + s[k + 1][j] for k in range(i + 1, j)], default=0)
                max_lst.append(max_skip)

                s[i][j] = max(max_lst)

    return s

def traceback(s):
    stack = []
    traceback_list = []

    stack.append((0, len(s) - 1))
    traceback_list.append((0, len(s) - 1))

    while len(stack) != 0:
        i, j = stack.pop()
        if i >= j:
            continue
        elif s[i + 1][j] == s[i][j]:
            stack.append((i + 1, j))
        elif s[i][j - 1] == s[i][j]:
            stack.append((i, j - 1))
        elif s[i + 1][j - 1] + 1 == s[i][j]:
            traceback_list.append((i, j))
            stack.append((i + 1, j - 1))
        else:
            for k in range(i + 1, j):
                if s[i][k] + s[k + 1][j] == s[i][j]:
                    stack.append((k + 1, j))
                    stack.append((i, k))
                    break

    return traceback_list

def generate_visualization(s, traceback_list, rna_sequence):
    columns = tuple(rna_sequence)
    rows = list(rna_sequence)

    colors = []
    for i in range(len(rna_sequence)):
        colors.append((["w"] * len(rna_sequence)))
    
    # Now, set the cells that should be colored as green
    for (r, c) in traceback_list:
        colors[r][c] = "#42f55d"

    _, ax = plt.subplots()
    ax.table(loc='center', cellColours=colors, colLabels=columns, rowLabels=rows, cellText=s)
    ax.axis('tight')
    ax.axis('off')
    plt.show()

if __name__ == "__main__":
    base_pairings = {
        'G' : ['C'],
        'C' : ['G'],
        'A' : ['U'],
        'U' : ['A']
    }

    seq = 'GCACGACG'
    table = nussinov(seq, base_pairings)
    traceback_list = traceback(table)
    generate_visualization(table, traceback_list, seq)
