'''
This block of code implements a GPS to find a route between 2 cities by using Greedy Best First algorithm,
which uses the least estimated distance to destination to choose the next node to be analysed.
At Search 4, there is a example where this algorithm fails to find a solution, as closer city to destination
has no route to there.
This problem is solved by using BestFirst.
'''

import enum
import unittest
import logging

"""
Description
---------
Set log configuration at formmat `dd/mm/aaaa hh:mn:ss am/pm message`.
The log level must be informe at `level` variable.

Levels
----------
Define log level by setting `level` variable with some of the followings
values:
- logging.DEBUG,
- logging.INFO,
- logging.WARNING,
- logging.ERROR,
- logging.CRITICAL.

"""
level = logging.INFO

logging.basicConfig(format="%(asctime)s # At %(funcName)s # Line %(lineno)d # %(message)s", level=level, datefmt='%d/%m/%Y %I:%M:%S %p')

logging.debug("Log de debug registrado")
logging.info("Log de info registrado")
logging.warning("Log de warning registrado")
logging.error("Log de error registrado")
logging.critical("Log crítico registrado")

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
    Piracanjuba = City("Piracanjuba", -17.30, -49.02, ["BelaVista", "ProfJamil", "CaldasNovas", "Cristianopolis", "Formiga"])
    Formiga = City("Formiga", -17.65, -49.08, ["Piracanjuba"])
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

    def __init__(self, cities_ids: list, cost_value: float, heuristic_value: float):
        self.__cities_ids = cities_ids
        self.__cost_value = cost_value
        self.__heuristic_value = heuristic_value

    @property
    def cities_ids(self):
        return self.__cities_ids

    @property
    def cost_value(self):
        return self.__cost_value

    @property
    def heuristic_value(self):
        return self.__heuristic_value

    @property
    def evaluation_value(self):
        return self.__cost_value + self.__heuristic_value

    @property
    def last_city_id(self):
        return self.__cities_ids[-1]

    def __repr__(self) -> str:
        return f"Route: cities Ids = {self.cities_ids}; cost = {self.cost_value}; heuristic = {self.heuristic_value}; evaluation = {self.evaluation_value}"

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
        evaluation value
        '''
        for index, curr_route in enumerate(self.__fringe):
            if curr_route.heuristic_value < route.heuristic_value:
                self.__fringe.insert(index, route)
                logging.debug(f"{route} added into fringe at index {index}")
                logging.debug(f"New fringe is {self.__fringe}")
                break
        else:
            self.__fringe.append(route)
            logging.debug(f"{route} added into fringe at index 0")
            logging.debug(f"New fringe is {self.__fringe}")
    
    def add_city_to_route(self, route: Route, city_id: str, destination: City) -> Route:
        '''
        Add `city_id` into `route`. The City will be added at the end of the route
        (will be the last city into route).
        By doing that, the cost, heuristic and evaluation route's values will be 
        changed.

        ## Parameters
        `- route: Route` which `city_id` will be added;
        `- city_id: str` having the id of the City that must be added into `route`;
        `- destination: City` having the destination (goal state) city that is been
        searched. It must be provided so heuristic value can be calculated.
        `- return: Route` having city added. It is a new instance, so a different 
        object from parameter `route`. 
        '''

        logging.debug(f"Adding {city_id} to {route}")

        cities_ids = route.cities_ids + [city_id]
        dist_route_city = Map.calc_cartesian_distance(route.last_city_id, city_id)
        dist_city_dest = Map.calc_cartesian_distance(city_id, destination.id)

        new_route = Route(cities_ids=cities_ids, cost_value=route.cost_value + dist_route_city, heuristic_value=dist_city_dest)

        logging.debug(f"City added to route. New route is {new_route}")

        return new_route

    def search(self, origin: City, destination: City) -> Route:

        logging.info(f"Starting to search a route from {origin} to {destination}")

        # create a route from origin to destination and add to fringe
        distance_to_destination = Map.calc_cartesian_distance(origin.id, destination.id)
        ini_route = Route([origin.id], 0, distance_to_destination)

        self.add_route(ini_route)

        #start searching
        while self.__fringe:
            
            # get next route on the line/fringe
            curr_route = self.next_route()
            logging.info(f"Analysing route {curr_route.cities_ids}")

            # check if it is destination
            if curr_route.last_city_id == destination.id:
                logging.info(f"Route to destination found by using {curr_route}")
                return curr_route
            
            # add last_city's route to visited cities
            self.__visited.append(curr_route.last_city_id)
            logging.debug(f"{curr_route.last_city_id} added to visited cities")

            # add routes for each neighbour
            neighbours_ids = Map.get_neighbours(curr_route.last_city_id)
            for neighbour_id in neighbours_ids:

                if neighbour_id in self.__visited:
                    logging.debug(f"{neighbour_id} will not be added to fringe as it has already been visited")
                    continue

                route = self.add_city_to_route(curr_route, neighbour_id, destination)
                self.add_route(route)
        
        else:
            logging.info(f"No route found from {origin} to {destination}")
            return None

if __name__ == "__main__":

    searcher = GPSGreedyBestFirst(Map)

    print("############################ SEARCH 1")
    #route = searcher.search(Map.Goiania.value, Map.Goiania.value)
    print("############################ SEARCH 2")
    #route2 = searcher.search(Map.Goiania.value, Map.BelaVista.value)
    print("############################ SEARCH 3")
    #route3 = searcher.search(Map.Goiania.value, Map.CaldasNovas.value)
    print("############################ SEARCH 4")
    route3 = searcher.search(Map.Piracanjuba.value, Map.Morrinhos.value)

