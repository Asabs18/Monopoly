import pygame
from abc import ABC, abstractmethod

# Importing assets and helper classes
from Assets.numAssets.boardAssets import *
from Assets.numAssets.colorAssets import *
from Assets.numAssets.fontAssets import *
from Assets.numAssets.imgAssets import *
from Assets.uiAssets.Button import *
from Assets.uiAssets.Helper import *

from Cards import *
from Auction import *

# Initialize pygame
pygame.init()


# Abstract base class for all cells on the board
class Cell(ABC):
    def __init__(self, name, screen):
        self.screen = screen  # Pygame screen object
        self.name = name  # Name of the cell
        self.show = True  # Whether to display the cell's UI

        # Player positions on the cell (coordinates for up to 4 players)
        self.p1_pos = self.getCoords()[0]
        self.p2_pos = self.getCoords()[1]
        self.p3_pos = self.getCoords()[2]
        self.p4_pos = self.getCoords()[3]

    def __str__(self):
        return f"{self.name}: {self.show}"

    # Get coordinates for the cell from the BOARDCOORDS dictionary
    def getCoords(self):
        return BOARDCOORDS[self.name]

    # Check if the cell can be bought (default is False)
    def canBuy(self, player):
        return False

    # Abstract method to handle player landing on the cell
    @abstractmethod
    def landedOn(self, player):
        pass

    # Abstract method to display the cell's UI
    @abstractmethod
    def display(self):
        pass


# Property class inherits from Cell
class Property(Cell):
    def __init__(self, name, screen):
        super().__init__(name, screen)

        self.isOwned = False  # Whether the property is owned by a player
        self.price = PROPPRICES[self.name]  # Price of the property
        self.mortgagePrice = MORTGAGEPRICES[self.name]  # Mortgage price
        self.unmortgagePirce = UNMORTGAGEPRICES[self.name]  # Unmortgage price

        # Position and orientation of the property tag
        self.tagPos = TAGCOORDS[self.name][0]
        self.isTagHorz = TAGCOORDS[self.name][1]

        self.auction = None

        # Buttons for buying and auctioning the property
        self.buyBtn = Button(self.screen, "Buy", (BUY_BTN_X, BUY_BTN_Y, BUY_BTN_WIDTH, BUY_BTN_HEIGHT), GREEN)
        self.auctionBtn = Button(self.screen, "Auction", (AUCT_BTN_X, AUCT_BTN_Y, AUCT_BTN_WIDTH, AUCT_BTN_HEIGHT), RED)

    # Override from Cell: Check if the player can buy the property
    def canBuy(self, player):
        return not self.isOwned and player.money >= self.price

    # Handle player landing on the property
    def landedOn(self, player):
        if self.canBuy(player):
            self.buy(player)
        elif self.canCharge(player):
            self.charge(player)
        else:
            player.money = 0
            print("You're bankrupt!")  # TODO: Add handling for bankrupt

    # Buy the property
    def buy(self, player):
        self.isOwned = True
        player.money -= self.price
        player.properties.append(self)

    # Charge rent to the player
    def charge(self, player):
        player.money -= self.profitInfo[self.currProfit]

    # Check if the player can be charged rent
    def canCharge(self, player):
        return self.isOwned and player.money >= self.profitInfo[self.currProfit]

    # Handle buy button action
    def buyBtnAction(self, player):
        if self.canBuy(player):
            self.buy(player)
        self.show = False

    # Handle  auction button action
    def auctionBtnAction(self, players):
        self.show = False
        self.auction = Auction(self.screen, players, self)
        self.auction.start()

    # Abstract method to check if buildings can be built on the property
    @abstractmethod
    def canBuild(self):
        pass

    # Abstract method to get rent based on the property's level
    @abstractmethod
    def getRent(self, level):
        pass

    # Abstract method to display the property's UI
    @abstractmethod
    def display(self):
        pass


# ColorSet class inherits from Property
class ColorSet(Property):
    def __init__(self, name, screen):
        super().__init__(name, screen)

        self.color = PROPCOLORS[self.name]  # Color of the property set
        self.buildCost = BUILDINGCOSTS[self.name]  # Cost to build houses/hotels
        self.currProfit = "Base"  # Current profit level (e.g., Base, House 1, etc.)
        self.rents = RENTPRICES[self.name]  # Rent prices for different levels
        self.houseCoords = HOUSECOORDS[self.name]  # Coordinates for displaying houses

    # Check if buildings can be built on the property
    def canBuild(self):
        return self.isOwned and self.currProfit != "Hotel"

    # Get rent based on the property's level
    def getRent(self, level):
        match level:
            case "Base":
                return self.rents[0]
            case "Color Set":
                return self.rents[1]
            case "House 1":
                return self.rents[2]
            case "House 2":
                return self.rents[3]
            case "House 3":
                return self.rents[4]
            case "House 4":
                return self.rents[5]
            case "Hotel":
                return self.rents[6]

    # Display the property's UI
    def display(self):
        if self.show and not self.isOwned:
            # Draw window
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X - 10, BUY_WIN_Y - 10, BUY_WIN_WIDTH + 20, BUY_WIN_HEIGHT + 20))
            pygame.draw.rect(self.screen, BLACK, (BUY_WIN_X - 2, BUY_WIN_Y - 2, BUY_WIN_WIDTH + 4, BUY_WIN_HEIGHT + 4))
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT))

            # Draw color background
            pygame.draw.rect(self.screen, BLACK, (BUY_WIN_X + 13, BUY_WIN_Y + 13, BUY_WIN_WIDTH - 26, (BUY_WIN_HEIGHT // 5) - 26))
            pygame.draw.rect(self.screen, self.color, (BUY_WIN_X + 15, BUY_WIN_Y + 15, BUY_WIN_WIDTH - 30, (BUY_WIN_HEIGHT // 5) - 30))

            textColor = BLACK

            # Property Name
            drawText(self.screen, self.name, PROPNAMEFONT, textColor, (PROP_NAME_X, PROP_NAME_Y))

            # Name Underline
            pygame.draw.line(self.screen, textColor, NAME_LN_START, NAME_LN_END, 2)

            # Price
            drawText(self.screen, f"Price: ${self.price}", PROPTXTFONT, textColor, (BUY_PRICE_X, BUY_PRICE_Y))

            # Rent levels
            for level in PROPLEVELS.keys():
                price = self.getRent(level)
                levelData = PROPLEVELS[level]
                drawText(self.screen, f"{levelData[0]} ${price}", PROPTXTFONT, textColor, levelData[1])

            # Buttons
            self.buyBtn.draw()
            self.auctionBtn.draw()

    # Get coordinates for displaying houses/hotels
    def getHouseCoords(self):
        match self.currProfit:
            case "House 1":
                return self.houseCoords[0]
            case "House 2":
                return self.houseCoords[1]
            case "House 3":
                return self.houseCoords[2]
            case "House 4":
                return self.houseCoords[3]
            case "Hotel":
                return self.houseCoords[4]


# Railroad class inherits from Property
class Railroad(Property):
    def __init__(self, name, screen):
        super().__init__(name, screen)

        self.currProfit = "Base"  # Current profit level
        self.profitInfo = RAILROADRENT  # Rent information for railroads

    # Railroads cannot have buildings
    def canBuild(self):
        return False

    # Get rent based on the number of railroads owned
    def getRent(self, level):
        return self.profitInfo[level]

    # Display the railroad's UI
    def display(self):
        if self.show and not self.isOwned:
            # Draw window
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X - 10, BUY_WIN_Y - 10, BUY_WIN_WIDTH + 20, BUY_WIN_HEIGHT + 20))
            pygame.draw.rect(self.screen, BLACK, (BUY_WIN_X - 2, BUY_WIN_Y - 2, BUY_WIN_WIDTH + 4, BUY_WIN_HEIGHT + 4))
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT))

            textColor = BLACK

            # Property Name
            drawText(self.screen, self.name, PROPNAMEFONT, textColor, (PROP_NAME_X, PROP_NAME_Y))

            # Name Underline
            pygame.draw.line(self.screen, textColor, NAME_LN_START, NAME_LN_END, 2)

            # Image
            imgRect = RAILROADIMG.get_rect()
            imgRect.center = (RAIL_IMG_X, RAIL_IMG_Y)
            self.screen.blit(RAILROADIMG, imgRect)

            # Price
            drawText(self.screen, f"Price: ${self.price}", PROPTXTFONT, textColor, (RAIL_BUY_PRICE_X, RAIL_BUY_PRICE_Y))

            # Rent levels
            for level in RAILROADLEVELS.keys():
                price = self.getRent(level)
                levelData = RAILROADLEVELS[level]
                drawText(self.screen, f"{levelData[0]} ${price}", PROPTXTFONT, textColor, levelData[1])

            # Buttons
            self.buyBtn.draw()
            self.auctionBtn.draw()


# Utility class inherits from Property
class Utility(Property):
    def __init__(self, name, screen):
        super().__init__(name, screen)

        self.currProfit = "Base"  # Current profit level
        self.profitInfo = UTILRENT  # Rent information for utilities

    # Utilities cannot have buildings
    def canBuild(self):
        return False

    # Get rent based on the dice roll
    def getRent(self, level):
        return self.profitInfo[level]

    # Display the utility's UI
    def display(self):
        if self.show and not self.isOwned:
            # Draw window
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X - 10, BUY_WIN_Y - 10, BUY_WIN_WIDTH + 20, BUY_WIN_HEIGHT + 20))
            pygame.draw.rect(self.screen, BLACK, (BUY_WIN_X - 2, BUY_WIN_Y - 2, BUY_WIN_WIDTH + 4, BUY_WIN_HEIGHT + 4))
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT))

            textColor = BLACK

            # Property Name
            drawText(self.screen, self.name, PROPNAMEFONT, textColor, (PROP_NAME_X, PROP_NAME_Y))

            # Name Underline
            pygame.draw.line(self.screen, textColor, NAME_LN_START, NAME_LN_END, 2)

            # Image
            imgRect = UTILIMGS[self.name].get_rect()
            imgRect.center = (UTIL_IMG_X, UTIL_IMG_Y)
            self.screen.blit(UTILIMGS[self.name], imgRect)

            # Price
            drawText(self.screen, f"Price: ${self.price}", PROPTXTFONT, textColor, (RAIL_BUY_PRICE_X, RAIL_BUY_PRICE_Y))

            # Rent levels
            for level in UTILLEVELS.keys():
                price = self.getRent(level)
                levelData = UTILLEVELS[level]
                drawText(self.screen, f"{levelData[0]}", PROPTXTFONT, textColor, (levelData[2][0], levelData[2][1] - 25))
                drawText(self.screen, f"{levelData[1]}{price}", PROPTXTFONT, textColor, levelData[2])
                drawText(self.screen, "times the amount shown on the dice", PROPTXTFONT, textColor, (levelData[2][0], levelData[2][1] + 25))

            # Buttons
            self.buyBtn.draw()
            self.auctionBtn.draw()


# FreeParking class inherits from Cell
class FreeParking(Cell):
    def __init__(self, screen):
        super().__init__("Free Parking", screen)

        self.value = 0  # Amount of money in the Free Parking pot
        self.okBtn = Button(self.screen, "Ok", (OK_BTN_X, OK_BTN_Y, OK_BTN_WIDTH, OK_BTN_HEIGHT), GREEN)

    # Handle player landing on Free Parking
    def landedOn(self, player):
        self.show = True

    # Display the Free Parking UI
    def display(self):
        if self.show:
            # Draw window
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X - 10, BUY_WIN_Y - 10, BUY_WIN_WIDTH + 20, BUY_WIN_HEIGHT + 20))
            pygame.draw.rect(self.screen, BLACK, (BUY_WIN_X - 2, BUY_WIN_Y - 2, BUY_WIN_WIDTH + 4, BUY_WIN_HEIGHT + 4))
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT))

            textColor = BLACK

            # Property Name
            drawText(self.screen, self.name, PROPNAMEFONT, textColor, (PROP_NAME_X, PROP_NAME_Y))

            # Name Underline
            pygame.draw.line(self.screen, textColor, NAME_LN_START, NAME_LN_END, 2)

            # Image
            imgRect = FREEPARKINGIMG.get_rect()
            imgRect.center = (FREE_PARKING_X, FREE_PARKING_Y)
            self.screen.blit(FREEPARKINGIMG, imgRect)

            # Description
            drawText(self.screen, "Free Parking!", PROPTXTFONT, textColor, (TAX_TXT_X, TAX_TXT_Y))
            drawText(self.screen, f"${self.value}", PROPTXTFONT, textColor, (TAX_TXT_X, TAX_TXT_Y + 50))

            # Buttons
            self.okBtn.draw()

    # Pay the Free Parking amount to the player
    def pay(self, player):
        player.money += self.value
        self.value = 0

    # Deposit money into the Free Parking pot
    def deposit(self, amount):
        self.value += amount

    # Handle OK button action
    def okBtnAction(self, player):
        self.pay(player)
        self.show = False


# GoToJail class inherits from Cell
class GoToJail(Cell):
    def __init__(self, screen):
        super().__init__("Go To Jail", screen)

        self.okBtn = Button(self.screen, "Ok", (OK_BTN_X, OK_BTN_Y, OK_BTN_WIDTH, OK_BTN_HEIGHT), GREEN)

    # Handle player landing on Go To Jail
    def landedOn(self, player):
        self.show = True

    # Display the Go To Jail UI
    def display(self):
        if self.show:
            # Draw window
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X - 10, BUY_WIN_Y - 10, BUY_WIN_WIDTH + 20, BUY_WIN_HEIGHT + 20))
            pygame.draw.rect(self.screen, BLACK, (BUY_WIN_X - 2, BUY_WIN_Y - 2, BUY_WIN_WIDTH + 4, BUY_WIN_HEIGHT + 4))
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT))

            textColor = BLACK

            # Property Name
            drawText(self.screen, self.name, PROPNAMEFONT, textColor, (PROP_NAME_X, PROP_NAME_Y))

            # Name Underline
            pygame.draw.line(self.screen, textColor, NAME_LN_START, NAME_LN_END, 2)

            # Image
            imgRect = GOTOJAILIMG.get_rect()
            imgRect.center = (GO_TO_JAIL_X, GO_TO_JAIL_Y)
            self.screen.blit(GOTOJAILIMG, imgRect)

            # Description
            drawText(self.screen, "Do Not Pass Go", PROPTXTFONT, textColor, (TAX_TXT_X, TAX_TXT_Y))
            drawText(self.screen, "Do Not Collect $200", PROPTXTFONT, textColor, (TAX_TXT_X, TAX_TXT_Y + 50))

            # Buttons
            self.okBtn.draw()

    # Handle OK button action
    def okBtnAction(self, player):
        player.sendToJail()
        self.show = False


# Jail class inherits from Cell
class Jail(Cell):
    def __init__(self, screen):
        super().__init__("In Jail", screen)

        self.payBtn = Button(screen, "Pay", (JAIL_TXT_X, JAIL_TXT_Y + 150, PAY_BTN_WIDTH, PAY_BTN_HEIGHT), GREEN)

    # Handle player landing in jail
    def landedOn(self, player):
        self.show = True

    # Display the jail UI
    def display(self):
        # Draw window
        pygame.draw.rect(self.screen, WHITE, (IN_JAIL_WIN_X - 10, IN_JAIL_WIN_Y - 10, IN_JAIL_WIN_WIDTH + 20, IN_JAIL_WIN_HEIGHT + 20))
        pygame.draw.rect(self.screen, BLACK, (IN_JAIL_WIN_X - 2, IN_JAIL_WIN_Y - 2, IN_JAIL_WIN_WIDTH + 4, IN_JAIL_WIN_HEIGHT + 4))
        pygame.draw.rect(self.screen, WHITE, (IN_JAIL_WIN_X, IN_JAIL_WIN_Y, IN_JAIL_WIN_WIDTH, IN_JAIL_WIN_HEIGHT))

        textColor = BLACK

        # Property Name
        drawText(self.screen, self.name, PROPNAMEFONT, textColor, (PROP_NAME_X, PROP_NAME_Y))

        # Name Underline
        pygame.draw.line(self.screen, textColor, NAME_LN_START, NAME_LN_END, 2)

        # Description
        drawText(self.screen, "Roll a Double", PROPTXTFONT, textColor, (JAIL_TXT_X, JAIL_TXT_Y))
        drawText(self.screen, "Or Pay Bail ($50)", PROPTXTFONT, textColor, (JAIL_TXT_X, JAIL_TXT_Y + 50))

        # Buttons
        self.payBtn.draw()

    # Handle pay button action
    def payBtnAction(self, player):
        player.payBail()
        self.show = False


# Tax class inherits from Cell
class Tax(Cell):
    def __init__(self, name, screen):
        super().__init__(name, screen)

        self.price = TAXPRICES[self.name]  # Tax amount
        self.okBtn = Button(self.screen, "Ok", (OK_BTN_X, OK_BTN_Y, OK_BTN_WIDTH, OK_BTN_HEIGHT), GREEN)

    # Handle player landing on a tax space
    def landedOn(self, player):
        if self.isOwned and player.money >= self.price:
            player.money -= self.profitInfo[self.currProfit]
        else:
            player.money = 0
            print("You are bankrupt!")  # Handle Later

    # Display the tax UI
    def display(self):
        if self.show:
            # Draw window
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X - 10, BUY_WIN_Y - 10, BUY_WIN_WIDTH + 20, BUY_WIN_HEIGHT + 20))
            pygame.draw.rect(self.screen, BLACK, (BUY_WIN_X - 2, BUY_WIN_Y - 2, BUY_WIN_WIDTH + 4, BUY_WIN_HEIGHT + 4))
            pygame.draw.rect(self.screen, WHITE, (BUY_WIN_X, BUY_WIN_Y, BUY_WIN_WIDTH, BUY_WIN_HEIGHT))

            textColor = BLACK

            # Property Name
            drawText(self.screen, self.name, PROPNAMEFONT, textColor, (PROP_NAME_X, PROP_NAME_Y))

            # Name Underline
            pygame.draw.line(self.screen, textColor, NAME_LN_START, NAME_LN_END, 2)

            # Image
            imgRect = TAXIMGS[self.name].get_rect()
            imgRect.center = (INCOME_TAX_X, INCOME_TAX_Y)
            self.screen.blit(TAXIMGS[self.name], imgRect)

            # Description
            drawText(self.screen, f"pay ${self.price}", PROPTXTFONT, textColor, (TAX_TXT_X, TAX_TXT_Y))

            # Buttons
            self.okBtn.draw()

    # Charge the player the tax amount
    def charge(self, player):
        if player.money >= self.price:
            player.money -= self.price
            return self.price
        return abs(player.money - self.price)

    # Handle OK button action
    def okBtnAction(self, player):
        self.show = False
        return self.charge(player)


# Card class inherits from Cell
class Card(Cell):
    def __init__(self, name, screen):
        super().__init__(name, screen)

        self.createDeck()  # Create the card deck
        self.currCard = self.deck.deal()  # Draw the current card
        self.okBtn = Button(self.screen, "Ok", (JAIL_TXT_X, JAIL_TXT_Y + 150, PAY_BTN_WIDTH, PAY_BTN_HEIGHT), GREEN)

    # Handle player landing on a card space
    def landedOn(self, player):
        self.currCard.action(player)
        self.currCard = self.deck.deal()

    # Display the card UI
    def display(self):
        if self.show:
            # Draw window
            pygame.draw.rect(self.screen, WHITE, (IN_JAIL_WIN_X - 10, IN_JAIL_WIN_Y - 10, IN_JAIL_WIN_WIDTH + 20, IN_JAIL_WIN_HEIGHT + 20))
            pygame.draw.rect(self.screen, BLACK, (IN_JAIL_WIN_X - 2, IN_JAIL_WIN_Y - 2, IN_JAIL_WIN_WIDTH + 4, IN_JAIL_WIN_HEIGHT + 4))
            pygame.draw.rect(self.screen, WHITE, (IN_JAIL_WIN_X, IN_JAIL_WIN_Y, IN_JAIL_WIN_WIDTH, IN_JAIL_WIN_HEIGHT))

            textColor = BLACK

            # Title
            if isinstance(self.currCard, ChanceCard):
                text = "Chance"
            else:
                text = "Community Chest"
            drawText(self.screen, text, PROPNAMEFONT, textColor, (PROP_NAME_X, PROP_NAME_Y))

            # Name Underline
            pygame.draw.line(self.screen, textColor, NAME_LN_START, NAME_LN_END, 2)

            # Description
            text_y = JAIL_TXT_Y
            for line in self.currCard.description.splitlines():
                drawText(self.screen, line, PROPTXTFONT, textColor, (JAIL_TXT_X, text_y))
                text_y += 30

            # Buttons
            self.okBtn.draw()

    # Create the card deck (Chance or Community Chest)
    def createDeck(self):
        self.deck = None
        if "Chance" in self.name:
            self.deck = ChanceDeck(screen)
        elif "Community Chest" in self.name:
            self.deck = ComChestDeck(screen)

    # Handle OK button action
    def okBtnAction(self, players):
        self.currCard.action(players)
        self.show = False


# DoNothings class inherits from Cell (for spaces that do nothing)
class DoNothings(Cell):
    def __init__(self, name, screen):
        super().__init__(name, screen)
        self.show = False

    # Handle player landing on a "do nothing" space
    def landedOn(self, player):
        pass

    # Display nothing
    def display(self):
        pass


# Cells class to manage all cells on the board
class Cells:
    def __init__(self, screen):
        self.properties = self.createProperties(screen)  # Create all properties

    # Create all properties on the board
    def createProperties(self, screen):
        properties = {}
        for colorset in PROPERTIES:
            properties[colorset] = ColorSet(colorset, screen)
        for railroad in RAILROADS:
            properties[railroad] = Railroad(railroad, screen)
        for util in UTILS:
            properties[util] = Utility(util, screen)
        for tax in TAXES:
            properties[tax] = Tax(tax, screen)
        for cardSpace in CARDSPACES:
            properties[cardSpace] = Card(cardSpace, screen)
        for space in FREESPACES:
            properties[space] = DoNothings(space, screen)
        properties["Free Parking"] = FreeParking(screen)
        properties["Go To Jail"] = GoToJail(screen)
        properties["In Jail"] = Jail(screen)
        return properties

    # Print all properties (for debugging)
    def print(self):
        for prop in self.properties.keys():
            print(self.properties[prop])