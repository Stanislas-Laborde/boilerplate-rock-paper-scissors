import random

def player(prev_play, opponent_history=[], player_history=[], play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }], opponent_type=[{
              "quincy": 0,
              "mrugesh": 0,
              "kris": 0,
              "abbey": 0,
          }], change=[False]):
    if prev_play == '':
        opponent_history.clear()
        player_history.clear()

        play_order[0]["RR"] = 0
        play_order[0]["RP"] = 0
        play_order[0]["RS"] = 0
        play_order[0]["PR"] = 0
        play_order[0]["PP"] = 0
        play_order[0]["PS"] = 0
        play_order[0]["SR"] = 0
        play_order[0]["SP"] = 0
        play_order[0]["SS"] = 0

        opponent_type[0]["quincy"] = 0
        opponent_type[0]["mrugesh"] = 0
        opponent_type[0]["kris"] = 0
        opponent_type[0]["abbey"] = 0
        # -1 means NO, 0 means MAYBE, 1 means YES

        change[0]=False

        opp_type = ""
    else:
        opponent_history.append(prev_play)

        k = list(opponent_type[0].keys())
        v = list(opponent_type[0].values())
        types = dict((x,v.count(x)) for x in set(v))

        if -1 in types.keys() and types[-1] == 4: # Unknown type
            opp_type = ""

        elif not ((-1 in types.keys() and types[-1] == 3) and (1 in types.keys() and types[1] == 1)):
            if opponent_type[0]["quincy"] == 0:
                opp_choices = ['R', 'R', 'P', 'P', 'S']
                if opponent_history[-1] != opp_choices[len(opponent_history) % len(opp_choices)]:
                    opponent_type[0]["quincy"] = -1

            if opponent_type[0]["mrugesh"] == 0:
                if opponent_history[0] != 'R':
                    opponent_type[0]["mrugesh"] = -1
                elif len(player_history) > 3: # DUE TO case most_frequent == ''
                    last_ten = player_history[-10:]

                    most_frequent = max(set(last_ten), key=last_ten.count)

                    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
                    
                    if opponent_history[-1] != ideal_response[most_frequent]:
                        opponent_type[0]["mrugesh"] = -1

            if opponent_type[0]["kris"] == 0:
                if opponent_history[0] != 'P':
                    opponent_type[0]["kris"] = -1
                elif len(player_history) >= 2:
                    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
                    if opponent_history[-1] != ideal_response[player_history[-2]]:
                        opponent_type[0]["kris"] = -1
            
            if opponent_type[0]["abbey"] == 0:
                if opponent_history[0] != 'P':
                    opponent_type[0]["abbey"] = -1
                elif len(player_history) >= 2:
                    if len(player_history) == 2:
                        last_two = "R" + player_history[-2]
                    else:
                        last_two = "".join(player_history[-3:-1])

                    play_order[0][last_two] += 1

                    potential_plays = [
                    player_history[-2] + "R",
                    player_history[-2] + "P",
                    player_history[-2] + "S",
                    ]

                    sub_order = {
                        k: play_order[0][k]
                        for k in potential_plays if k in play_order[0]
                    }

                    prediction = max(sub_order, key=sub_order.get)[-1:]

                    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}       
                    if opponent_history[-1] != ideal_response[prediction]:
                        opponent_type[0]["abbey"] = -1

            v = list(opponent_type[0].values())
            types = dict((x,v.count(x)) for x in set(v))

            if -1 in types.keys() and types[-1] == 3:
                opponent_type[0][k[v.index(0)]] = 1
                change[0] = True

        if (-1 in types.keys() and types[-1] == 3) and (1 in types.keys() and types[1] == 1):
            opp_type = k[v.index(1)]
        else:
            opp_type = ""

    if opp_type == "quincy":
        choices = ['P', 'P', 'S', 'S', 'R']
        move = choices[(1 + len(opponent_history)) % len(choices)]

    elif opp_type == "mrugesh":
        if len(player_history) == 0:
            most_frequent = 'S'
        else:
            last_ten = player_history[-10:]
            most_frequent = max(set(last_ten), key=last_ten.count)

        ideal_response = {'P': 'R', 'R': 'S', 'S': 'P'}
        move = ideal_response[most_frequent]

    elif opp_type == "kris":
        if len(player_history) == 0:
            last_move = 'R'
        else:
            last_move = player_history[-1]

        ideal_response = {'P': 'R', 'R': 'S', 'S': 'P'}
        move = ideal_response[last_move]

    elif opp_type == "abbey":
        if len(player_history) < 2:
            if len(player_history) == 0:
                last_move = 'R'
            else:
                last_move = player_history[-1]

            ideal_response = {'P': 'R', 'R': 'S', 'S': 'P'}
            move = ideal_response[last_move]
        else:
            if change[0]:
                last_two = "".join(player_history[-3:-1])
                play_order[0][last_two] += 1
                change[0] = False

            last_two = "".join(player_history[-2:])
            play_order[0][last_two] += 1

            potential_plays = [
                player_history[-1] + 'R',
                player_history[-1] + 'P',
                player_history[-1] + 'S',
            ]

            sub_order = {
                k: play_order[0][k]
                for k in potential_plays if k in play_order[0]
            }

            prediction = max(sub_order, key=sub_order.get)[-1:]

            ideal_response = {'P': 'R', 'R': 'S', 'S': 'P'}
            move = ideal_response[prediction]

    else:
        move = random.choice(['R', 'P', 'S'])

    player_history.append(move)
    return move
