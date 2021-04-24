import random

class Fighter(object):
    def __init__(self, name, atk, atkMod, magicDmg, magicMtplr, armorClass, hp, initMagicCharge):
        self.name = name 
        self.atk = atk
        self.atkMod = atkMod
        self.magicDmg = magicDmg
        self.magicMtplr = magicMtplr
        self.armorClass = armorClass
        self.hp = hp

        self.inCombat = 0
        self.isAlive = 1
        self.initMagicCharge = initMagicCharge
        self.magicCharge = initMagicCharge
    
    def getName(self):
        return self.name
    
    def getAtk(self):
        return self.atk

    def getAtkMod(self):
        return self.atkMod
    
    def getArmor(self):
        return self.armorClass
    
    def getHp(self):
        return self.hp
    
    def getMagicDmg(self):
        return self.magicDmg

    def getStats(self):
        return ('name: ' + self.name 
                + '\natk: ' + str(self.atk)
                + '\natk modifier: ' + str(self.atkMod)
                + '\nmagic atk: ' + str(self.magicDmg)
                + '\nmana blast atk: ' + str(self.magicMtplr * self.magicDmg)
                + '\narmor class: ' + str(self.armorClass)
                + '\nhp: ' + str(self.hp)
                + '\ncharge time for mana blast: ' + str(self.initMagicCharge)
                + '\nturns until mana blast: ' + str(self.magicCharge) 
                + '\nalive: ' + str(bool(self.isAlive))
)

    def getAlive(self):
        return self.isAlive

    def getCharged(self):
        return self.magicCharge
    
    def getCombat(self):
        return self.inCombat


    def setName(self, n):
        self.name = n

    def setCombat(self, i):
        self.inCombat = i

    def setStats(self, name, atk, atkMod, magicDmg, magicMtplr, armorClass, hp, initMagicCharge):
        self.name = name 
        self.atk = atk
        self.atkMod = atkMod
        self.magicDmg = magicDmg
        self.magicMtplr = magicMtplr
        self.armorClass = armorClass
        self.hp = hp
        self.magicCharge = initMagicCharge
        self.initMagicCharge = initMagicCharge

        self.inCombat = 0
        self.isAlive = 1
    
    
    def attack(self, opponent, bonus):
        if self.isAlive == 0:
            return self.name + ' is dead and cannot attack.'
        yourAttack = random.randint(1, 21) + self.atkMod + bonus
        if yourAttack >= opponent.getArmor():
            oppDamage = opponent.takeDamage(self.atk)
            return self.name + ' hit ' + opponent.getName() + ' for ' + str(self.atk) + ' damage. \n' + str(oppDamage)
        else:
            return self.name + ': attack on ' + opponent.getName() + ' missed'
        
    
    def magic(self, opponent, bonus):
        if self.isAlive == 0:
            return self.name + ' is dead and cannot do magic.'
        yourAttack = random.randint(1, 21) + self.atkMod + bonus
        if yourAttack >= opponent.getArmor():
            oppDamage = opponent.takeDamage(self.magicDmg)
            if self.magicCharge > 0:
                self.magicCharge -=1
            return self.name + ' hit ' + opponent.getName() + ' for ' + str(self.magicDmg) + ' magic damage. \n' + str(oppDamage)
        else:
            return self.name + ': attack on ' + opponent.getName() + ' missed'

    def manaBlast(self, opponent):
        if self.isAlive == 0:
            return self.name + 'is dead and cannot do magic'
        oppDamage = opponent.takeDamage(self.magicDmg * self.magicMtplr)
        self.magicCharge = self.initMagicCharge
        return self.name + ' hit ' + opponent.getName() + ' with mana blast for ' + str(self.magicDmg * self.magicMtplr) + ' magic damage. \n' + str(oppDamage)

    
    def takeDamage(self, dmg):
        self.hp = self.hp - dmg
        if self.hp <= 0:
            self.isAlive = 0
            return self.name + ' has died.'
        return self.name + ' takes ' + str(dmg) + ' damage.'







