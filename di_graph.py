import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import networkx as nx
import nxviz as nv

df = pd.read_csv("email_count.csv")
df = df.sort_values('Count',ascending=False)
df = df.loc[df['Count'] >= 100]
print(df.shape)

G = nx.DiGraph()

for _, row in df.iterrows():
    G.add_weighted_edges_from([(row["To"],row["From"],row["Count"])])

plt.figure(figsize=(50,50))
pos = nx.spring_layout(G,weight='Count',k=0.2)
nx.draw(G,node_color='red',with_labels=False,edge_color='blue')
plt.show()