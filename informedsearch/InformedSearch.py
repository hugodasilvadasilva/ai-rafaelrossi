import enum

class City:

    def __init__(self, id, lat: float, lon: float, neighbours: list):
        self.id = id
        self.lat = lat
        self.lon = lon
    
class Map(enum.Enum):

    Goiania = City("Goiania", -16.69, -49.25, ["Hidrolandia", "BelaVista"])
    Hidrolandia = City("Hidrolandia", -16.97, -49.22, ["Goiania", "ProfJamil", "BelaVista"])
    BelaVista = City("BelaVista", -16.97, -48.97, ["Goiania", "Hidrolandia", "Piracanjuba", "Cristianopolis"])
    ProfJamil = City("ProfJamil", -17.25, -49.25, ["Hidrolandia", "Morrinhos", "Piracanjuba"])
    Cristianopolis = City("Cristianopolis", -17.19, -48.70, ["BelaVista", "Piracanjuba", "CaldasNovas"])
    Piracamjuba = City("Piracamjuba", -17.30, -49.03, ["BelaVista", "ProfJamil", "Morrinhos", "CaldasNovas", "Cristianopolis"])
    Morrinhos = City("Morrinhos", -17.73, -49.12, ["ProfJamil", "CaldasNovas"])
    CaldasNovas = City("CaldasNovas", -17.74, 48.62, ["Cristianopolis", "Piracamjuba", "Morrinhos"])

    def get_neighbours(self, id)-> list:
        return 

class GPSInformedSearch:

    def __init__(self):
        self.__visited = []
        self.__routes = []
        self.__border = []

    def search_route(self, ori: str, dst: str) -> list:

        if ori == dst:
            return ori

        self.__border.append([ori]) 
        
