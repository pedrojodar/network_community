import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import networkx as nx  
import sys
class Network : 
    def elements_in_commom(self, series_id_1, series_id_2):
        return set(list(set(series_id_1).intersection(set(series_id_2))))
    def __init__ (self, user):
        self.user=user
        res = open('followers.txt').read().split('\n')
        self.result=[]
        for i in range(len(res)):
            self.result.append(res[i].split('\t'))
        self.percentage=0.1
        self.Graph = self.create_Network()
    def create_Network (self):
        G=nx.Graph()
        for i in range (len(self.result)):
            for j in range (i+1, len(self.result)):
                aux = self.elements_in_commom(self.result[i], self.result[j])
                if (self.user in set (aux)):
                    if (len(aux)>2):
                        #print ((len(aux)-1)/(1.0*norm), len(aux))
                        aux_weight_i_j=(len(aux)-2)/(1.0*len(self.result[i][0])-1)
                        if (aux_weight_i_j>self.percentage):
                           G.add_edge(self.result[i][0], self.result[j][0], weight=aux_weight_i_j)
                        aux_weight_j_i=(len(aux)-2)/(1.0*len(self.result[j][0])-1)
                        if (aux_weight_j_i>self.percentage):
                            G.add_edge(self.result[j][0], self.result[i][0], weight=aux_weight_j_i)
                else:
                    if (len(aux)>1):
                        aux_weight_i_j=(len(aux)-2)/(1.0*len(self.result[i][0])-1)
                        if (aux_weight_i_j>self.percentage):
                           G.add_edge(self.result[i][0], self.result[j][0], weight=aux_weight_i_j)
                        aux_weight_j_i=(len(aux)-2)/(1.0*len(self.result[j][0])-1)
                        if (aux_weight_j_i>self.percentage):
                            G.add_edge(self.result[j][0], self.result[i][0], weight=aux_weight_j_i)
        return G
    def print_report (self):
        #c=nx.greedy_modularity_communities(G)
        print ('Number of nodes ', self.Graph.number_of_nodes())
        nx.draw(self.Graph)
        print('Number of connected components ', nx.number_connected_components(self.Graph))
        plt.show()
    def select_communities (self):
        c=list(nx.algorithms.community.greedy_modularity_communities(self.Graph))
        c_final=[]
        centrality = (nx.degree_centrality(self.Graph))
        for i in range (len(c)):
            if (len(c[i])>0.3*self.Graph.number_of_nodes()):
                G2=nx.Graph(self.Graph.subgraph(list(c[i])))
                threshold = 0.2
                # filter out all edges above threshold and grab id's
                long_edges = list(filter(lambda e: e[2] < threshold, (e for e in G2.edges.data('weight'))))
                le_ids = list(e[:2] for e in long_edges)
                # remove filtered edges from graph G
                G2.remove_edges_from(le_ids)
                c_aux=list(nx.algorithms.community.greedy_modularity_communities(G2))
                for j in range (len(c_aux)):
                    c_final.append(c_aux[j])

                #centrality.update (nx.degree_centrality(G2))
            else:
                c_final.append(c[i])
                #centrality.update (nx.degree_centrality(self.Graph, c[i]))

        return c_final, centrality
    def print_communities (self, communities):
        """
        Convert the value of the 
        """
        
        key={}
        for i in range (len(communities)):
            for j in range (len(list(communities[i]))):
                key[list(communities[i])[j]]=i
        possible_color=    ["r", "m", "b", "y", "g", "brown", "k","grey", "pink", "c", "violet"]
                
        color=[]
        nodes = list(self.Graph.nodes())
        print (len(nodes), len(key.keys()))
        for i in range (self.Graph.number_of_nodes()):
            try:
                color.append(possible_color[key[nodes[i]]-1])
            except:
                print (nodes[i])
                print (key[nodes[i]])
                sys.exit()
        G2=nx.Graph(self.Graph)
        threshold = 0.3
        # filter out all edges above threshold and grab id's
        long_edges = list(filter(lambda e: e[2] < threshold, (e for e in G2.edges.data('weight'))))
        le_ids = list(e[:2] for e in long_edges)
        # remove filtered edges from graph G
        G2.remove_edges_from(le_ids)


        
        #nx.draw(G2, node_color=color, with_labels=True)
        nx.draw(G2, node_color=color)

        plt.show()
        


n = Network('pedrojjs97')
n.print_report()
c_final, centrality = n.select_communities()


f=open('community.txt','w')
for i in range (len(c_final)):
    f.write('Community '+str(i)+'\n')
    for j in range (len(c_final[i])):
        f.write (list(c_final[i])[j])
        f.write('\n')
    f.write ('\n'+'\n'+'\n')
f.close()

f=open('Centrality.txt', 'w')
for i in list(centrality.keys()):
    f.write(str(i)+'\t'+str(centrality[i])+'\n')
f.close()
n.print_communities(c_final)