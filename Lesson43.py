# -*- coding: utf-8 -*-
# ToDos: leave working code. This requires rewriting to lambda-style (see lines 88-96, 41-43)
# Implement credit and bankruptcy
# Implement action-driven (total APs - 5 per day)
# + Implement carrier activity (up and down carrier ladder, getting employed and unemployed)
# Implement life-flow
#   Propose (suggested):
#   1. home,work,(club|bank|shop),home - Monday..Friday
#   2. home,(club|bank|shop),home - Saturday, Sunday

stats = {\
    "APs":5,\
    "health":100,\
    "maxhealth":100,\
    "money":100,\
    "account":0,\
    "inventory":[],\
    "work":0,\
    "credit":False,\
    "exp":0\
}
 #self.rn % 5 
dailytips = [\
    {"day":"Monday","description":"You should go to the work, or become less employed."},\
    {"day":"Tuesday","description":"You should go to the work, or become less employed."},\
    {"day":"Wensday","description":"You should go to the work, or become less employed."},\
    {"day":"Thursday","description":"You should go to the work, or become less employed."},\
    {"day":"Friday","description":"You should go to the work, AND today is FRIDAY! (!club!)"},\
    {"day":"Saturday","description":"You can go to shop,bank or club"},\
    {"day":"Sunday","description":"You can go to shop,bank or club"},\
    {"day":"Neverday","description":"Neverdreamed of this day?"},\
]

# dailywage - how much money the work gives
# exp - how much expirience the work gives
# exp_req - how much expirience required to get to next level of work

works = [
    {"description":"Unemployed","dailywage":5,"exp":1,"exp_req":5},\
    {"description":"Stager","dailywage":15,"exp":2,"exp_req":50},\
    {"description":"Clerk","dailywage":35,"exp":4,"exp_req":500},\
    {"description":"Senior","dailywage":50,"exp":8,"exp_req":5000},\
    {"description":"CEO","dailywage":125,"exp":16,"exp_req":50000},\
    {"description":"Company owner","dailywage":500,"exp":32,"exp_req":50000000000000},\
]

def apply_action(stats,action):
    for i in stats:
        if i in action: stats[i]+=action[i]

def check_stats(p):
    if p["health"]<=0:
        print "You lose your life."
        return False
    if p["money"]<0:
        print "You are bankrupt. Bank sold your whole body for organs."
        return False
    if p["health"]<p["maxhealth"]/10:
        p["maxhealth"]-=1
    if p["exp"]>= works[p["work"]]["exp_req"]:
        p["work"]+=1
    return True
    
class Room(object):
    name = "Empty room"
    actions = [{"description":"-","action":lambda p:{}}]

    def action(self,person,useraction):
        ua = useraction % len(self.actions)
        return self.actions[ua]["action"](person)

    def help(self):
        for (n,i) in zip(range(len(self.actions)),self.actions): print "%d) %s" % (n,self.actions[n]["description"])

class Work(Room):
    """Lose your health, take your payment"""
    name = "Work"
    actions = [\
        {"description":"Work my Job","action":lambda p:{"health":-7,"money":works[p["work"]]["dailywage"],"exp":works[p["work"]]["exp"]}},\
    ]

class Home(Room):
    """Home, sweet home. Rest here ."""
    name = "Home"
    actions = [\
        {"description":"Cook & Eat dinner","action":lambda p:{"health":+2}},\
        {"description":"Read","action":lambda p:{"exp":+2}},\
        {"description":"Do some physical training","action":lambda p:{"maxhealth":+2}},\
        {"description":"Watch TV","action":lambda p:{}},\
    ]

class Shop(Room):
    """The shop (now closed)"""
    name = "Shop (closed)"
    pass

class Bank(Room):
    """The Bank (now closed)"""
    name = "Bank (closed)"
    pass

class Club(Room):
    """The place to get high on mood... and low to money
    """
    name = "Club"
    
    actions=[\
    {"description":"$0 - Just go home","action":lambda p:{}},\
    {"description":"$0 - Dance","action":lambda p:{"health":2,"exp":+1}},\
    {"description":"$5 - Beer","action":lambda p:{"health":+5,"money":-5}},\
    {"description":"$15 - non-alcohol Pina Collada coctail","action":lambda p:{"health":+5,"money":-15,"maxhealth":+1}},\
    {"description":"$50 - Lapdance","action":lambda p:{"health":+35,"money":-50}},\
    {"description":"$75 - Lapdance with a hot kiss afterwhile","action":lambda p:{"health":+50,"money":-75}},\
    {"description":"$250 - Cocaine-powdered drunk-sex-party in the private room","action":lambda p:{"health":+250,"money":-250,"maxhealth":-5,"exp":+50}}\
    ]



class Game(object):
    """The game itself"""
    def __init__(self,rooms):
        self.rooms = rooms
        

    def play(self,person=stats):
        # rn - room number
        lifespan = len(self.rooms)
        rn=0
        ok=True
        while ok:
            room=self.rooms[rn % lifespan]
            day=rn/lifespan
            print "-"*78
            print "Day %d (%s): %s" % (day,dailytips[day%7]["day"],dailytips[day%7]["description"])
            print "Money: %(money)05d/%(account)06d\nHealth: %(health)s/%(maxhealth)s" % person
            print "Employment:%s (%d per day), %d exp to next level" % (works[person["work"]]["description"],works[person["work"]]["dailywage"],works[person["work"]]["exp_req"]-person["exp"])
            if not(person["inventory"]):
                for i in person["inventory"]: print i
            print room.__doc__
            room.help()
            print "Your actions (? for help, Ctrl+C to exit):",
            userinput=int(raw_input())
            
            result=room.action(person,userinput)
            apply_action(person,result)
            ok = check_stats(person)
            rn+=1

home = Home()
work = Work()
bank = Bank()
club = Club()
shop = Shop()

Clerc = Game([home,work,club])
Clerc.play(stats)

# Errors:
# 1. Having this period of non-programming was dreadful
# 2. lambdas are perfect... if your know how to cook them
# 3. variable scope. I tested it by interpreter instead of mind
# 4. 5 hours from scratch.

# Great:
# 1. lambdas. The thing I've always wanted
# 2. Modularity. Game is ready to be ported as web service. new rooms to be added easely.
# 3. Class inheritance.
