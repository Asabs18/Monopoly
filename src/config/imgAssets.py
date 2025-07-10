import pygame

from src.config.displayAssets import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



#BOARD IMAGE
board_img = pygame.image.load("Assets/images/board/board.png").convert_alpha()
board_img = pygame.transform.smoothscale(board_img.convert_alpha(), (BOARD_WIDTH, BOARD_HEIGHT))
BOARDIMG = board_img



#DIE IMAGES
sidePaths = [
            "Assets/images/dice/dice1.png",
            "Assets/images/dice/dice2.png",
            "Assets/images/dice/dice3.png",
            "Assets/images/dice/dice4.png",
            "Assets/images/dice/dice5.png",
            "Assets/images/dice/dice6.png",
        ]
    
die_images = [pygame.image.load(path).convert_alpha() for path in sidePaths]
die_images = [pygame.transform.smoothscale(image, (DICE_WIDTH, DICE_HEIGHT)) for image in die_images]

DIEIMGS = die_images



#START PIECE IMAGES

#Boat
boat_img = pygame.image.load("Assets/images/pieces/boat.png").convert_alpha()
boat_img = pygame.transform.smoothscale(boat_img.convert_alpha(), (ST_PIECE_WIDTH, ST_PIECE_HEIGHT))
STBOATIMG = boat_img

#Car
car_img = pygame.image.load("Assets/images/pieces/car.png").convert_alpha()
car_img = pygame.transform.smoothscale(car_img.convert_alpha(), (ST_PIECE_WIDTH, ST_PIECE_HEIGHT))
STCARIMG = car_img

#Hat
hat_img = pygame.image.load("Assets/images/pieces/hat.png").convert_alpha()
hat_img = pygame.transform.smoothscale(hat_img.convert_alpha(), (ST_PIECE_WIDTH, ST_PIECE_HEIGHT))
STHATIMG = hat_img

#Scope
scope_img = pygame.image.load("Assets/images/pieces/scope.png").convert_alpha()
scope_img = pygame.transform.smoothscale(scope_img.convert_alpha(), (ST_PIECE_WIDTH, ST_PIECE_HEIGHT))
STSCOPEIMG = scope_img

#Shoe
shoe_img = pygame.image.load("Assets/images/pieces/shoe.png").convert_alpha()
shoe_img = pygame.transform.smoothscale(shoe_img.convert_alpha(), (ST_PIECE_WIDTH, ST_PIECE_HEIGHT))
STSHOEIMG = shoe_img

#WheelBarrow
wheelbarrow_img = pygame.image.load("Assets/images/pieces/wheelbarrow.png").convert_alpha()
wheelbarrow_img = pygame.transform.smoothscale(wheelbarrow_img.convert_alpha(), (ST_PIECE_WIDTH, ST_PIECE_HEIGHT))
STWHEELBARROWIMG = wheelbarrow_img

#List of pieces
ST_PIECE_IMGS = [STBOATIMG, STCARIMG, STHATIMG, STSCOPEIMG, STSHOEIMG, STWHEELBARROWIMG]


#PLAY PIECE IMAGES
#Boat
boat_img = pygame.image.load("Assets/images/pieces/boat.png").convert_alpha()
boat_img = pygame.transform.smoothscale(boat_img.convert_alpha(), (PIECE_WIDTH, PIECE_HEIGHT))
BOATIMG = boat_img

#Car
car_img = pygame.image.load("Assets/images/pieces/car.png").convert_alpha()
car_img = pygame.transform.smoothscale(car_img.convert_alpha(), (PIECE_WIDTH, PIECE_HEIGHT))
CARIMG = car_img

#Hat
hat_img = pygame.image.load("Assets/images/pieces/hat.png").convert_alpha()
hat_img = pygame.transform.smoothscale(hat_img.convert_alpha(), (PIECE_WIDTH, PIECE_HEIGHT))
HATIMG = hat_img

#Scope
scope_img = pygame.image.load("Assets/images/pieces/scope.png").convert_alpha()
scope_img = pygame.transform.smoothscale(scope_img.convert_alpha(), (PIECE_WIDTH, PIECE_HEIGHT))
SCOPEIMG = scope_img

#Shoe
shoe_img = pygame.image.load("Assets/images/pieces/shoe.png").convert_alpha()
shoe_img = pygame.transform.smoothscale(shoe_img.convert_alpha(), (PIECE_WIDTH, PIECE_HEIGHT))
SHOEIMG = shoe_img

#WheelBarrow
wheelbarrow_img = pygame.image.load("Assets/images/pieces/wheelbarrow.png").convert_alpha()
wheelbarrow_img = pygame.transform.smoothscale(wheelbarrow_img.convert_alpha(), (PIECE_WIDTH, PIECE_HEIGHT))
WHEELBARROWIMG = wheelbarrow_img

#List of pieces
PIECE_IMGS = [BOATIMG, CARIMG, HATIMG, SCOPEIMG, SHOEIMG, WHEELBARROWIMG]

#Railroad card img
railroad_img = pygame.image.load("Assets/images/cards/railroad.png").convert_alpha()
railroad_img = pygame.transform.smoothscale(railroad_img.convert_alpha(), (RAIL_IMG_WIDTH, RAIL_IMG_HEIGHT))
RAILROADIMG = railroad_img

#Railroad card img (SMALL)
railroad_imgSML = pygame.image.load("Assets/images/cards/railroad.png").convert_alpha()
railroad_imgSML = pygame.transform.smoothscale(railroad_img.convert_alpha(), (RAIL_IMG_WIDTH_SML, RAIL_IMG_HEIGHT_SML))
RAILROADIMGSML = railroad_imgSML

#Util card img
electric_company_img = pygame.image.load("Assets/images/cards/electric_company.png").convert_alpha()
electric_company_img = pygame.transform.smoothscale(electric_company_img.convert_alpha(), (UTIL_IMG_WIDTH, UTIL_IMG_HEIGHT))
ELECTRICCOMPANYIMG = electric_company_img

waterworks_img = pygame.image.load("Assets/images/cards/waterworks.png").convert_alpha()
waterworks_img = pygame.transform.smoothscale(waterworks_img.convert_alpha(), (UTIL_IMG_WIDTH, UTIL_IMG_HEIGHT))
WATERWORKSIMG = waterworks_img

UTILIMGS = {
    "Electric Company": ELECTRICCOMPANYIMG,
    "Water Works": WATERWORKSIMG
}

#Util card img (SMALL)
electric_company_imgSML = pygame.image.load("Assets/images/cards/electric_company.png").convert_alpha()
electric_company_imgSML = pygame.transform.smoothscale(electric_company_img.convert_alpha(), (UTIL_IMG_WIDTH_SML, UTIL_IMG_HEIGHT_SML))
ELECTRICCOMPANYIMGSML = electric_company_imgSML

waterworks_imgSML = pygame.image.load("Assets/images/cards/waterworks.png").convert_alpha()
waterworks_imgSML = pygame.transform.smoothscale(waterworks_img.convert_alpha(), (UTIL_IMG_WIDTH_SML, UTIL_IMG_HEIGHT_SML))
WATERWORKSIMGSML = waterworks_imgSML

UTILIMGSSML = {
    "Electric Company": ELECTRICCOMPANYIMGSML,
    "Water Works": WATERWORKSIMGSML
}

#Tax card img
income_tax_img = pygame.image.load("Assets/images/cards/income_tax.png").convert_alpha()
income_tax_img = pygame.transform.smoothscale(income_tax_img.convert_alpha(), (INCOME_TAX_WIDTH, INCOME_TAX_HEIGHT))
INCOMETAXIMG = income_tax_img

luxury_tax_img = pygame.image.load("Assets/images/cards/luxury_tax.png").convert_alpha()
luxury_tax_img = pygame.transform.smoothscale(luxury_tax_img.convert_alpha(), (LUXURY_TAX_WIDTH, LUXURY_TAX_HEIGHT))
LUXURYTAXIMG = luxury_tax_img

TAXIMGS = {
    "Income Tax": INCOMETAXIMG,
    "Luxury Tax": LUXURYTAXIMG
}

#Free Parking card img
free_parking_img = pygame.image.load("Assets/images/cards/free_parking.png").convert_alpha()
free_parking_img = pygame.transform.smoothscale(free_parking_img.convert_alpha(), (FREE_PARKING_WIDTH, FREE_PARKING_HEIGHT))
FREEPARKINGIMG = free_parking_img

#Go to JJail card img
go_to_jail_img = pygame.image.load("Assets/images/cards/go_to_jail.png").convert_alpha()
go_to_jail_img = pygame.transform.smoothscale(go_to_jail_img.convert_alpha(), (GO_TO_JAIL_WIDTH, GO_TO_JAIL_HEIGHT))
GOTOJAILIMG = go_to_jail_img