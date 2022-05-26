import pydealer as pd

deck = pd.Deck()

game_running = False
num_players = 0

input_num_players = int(input("Please enter number of players (>=): "))

if input_num_players >= 2:
    pass
else:
    print("please enter number >= 2: ")
    quit()

player_list = []
print()
for players in range(1, input_num_players + 1):
    player_name = input("Please enter player's names by order: ")
    player_list.append(player_name)

print("Here is the order of players: ")
print(player_list)
deck.shuffle()

game_desk = {}

for player in player_list:
    hand_cards = deck.deal(round(52 / input_num_players))
    game_desk.update({player: hand_cards})

card_pool = {}

print(game_desk)

# player's hand cards

print(game_desk[player_list[0]])
for starter in game_desk:



