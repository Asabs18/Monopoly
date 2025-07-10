import pygame

pygame.init()

class ChanceActions:
    def __init__(self):
        self.actions = {
            0: self.advanceToGo,
            1: self.advanceToBoardwalk,
            2: self.advanceToIllinoisAve,
            3: self.advanceToStCharlesPlace,
            4: self.advanceToNearestRailroad,
            5: self.advanceToNearestUtility,
            6: self.bankDividend,
            7: self.getOutOfJailFree,
            8: self.goBack3Spaces,
            9: self.goToJail,
            10: self.makeGeneralRepairs,
            11: self.paySpeedingFine,
            12: self.goToReadingRailroad,
            13: self.chairmanOfTheBoard,
            14: self.buildingLoanMatures,
        }

    #Do action based on card id to player
    def doAction(self, players, cardId):
        currPlayer = self.getCurrPlayer(players)
        self.actions[cardId](players, currPlayer)

    def getCurrPlayer(self, players):
        for player in players:
            if player.isTurn:
                return player

    #Action Methods
    def advanceToGo(self, players, player):
        player.moveTo(40)

    def advanceToBoardwalk(self, players, player):
        player.moveTo(39)

    def advanceToIllinoisAve(self, players, player):
        player.moveTo(24)

    def advanceToStCharlesPlace(self, players, player):
        player.moveTo(11)

    def advanceToNearestRailroad(self, players, player):
        if player.location[1] < 5:
            player.moveTo(5)
        elif player.location[1] < 15:
            player.moveTo(15)
        elif player.location[1] < 25:
            player.moveTo(25)
        elif player.location[1] < 35:
            player.moveTo(35)
        else:
            player.moveTo(5)

    def advanceToNearestUtility(self, players, player):
        if player.location[1] < 12:
            player.moveTo(12)
        elif player.location[1] < 28:
            player.moveTo(28)
        else:
            player.moveTo(12)

    def goBack3Spaces(self, players, player):
        player.move(-3)

    def goToJail(self, players, player): #TODO: Verify turns go correct order when sent to jail thru chance
        player.sendToJail()

    def getOutOfJailFree(self, players, player):
        player.getOutOfJailFreeCards += 1

    def goToReadingRailroad(self, players, player):
        player.moveTo(5)

    def makeGeneralRepairs(self, players, player):
        total = 0
        total += len(player.buildings["houses"]) * 25
        total += len(player.buildings["hotels"]) * 100
        player.charge(total)

    def paySpeedingFine(self, players, player):
        player.money -= 15

    def chairmanOfTheBoard(self, players, player):
        price = (len(players) - 1) * 50
        player.charge(price)
        for person in players:
            if not person.isTurn:
                person.money += price

    def buildingLoanMatures(self, players, player):
        player.money += 150

    def bankDividend(self, players, player):
        player.money += 50




class ComChestActions:
    def __init__(self):
        self.actions = {
            0: self.advanceToGo,
            1: self.bankErrorInFavor,
            2: self.doctorFees,
            3: self.saleOfStock,
            4: self.getOutOfJailFree,
            5: self.goToJail,
            6: self.holidayFundMatures,
            7: self.incomeTaxRefund,
            8: self.itsYourBirthday,
            9: self.lifeInsuranceMatures,
            10: self.payHospitalFees,
            11: self.paySchoolFees,
            12: self.consultingFee,
            13: self.streetRepairs,
            14: self.secondPrizeBeautyContest,
            15: self.inheritance,
        }

    def doAction(self, players, cardId):
        currPlayer = self.getCurrPlayer(players)
        self.actions[cardId](players, currPlayer)

    def getCurrPlayer(self, players):
        for player in players:
            if player.isTurn:
                return player


    #Action Methods
    def advanceToGo(self, players, player):
        player.moveTo(40)

    def bankErrorInFavor(self, players, player):
        player.money += 200

    def doctorFees(self, players, player):
        player.charge(50)

    def saleOfStock(self, players, player):
        player.money += 50

    def getOutOfJailFree(self, players, player):
        player.getOutOfJailFreeCards += 1

    def goToJail(self, players, player):
        player.sendToJail()

    def holidayFundMatures(self, players, player):
        player.money += 100

    def incomeTaxRefund(self, players, player):
        player.money += 20

    def itsYourBirthday(self, players, player):
        for person in players:
            if not person.isTurn:
                person.charge(10)
        player.money += 10 * (len(players) - 1)

    def lifeInsuranceMatures(self, players, player):
        player.money += 100

    def payHospitalFees(self, players, player):
        player.charge(100)

    def paySchoolFees(self, players, player):
        player.charge(50)

    def consultingFee(self, players, player):
        player.money += 25

    def streetRepairs(self, players, player):
        total = 0
        total += len(player.buildings["houses"]) * 40
        total += len(player.buildings["hotels"]) * 115
        player.charge(total)

    def secondPrizeBeautyContest(self, players, player):
        player.money += 10

    def inheritance(self, players, player):
        player.money += 100