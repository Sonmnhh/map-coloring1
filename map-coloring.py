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

# Xác định vùng và biên
regions = [f'A{i}' for i in range(1, 16)]
edges = [
    ('A1', 'A2'), ('A2', 'A3'), ('A3', 'A4'), ('A4', 'A5'),
    ('A5', 'A6'), ('A6', 'A7'), ('A7', 'A8'), ('A8', 'A9'),
    ('A9', 'A10'), ('A10', 'A11'), ('A11', 'A12'), ('A12', 'A13'),
    ('A13', 'A14'), ('A14', 'A15'), ('A15', 'A1'), ('A1', 'A5'),
    ('A5', 'A10'), ('A10', 'A15'), ('A2', 'A7'), ('A7', 'A12'),
    ('A12', 'A2'), ('A3', 'A8'), ('A8', 'A13'), ('A13', 'A3'),
    ('A4', 'A9'), ('A9', 'A14'), ('A14', 'A4'), ('A6', 'A11'),
    ('A11', 'A6')
]
colors = ['Red', 'Green', 'Blue']

# tạo map
def create_graph(regions, edges):
    G = nx.Graph()
    G.add_nodes_from(regions)
    G.add_edges_from(edges)
    return G

G = create_graph(regions, edges)
pos = nx.spring_layout(G, seed=42)


# In[13]:

# kiểm tra xem việc gán màu cụ thể cho một nút có hợp lệ hay không
def is_valid_coloring(node, color, assignment, graph):
    for neighbor in graph.neighbors(node):
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True
    
# áp dụng backtracking algorithm
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

# demo trên streamlit share
st.title('Map Coloring Problem')

# giải thích cách làm
st.markdown("""
### How to do:
1. Select a color for each region from the dropdown menus.
2. Ensure that no two adjacent regions have the same color.
3. Click "Validate Coloring" to check if your coloring is valid.
4. Click "Color the Map Automatically" to let the app color the map for you.
""")

# đầu vào
assignments = {}
cols = st.columns(4)
for idx, region in enumerate(regions):
    col = cols[idx % 4]
    with col:
        st.markdown(f"#### {region}")
        color = st.selectbox(f'Select color for {region}', ['', 'Red', 'Green', 'Blue'], key=f"selectbox_{region}")
        if color:
            assignments[region] = color

# kiểm tra màu khi được fill vào có hợp lệ không?
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

# Vẽ bản đồ
def draw_colored_map(graph, assignment):
    color_map = [assignment.get(node, '#FFFFFF') for node in graph.nodes]
    color_map = [to_hex(c) if c.startswith('#') else c for c in color_map]
    plt.figure(figsize=(10, 10))
    nx.draw(graph, pos, with_labels=True, node_color=color_map, node_size=2000, font_size=16, font_color='black')
    plt.show()

st.pyplot(draw_colored_map(G, assignments))

# giải bài toán tự động
if st.button('Color the Map Automatically'):
    result = backtracking({}, G, regions, colors)
    if result:
        assignments = result
        st.success('The map has been colored successfully.')
    else:
        st.error('Failed to color the map with the given constraints.')

# Vẽ lại bản đồ bằng cách tô màu tự động
st.pyplot(draw_colored_map(G, assignments))


# Set màu nền demo
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .block-container {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# In[ ]:




