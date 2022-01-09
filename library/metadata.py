# !!! Important: menu type change requires to 
# rewrite logic related with portions
# Source: https://likumi.lv/ta/id/245300#piel2

MENU_TYPES = [ "MainDesert", "SoupMain", "SoupDesert" ]
MENU_TYPE_PROB = [ 0.65, 0.30, 0.05 ]

# Children and family decisions
# dislike case
EAT_DECISIONS = ["NotEat", "PartiallyEat", "Eat"]

EAT_DECISION_PROB = [0.36, 0.36, 0.28]

EXTERNAL_FOOD_TYPES = ["TakeFromHome", "BuyInSchool", "BuyInShop"]
EXTERNAL_FOOD_TYPE_PROB = [ 0.2, 0.4, 0.4 ]

STOP_EAT_IF_TIME_OUT = 0.67