# Wikipedia-Network
A python script that scrapes all links from a wikipedia article and creates a network out of the most similar ones.


## How it works ! 

This script uses **Spacy** library with the **Bert-Base-Uncased** model ,which is trained in english papers, to assign a similarity number among the starting article and the scraped links. Then the user decides how similar the articles must be in order to not be discarded and the script creates a dataframe of all these articles to be imported into **networkx** library. The script then draws and saves the previously created graph using the ***kamada-kawai*** algorithm and on top of that saves a *.gexf* file to be edited later using **Gephi**.


## How to use the algorithm !

Assuming you already have anaconda installed on your system (if not you can find instructions here) you have to create a new enviroment buy opening **cmd** and typing the command `conda create -n wikinet`. Then activate the enviroment `conda activate wikinet` and install the packages that you can find on **requirements.txt** . After that download the **Bert-Base-Uncased** model by using the command `python -m spacy download en_trf_bertbaseuncased_lg` and finally import the module on your **jupyter notebook** .






