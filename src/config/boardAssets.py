"""
Monopoly Game Board Assets Module

This module contains all the static data and coordinates for the Monopoly board game.
Includes property definitions, board positions, rent calculations, pricing structures,
and visual positioning data for players, houses, and property ownership tags.

Author: Aidan Sabatini
"""

from src.config.displayAssets import *
from src.config.colorAssets import *

#(In order) - goes in order from go to boardwalk 

#Track player follows around board in order, 
#after boardwalk circle back to go (Just Visiting can also be considered in jail)
TRACK = ["Go", "Mediterranean Avenue", "Community Chest 1", "Baltic Avenue", "Income Tax", "Reading Railroad", 
        "Oriental Avenue", "Chance 1", "Vermont Avenue", "Connecticut Avenue", "Just Visiting", "St. Charles Place",
        "Electric Company", "States Avenue", "Virginia Avenue", "Pennsylvania Railroad", "St. James Place", "Community Chest 2",
        "Tennessee Avenue", "New York Avenue", "Free Parking", "Kentucky Avenue", "Chance 2", "Indiana Avenue",
        "Illinois Avenue", "B. & O. Railroad", "Atlantic Avenue", "Ventnor Avenue", "Water Works", "Marvin Gardens",
        "Go To Jail", "Pacific Avenue", "North Carolina Avenue", "Community Chest 3", "Pennsylvania Avenue", "Short Line",
        "Chance 3", "Park Place", "Luxury Tax", "Boardwalk"]

#List of properties that belong to a color set (In order)
PROPERTIES = ["Mediterranean Avenue", "Baltic Avenue", "Oriental Avenue", "Vermont Avenue", 
            "Connecticut Avenue", "St. Charles Place", "States Avenue", "Virginia Avenue", 
            "St. James Place","Tennessee Avenue", "New York Avenue", "Kentucky Avenue", 
            "Indiana Avenue","Illinois Avenue", "Atlantic Avenue", "Ventnor Avenue", 
            "Marvin Gardens", "Pacific Avenue", "North Carolina Avenue", "Pennsylvania Avenue", 
            "Park Place", "Boardwalk"]

#List of all four railroad names (In order)
RAILROADS = ["Reading Railroad", "Pennsylvania Railroad", "B. & O. Railroad", "Short Line"]
    
#List of all utilities (In order)
UTILS = ["Electric Company", "Water Works"]

#List of all free spaces (In order)
FREESPACES = ["Go", "Just Visiting", "In Jail"]

#List of all tax spaces (In order)
TAXES = ["Income Tax", "Luxury Tax"]

#List of all card spaces
CARDSPACES = ["Community Chest 1", "Community Chest 2", "Community Chest 3", 
            "Chance 1", "Chance 2", "Chance 3"]

#Dictionary of both tax spaces and their costs
TAXPRICES = {
    "Income Tax": 200,
    "Luxury Tax": 100,
}

#List of coords for rent information on property buy cards 
PROPLEVELS = {
    "Base": ("Rent", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.41)), 
    "Color Set": ("Rent with Color Set", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.45)), 
    "House 1": ("Rent with 1 House(s)", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.49)), 
    "House 2": ("Rent with 2 House(s)", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.53)), 
    "House 3": ("Rent with 3 House(s)", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.57)), 
    "House 4": ("Rent with 4 House(s)", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.61)), 
    "Hotel": ("Rent with Hotel", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65)),
    }

#List of coords for rent information on railroad buy cards
RAILROADLEVELS = {
    "Base": ("Rent", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.55)),
    "Own 2": ("Rent with 1 Railroad", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.59)),
    "Own 3": ("Rent with 2 Railroads", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.63)),
    "Own 4": ("Rent with 3 Railroads", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.67)),
}

#Liist of coords for rent information on utility buy cards
UTILLEVELS = {
    "Base": ("If one Utility is owned,", "rent is ", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.56)),
    "Own 2": ("If both Utilities are", "owned, rent is ", (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.66)),
}

# SMALL VERSIONS

#List of coords for rent information on property buy cards 
PROPLEVELS_SMALL = {
    "Base": ("Rent", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.46)), 
    "Color Set": ("Rent with Color Set", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.485)), 
    "House 1": ("Rent with 1 House(s)", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.51)), 
    "House 2": ("Rent with 2 House(s)", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.535)), 
    "House 3": ("Rent with 3 House(s)", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.56)), 
    "House 4": ("Rent with 4 House(s)", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.585)), 
    "Hotel": ("Rent with Hotel", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.61)),
    }

#List of coords for rent information on railroad buy cards
RAILROADLEVELS_SMALL = {
    "Base": ("Rent", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.54)),
    "Own 2": ("Rent with 1 Railroad", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.56)),
    "Own 3": ("Rent with 2 Railroads", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.58)),
    "Own 4": ("Rent with 3 Railroads", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.6)),
}

#Liist of coords for rent information on utility buy cards
UTILLEVELS_SMALL = {
    "Base": ("If one Utility is owned,\nrent is ", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.54)),
    "Own 2 Multiplier": ("If both Utilities are\nowned, rent is ", (SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.58)),
}

#Board Coords for players, tuples with coords for (p1, p2, p3, p4)
BOARDCOORDS = {
    "Go":                       ((SCREEN_WIDTH * 0.72, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.755, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.72, SCREEN_HEIGHT * 0.88),
                                (SCREEN_WIDTH * 0.755, SCREEN_HEIGHT * 0.88)), 
    "Mediterranean Avenue":     ((SCREEN_WIDTH * 0.665, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.688, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.665, SCREEN_HEIGHT * 0.88), 
                                (SCREEN_WIDTH * 0.688, SCREEN_HEIGHT * 0.88)),
    "Community Chest 1":        ((SCREEN_WIDTH * 0.62, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.643, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.62, SCREEN_HEIGHT * 0.88), 
                                (SCREEN_WIDTH * 0.643, SCREEN_HEIGHT * 0.88)),
    "Baltic Avenue":            ((SCREEN_WIDTH * 0.575, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.595, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.575, SCREEN_HEIGHT * 0.88), 
                                (SCREEN_WIDTH * 0.595, SCREEN_HEIGHT * 0.88)),
    "Income Tax":               ((SCREEN_WIDTH * 0.527, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.548, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.527, SCREEN_HEIGHT * 0.88), 
                                (SCREEN_WIDTH * 0.548, SCREEN_HEIGHT * 0.88)),
    "Reading Railroad":         ((SCREEN_WIDTH * 0.481, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.503, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.481, SCREEN_HEIGHT * 0.88), 
                                (SCREEN_WIDTH * 0.503, SCREEN_HEIGHT * 0.88)),
    "Oriental Avenue":          ((SCREEN_WIDTH * 0.434, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.456, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.434, SCREEN_HEIGHT * 0.88), 
                                (SCREEN_WIDTH * 0.456, SCREEN_HEIGHT * 0.88)),
    "Chance 1":                 ((SCREEN_WIDTH * 0.387, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.407, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.387, SCREEN_HEIGHT * 0.88), 
                                (SCREEN_WIDTH * 0.407, SCREEN_HEIGHT * 0.88)),
    "Vermont Avenue":           ((SCREEN_WIDTH * 0.34, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.362, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.34, SCREEN_HEIGHT * 0.88), 
                                (SCREEN_WIDTH * 0.362, SCREEN_HEIGHT * 0.88)),
    "Connecticut Avenue":       ((SCREEN_WIDTH * 0.293, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.316, SCREEN_HEIGHT * 0.84), 
                                (SCREEN_WIDTH * 0.293, SCREEN_HEIGHT * 0.88), 
                                (SCREEN_WIDTH * 0.316, SCREEN_HEIGHT * 0.88)),
    "Just Visiting":            ((SCREEN_WIDTH * 0.265, SCREEN_HEIGHT * 0.898), 
                                (SCREEN_WIDTH * 0.238, SCREEN_HEIGHT * 0.898), 
                                (SCREEN_WIDTH * 0.216, SCREEN_HEIGHT * 0.865), 
                                (SCREEN_WIDTH * 0.216, SCREEN_HEIGHT * 0.83)),
    "St. Charles Place":        ((SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.75), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.75), 
                                (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.78), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.78)),
    "Electric Company":         ((SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.68), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.68), 
                                (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.71), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.71)),
    "States Avenue":            ((SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.61), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.61), 
                                (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.64), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.64)),
    "Virginia Avenue":          ((SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.54), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.54), 
                                (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.57), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.57)),
    "Pennsylvania Railroad":    ((SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.47), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.47), 
                                (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.5), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.5)),
    "St. James Place":          ((SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.4), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.4), 
                                (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.43), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.43)),
    "Community Chest 2":        ((SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.33), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.33), 
                                (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.36), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.36)),
    "Tennessee Avenue":         ((SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.26), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.26), 
                                (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.29), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.29)),
    "New York Avenue":          ((SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.19), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.19), 
                                (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.22), 
                                (SCREEN_WIDTH * 0.245, SCREEN_HEIGHT * 0.22)),
    "Free Parking":             ((SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.26, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.135), 
                                (SCREEN_WIDTH * 0.26, SCREEN_HEIGHT * 0.135)),
    "Kentucky Avenue":          ((SCREEN_WIDTH * 0.293, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.315, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.293, SCREEN_HEIGHT * 0.11), 
                                (SCREEN_WIDTH * 0.315, SCREEN_HEIGHT * 0.11)),
    "Chance 2":                 ((SCREEN_WIDTH * 0.34, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.362, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.34, SCREEN_HEIGHT * 0.11), 
                                (SCREEN_WIDTH * 0.362, SCREEN_HEIGHT * 0.11)),
    "Indiana Avenue":           ((SCREEN_WIDTH * 0.387, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.408, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.387, SCREEN_HEIGHT * 0.11), 
                                (SCREEN_WIDTH * 0.408, SCREEN_HEIGHT * 0.11)),
    "Illinois Avenue":          ((SCREEN_WIDTH * 0.434, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.456, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.434, SCREEN_HEIGHT * 0.11), 
                                (SCREEN_WIDTH * 0.456, SCREEN_HEIGHT * 0.11)),
    "B. & O. Railroad":         ((SCREEN_WIDTH * 0.481, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.503, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.481, SCREEN_HEIGHT * 0.11), 
                                (SCREEN_WIDTH * 0.503, SCREEN_HEIGHT * 0.11)),
    "Atlantic Avenue":          ((SCREEN_WIDTH * 0.527, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.549, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.527, SCREEN_HEIGHT * 0.11), 
                                (SCREEN_WIDTH * 0.549, SCREEN_HEIGHT * 0.11)),
    "Ventnor Avenue":           ((SCREEN_WIDTH * 0.574, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.596, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.574, SCREEN_HEIGHT * 0.11), 
                                (SCREEN_WIDTH * 0.596, SCREEN_HEIGHT * 0.11)),
    "Water Works":              ((SCREEN_WIDTH * 0.620, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.642, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.620, SCREEN_HEIGHT * 0.11), 
                                (SCREEN_WIDTH * 0.642, SCREEN_HEIGHT * 0.11)),
    "Marvin Gardens":           ((SCREEN_WIDTH * 0.667, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.688, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.667, SCREEN_HEIGHT * 0.11), 
                                (SCREEN_WIDTH * 0.688, SCREEN_HEIGHT * 0.11)),
    "Go To Jail":               ((SCREEN_WIDTH * 0.72, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.08), 
                                (SCREEN_WIDTH * 0.72, SCREEN_HEIGHT * 0.12), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.12)),
    "Pacific Avenue":           ((SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.19), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.19), 
                                (SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.22), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.22)),
    "North Carolina Avenue":    ((SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.26), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.26), 
                                (SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.29), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.29)),
    "Community Chest 3":        ((SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.33), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.33), 
                                (SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.36), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.36)),
    "Pennsylvania Avenue":      ((SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.4), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.4), 
                                (SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.43), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.43)),
    "Short Line":               ((SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.47), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.47), 
                                (SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.5), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.5)),
    "Chance 3":                 ((SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.54), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.54), 
                                (SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.57), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.57)),
    "Park Place":               ((SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.61), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.61), 
                                (SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.64), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.64)),
    "Luxury Tax":               ((SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.68), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.68), 
                                (SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.71), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.71)),
    "Boardwalk":                ((SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.75), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.75), 
                                (SCREEN_WIDTH * 0.732, SCREEN_HEIGHT * 0.78), 
                                (SCREEN_WIDTH * 0.76, SCREEN_HEIGHT * 0.78)),
    "In Jail":                  ((SCREEN_WIDTH * 0.24, SCREEN_HEIGHT * 0.83), 
                                (SCREEN_WIDTH * 0.268, SCREEN_HEIGHT * 0.83), 
                                (SCREEN_WIDTH * 0.24, SCREEN_HEIGHT * 0.86), 
                                (SCREEN_WIDTH * 0.268, SCREEN_HEIGHT * 0.86)),
}

HOUSECOORDS = {
    "Mediterranean Avenue":     ((SCREEN_WIDTH * 0.665, SCREEN_HEIGHT * 0.823), True),
    "Baltic Avenue":            ((SCREEN_WIDTH * 0.572, SCREEN_HEIGHT * 0.823), True),
    "Oriental Avenue":          ((SCREEN_WIDTH * 0.432, SCREEN_HEIGHT * 0.823), True),
    "Vermont Avenue":           ((SCREEN_WIDTH * 0.338, SCREEN_HEIGHT * 0.823), True),
    "Connecticut Avenue":       ((SCREEN_WIDTH * 0.292, SCREEN_HEIGHT * 0.823), True),
    "St. Charles Place":        ((SCREEN_WIDTH * 0.277, SCREEN_HEIGHT * 0.748), False),
    "States Avenue":            ((SCREEN_WIDTH * 0.277, SCREEN_HEIGHT * 0.608), False),
    "Virginia Avenue":          ((SCREEN_WIDTH * 0.277, SCREEN_HEIGHT * 0.538), False),
    "St. James Place":          ((SCREEN_WIDTH * 0.277, SCREEN_HEIGHT * 0.397), False),
    "Tennessee Avenue":         ((SCREEN_WIDTH * 0.277, SCREEN_HEIGHT * 0.257), False),
    "New York Avenue":          ((SCREEN_WIDTH * 0.277, SCREEN_HEIGHT * 0.187), False),
    "Kentucky Avenue":          ((SCREEN_WIDTH * 0.292, SCREEN_HEIGHT * 0.165), True),
    "Indiana Avenue":           ((SCREEN_WIDTH * 0.385, SCREEN_HEIGHT * 0.165), True),
    "Illinois Avenue":          ((SCREEN_WIDTH * 0.432, SCREEN_HEIGHT * 0.165), True),
    "Atlantic Avenue":          ((SCREEN_WIDTH * 0.525, SCREEN_HEIGHT * 0.165), True),
    "Ventnor Avenue":           ((SCREEN_WIDTH * 0.572, SCREEN_HEIGHT * 0.165), True),
    "Marvin Gardens":           ((SCREEN_WIDTH * 0.665, SCREEN_HEIGHT * 0.165), True),
    "Pacific Avenue":           ((SCREEN_WIDTH * 0.714, SCREEN_HEIGHT * 0.187), False),
    "North Carolina Avenue":    ((SCREEN_WIDTH * 0.714, SCREEN_HEIGHT * 0.257), False),
    "Pennsylvania Avenue":      ((SCREEN_WIDTH * 0.714, SCREEN_HEIGHT * 0.397), False),
    "Park Place":               ((SCREEN_WIDTH * 0.714, SCREEN_HEIGHT * 0.608), False),
    "Boardwalk":                ((SCREEN_WIDTH * 0.714, SCREEN_HEIGHT * 0.748), False),
}

#Dictionary of prices for all buyable properties
PROPPRICES = {
    "Mediterranean Avenue": 60,
    "Baltic Avenue": 60,
    "Oriental Avenue": 100,
    "Vermont Avenue": 100,
    "Connecticut Avenue": 120,
    "St. Charles Place": 140,
    "States Avenue": 140,
    "Virginia Avenue": 160,
    "St. James Place": 180,
    "Tennessee Avenue": 180,
    "New York Avenue": 200,
    "Kentucky Avenue": 220,
    "Indiana Avenue": 220, 
    "Illinois Avenue": 240,
    "Atlantic Avenue": 260,
    "Ventnor Avenue": 260,
    "Marvin Gardens": 280,
    "Pacific Avenue": 300,
    "North Carolina Avenue": 300,
    "Pennsylvania Avenue": 320,
    "Park Place": 350,
    "Boardwalk": 400,
    "Reading Railroad": 200,
    "Pennsylvania Railroad": 200,
    "B. & O. Railroad": 200,
    "Short Line": 200,
    "Electric Company": 150,
    "Water Works": 150,
}

#Dictionary of color set value for all properties in color sets
PROPCOLORS = {
    "Mediterranean Avenue": BROWN,
    "Baltic Avenue": BROWN,
    "Oriental Avenue": LIGHT_BLUE,
    "Vermont Avenue": LIGHT_BLUE,
    "Connecticut Avenue": LIGHT_BLUE,
    "St. Charles Place": PURPLE,
    "States Avenue": PURPLE,
    "Virginia Avenue": PURPLE,
    "St. James Place": ORANGE,
    "Tennessee Avenue": ORANGE,
    "New York Avenue": ORANGE,
    "Kentucky Avenue": RED,
    "Indiana Avenue": RED, 
    "Illinois Avenue": RED,
    "Atlantic Avenue": YELLOW,
    "Ventnor Avenue": YELLOW,
    "Marvin Gardens": YELLOW,
    "Pacific Avenue": GREEN,
    "North Carolina Avenue": GREEN,
    "Pennsylvania Avenue": GREEN,
    "Park Place": DARK_BLUE,
    "Boardwalk": DARK_BLUE,
}

#Dictionary of price player gets back for mortgaging a property
MORTGAGEPRICES = {
    "Mediterranean Avenue": 30,
    "Baltic Avenue": 30,
    "Oriental Avenue": 50,
    "Vermont Avenue": 50,
    "Connecticut Avenue": 60,
    "St. Charles Place": 70,
    "States Avenue": 70,
    "Virginia Avenue": 80,
    "St. James Place": 90,
    "Tennessee Avenue": 90,
    "New York Avenue": 100,
    "Kentucky Avenue": 110,
    "Indiana Avenue": 110, 
    "Illinois Avenue": 120,
    "Atlantic Avenue": 130,
    "Ventnor Avenue": 130,
    "Marvin Gardens": 140,
    "Pacific Avenue": 150,
    "North Carolina Avenue": 150,
    "Pennsylvania Avenue": 160,
    "Park Place": 175,
    "Boardwalk": 200,
    "Reading Railroad": 100,
    "Pennsylvania Railroad": 100,
    "B. & O. Railroad": 100,
    "Short Line": 100,
    "Electric Company": 75,
    "Water Works": 75,
}

#Dictionary of price player pays to unmortgage a property
UNMORTGAGEPRICES = {
    "Mediterranean Avenue": 33,
    "Baltic Avenue": 33,
    "Oriental Avenue": 55,
    "Vermont Avenue": 55,
    "Connecticut Avenue": 66,
    "St. Charles Place": 77,
    "States Avenue": 77,
    "Virginia Avenue": 88,
    "St. James Place": 99,
    "Tennessee Avenue": 99,
    "New York Avenue": 110,
    "Kentucky Avenue": 121,
    "Indiana Avenue": 121, 
    "Illinois Avenue": 132,
    "Atlantic Avenue": 143,
    "Ventnor Avenue": 143,
    "Marvin Gardens": 154,
    "Pacific Avenue": 165,
    "North Carolina Avenue": 165,
    "Pennsylvania Avenue": 176,
    "Park Place": 193,
    "Boardwalk": 220,
    "Reading Railroad": 110,
    "Pennsylvania Railroad": 110,
    "B. & O. Railroad": 110,
    "Short Line": 110,
    "Electric Company": 83,
    "Water Works": 83,
}

#Dictionary of all building costs for all properties in color sets 
BUILDINGCOSTS = {
    "Mediterranean Avenue": 50,
    "Baltic Avenue": 50,
    "Oriental Avenue": 50,
    "Vermont Avenue": 50,
    "Connecticut Avenue": 50,
    "St. Charles Place": 100,
    "States Avenue": 100,
    "Virginia Avenue": 100,
    "St. James Place": 100,
    "Tennessee Avenue": 100,
    "New York Avenue": 100,
    "Kentucky Avenue": 150,
    "Indiana Avenue": 150, 
    "Illinois Avenue": 150,
    "Atlantic Avenue": 150,
    "Ventnor Avenue": 150,
    "Marvin Gardens": 150,
    "Pacific Avenue": 200,
    "North Carolina Avenue": 200,
    "Pennsylvania Avenue": 200,
    "Park Place": 200,
    "Boardwalk": 200,
}


#Dictionary for all rent levels for all color set properties (Base, ColorSet, 1, 2, 3, 4, H)
RENTPRICES = {
    "Mediterranean Avenue": (2, 4, 10, 30, 90, 160, 250),
    "Baltic Avenue": (4, 8, 20, 60, 180, 320, 450),
    "Oriental Avenue": (6, 12, 30, 90, 270, 400, 550),
    "Vermont Avenue": (6, 12, 30, 90, 270, 400, 550),
    "Connecticut Avenue": (8, 16, 40, 100, 300, 450, 600),
    "St. Charles Place": (10, 20, 50, 150, 450, 625, 750),
    "States Avenue": (10, 20, 50, 150, 450, 625, 750),
    "Virginia Avenue": (12, 24, 60, 180, 500, 700, 900),
    "St. James Place": (14, 28, 70, 200, 550, 750, 950),
    "Tennessee Avenue": (14, 28, 70, 200, 550, 750, 950),
    "New York Avenue": (16, 32, 80, 220, 600, 800, 1000),
    "Kentucky Avenue": (18, 36, 90, 250, 700, 875, 1050),
    "Indiana Avenue": (18, 36, 90, 250, 700, 875, 1050), 
    "Illinois Avenue": (20, 40, 100, 300, 750, 925, 1100),
    "Atlantic Avenue": (22, 44, 110, 330, 800, 975, 1150),
    "Ventnor Avenue": (22, 44, 110, 330, 800, 975, 1150),
    "Marvin Gardens": (24, 48, 120, 360, 850, 1025, 1200),
    "Pacific Avenue": (26, 52, 130, 390, 900, 1100, 1275),
    "North Carolina Avenue":  (26, 52, 130, 390, 900, 1100, 1275),
    "Pennsylvania Avenue": (28, 56, 150, 450, 1000, 1200, 1400),
    "Park Place": (35, 70, 175, 500, 1100, 1300, 1500),
    "Boardwalk": (50, 100, 200, 600, 1400, 1700, 2000),
}

#Dictionary of all rent levels for all railroads (Base, Own 2, Own 3, Own 4)
RAILROADRENT = {
    "Base": 25,
    "Own 2": 50,
    "Own 3": 100,
    "Own 4": 200, 
}

#Dictionary of all rent levels for all utilities (Base, Own 2 Multiplier)
UTILRENT = {
    "Base": 4,
    "Own 2": 10,
}

#List of descriptions for chance deck
CHANCE_CARDS = [
    "Advance to Go (Collect $200).",
    "Advance to Boardwalk.",
    "Advance to Illinois Avenue. If you pass Go, collect $200.",
    "Advance to St. Charles Place. If you pass Go, collect $200.",
    "Advance to the nearest Railroad. \nIf unowned, you may buy it from the Bank. \nIf owned, pay the owner the entitled rent.",
    "Advance to nearest Utility. If unowned, you may buy it from \n the Bank. If owned, pay the owner the entitled rent.",
    "Bank pays you dividend of $50.",
    "Get Out of Jail Free.",
    "Go Back 3 Spaces.",
    "Go to Jail. \nGo directly to Jail, do not pass Go, do not collect $200.",
    "Make general repairs on all your property. \nFor each house pay $25. For each hotel pay $100.",
    "Speeding fine $15.",
    "Take a trip to Reading Railroad. If you pass Go, collect $200.",
    "You have been elected Chairman of the Board. \nPay each player $50.",
    "Your building and loan matures. Collect $150.",
]

COM_CHEST_CARDS = [
    "Advance to Go (Collect $200).",
    "Bank error in your favor. Collect $200.",
    "Doctor's fee. Pay $50.",
    "From sale of stock you get $50.",
    "Get Out of Jail Free.",
    "Go to Jail. \nGo directly to jail, do not pass Go, do not collect $200.",
    "Holiday fund matures. Receive $100.",
    "Income tax refund. Collect $20.",
    "It is your birthday. Collect $10 from every player.",
    "Life insurance matures. Collect $100.",
    "Pay hospital fees of $100.",
    "Pay school fees of $50.",
    "Receive $25 consultancy fee.",
    "You are assessed for street repair. \n$40 per house. $115 per hotel.",
    "You have won second prize in a beauty contest. \nCollect $10.",
    "You inherit $100.",
]

#Player property owned tag information and coordinates
TAG_Y_OFFSET = SCREEN_HEIGHT * 0.05

TAGCOORDS = {
    "Mediterranean Avenue": ((SCREEN_WIDTH * 0.6665, SCREEN_HEIGHT * 0.925), True),
    "Baltic Avenue": ((SCREEN_WIDTH * 0.5735, SCREEN_HEIGHT * 0.925), True),
    "Oriental Avenue": ((SCREEN_WIDTH * 0.4335, SCREEN_HEIGHT * 0.925), True),
    "Vermont Avenue": ((SCREEN_WIDTH * 0.3405, SCREEN_HEIGHT * 0.925), True),
    "Connecticut Avenue": ((SCREEN_WIDTH * 0.294, SCREEN_HEIGHT * 0.925), True),
    "St. Charles Place": ((SCREEN_WIDTH * 0.206, SCREEN_HEIGHT * 0.75), False),
    "States Avenue": ((SCREEN_WIDTH * 0.206, SCREEN_HEIGHT * 0.612), False),
    "Virginia Avenue": ((SCREEN_WIDTH * 0.206, SCREEN_HEIGHT * 0.542), False),
    "St. James Place": ((SCREEN_WIDTH * 0.206, SCREEN_HEIGHT * 0.402), False),
    "Tennessee Avenue": ((SCREEN_WIDTH * 0.206, SCREEN_HEIGHT * 0.262), False),
    "New York Avenue": ((SCREEN_WIDTH * 0.206, SCREEN_HEIGHT * 0.192), False),
    "Kentucky Avenue": ((SCREEN_WIDTH * 0.294, SCREEN_HEIGHT * 0.06), True),
    "Indiana Avenue": ((SCREEN_WIDTH * 0.388, SCREEN_HEIGHT * 0.06), True), 
    "Illinois Avenue": ((SCREEN_WIDTH * 0.434, SCREEN_HEIGHT * 0.06), True),
    "Atlantic Avenue": ((SCREEN_WIDTH * 0.528, SCREEN_HEIGHT * 0.06), True),
    "Ventnor Avenue": ((SCREEN_WIDTH * 0.574, SCREEN_HEIGHT * 0.06), True),
    "Marvin Gardens": ((SCREEN_WIDTH * 0.668, SCREEN_HEIGHT * 0.06), True),
    "Pacific Avenue": ((SCREEN_WIDTH * 0.783, SCREEN_HEIGHT * 0.192), False),
    "North Carolina Avenue": ((SCREEN_WIDTH * 0.783, SCREEN_HEIGHT * 0.262), False),
    "Pennsylvania Avenue": ((SCREEN_WIDTH * 0.783, SCREEN_HEIGHT * 0.402), False),
    "Park Place": ((SCREEN_WIDTH * 0.783, SCREEN_HEIGHT * 0.612), False),
    "Boardwalk": ((SCREEN_WIDTH * 0.783, SCREEN_HEIGHT * 0.752), False),
    "Reading Railroad": ((SCREEN_WIDTH * 0.481, SCREEN_HEIGHT * 0.925), True),
    "Pennsylvania Railroad": ((SCREEN_WIDTH * 0.206, SCREEN_HEIGHT * 0.472), False),
    "B. & O. Railroad": ((SCREEN_WIDTH * 0.481, SCREEN_HEIGHT * 0.06), True),
    "Short Line": ((SCREEN_WIDTH * 0.783, SCREEN_HEIGHT * 0.472), False),
    "Electric Company": ((SCREEN_WIDTH * 0.206, SCREEN_HEIGHT * 0.682), False),
    "Water Works": ((SCREEN_WIDTH * 0.621, SCREEN_HEIGHT * 0.06), True),
}