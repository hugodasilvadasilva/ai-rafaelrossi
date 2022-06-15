from dis import dis
import enum
import unittest

class City:

    def __init__(self, id, lat: float, lon: float, neighbours: list):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.neighbours = neighbours
    
class Map(enum.Enum):

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
        cityA = Map[id_a].value
        cityB = Map[id_b].value

        dist = ((cityA.lat - cityB.lat) ** 2 + (cityA.lon - cityB.lon)**2)**(1/2)
        return dist

class GPSInformedSearch:

    def __init__(self, map: Map):
        self.__map = map
        self.__visited = []
        self.__routes = []

    def search_route(self, ori: str, dst: str) -> list:

        # Add origin city to possible routes
        self.__routes.append([ori])

        while self.__routes:

            # Get next route
            curr_route = self.__routes.pop(-1)
            print(f"Analyse route {curr_route}")

            # Get last city
            curr_city = curr_route[-1]

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

                dist = Map.calc_cartesian_distance(ori, neighbour_id)
                print(f"Distance from {ori} to {neighbour_id} = {dist}")

                route = (neighbour_id, dist)

                new_routes.append(route)

            # Order new routes
            sorted(new_routes, key=lambda r: r[1], reverse=True)
            print(f"New routes sorted: {new_routes}")

            # Add new routes to line of routes to be analysed
            for new_route in new_routes:
                self.__routes.append(curr_route + [new_route[0]])
            
            print(f"New routes added to line of routes to be analysed: {self.__routes}")

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

    gps = GPSInformedSearch(Map)
    origin = Map.Goiania.value.id
    destination = Map.CaldasNovas.value.id
    r = gps.search_route(origin, destination)
    print(f"Route from {origin} to {destination} is {r}")