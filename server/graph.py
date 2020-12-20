import math

def find_pairing_indices(dot_paren_string):
    stack = []

    pairing_indices = []

    for i in range(len(dot_paren_string)):
        if dot_paren_string[i] == '(':
            stack.append(i)
        elif dot_paren_string[i] == ')':
            j = stack.pop()
            pairing_indices.append((j, i))
    
    return pairing_indices

def pairing_indices_dict(dot_paren_string):
    pairing_indices = find_pairing_indices(dot_paren_string)
    d = {}

    for (i, j) in pairing_indices:
        d[i] = j
        d[j] = i

    return d

def create_circular_graph(rna_sequence, dot_paren_string):
    pairing_indices = find_pairing_indices(dot_paren_string)

    # scale circle radius according to number of nodes
    radius = len(rna_sequence) / 10
    d_angle = (2 * math.pi) / len(rna_sequence)

    nodes = []
    edges = []
    edge_id = 0

    for i in range(len(rna_sequence)):
        node = {}
        node["x"] = radius * math.cos(i * d_angle)
        node["y"] = radius * math.sin(i * d_angle)
        node["id"] = i
        node["label"] = rna_sequence[i]
        nodes.append(node)

    for i in range(len(rna_sequence) - 1):
        edge = {}
        id_str = f"e{edge_id}"
        edge["id"] = id_str
        edge["source"] = i
        edge["target"] = i + 1
        edge["color"] = "#000000"
        edges.append(edge)
        edge_id += 1

    for (i, j) in pairing_indices:
        edge = {}
        id_str = f"e{edge_id}"
        edge["id"] = id_str
        edge["source"] = i
        edge["target"] = j
        edge["color"] = "#FF0000"
        edges.append(edge)
        edge_id += 1

    d = {
        "nodes": nodes,
        "edges": edges
    }
    return d

def create_regular_graph_rec(rna_sequence, dot_paren_string, pairing_dict, begin_idx, end_idx):
    node_positions = {}

    # first thing: split top-level parentheses and recurse
    top_level_parens = []
    recursion_indices = []
    top_level_dots = []

    i = begin_idx
    while i <= end_idx:
        if dot_paren_string[i] == '(':
            pair_idx = pairing_dict[i]
            top_level_parens.append((i, pair_idx))
            recursion_indices.append((i + 1, pair_idx - 1))

            # skip to next possible top-level parentheses location
            i = pair_idx + 1
        elif dot_paren_string[i] == '.':
            top_level_dots.append(i)
            i += 1

    # circle is formed by top level dots and top level parens
    # parens form connection points to circle
    # the inside of top-level parens is recurseively generated at rotated/connected to the connection points
    num_circle_nodes = len(top_level_dots) + len(top_level_parens) * 2
    d_angle = (2 * math.pi) / num_circle_nodes
    
    # TODO: tune this?
    radius = 1

    top_level_parens_idx = 0
    circle_idx = 0
    for top_level_dot_idx in top_level_dots:
        # if we have passed the right paren of a top-level pair, we need to add the connection points and recurse first
        if top_level_parens_idx < len(top_level_parens) and top_level_dot_idx > top_level_parens[top_level_parens_idx][1]:
            left_paren_idx = top_level_parens[top_level_parens_idx][0]
            right_paren_idx = top_level_parens[top_level_parens_idx][1]
            node_positions[left_paren_idx] = (radius * math.cos(circle_idx * d_angle), radius * math.sin(circle_idx * d_angle))
            circle_idx += 1
            node_positions[right_paren_idx] = (radius * math.cos(circle_idx * d_angle), radius * math.sin(circle_idx * d_angle))
            circle_idx += 1
            
            # recursively create branch
            if left_paren_idx + 1 <= right_paren_idx - 1:
                branch_node_positions = create_regular_graph_rec(rna_sequence, dot_paren_string, pairing_dict, left_paren_idx + 1, right_paren_idx - 1)
                
                (left_paren_x, left_paren_y) = node_positions[left_paren_idx]
                (right_paren_x, right_paren_y) = node_positions[right_paren_idx]

                (after_left_paren_x, after_left_paren_y) = branch_node_positions[left_paren_idx + 1]
                (before_right_paren_x, before_right_paren_y) = branch_node_positions[right_paren_idx - 1]

                # the angle above the x-axis for the connection points
                if left_paren_x - right_paren_x != 0:
                    connection_angle = math.atan((left_paren_y - right_paren_y) / (left_paren_x - right_paren_x))
                else:
                    connection_angle = math.pi / 2

                if after_left_paren_x - before_right_paren_x != 0:
                    next_nodes_angle = math.atan((after_left_paren_y - before_right_paren_y) / (after_left_paren_x - before_right_paren_x))
                else:
                    next_nodes_angle = math.pi / 2

                rot_angle = connection_angle - next_nodes_angle
                
                connection_length = math.sqrt((left_paren_x - right_paren_x) ** 2 + (left_paren_y - right_paren_y) ** 2)
                next_nodes_length = math.sqrt((after_left_paren_x - before_right_paren_x) ** 2 + (after_left_paren_y - before_right_paren_y) ** 2)
                scale = connection_length / next_nodes_length

                middle_direction = ((left_paren_x + right_paren_x) / 2, (left_paren_y + right_paren_y) / 2)

                # rotate and offset
                for key in branch_node_positions.keys():
                    (x, y) = branch_node_positions[key]

                    new_x = x
                    new_y = y

                    if rot_angle > math.pi:
                        new_x = -new_x

                    new_x = new_x * scale
                    new_y = new_y * scale

                    new_x = new_x * math.cos(rot_angle) - new_y * math.sin(rot_angle)
                    new_y = new_x * math.sin(rot_angle) + new_y * math.cos(rot_angle)

                    new_x += middle_direction[0] * 2
                    new_y += middle_direction[1] * 2

                    node_positions[key] = (new_x, new_y)
            
                top_level_parens_idx += 1

        # otherwise add to the circle
        node_positions[top_level_dot_idx] = (radius * math.cos(circle_idx * d_angle), radius * math.sin(circle_idx * d_angle))
        circle_idx += 1
    
    return node_positions

# def create_regular_graph(rna_sequence, dot_paren_string):
#     pairing_indices = find_pairing_indices(dot_paren_string)
#     pairing_dict = pairing_indices_dict(dot_paren_string)
#     pos = create_regular_graph_rec(rna_sequence, dot_paren_string, pairing_dict, 0, len(rna_sequence) - 1)

#     G = nx.Graph()
#     labels = {}

#     for i in range(len(rna_sequence)):
#         G.add_node(i)
#         labels[i] = rna_sequence[i]

#     edge_colors = {}
#     for i in range(len(rna_sequence) - 1):
#         G.add_edge(i, i + 1)
#         edge_colors[(i, i + 1)] = 'black'

#     for (i, j) in pairing_indices:
#         G.add_edge(i, j)
#         edge_colors[(i, j)] = 'red'

#     colors = []
#     edges = G.edges()
#     for edge in edges:
#         colors.append(edge_colors[edge])

#     nx.draw(G, pos, labels=labels, edge_color=colors)
#     plt.show()

# create_circular_graph('GGAAGGAA', '((....))')