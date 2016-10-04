import csv 
import glob 
import networkx as nx




def getWebsiteLists():
    
    interactions = []
    for file in glob.glob("*.csv"): # Get all csv files in directory
        
        links = getLinks(file) # get links from file
        
        websites = []
        for link in links:
            if link.startswith('http'):
                website = getWebsite(link)
                if website != "":
                    websites.append(website)
        
        interactions.append(websites) 
        
    return interactions 

        

def getLinks(file):

    with open(file, 'r', encoding='mac_roman') as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        
        links = []
        for row in readCSV:
            if row != []:
                links.append(row[0])
                
            
        return links


badSites = ['hashtag', 'topic', 'pages', 'jack.mccarthy.509', 'privacy', 'help', 'deutschdoza', 'shares', 'search', 'ufi'] # outliers, mistakes to not be included
def getWebsite(link):
    link = link.lower()
    website = find_between(link, '://', '/')
    if website == 'www.google.com':
        return ''
    #elif website == 'www.facebook.com' or website == 'l.facebook.com':
        #website = find_between(link, '.com/', '/')
        #if website in badSites:
            #website = ''
    #else:
        
    ## FOR FACEBOOK BUT NOT GOOGLE
        #website = find_between(website, 'www.', '.com')  
        
    return website


def find_between( s, first, last):
    """From StackOverflow, http://stackoverflow.com/questions/3368969/find-string-between-two-substrings"""
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""




def createGraph(interactions):

    graph = nx.MultiGraph()
    for inter in interactions:
        interNoDup = list(set(inter)) # Remove Duplicates
        for i in range(len(interNoDup)):
            for j in range(i+1, len(interNoDup)):
                graph.add_edge(interNoDup[i], interNoDup[j], weight=1) 
                
    return graph    
    
    
    
def convertToWeightedGraph(M):
    
    G = nx.Graph()
    for u,v,data in M.edges_iter(data=True):
        w = data['weight']
        if G.has_edge(u,v):
            G[u][v]['weight'] += w
        else:
            G.add_edge(u, v, weight=w)
    
    return G
    
    

    


def main():
    g = createGraph(getWebsiteLists()) # create graph using csv files in current directory

    gw = convertToWeightedGraph(g)
    
    nx.write_gexf(gw,"GoogleKatie.gexf") # Put name of file to be created here 
    
    
main()

  