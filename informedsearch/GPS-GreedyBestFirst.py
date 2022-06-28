import enum
import unittest

'''
This block of code implements a GPS to find a route between 2 cities by using Greedy Best First algorithm,
which uses the least estimated distance to destination to choose the next node to be analysed. 
'''

class City:
    '''
    This class implements a City which is a concrete implementation of a node (for grapho)
    or state (for search algorithm), where each City has a Id, latitude, longitude and 
    a list of neighbour cities.
    '''

    def __init__(self, id, lat: float, lon: float, neighbours: list):
        self.__id = id
        self.__lat = lat
        self.__lon = lon
        self.__neighbours = neighbours

    @property
    def id(self):
        return self.__id

    @property
    def latitude(self):
        return self.__lat

    @property
    def longitude(self):
        return self.__lon

    @property
    def neighbours(self):
        return self.__neighbours

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id

    def __repr__(self) -> str:
        return self.id
    
class Map(enum.Enum):
    '''
    The Map is a concrete implementation of a grapho. In this case, the Map
    has a list of City.
    GPSGreedyBestFirst use this class to analyse routes and find path between origin
    and destination.
    '''

    Goiania = City("Goiania", -16.69, -49.25, ["Hidrolandia", "BelaVista"])
    Hidrolandia = City("Hidrolandia", -16.97, -49.22, ["Goiania", "ProfJamil", "BelaVista"])
    BelaVista = City("BelaVista", -16.97, -48.97, ["Goiania", "Hidrolandia", "Piracanjuba", "Cristianopolis"])
    ProfJamil = City("ProfJamil", -17.25, -49.25, ["Hidrolandia", "Morrinhos", "Piracanjuba"])
    Cristianopolis = City("Cristianopolis", -17.19, -48.73, ["BelaVista", "Piracanjuba", "CaldasNovas"])
    Piracanjuba = City("Piracanjuba", -17.30, -49.02, ["BelaVista", "ProfJamil", "Morrinhos", "CaldasNovas", "Cristianopolis"])
    Morrinhos = City("Morrinhos", -17.73, -49.12, ["ProfJamil", "CaldasNovas"])
    CaldasNovas = City("CaldasNovas", -17.74, -48.62, ["Cristianopolis", "Piracanjuba", "Morrinhos"])

    def get_neighbours(id: str)-> list:
        '''
        Gives a list having the name of neighbours of the city informed as parameter.

        ## Parameters
        `- id: str` having the city's id which neighbours are requested.
        `- return: list` having the neighbours's id. If city id doesn't exist return a empty list.
        '''
        for city in (Map):
            if city.value.id == id:
                return city.value.neighbours
        return []
    
    def calc_cartesian_distance(id_a: str, id_b: str):
        '''
        Calculate the cartesian distance between two cities by using their latitute
        and longitude.
        The cartesian distance is defined by calculating the square root of the sum
        of each side at power of two.

        ## Parameters
        `- id_a: str` having the Id of CityA;
        `- id_b: str` having the Id of CityB;
        `- return: float` having the cartesian distance between `id_a` and `id_b`
        '''
        cityA = Map[id_a].value
        cityB = Map[id_b].value

        dist = ((cityA.latitude - cityB.latitude) ** 2 + (cityA.longitude - cityB.longitude)**2)**(1/2)
        return dist

class Route:

    def __init__(self, cities_ids: list, cost: float, evaluation: float):
        self.__cities_ids = cities_ids
        self.__cost = cost
        self.__evaluation = evaluation

    @property
    def cities_ids(self):
        return self.__cities_ids

    @property
    def cost(self):
        return self.__cost

    @property
    def evaluation(self):
        return self.__evaluation

    @property
    def heuristic(self):
        return self.cost + self.evaluation

    @property
    def last_city_id(self):
        return self.__cities_ids[-1]

    def __repr__(self) -> str:
        return f"Route: cities Ids = {self.cities_ids}; cost = {self.cost}; evaluation = {self.evaluation}; heuristic = {self.heuristic}"

class GPSGreedyBestFirst:

    def __init__(self, map: Map):
        self.__map = map
        self.__fringe = []
        self.__visited = []

    def next_route(self) -> Route:
        '''
        Returns the next route to be analysed
        '''
        return self.__fringe.pop(-1)

    def add_route(self, route: Route):
        '''
        Add a route to fringe at a position acording to its
        heuristic
        '''
        for index, curr_route in enumerate(self.__fringe):
            if curr_route.heuristic < route.heuristic:
                self.__fringe.insert(index, route)
                print(f"{route} added into fringe at index {index}")
                print(f"New fringe is {self.__fringe}")
                break
        else:
            self.__fringe.append(route)
            print(f"{route} added into fringe at index 0")
            print(f"New fringe is {self.__fringe}")
    
    def get_neighbour_closer_to_destination(self, neighbours_ids: list, destination_id: str) -> tuple:
        '''
        Select the neighbour that has the least distance to `destination_id`;
        `- neighbours_id: list` of neighbours ids which distance to destination will be 
        calculated and the least distante will be returned;
        `- destination: str` having the id of destination city;
        `- return: tuple (str, float)` where `str` is the neighbour's id that is closer to destinatination
        and `float` is its distance.
        '''

        # loop througth neighbours id getting the one with the least 
        # distance to destination
        prev_neighbour_id = None
        prev_neighbour_distance = -1
        print(f"Selecting next city between {neighbours_ids} neighbours")

        # loop througth all neighbours and every time one has the least distance its id 
        # is stored to be returned
        for neighbour_id in neighbours_ids:

            # first check if the neighbour has already been visied
            if neighbour_id in self.__visited:
                print(f"Neighbour {neighbour_id} will not be analysed because is has already been visited")
                continue

            # if neighbour has never been visited, calculate it's distance to destination
            neighbour_distance = Map.calc_cartesian_distance(neighbour_id, destination_id)

            # if neighbour's distance to destination is the least untill now, its id is stored
            # Also check if this is the first neighbour been analysed by verifying 
            # if prev_neighbour_distance is -1
            if neighbour_distance < prev_neighbour_distance or prev_neighbour_distance == -1:
                prev_neighbour_id = neighbour_id
                prev_neighbour_distance = neighbour_distance
                print(f"For now, neighbour {neighbour_id} has been considered the closer to destination with a distance of {neighbour_distance}")

        print(f"The next city selected between all neighbours is {neighbour_id}")
        return neighbour_id, neighbour_distance

    def search(self, origin: City, destination: City) -> Route:

        print(f"Starting to search a route from {origin} to {destination}")

        # create a route from origin to destination and add to fringe
        distance_to_destination = Map.calc_cartesian_distance(origin.id, destination.id)
        ini_route = Route([origin.id], 0, distance_to_destination)

        self.add_route(ini_route)

        #start searching
        while self.__fringe:
            
            # get next route on the line/fringe
            curr_route = self.next_route()
            print(f"Analysing {curr_route}")

            # check if it is destination
            if curr_route.last_city_id == destination.id:
                print(f"Route to destination found by using {curr_route}")
                return curr_route
            
            # add last_city's route to visited cities
            self.__visited.append(curr_route.last_city_id)
            print(f"{curr_route.last_city_id} added to visited cities")

            # add route for closer neighbour to line (fringe)
            neighbours_ids = Map.get_neighbours(curr_route.last_city_id)
            next_city_id, next_city_distance_to_destination = self.get_neighbour_closer_to_destination(neighbours_ids=neighbours_ids, destination_id=destination.id)

            next_route_cities_id = curr_route.cities_ids + [next_city_id]
            next_route_cost = curr_route.cost + Map.calc_cartesian_distance(curr_route.last_city_id, next_city_id)
            next_route_evaluation = next_city_distance_to_destination

            self.add_route(Route(cities_ids=next_route_cities_id, cost=next_route_cost, evaluation=next_route_evaluation))
        
        else:
            print(f"No route found from {origin} to {destination}")
            return None

if __name__ == "__main__":

    searcher = GPSGreedyBestFirst(Map)

    print("############################ SEARCH 1")
    route = searcher.search(Map.Goiania.value, Map.Goiania.value)
    print("############################ SEARCH 2")
    route2 = searcher.search(Map.Goiania.value, Map.BelaVista.value)
    print("############################ SEARCH 3")
    route3 = searcher.search(Map.Goiania.value, Map.CaldasNovas.value)

