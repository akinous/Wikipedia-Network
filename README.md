# Wikipedia-Network
A python script that scrapes all links from a wikipedia article and creates a network out of the most similar ones.


## How it works ! 

This script uses **Spacy** library with the **Bert-Base-Uncased** model ,which is trained in english papers, to assign a similarity number among the starting article and the scraped links. Then the user decides how similar the articles must be in order to not be discarded and the script creates a dataframe of all these articles to be imported into **networkx** library. The script then draws and saves the previously created graph using the ***kamada-kawai*** algorithm and on top of that saves a *.gexf* file to be edited later using **Gephi**.




