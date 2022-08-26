import json

from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import pydealer
from poker_game import game, player
import json

app = Flask(__name__)
api = Api(app)
PLAYER_LIST = []
HAND_CARD = None
PLAYER_CARD_DICT = {}
BIGTWO = game()
CARD_PILE = []

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

class dealt_card(Resource):

    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('player', required=False)  # add args
        parser.add_argument('value', required=False)
        parser.add_argument('suit', required=False)


        args = parser.parse_args()  # parse arguments to dictionary

        BIGTWO.check_player_status_refresh() # checking available player in list
        if args['player'] == BIGTWO.current_player:
            if "player" in args.keys() and "value" in args.keys() and "suit" in args.keys():
                flag = BIGTWO.dealt_card(args['player'], args['value'], args['suit'])
                if flag:
                    # ---------------move to next player--------------------
                    BIGTWO.change_current_player()
                    print(f"card_pile : {BIGTWO.card_pile}")
                    print(f"CURRENT PLAYER IS {BIGTWO.current_player}")
                    pass
                else:
                    return {'indicator': False, "message": "it is not an available card"}
        else:
            return {'indicator': False, "message": "it is not the current player"}
        # ---------------check if winner--------------------
        winner = BIGTWO.check_winner()
        if winner:
            return {'indicator': True, "message": winner + " is winner"}

        return {'indicator': True, "message": convert_stack_to_list()}, 200  # return data with 200 OK
    pass

class change_name(Resource):
    def post(self):
        # Change player's name
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('old_player', required=False)  # add args
        parser.add_argument('new_player', required=False)

        args = parser.parse_args()  # parse arguments to dictionary

        temp_dict = convert_stack_to_list()
        if args['old_player'] in temp_dict.keys():
            temp_dict[args['new_player']] = temp_dict[args['old_player']]
            del temp_dict[args['old_player']]

        return {'indicator': True, "message": temp_dict}, 200  # return data with 200 OK

    pass

class dealt_pair(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('player', required=False)  # add args
        parser.add_argument('value', required=False)
        parser.add_argument('suit_1', required=False)
        parser.add_argument('suit_2', required=False)

        args = parser.parse_args()  # parse arguments to dictionary
        if "player" in args.keys() and "value" in args.keys() and "suit_1" in args.keys() and "suit_2" in args.keys():
            flag = BIGTWO.dealt_pair(args['player'], args['value'], args['suit_1'], args['suit_2'])
            if flag:
                BIGTWO.change_current_player()
                pass
            else:
                return {'indicator': False, "message": "it is not an available card"}

        return {'indicator': True, "message": convert_stack_to_list()}, 200  # return data with 200 OK
        # 比對子:?num=[1,2]&suit=[heart,spade] 轉成json format.
        # look up how to transfer data into json by using postman
    pass

class Pass(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('player', required=False)  # add args

        args = parser.parse_args()  # parse arguments to dictionary

        if args['player'] == BIGTWO.current_player:

                BIGTWO.change_current_player()
                BIGTWO.player_status.remove(args['player'])
                print(f"CURRENT PLAYER IS {BIGTWO.current_player}")

                print(f"{args['player']} had been passed.")
        else:
            return {'indicator': False, "message": "it is not the current player"}

        BIGTWO.check_player_status_refresh() # checking available player in list

        print(BIGTWO.player_status)
        print(BIGTWO.card_pile)

        return {'indicator': True, "message": convert_stack_to_list()}, 200  # return data with 200 OK
    pass

api.add_resource(dealt_card, '/dealt_card')
api.add_resource(change_name, '/change_name')
api.add_resource(dealt_pair, '/dealt_pair')
api.add_resource(Pass, '/Pass')

def convert_stack_to_list():
    _dict = {}
    for player in BIGTWO.player_list:
        temp_list = []
        for card in player.card_list:
            temp_list.append({"num": card.value, "suit": card.suit})
        _dict[player.name] = temp_list

    return _dict

@app.route("/dealt", methods=["POST","GET"])
def press_to_dealt():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        _dict = convert_stack_to_list()
        _str = ""
        for L in _dict[user_name]:
            _str += '''
             <div class="card">
             <input type="submit" name="suit_num" value="%s-%s">
             </div>
             ''' % (L["suit"], L["num"])
        _card = '''
             <div class="card">
             <input type="submit" name="suit_num" value="%s">
             </div>
             ''' % (request.values['suit_num'])
        return render_template("interface.html",Card_pool=_card,player1=BIGTWO.player_list[0].name, player2=BIGTWO.player_list[1].name, player3=BIGTWO.player_list[2].name, player4=BIGTWO.player_list[3].name, Current_Player=user_name, handcard=_str)
@app.route("/bigtwogame/<user_name>")
def interface(user_name):
    _dict = convert_stack_to_list()
    _str = ""
    for L in _dict[user_name]:
        _str += '''
        <div class="card">
        <input type="submit" name="suit_num" value="%s-%s">
        </div>
        ''' % (L["suit"], L["num"])

    return render_template("interface.html",player1=BIGTWO.player_list[0].name, player2=BIGTWO.player_list[1].name, player3=BIGTWO.player_list[2].name, player4=BIGTWO.player_list[3].name, Current_Player=user_name, handcard=_str)

if __name__ == '__main__':

    BIGTWO.generate_player()
    BIGTWO.deal_cards_to_player()
    BIGTWO.check_player_status_refresh()




    app.run()  # run our Flask app



