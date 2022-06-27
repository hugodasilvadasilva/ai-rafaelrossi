import enum
import unittest

'''
This block of code implements a GPS to find a route between 2 cities by using Branch and Bound algorithm,
which uses only the cost (distance of each route from origin to current city) to define which route is
more promessing. 
'''

class City:
    '''
    This class implements a City which is a concrete implementation of a node (for grapho)
    or state (for search algorithm), where each City has a Id, latitude, longitude and 
    a list of neighbour cities.
    '''

    def __init__(self, id, lat: float, lon: float, neighbours: list):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.neighbours = neighbours
    
class Map(enum.Enum):
    '''
    The Map is a concrete implementation of a grapho. In this case, the Map
    has a list of City.
    GPSInformedSearch use this class to analyse routes and find path between origin
    and destination.
    '''

    Goiania = City("Goiania", -16.69, -49.25, ["Hidrolandia", "BelaVista"])
    Hidrolandia = City("Hidrolandia", -16.97, -49.22, ["Goiania", "ProfJamil", "BelaVista"])
    BelaVista = City("BelaVista", -16.97, -48.97, ["Goiania", "Hidrolandia", "Piracanjuba", "Cristianopolis"])
    ProfJamil = City("ProfJamil", -17.25, -49.25, ["Hidrolandia", "Morrinhos", "Piracanjuba"])
    Cristianopolis = City("Cristianopolis", -17.19, -48.70, ["BelaVista", "Piracanjuba", "CaldasNovas"])
    Piracanjuba = City("Piracanjuba", -17.30, -49.03, ["BelaVista", "ProfJamil", "Morrinhos", "CaldasNovas", "Cristianopolis"])
    Morrinhos = City("Morrinhos", -17.73, -49.12, ["ProfJamil", "CaldasNovas"])
    CaldasNovas = City("CaldasNovas", -17.74, 48.62, ["Cristianopolis", "Piracanjuba", "Morrinhos"])

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

        dist = ((cityA.lat - cityB.lat) ** 2 + (cityA.lon - cityB.lon)**2)**(1/2)
        return dist

class GPSBranchAndBound:
    '''
    This class implements the Branch and Bound algorithm to find the distance between two cities.
    For that you have to provide a `Map` as environment where each state is a `City`.
    '''

    def __init__(self, map: Map):
        '''
        Initialize the class by getting a `Map` as parameter.

        ## Parameters
        `- map: Map` having the list of cities where each City has a list of neighbours.
        '''
        self.__map = map
        self.__visited = []
        self.__routes = []

    def search_route(self, ori: str, dst: str) -> tuple:
        '''
        Search a route between two cities (`ori` and `dst`) returning a tuple having a list 
        of cities at position 0 and the total distance (total cost) by using this route.

        ## Parameters
        `ori: str` with origin city Id;
        `dst: str` with destination city Id
        '''

        # Add origin city to possible routes
        self.__routes.append(([ori], 0))

        while self.__routes:

            # Get next route
            curr_route = self.__routes.pop(-1)
            print(f"Analysing route {curr_route}")

            # Get last city
            curr_city = curr_route[0][-1]

            # Check if curr_city has been visited
            if curr_city in self.__visited:
                print(f"{curr_city} has already been visited")
                continue

            # Check if curr_city is destination
            if curr_city == dst:
                return curr_route
            print(f"Destination not found at route {curr_route}")

            self.__visited.append(curr_city)

            # If it's not destination, add routes for its neighbours
            neighbours_id = Map.get_neighbours(curr_city)
            print(f"Adding routes for each neighbour of {curr_city}. Neighbours = {neighbours_id}")

            # New routes
            new_routes = []
            for neighbour_id in neighbours_id:
                if neighbour_id in self.__visited:
                    print(f"{neighbour_id} will not be considered because has already been visited")
                    continue

                dist = Map.calc_cartesian_distance(curr_city, neighbour_id)
                print(f"Distance from {curr_city} to {neighbour_id} = {dist}")
                
                cost = curr_route[1] + dist

                new_route = (curr_route[0] + [neighbour_id], cost)
                print(f"New (route, dist) created = {new_route}")

                # Include new_route into new_routes list
                # new_routes list is decended sorted
                index = 0
                for r in self.__routes:

                    # new_route will be included according to its distance 
                    if new_route[1] > r[1]:
                        self.__routes.insert(index, new_route)
                        print(f"new_route {new_route} included at {index} position.")
                        print(f"Waiting list of routes now is {self.__routes}")
                        break
                    index += 1
                else:
                    self.__routes.append(new_route)

        return None


##################################
########## TEST CLASSES ##########
##################################

class Test_Map_getNeighbours(unittest.TestCase):
    def test_get_neighbours_goiania(self):
        self.assertEqual(["Hidrolandia", "BelaVista"], Map.get_neighbours("Goiania"))

    def test_get_neighbours_saopaulo(self):
        self.assertEqual([], Map.get_neighbours("SaoPaulo"))

class Test_Map_CalcCartesianDistance(unittest.TestCase):
    def test_calc_cartesian_distance_goiania_belavista(self):
        expected = ((Map.Goiania.value.lat - Map.BelaVista.value.lat)**2 + (Map.Goiania.value.lon - Map.BelaVista.value.lon)**2)**(1/2)
        result = Map.calc_cartesian_distance("Goiania", "BelaVista")
        self.assertEqual(expected, result)

if __name__ == "__main__":
    #unittest.main()

    gps = GPSBranchAndBound(Map)
    origin = Map.Goiania.value.id
    destination = Map.Cristianopolis.value.id
    r = gps.search_route(origin, destination)
    print(f"Route from {origin} to {destination} is {r}")
    