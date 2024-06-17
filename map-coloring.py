#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex


# In[12]:


import networkx as nx
# Disable the PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Define regions and edges
regions = [f'A{i}' for i in range(1, 21)]
edges = [
    ('A1', 'A2'), ('A2', 'A3'), ('A3', 'A4'), ('A4', 'A5'), ('A5', 'A6'),
    ('A6', 'A7'), ('A7', 'A8'), ('A8', 'A9'), ('A9', 'A10'), ('A10', 'A11'),
    ('A11', 'A12'), ('A12', 'A13'), ('A13', 'A14'), ('A14', 'A15'), ('A15', 'A16'),
    ('A16', 'A17'), ('A17', 'A18'), ('A18', 'A19'), ('A19', 'A20'), ('A20', 'A1'),
    ('A1', 'A5'), ('A5', 'A10'), ('A10', 'A15'), ('A15', 'A20'), ('A2', 'A7'),
    ('A7', 'A12'), ('A12', 'A17'), ('A17', 'A2'), ('A3', 'A8'), ('A8', 'A13'),
    ('A13', 'A18'), ('A18', 'A3'), ('A4', 'A9'), ('A9', 'A14'), ('A14', 'A19'),
    ('A19', 'A4'), ('A6', 'A11'), ('A11', 'A16'), ('A16', 'A6')
]
colors = ['Red', 'Green', 'Blue']

# Create graph
def create_graph(regions, edges):
    G = nx.Graph()
    G.add_nodes_from(regions)
    G.add_edges_from(edges)
    return G

G = create_graph(regions, edges)


# In[13]:


def is_valid_coloring(node, color, assignment, graph):
    for neighbor in graph.neighbors(node):
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def backtracking(assignment, graph, regions, colors):
    if len(assignment) == len(regions):
        return assignment

    unassigned = [region for region in regions if region not in assignment]
    first = unassigned[0]

    for color in colors:
        if is_valid_coloring(first, color, assignment, graph):
            local_assignment = assignment.copy()
            local_assignment[first] = color
            result = backtracking(local_assignment, graph, regions, colors)
            if result is not None:
                return result

    return None


# In[15]:


import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex

# Streamlit app
st.title('Map Coloring Game')

# User inputs
assignments = {}
for region in regions:
    color = st.selectbox(f'Select color for {region}', ['', 'Red', 'Green', 'Blue'], key=f"selectbox_{region}")
    if color:
        assignments[region] = color

# Validate coloring
def validate_coloring():
    for region, color in assignments.items():
        if not is_valid_coloring(region, color, assignments, G):
            return False
    return True

if st.button('Validate Coloring'):
    if validate_coloring():
        st.success('Congratulations! The coloring is valid.')
    else:
        st.error('Invalid coloring! Please try again.')

# Draw the map
def draw_colored_map(graph, assignment):
    pos = nx.spring_layout(graph)
    color_map = [assignment.get(node, '#FFFFFF') for node in graph.nodes]
    color_map = [to_hex(c) if c.startswith('#') else c for c in color_map]
    nx.draw(graph, pos, with_labels=True, node_color=color_map, node_size=2000, font_size=16, font_color='black')
    plt.show()

st.pyplot(draw_colored_map(G, assignments))

if st.button('Color the Map Automatically'):
    result = backtracking({}, G, regions, colors)
    if result:
        assignments = result
        st.success('The map has been colored successfully.')
    else:
        st.error('Failed to color the map with the given constraints.')

# Draw the map again with automatic coloring
st.pyplot(draw_colored_map(G, assignments))

# In[ ]:




