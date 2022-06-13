from abc import ABC, abstractmethod
from curses.panel import new_panel

class Grapho(ABC):
    '''
    # Description 

    It's a interface that represents a general purpose grapho. This grapho will be used by Search algorithm classes.
    This interface is implemented by NoCostGrapho or CostGrapho.
    '''

    @abstractmethod
    def get_neighbours(self, node_name:str) -> list:
        '''
        # Description     
    
        Abstract method that will be used by Search classes to get the neighbours of a specific node.
        '''
        pass

class NoCostGrapho(Grapho):
    '''
    # Description 
        
    It's a concrete class that implements `Grapho` absctract
    class.
    This class implements a grapho with no cost, which means
    that each cost has a cost of 1.
    '''

    def __init__(self):
        self.__grapho = dict()

    def add_node(self, node: str, neighbours: list):
        '''
        # Description 
    
        Adds a new node to the grapho.

        ## Parameters
        `- node: str` having the name of the node;
        `- neighbours: list` of strings having the name of 
        all neighbours.
        '''
        self.__grapho[node] = neighbours
    
    def get_neighbours(self, node_name: str) -> list:
        '''
        # Description 
    
        Gives a list having the neighbours names.

        ## Parameters
        `- node_name: str` of the node.
        `- return: list` of strings where each item is a 
        neighbour.
        '''
        return self.__grapho[node_name]

class GraphoExamplesFactory:
    '''
    # Description

    This class provides examples of Graphos to be used and test
    Search Classes
    '''

    def get_eg_goias_no_cost_grapho(self):
        goias = NoCostGrapho()
        goias.add_node("Goiania", ["Hidrolandia", "BelaVista"])
        goias.add_node("Hidrolandia", ["Goiania", "ProfJamil", "BelaVista"])
        goias.add_node("BelaVista", ["Goiania", "Hidrolandia", "Piracanjuba", "Cristianopolis"])
        goias.add_node("ProfJamil", ["Hidrolandia", "Piracanjuba", "Morrinhos"])
        goias.add_node("Piracanjuba", ["ProfJamil", "BelaVista", "Cristianopolis", "CaldasNovas"])
        goias.add_node("Cristianopolis", ["BelaVista", "Piracanjuba", "CaldasNovas"])
        goias.add_node("Morrinhos", ["ProfJamil", "CaldasNovas"])
        goias.add_node("CaldasNovas", ["Morrinhos", "Piracanjuba", "Cristianopolis"])

        return goias

class BlindSearch:
    '''
    # Description

    This abstract class implement the Blind Search 
    '''

    def __init__(self, grapho: NoCostGrapho):
        self.__grapho = grapho
        self.__paths = []
        self.__visiteds = []

    def breadth_search(self, ini: str, end: str):

        # add initial state to paths
        self.__paths.append([ini])

        while self.__paths:
            # get next path to be analysed
            path = self.__paths.pop(0)

            # get last path's item
            item = path[-1]

            # check if current item is final state
            if item == end:
                return path

            # if it's not final state yet, 
            # add current item to list of visiteds
            self.__visiteds.append(item)

            # get current item's neighbours
            neighbours = self.__grapho.get_neighbours(item)

            # for each neighbour add new path into list of paths
            for neighbour in neighbours:

                # creates a new path with current neighbour
                new_path = path + [neighbour]

                # add new path to waiting list
                self.__paths.append(new_path)
        
        # if path to final state has not been found, return empty list
        return []

class BreadthSearch(BlindSearch):

    def _get_next(self) -> list:
        return super().__paths.pop(0)


if __name__ == "__main__":

    #Create grapho
    grapho = GraphoExamplesFactory().get_eg_goias_no_cost_grapho()
    blindsearch = BlindSearch(grapho)
    path = blindsearch.breadth_search("Goiania", "CaldasNovas")

    print(f"Route from Goiania to CaldasNovas is: {path}")