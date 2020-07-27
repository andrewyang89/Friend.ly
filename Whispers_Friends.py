#!/usr/bin/env python
# coding: utf-8

# In[9]:


import matplotlib.pyplot as plt
from camera import take_picture
from facenet_models import FacenetModel
from matplotlib.patches import Rectangle


import matplotlib.pyplot as plt
from camera import take_picture
from facenet_models import FacenetModel
from matplotlib.patches import Rectangle


def run_loaded_image(model, path):
    """
    Loads a picture and then processes the image using MTCNN and FaceNet
    :param model: the FaceNet model
    :param path: the path for the image file
    :return: the descriptor array, the shape of the array
    """
    pic = plt.imread(path)
    if pic.shape[-1] > 4:
        pic = pic[:, :, :3]
    boxes = show_boxes(model, pic)
    descriptors = model.compute_descriptors(pic, boxes)
    return descriptors, descriptors.shape


def run_loaded_image(model, path):
    """
    Loads a picture and then processes the image using MTCNN and FaceNet
    :param model: the FaceNet model
    :param path: the path for the image file
    :return: the descriptor array, the shape of the array
    """
    pic = plt.imread(path)
    boxes = show_boxes(model, pic)
    descriptors = model.compute_descriptors(pic, boxes)
    return descriptors, descriptors.shape


def show_boxes(model, pic):
    """
    Plots the image with the boxes applied and returns the boxes needed to compute the descriptors
    :param model: the FaceNet model
    :param pic: the picture to be processed
    :return: the boxes (detected faces)
    """
    fig, ax = plt.subplots()
    ax.imshow(pic)

    boxes, probabilities, landmarks = model.detect(pic)

    for box, prob, landmark in zip(boxes, probabilities, landmarks):
        # draw the box on the screen
        ax.add_patch(Rectangle(box[:2], *(box[2:] - box[:2]), fill=None, lw=2, color="green"))
        # Get the landmarks/parts for the face in box d.
        # Draw the face landmarks on the screen.
        for i in range(len(landmark)):
            ax.plot(landmark[i, 0], landmark[i, 1], '+', color="blue")

    plt.show()
    return boxes

def show_boxes_labels(model, pic):
    """
    Plots the image with the boxes applied and returns the boxes needed to compute the descriptors
    :param model: the FaceNet model
    :param pic: the picture to be processed
    :return: the boxes (detected faces)
    """
    fig, ax = plt.subplots()
    ax.imshow(pic)

    boxes, probabilities, landmarks = model.detect(pic)
    # labels = match(pic)

    for box, prob, landmark, label in zip(boxes, probabilities, landmarks, labels):
        # draw the box on the screen
        ax.add_patch(Rectangle(box[:2], *(box[2:] - box[:2]), fill=None, lw=2, color="green"))
        if label is None:
            ax.annotate("Unknown", box[:2], color="red")
        else:
            ax.annotate(label, box[:2], color="blue")
        # Get the landmarks/parts for the face in box d.
        # Draw the face landmarks on the screen.
        for i in range(len(landmark)):
            ax.plot(landmark[i, 0], landmark[i, 1], '+', color="blue")

    plt.show()
    return boxes


# In[10]:


import numpy as np




def cos_dist(d1, d2):
    """
    Returns the cosine distance between two description vectors.
    
    Parameters
    ----------
    d1: np.array
        First description vector
    d2: np.array
        Second description vector
        
    Returns
    -------
    cos_dist: float
        The distance between the two input vectors on range [0, 2]
    """

    M = d2.shape[0]
   #print(M)
    d2 = d2.reshape(M, 1)
    cos = d1 @ d2 / (np.linalg.norm(d1) * np.linalg.norm(d2))
    return 1 - cos


# In[11]:


class Node:
    """ Describes a node in a graph, and the edges connected
        to that node."""

    def __init__(self, ID, neighbors, descriptor, truth=None, file_path=None, Name = None):
        """ 
        Parameters
        ----------
        Name: str
            The name of the person
        
        ID : int
            A unique identifier for this node. Should be a
            value in [0, N-1], if there are N nodes in total.

        neighbors : Sequence[int]
            The node-IDs of the neighbors of this node.

        descriptor : numpy.ndarray
            The (M,) descriptor vector for this node's picture

        truth : Optional[str]
            If you have truth data, for checking your clustering algorithm,
            you can include the label to check your clusters at the end.

            If this node corresponds to a picture of Ryan, this truth
            value can just be "Ryan"

        file_path : Optional[str]
            The file path of the image corresponding to this node, so
            that you can sort the photos after you run your clustering
            algorithm
        """
        self.Name = Name
        
        self.id = ID  # a unique identified for this node - this should never change

        # The node's label is initialized with the node's ID value at first,
        # this label is then updated during the whispers algorithm
        self.label = ID

        # (n1_ID, n2_ID, ...)
        # The IDs of this nodes neighbors. Empty if no neighbors
        self.neighbors = tuple(neighbors)
        self.descriptor = descriptor

        self.truth = truth
        self.file_path = file_path


def plot_graph(graph, adj):
    """ Use the package networkx to produce a diagrammatic plot of the graph, with
    the nodes in the graph colored according to their current labels.

    Note that only 20 unique colors are available for the current color map,
    so common colors across nodes may be coincidental.

    Parameters
    ----------
    graph : Tuple[Node, ...]
        The graph to plot
    adj : numpy.ndarray, shape=(N, N)
        The adjacency-matrix for the graph. Nonzero entries indicate
        the presence of edges.

    Returns
    -------
    Tuple[matplotlib.fig.Fig, matplotlib.axis.Axes]
        The figure and axes for the plot."""
    import networkx as nx
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt

    g = nx.Graph()
    for n, node in enumerate(graph):
        g.add_node(n)

    # construct a network-x graph from the adjacency matrix: a non-zero entry at adj[i, j]
    # indicates that an egde is present between Node-i and Node-j. Because the edges are 
    # undirected, the adjacency matrix must be symmetric, thus we only look ate the triangular
    # upper-half of the entries to avoid adding redundant nodes/edges
    g.add_edges_from(zip(*np.where(np.triu(adj) > 0)))

    # we want to visualize our graph of nodes and edges; to give the graph a spatial representation,
    # we treat each node as a point in 2D space, and edges like compressed springs. We simulate
    # all of these springs decompressing (relaxing) to naturally space out the nodes of the graph
    # this will hopefully give us a sensible (x, y) for each node, so that our graph is given
    # a reasonable visual depiction 
    pos = nx.spring_layout(g)

    # make a mapping that maps: node-lab -> color, for each unique label in the graph
    color = list(iter(cm.tab20b(np.linspace(0, 1, len(set(i.label for i in graph))))))
    color_map = dict(zip(sorted(set(i.label for i in graph)), color))
    #print(color_map)
    colors = [color_map[i.label] for i in graph]  # the color for each node in the graph, according to the node's label

    # render the visualization of the graph, with the nodes colored based on their labels!
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(g, pos=pos, ax=ax, nodelist=range(len(graph)), node_color=colors)
    nx.draw_networkx_edges(g, pos, ax=ax, edgelist=g.edges())
    return fig, ax


# In[12]:


def whispers(descriptors, iterations, threshold, names = None, path_files = None):       
    """ 
        Parameters
        ----------

        descriptors : numpy.ndarray(N, M)
            The descriptor vector for each N pictures - len of M for each

        iterations : int
            The number of times the Whispers algorithm should iterate

        threshold : int
            The value at which to determine if two pictures are the same or not
            
        names: list[str] - len = N
            The names of the people
            
        path_files = list[str] - len = N
            Contains the path to the photos of the N people
            
        """
    
    N = descriptors.shape[0]
    
    adj = np.zeros((N,N))

    cos_dis = np.zeros((N,N))
    
    
    #Compute Cosine Values between all descriptor vectors
    for i in range(N):
        for j in range(N):
            if i != j:
                cos_dis[i][j] = cos_dist(descriptors[i, :], descriptors[j, :])
    
    
    
    #Compute Adj matrix
    for i in range(N):
        for j in range(N):
            adj[i][j] = 0
            if cos_dis[i][j] < threshold and i != j:
                adj[i][j] = 1 / (cos_dis[i][j] ** 2)
    
    
    
    #print histogram
    ##x = cos_dis
    #plt.hist(x, bins = 10)
    #plt.show()

    
    
    #Create all nodes along with respective neighbors
    all_nodes = np.ndarray((N,), dtype = Node )

    for i in range(N):
        neighbors = []
        ID = i
        for j in range(N):
            if adj[i][j] != 0:
                neighbors.append(j)

        if path_files == None:
            if names == None:
                all_nodes[i] = Node(ID, neighbors, descriptors[i, :])
            else:
                all_nodes[i] = Node(ID, neighbors, descriptors[i, :], Name = names[i])
        
        else:
            if names == None:
                all_nodes[i] = Node(ID, neighbors, descriptors[i, :], file_path = path_files[i])
            else:
                all_nodes[i] = Node(ID, neighbors, descriptors[i, :],file_path = path_files[i], Name = names[i])
            
    
        
    
    
    
    
    #Go through actual iterations of the Whispers Algorithm 
    for i in range(iterations):
        current_node_idx = np.random.randint(N,)

        c = current_node_idx
        dictionary = {}

        for j in range(N):


            if all_nodes[j].label in dictionary.keys():
                dictionary[all_nodes[j].label] = dictionary[all_nodes[j].label] + adj[c][j]

            else:
                dictionary[all_nodes[j].label] = adj[c][j]



        new_label = 0
        max_weight = 0

        for idx,val in dictionary.items():
            if val > max_weight:
                max_weight = val
                new_label = idx

        #print(new_label)
        all_nodes[c].label = new_label
    
    
    
    #print total number of unique people
    total = set()
    for i in range(N):
       # print(all_nodes[i].label)
        total.add(all_nodes[i].label)


    
    
    #Plot graph
    
    
    print("total number of friend groups:", len(total))  
    
    plot_graph(tuple(all_nodes), adj)
    
    sorted_nodes = sorted(all_nodes, key = lambda Node: Node.label)

    prev = sorted_nodes[0].label
    num = 1
    count = 0
    
    group_list = []
    loner = []
    
    for i in sorted_nodes:
        
        if(i.label != prev):
            if count > 1:
                print("\n")
                print("Group:", num, ",   Number of people:", count)
                
                
                for j in group_list:
                    print(j.Name)
                   # if j.file_path != None:
                        #pic = plt.imread(j.file_path)
                        #fig, ax = plt.subplots()
                        #ax.imshow(pic)
                
              
                num+=1
            else:
                loner.append(i)
            
            count = 1
            group_list = []
            group_list.append(i)
            
        else:
            group_list.append(i)
            count+=1
        
        #pic = plt.imread(i.file_path)
        #fig, ax = plt.subplots()
        #ax.imshow(pic)
        
        prev = i.label
    
    print("\n")
    print("Group:", num, ",   Number of people:", count)
    #group_list.append(sorted_nodes[len(sorted_nodes) - 1].Name)
    for j in group_list:
        print(j.Name)
        #if j.file_path != None:
            #pic = plt.imread(j.file_path)
            #fig, ax = plt.subplots()
            #ax.imshow(pic)
    
    print("\n")
    print("Loners:", len(loner))
    for j in loner:
        print(j.Name)
        #if j.file_path != None:
            #pic = plt.imread(j.file_path)
            #fig, ax = plt.subplots()
            #ax.imshow(pic)

    


# In[ ]:




