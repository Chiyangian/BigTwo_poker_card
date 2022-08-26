import pydealer
from collections import deque
import json

NEW_RANKS = {
    "values": {
        "2": 13,
        "Ace": 12,
        "King": 11,
        "Queen": 10,
        "Jack": 9,
        "10": 8,
        "9": 7,
        "8": 6,
        "7": 5,
        "6": 4,
        "5": 3,
        "4": 2,
        "3": 1
    },
    "suits": {
        "Spades": 4,
        "Hearts": 3,
        "Clubs": 1,
        "Diamonds": 2
    }
}


class card(pydealer.Card):
    def __init__(self, suit, value):
        super(card, self).__init__(value, suit)


class game:
    def __init__(self):
        self.player_list = []  # store player's class
        self.deck = pydealer.Deck()
        self.card_pile_full = False
        self.card_pile = []
        self.empty_pile = []


        self.player_status = []
        self.current_player = None

        self.deck.shuffle()

    def generate_player(self):
        input_num_players = int(input("Please enter number of players (>=): "))
        if input_num_players >= 2:
            pass
        else:
            print("please enter number >= 2: ")
            quit()
        for _ in range(input_num_players):
            player_name = input("Please enter player's names by order: ")
            _player = player()
            # store player's name in Class player
            _player.name = player_name
            # add player in to player's list
            self.player_list.append(_player)

    # function works
    def deal_cards_to_player(self):
        for _player in self.player_list:
            temp_hand_cards = self.deck.deal(round(12 / len(self.player_list)))
            temp_hand_cards.sort(NEW_RANKS)
            _player.card_list = temp_hand_cards
            print(_player.name)
            print(_player.card_list)

    def find_first_player(self):
        first_card = None
        firstPlayer = None
        for p in self.player_list:
            for _card in p.card_list:
                if first_card is None or _card.lt(first_card, NEW_RANKS) is True:
                    first_card = _card
                    firstPlayer = p
        return firstPlayer

    def deal_min_card(self, _p):
        for card in _p.card_list:
            if len(self.card_pile) == 0 or self.card_pile[-1].lt(card, NEW_RANKS):
                self.card_pile.append(card)
                _p.card_list.get(str(card))
                break

    def total_max_card(self):
        max_card = None
        for p in self.player_list:
            for _card in p.card_list:
                if max_card is None or _card.ge(max_card, NEW_RANKS) is True:
                    max_card = _card
        return max_card

    def check_if_clean_pile(self):
        if self.total_max_card().lt(self.card_pile[-1], NEW_RANKS) is True:
            self.card_pile.clear()
        else:
            pass

    def check_winner(self):
        empty_stack = pydealer.Stack()
        for p in self.player_list:
            if p.card_list == empty_stack:
                print(f"{p.name} is winner!!")
                return p.name
            else:
                return None

    def play_card(self, x):
        first_player_index = self.player_list.index(x)
        while self.card_pile_full is False:
            for _player in self.player_list[first_player_index:] + self.player_list[:first_player_index]:
                self.deal_min_card(_player)
                self.check_if_clean_pile()
                self.check_winner()
                if self.card_pile == self.empty_pile:
                    self.deal_min_card(_player)
                else:
                    pass

    def dealt_card(self, player_name, value, suit):
        for _p in self.player_list:
            if player_name == _p.name:
                for card in _p.card_list:
                    if value == card.value and suit == card.suit:
                        if len(self.card_pile) == 0 or card.ge(self.card_pile[-1]):
                            self.card_pile.append(card)
                            _p.card_list.get(str(card))
                            return True
                        elif card.lt(self.card_pile[-1]):
                            return False
                        break
                break

    def dealt_pair(self, player_name, value, suit_1, suit_2):
        pair = []
        for _p in self.player_list:
            if player_name == _p.name:
                for card in _p.card_list:
                    if value == card.value and suit_1 == card.suit or value == card.value and suit_2 == card.suit:
                        pair.append(card)
                if pair[1].ge(pair[0]):
                    pair.reverse()

                if len(self.card_pile) == 0 or pair[0].ge(self.card_pile[-1][0]):
                    self.card_pile.append(pair)
                    _p.card_list.get(str(pair[0]))
                    _p.card_list.get(str(pair[1]))
                    return True
                    # elif card.lt(self.card_pile[-1]):
                    #     return False
                break

    def name_change(self, old_player, new_player):
        old_player.name = new_player

    def check_player_status_refresh(self):
        if len(self.player_status) == 1:
            temp_list = []
            for player in self.player_list:
                temp_list.append(player.name)
            first_player = self.player_status[0]
            first_player_index = temp_list.index(first_player)
            for _player in temp_list[first_player_index+1:] + temp_list[:first_player_index]:
                self.player_status.append(_player)
            self.card_pile.clear()


        elif len(self.player_status) == 0:
            for player in self.player_list:
                self.player_status.append(player.name)
                self.current_player = self.player_status[0]


        print(self.player_status)

    def change_current_player(self):
        x = self.player_status.index(self.current_player)
        if x == len(self.player_status) - 1:
            self.current_player = self.player_status[0]
        else:
            self.current_player = self.player_status[x + 1]





class player:
    def __init__(self):
        self.name = ""
        self.card_list = []


if __name__ == "__main__":
    # declare a game
    BigTwo = game()

    # enter player_num
    BigTwo.generate_player()
    BigTwo.deal_cards_to_player()

    # find first player
    first_player = BigTwo.find_first_player()

    # starting game at first player
    BigTwo.play_card(first_player)

    # playing card
