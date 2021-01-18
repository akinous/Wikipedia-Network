import wikipedia
import numpy as np 
import spacy 
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os 
import time
from IPython.display import clear_output


def clear_():
	
	time.sleep(2)

	clear_output()

	os.system('cls')

# Function that scrapes all links from an article and assigns them a simialrity value using spacy.

def similar_(article) :
	
	results = []
	similarity_list = []
	nlp = spacy.load("en_trf_bertbaseuncased_lg")
	search = wikipedia.search(str(article))

	for i in range(len(search)) :


		results.append([i,search[i]])

	print(results)

	a = int(input("If your choice is any of the above type the number before the article."))

	clear_()

	article = results[a][1]

	page = wikipedia.page(str(article))


	token = nlp(article)
	for x in page.links :

		similarity_list.append([article.capitalize(),str(x),float(token.similarity(nlp(x)))])

	return similarity_list

def similar(article) :
    
    similarity_list = []
    nlp = spacy.load("en_trf_bertbaseuncased_lg")
    search = wikipedia.page(str(article))
    token = nlp(article)
    for x in search.links :

        similarity_list.append([article.capitalize(),str(x),float(token.similarity(nlp(x)))])

    return similarity_list


# Keep the most similar articles to our first one

def processing(similarity_list,lower,upper) :
	
	similarity_list.sort(key=lambda x: x[2],reverse =True)
	
	similarity_list = [x for x in similarity_list if x[2]>float(lower) and x[2] < float(upper)]
		
   
	
	return similarity_list


# Below we go deeper into the link tree

def deep(similarity_list,range_,lower,upper) :
	
	deep_list = []
	
	for i in range(range_) :
		
		try:

			foo = similar(similarity_list[i][1])
			
			foo = processing(foo,lower,upper)
			
			deep_list.append(foo)

		except:

			continue
		
	deep_list.insert(0,similarity_list)
	
	
	return deep_list




def go_deeper(deep_list,range_,index_,lower,upper):

	new_deep_list = []
	index = index_
	old_list = deep_list
	

	

		
		
		
	for i in range(index+1,len(old_list)) :

		for j in range(range_):

			try :

				foo = similar(deep_list[i][j][1])

				foo = processing(foo,lower,upper)

				new_deep_list.append(foo)

				print("Successfully processed articles...")

				clear_()

			except :

				continue
		
		
	for i in range(len(old_list)) :

		new_deep_list.insert(i,old_list[i])
			
		
		
		
	
		
		
	index = len(old_list)
		
	print(index)

	clear_()   

	return new_deep_list,index




# This function removes the duplicates.

def fix_dups(lis) :
	
	num = 0
	res = [] 
	for i in lis: 
		
		if i not in res: 
			res.append(i)
			
		else :
			
			num += 1
			
	if len(res) == len(lis):
		
		print("The were no duplicates !")

		clear_()
		
	else :
		
		print("There were {} duplicates !".format(num))

		clear_()
			
	lis = res 
	
	return lis



# Below we create the dataframe to be used by networkx

def user_choice() :
	
	choice = input("Do you want to go deeper into the tree ?")

	clear_()

	
	if choice.capitalize() == "Yes" :
		
		return True
	
	else :
		
		return False



def create_df(x) :
	
	singles_list = []

	item_list = []
	
	for i in x :
		
		
	   

		for j in i :

			singles_list.append(j)
			
	

	for i in range(len(singles_list)):

		my_dict = {


			"From" : singles_list[i][0],

			"To" : singles_list[i][1]


		}

		item_list.append(my_dict)


	df = pd.DataFrame(item_list)
	
	return df


# This is the function to be called and it sums up the above process .

def graph_creation(article,range_,lower,upper) :
	
	
	index_ = 0
	
	
	l = similar_(article)
	
	print("Articles Fetched")

	clear_()
	
	l = processing(l,lower,upper)
	
	a = deep(l,range_,lower,upper)
	
	while user_choice() :
		
		a , index = go_deeper(a,range_,index_,lower,upper)
		
		a = fix_dups(a)
		
		index_ = index
		
	#print(len(a))
		
	df = create_df(a)
	
	G = nx.from_pandas_edgelist(df,source = "From",target = "To")
	
	return df , G


# Below we draw the network save the .png file and also the .gexf to be used by gephi.

def color_list(df,graph):
	colors = []
	for node in graph:
		if node in df["From"].values:
			colors.append("red")
		else: colors.append("green")
			
	return colors


def draw_network(df,graph,save=False,filepath = "NONE",filename = "NONE") :
	
	colors = color_list(df,graph)
	
	plt.figure(figsize=(30,30))

	nx.draw_kamada_kawai(graph,node_size=50, node_color=colors, alpha=0.3,with_labels=True,font_size=6)

	
	if save == True:
	
		nx.write_gexf(graph, r"{}\\{}.gexf".format(filepath,filename))

		plt.savefig(r"{}\\{}.png".format(filepath,filename),dpi=1000)

	plt.show()


# This is a class that processes the network and returns useful results.

class network_attributes :
	
	def __init__(self,G) :
		
		self.G = G
		
		
	
	def average_statistics(self):
		
		diameter = nx.diameter(self.G)
		radius = nx.radius(self.G)
		av_clust = nx.average_clustering(self.G)
		transit = nx.transitivity(self.G)
		node_con = nx.node_connectivity(self.G)
		edge_con = nx.edge_connectivity(self.G)
		
		print("The Diameter of the Graph is {}.".format(diameter))
		print("\n")
		print("The Radius of the Graph is {}.".format(radius))
		print("\n")
		print("The Average Clustering of The graph is {}.".format(av_clust))
		print("\n")
		print("The Transitivity of the Graph is {}.".format(transit))
		print("\n")
		print("The Node Connectivity is {}.".format(node_con))
		print("\n")
		print("The Edge Connectivity is {}.".format(edge_con))
		
	def degree_distribution(self) :
		
		deg = sorted([i for i in self.G.degree()],key= lambda x:x[1],reverse=True)
		
		return(deg)
	
	
		
	def degree_centrality(self) :

		a = np.array([i for i in nx.degree_centrality(self.G)])
		val = np.array([i for i in nx.degree_centrality(self.G).values()])
		deg_c = sorted(np.c_[a, val].tolist(),key = lambda x:x[1],reverse = True)

		return deg_c

	def closeness_centrality(self):

		a = np.array([i for i in nx.closeness_centrality(self.G)])
		val = np.array([i for i in nx.closeness_centrality(self.G).values()])
		deg_c = sorted(np.c_[a, val].tolist(),key = lambda x:x[1],reverse = True)

		return deg_c

	def betweenness_centrality(self):

		a = np.array([i for i in nx.betweenness_centrality(self.G, normalized = True,endpoints = False)])
		val = np.array([i for i in nx.betweenness_centrality(self.G, normalized = True,endpoints = False).values()])
		deg_c = sorted(np.c_[a, val].tolist(),key = lambda x:x[1],reverse = True)

		return deg_c

	def page_rank(self):

		a = np.array([i for i in nx.pagerank(self.G, alpha = 0.8)])
		val = np.array([i for i in nx.pagerank(self.G, alpha = 0.8).values()])
		deg_c = sorted(np.c_[a, val].tolist(),key = lambda x:x[1],reverse = True)

		return deg_c






def main():

	parser = argparse.ArgumentParser(description = "Create a wikipedia network")
	parser.add_argument("-a","--article",type = str,help = "The article to begin the process of build the similar links list")
	parser.add_argument("-r","--range",type = int,help = "The range of the similar links list we want to process")
	parser.add_argument("-l","--lower",type = float,help = "The lower bound of the bert model output we want to keep")
	parser.add_argument("-hi","--higher",type = float,help = "The higher bound of the bert model output we want to keep")
	parser.add_argument("-s","--save",help ="Save the output",action="store_true")
	parser.add_argument("-fp","--filepath",type = str,help = "The path of the ouput png/gfx files")
	parser.add_argument("-fn","--filename",type = str,help = "The name of the ouput png/gfx files")
	args = parser.parse_args()

	df , G = graph_creation(args.article,args.range,args.lower,args.higher)

	draw_network(df,G,args.save,args.filepath,args.filename)

	





# to run it on the command line

if __name__ == "__main__":

	main()

	