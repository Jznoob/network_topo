import json
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def json_to_topology_graph(json_data):
    G = nx.Graph()
    nodes = json_data.get('nodes', [])
    links = json_data.get('links', [])

    for node in nodes:
        G.add_node(node['id'])
    for link in links:
        G.add_edge(link['source'], link['target'])

    return G

def draw_graph_base64(G):
    plt.figure(figsize=(8,6))
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

#  示例接收的JSON数据（上传）
# json_str = '''
# {
#   "nodes": [{"id":"A"}, {"id":"B"}, {"id":"C"}, {"id":"D"}],
#   "links": [{"source":"A", "target":"B"}, {"source":"A", "target":"C"}, {"source":"B", "target":"D"}, {"source":"C", "target":"D"}]
# }
# '''

# data = json.loads(json_str)
# graph = json_to_topology_graph(data)
# img_base64 = draw_graph_base64(graph)

# img_base64 可直接发送给前端做 <img src="data:image/png;base64,{img_base64}">
