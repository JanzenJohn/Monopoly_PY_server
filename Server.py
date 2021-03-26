import socket
import Server_Network
from _thread import *
from threading import Event
import libs
import random
from copy import deepcopy


s = Server_Network.Network()
while True:
    print("STARTED NEW GAME")
    class bcolors:
        HEADER = ''
        OKBLUE = ''
        OKCYAN = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''

    match_start = Event()
    amount = int(2)
    connections = []
    s.client.listen(amount)
    for i in range(amount):
        conn, addr = s.client.accept()
        user = libs.Player()
        user.conn = conn
        s.send("str", "CONNECTED", user)
        connections.append(conn)
        s.send("str", "WAITING FOR PLAYERS", user)
        print("connected")

    print("moving on")


    class ServerController:
        def __init__(self, connections):
            self.turn = 0
            self.conns = connections
            print("setup connections")
            self.board = libs.make_board()
            print("setup board")
            self.users = []

    def old_board(to_send):
        try:
            s.send("str", "######################################################", to_send)
            for i in range(int(len(sc.board) / 2)):
                temp_price = str(sc.board[i].price)
                while len(temp_price) < 5:
                    temp_price = " " + temp_price
                name = sc.board[i].owner_id
                if name == "00000000":
                    name = "no one"
                elif name == "SYSTEM":
                    name = "SYSTEM"
                else:
                    temp = libs.get_name_by_id(name, sc.users)
                    name = [" ", " ", " ", " ", " ", " "]
                    for x in range(6):
                        try:
                            name[x] = temp[x]
                        except IndexError:
                            pass
                        except TypeError:
                            pass
                    name = "".join(name)
                counter = str(i)
                if len(counter) < 2:
                    counter = "0" + counter
                output = f"{bcolors.WARNING}{counter}{bcolors.ENDC}"
                if sc.board[i].owner_id == to_send.id:
                    output += f" : {bcolors.OKGREEN}{sc.board[i].name}{bcolors.ENDC}"
                elif sc.board[i].owner_id == "00000000":
                    output += f" : {bcolors.OKBLUE}{sc.board[i].name}{bcolors.ENDC}"
                else:
                    output += f" : {bcolors.FAIL}{sc.board[i].name}{bcolors.ENDC}"

                output += f":{bcolors.BOLD}{temp_price}${bcolors.ENDC}," \
                        f" Owner : {bcolors.OKBLUE}{name}{bcolors.ENDC}" \
                        f" Houses : [ {bcolors.OKCYAN}"
                output += str("#" * sc.board[i].houses) + str(" " * (5 - sc.board[i].houses))
                output += f" {bcolors.ENDC}]"
                output += " Players : [ "
                counter = 0
                for user in sc.users:
                    if user.position == i:
                        counter += 1
                        if user == to_send:
                            output += f"{bcolors.OKGREEN}{user.name[0:6]}{' ' * (6 - len(user.name))} "
                        else:
                            output += f"{bcolors.FAIL}{user.name[0:6]}{' ' * (6 - len(user.name))} "
                output += f"{bcolors.ENDC}"
                while counter < len(sc.users):
                    output += "       "
                    counter += 1
                name = sc.board[i + 20].owner_id
                if name == "00000000":
                    name = "No one"
                elif name == "SYSTEM":
                    name = "SYSTEM"
                else:
                    temp = libs.get_name_by_id(name, sc.users)
                    name = [" ", " ", " ", " ", " ", " "]
                    for x in range(6):
                        try:
                            name[x] = temp[x]
                        except IndexError:
                            pass
                        except TypeError:
                            name = ["N", "o", " ", "o", "n", "e"]
                    name = "".join(name)
                temp_price = str(sc.board[i + 20].price)
                while len(temp_price) < 5:
                    temp_price = " " + temp_price
                output += " ] "
                output += f"{bcolors.WARNING}{i + 20}{bcolors.ENDC}"
                if sc.board[i + 20].owner_id == to_send.id:
                    output += f" : {bcolors.OKGREEN}{sc.board[i + 20].name}{bcolors.ENDC}"
                elif sc.board[i + 20].owner_id == "00000000":
                    output += f" : {bcolors.OKBLUE}{sc.board[i + 20].name}{bcolors.ENDC}"
                else:
                    output += f" : {bcolors.FAIL}{sc.board[i + 20].name}{bcolors.ENDC}"
                output += f":{bcolors.BOLD}{temp_price}${bcolors.ENDC}," \
                        f" Owner : {bcolors.OKBLUE}{name}{bcolors.ENDC} Houses " \
                        f": [ {bcolors.OKCYAN}"
                output += str("#" * sc.board[i + 20].houses) + str(" " * (5 - sc.board[i + 20].houses))
                output += f" {bcolors.ENDC}]"
                output += " Players : [ "
                for user in sc.users:
                    if user.position == i + 20:
                        if user == to_send:
                            output += f"{bcolors.OKGREEN}{user.name} "
                        else:
                            output += f"{bcolors.FAIL}{user.name} "
                output += f" {bcolors.ENDC}]"
                s.send("str", output, to_send)
            for i in sc.users:
                owned = []
                for x in sc.board:
                    if sc.board[x].owner_id == i.id:
                        owned.append(sc.board[x])
                s.send("str", f"{i.name} : {i.id} : {i.money}$", to_send)
                line_0 = ""
                line_1 = ""
                for x in owned:
                    line_0 += x.name + " "
                    line_1 += str(x.houses) + "     "
                    if x.morg:
                        line_1 += "mort "
                    else:
                        line_1 += "     "
                s.send("str", line_0, to_send)
                s.send("str", line_1, to_send)
            s.send("str", "######################################################", to_send)
        except BrokenPipeError:
            pass


    class Updater:
        def update(self):
            for to_send in sc.users:
                if to_send.OS == "nt":
                    class bcolors:
                        HEADER = ''
                        OKBLUE = ''
                        OKCYAN = ''
                        OKGREEN = ''
                        WARNING = ''
                        FAIL = ''
                        ENDC = ''
                        BOLD = ''
                        UNDERLINE = ''
                    s.send("str", "WINDOWS MODE", to_send)
                    old_board(to_send)
                else:
                    class bcolors:
                        HEADER = '\033[95m'
                        OKBLUE = '\033[94m'
                        OKCYAN = '\033[96m'
                        OKGREEN = '\033[92m'
                        WARNING = '\033[93m'
                        FAIL = '\033[91m'
                        ENDC = '\033[0m'
                        BOLD = '\033[1m'
                        UNDERLINE = '\033[4m'
                    s.send("str", "POSIX MODE", to_send)
                    old_board(to_send)
                


    print("creating servercontroller")
    sc = ServerController(connections)
    print("created servercontroller")
    for i in range(len(sc.conns)):
        sc.users.append(libs.Player())
        sc.users[i].conn = sc.conns[i]
        candidat = ""
        while True:
            candidat = random.randint(0, 99999999)
            Flag = False
            for user in sc.users:
                if candidat == user.id:
                    Flag = True
            if Flag:
                continue
            else:
                break
        sc.users[i].id = candidat
        try:
            sc.users[i].name = s.request("str", "name ?", sc.users[i])
            sc.users[i].OS = s.request("str", "OS", sc.users[i])
        except BrokenPipeError:
            sc.users[i].name = "disconnected"
            sc.users[i].OS = "nt"

    print("gave everyone a name")

    draw = True
    while True:
        try:
            if draw:
                updater = Updater()
                updater.update()
            draw = True
            try:
                user = sc.users[sc.turn]
            except IndexError:
                try:
                    user = sc.users[0]
                except IndexError:
                    print("NO PLAYERS LEFT")
                    break
            if len(sc.users) == 1:
                s.send("str", "you won", sc.users[0])
                break
            try:
                command = s.request("str", f"{user.name}>", user)
                if command == "disconnected":
                    sc.users.remove(user)
                    continue
            except BrokenPipeError:
                print(f"User {user.name} disconnected")
                sc.users.remove(user)
                continue
            print(f"COMMAND FROM {user.name} {command}")
            structure = command.split()
            if len(structure) == 0:
                draw = False
                continue
            if structure[0] == "done":
                if user.walked and len(user.debt) == 0:
                    sc.turn += 1
                    if sc.turn == len(sc.users):
                        sc.turn = 0
                    user.walked = False
                    continue
                for i in user.debt:
                    s.request("str", f"You owe {libs.get_name_by_id(i[0], sc.users)}, {i[1]}$", user)
                s.request("str", "You still need to walk / pay you debts", user)
            elif structure[0] == "giveup":
                for prop in sc.board:
                    if sc.board[prop].owner_id == user.id:
                        sc.board[prop].owned = False
                        sc.board[prop].owner_id = "00000000"
                sc.users.remove(user)
                s.send("str", "you loose", user)
            elif structure[0] == "telp":
                try:
                    id = int(structure[1])
                except IndexError:
                    s.send("str", "id ??????", user)
                    continue
                if 0 > id or id > 40:
                    s.send("str", "no", user)
                    continue
                user.position = id
            elif structure[0] == "go":
                if user.walked:
                    s.send("str", "You already walked", user)
                    continue
                dice_0 = random.randint(1, 6)
                dice_1 = random.randint(1, 6)
                total = dice_0 + dice_1
                if not user.in_prison:
                    for i in range(total):
                        user.position += 1
                        if user.position == 40:
                            user.position = 0
                        if user.position == 0:
                            user.money += 4000
                    libs.land(user, sc.board, sc.users, s, total=total)
                    user.walked = True
                else:
                    user.prison_counter += 1
                    if dice_0 == dice_1:
                        s.request("str", "You got both dice the same you are free", user)
                        user.in_prison = False
                        user.prison_counter = 0
                        user.walked = True
                        continue
                    if user.prison_counter == 3:
                        user.prison_counter = 0
                        user.in_prison = False
                        if user.prison_card_c:
                            user.prison_card_c = False
                            s.request("str", "you used your get out of prison card", user)
                        elif user.prison_card_e:
                            user.prison_card_e = False
                            s.request("str", "you used your get out of prison card", user)
                        else:
                            user.debt.append(["SYSTEM", 1000])
                            s.request("str", f"You owe the state 1000$ bribing money", user)
                        user.block = True
                        user.walked = True
                        continue
                    else:
                        s.request("str", "You are still in prison", user)
                        user.walked = True
            elif structure[0] == "pay":
                for i in user.debt:
                    if user.money >= int(i[1]):
                        user.money -= int(i[1])
                        for w_user in sc.users:
                            if w_user.id == i[0]:
                                w_user.money += int(i[1])
                        user.debt.remove(i)
                        if len(user.debt) < 1:
                            user.block = False
                    else:
                        s.request("str", f"You dont have enough money ({i[1]} to pay {i[0]})", user)
            elif structure[0] == "buy":
                field_type = sc.board[user.position].type
                if not sc.board[user.position].owned:
                    if field_type == "PROPERTY" or field_type == "SPECIAL-PROPERTY" or field_type == "SPECIAL-PROPERTY-2":
                        libs.buy(user, sc.board[user.position], s)
                else:
                    s.request("str", f"{sc.board[user.position].name} isn't available for purchase", user)
            elif structure[0] == "mortgage":
                try:
                    int(structure[1])
                except ValueError or IndexError:
                    s.request("str", "ID not Present or invalid", user)
                    continue
                id = int(structure[1])
                if sc.board[id].houses > 0:
                    s.request("str", f"{sc.board[id].name} has houses on it.", user)
                    continue
                if sc.board[id].owner_id != user.id:
                    s.request("str", f"You dont own {sc.board[id].name}", user)
                    continue
                if sc.board[id].morg:
                    s.request("str", f"{sc.board[id].name} already has a mortgage", user)
                    continue
                if sc.board[id].houses > 0:
                    s.request("str", f"{sc.board[id].name} has houses sell them first", user)
                    continue
                sc.board[id].morg = True
                user.money += int(int(sc.board[id].price) / 2)
            elif structure[0] == "unmortgage":
                try:
                    int(structure[1])
                except ValueError or IndexError:
                    s.request("str","ID not Present or invalid",user)
                    continue
                id = int(structure[1])
                if sc.board[id].owner_id != user.id:
                    s.request("str", f"You dont own {sc.board[id].name}", user)
                    continue
                if not sc.board[id].morg:
                    s.request("str", f"{sc.board[id].name} doensn't have a morgage", user)
                    continue
                if int(int(sc.board[id].price) / 2) > user.money:
                    s.request("str", f"You dont have enough money to clear {sc.board[id].name}", user)
                    continue
                sc.board[id].morg = False
                user.money -= int(int(sc.board[id].price) / 2)
            elif structure[0] == "chat":
                draw = False
                try:
                    for curUser in sc.users:
                        s.send("str", f"{user.name}:{structure[1]}", curUser)
                except Exception as e:
                    print("what")
            elif structure[0] == "houses":
                try:
                    _ = structure[1]
                    _ = int(structure[2])
                except IndexError:
                    s.request("str", "Specify ID, and if you want to buy or sell", user)
                    continue
                except ValueError:
                    s.request("str", "ID not Valid", user)
                    continue
                if structure[1] == "buy" or structure[1] == "sell":
                    pass
                else:
                    s.request("str", "Specify if you want to buy or sell", user)
                    continue
                id = int(structure[2])
                try:
                    _ = sc.board[id]
                except IndexError:
                    s.request("str", "ID not valid", user)
                    continue
                except KeyError:
                    s.request("str", "ID not valid", user)
                    continue
                if structure[1] == "buy":
                    if sc.board[id].morg:
                        s.request("str", f"{sc.board[id].name} has a mortgage applied", user)
                        continue
                    owner = sc.board[id].owner_id
                    if user.id != owner:
                        s.request("str", f"You dont own {sc.board[id].name}", user)
                        continue
                    if sc.board[id].houses == 5:
                        s.request("str", "Enough houses", user)
                        continue
                    group_fields = []
                    for i in range(len(sc.board)):
                        field = sc.board[i]
                        if field.group == sc.board[id].group:
                            group_fields.append(field)
                    flag = False
                    for i in group_fields:
                        if i.houses < sc.board[id].houses:
                            s.request("str", f"{i.name} has too few houses to build houses here", user)
                            flag = True
                        if i.owner_id != user.id:
                            s.request("str", f"{i.name} isnt owned by you, you need to own every street of its group to build",
                                    user)
                            flag = True

                    if flag:
                        continue
                    if sc.board[id].type != "PROPERTY":
                        s.request("str", f"Cant build on {sc.board[id].name}", user)
                        continue
                    group = int(sc.board[id].group)
                    amount = 0
                    if group == 1 or group == 2:
                        amount = 1000
                    elif group == 3 or group == 4:
                        amount = 2000
                    elif group == 5 or group == 6:
                        amount = 3000
                    elif group == 7 or group == 8:
                        amount = 4000

                    if user.money >= amount:
                        user.money -= amount
                        sc.board[id].houses += 1
                    else:
                        s.request("str", f"You dont have enough money to build a house here {user.money} vs {amount}", user)
                        continue
                elif structure[1] == "sell":
                    if sc.board[id].houses != 0:
                        owner = sc.board[id].owner_id
                        if user.id != owner:
                            s.request("str", f"You dont own {sc.board[id].name}", user)
                            continue
                        group_fields = []
                        for i in range(len(sc.board)):
                            field = sc.board[i]
                            if field.group == sc.board[id].group:
                                group_fields.append(field)
                        flag = False
                        for i in group_fields:
                            if i.houses > sc.board[id].houses:
                                s.request("str", f"{i.name} has too many houses to sell houses here", user)
                                flag = True
                            if i.owner_id != user.id:
                                s.request("str", f"If this Error shows shits getting real", user)
                                flag = True

                        if flag:
                            continue
                        if sc.board[id].type != "PROPERTY":
                            s.request("str", f"Cant sell of {sc.board[id].name}", user)
                            continue
                        group = int(sc.board[id].group)
                        amount = 0
                        if group == 1 or group == 2:
                            amount = 500
                        elif group == 3 or group == 4:
                            amount = 1000
                        elif group == 5 or group == 6:
                            amount = 1500
                        elif group == 7 or group == 8:
                            amount = 2000

                        user.money += amount
                        sc.board[id].houses -= 1
                    else:
                        s.request("str", f"What houses are you trying to sell", user)
            elif structure[0] == "trade":
                try:
                    to_trade_with = structure[1]
                except IndexError:
                    s.request("str", "You need to pass the ID you want to trade", user)
                    continue
                for w_user in sc.users:
                    if int(w_user.id) == int(to_trade_with):
                        to_trade_with = w_user

                        break
                if user == w_user:
                    s.request("str", "You cant trade with yourself", user)
                    continue

                if type(to_trade_with) == str:
                    s.request("str", "user doesn't exist", user)
                    continue
                s.send("str", "########   TRADING USAGE   ########", user)
                s.send("str", "To add something you want use request", user)
                s.send("str", "    - prop:ID       for property", user)
                s.send("str", "    - money:Amount for money", user)
                s.send("str", "To add something you want to give use offer", user)
                s.send("str", "    - prop:ID       for property", user)
                s.send("str", "    - money:Amount for money", user)
                s.send("str", "To cancel Trade use cancel", user)
                s.send("str", "To make the Trade type \"try\"", user)
                requests = {"money": 0, "props": []}
                offers = {"money": 0, "props": []}
                while True:
                    trade_command = s.request("str", "what do you want to trade ?", user).lower()
                    trade_structure = trade_command.split()
                    if trade_command.startswith("cancel"):
                        break
                    if len(trade_structure) == 0:
                        continue
                    elif trade_structure[0] == "request":
                        try:
                            requested = trade_structure[1]
                            if requested.startswith("prop"):
                                prop = requested.split(":")
                                prop = int(prop[1])
                                possible = False
                                for field_id in range(len(sc.board)):
                                    if field_id == prop:
                                        possible = sc.board[field_id].owner_id == to_trade_with.id
                                if possible:
                                    requests["props"].append(prop)
                                    s.request("str", "added to requests", user)
                                else:
                                    s.request("str", "user does not own that field", user)
                            elif requested.startswith("money"):
                                money = requested.split(":")
                                flag = True
                                requests["money"] += int(money[1])


                        except IndexError:
                            s.request("str", "syntax error", user)
                        except ValueError:
                            s.request("str", "syntax error", user)
                    elif trade_structure[0] == "offer":
                        try:
                            requested = trade_structure[1]
                            if requested.startswith("prop"):
                                prop = requested.split(":")
                                prop = int(prop[1])
                                possible = False
                                for field_id in range(len(sc.board)):
                                    if field_id == prop:
                                        possible = sc.board[field_id].owner_id == user.id
                                if possible:
                                    offers["props"].append(prop)
                                    s.request("str", "added to offers", user)
                                else:
                                    s.request("str", "you do not own that field", user)
                            elif requested.startswith("money"):
                                money = requested.split(":")
                                flag = True
                                offers["money"] += int(money[1])


                        except IndexError:
                            s.request("str", "syntax error", user)
                        except ValueError:
                            s.request("str", "syntax error", user)
                    elif trade_structure[0] == "print":
                        s.request("str", f"offers : {offers}", user)
                        s.request("str", f"requests : {requests}", user)
                    elif trade_structure[0] == "try":
                        s.request("str", f"{user.name} wants to trade", to_trade_with)
                        s.request("str", "the player wants : ", to_trade_with)
                        s.send("str", f"Money : {requests['money']}", to_trade_with)
                        for i in requests["props"]:
                            s.send("str", f"Property: {sc.board[i].name}", to_trade_with)
                        s.send("str", f"{user.name} offers you", to_trade_with)
                        s.send("str", f"Money : {offers['money']}", to_trade_with)
                        for i in offers["props"]:
                            s.send("str", f"Property: {sc.board[i].name}", to_trade_with)
                        flag = False
                        while not flag:
                            dec = s.request("str", "Do you accept ?", to_trade_with).lower()
                            if dec == "yes" or dec == "no":
                                flag = True
                        if dec == "yes":
                            money_needed_trader = requests['money']
                            money_available = getattr(to_trade_with, "money")
                            for field_id_0 in requests["props"]:
                                for field_id in sc.board:
                                    if sc.board[field_id].group == sc.board[field_id_0].group:
                                        houses = getattr(sc.board[field_id], "houses")
                                        for i in range(houses):
                                            if 0 < field_id < 10:
                                                money_available += 500
                                            elif 10 < field_id < 20:
                                                money_available += 1000
                                            elif 20 < field_id < 30:
                                                money_available += 1500
                                            elif 30 < field_id:
                                                money_available += 2000
                            if money_available < money_needed_trader:
                                s.request("str", "not enough money", to_trade_with)
                                s.request("str", "trading partner doesn't have enough money", user)
                                break
                            money_needed_user = offers["money"]
                            money_available_user = getattr(user, "money")
                            for field_id_0 in offers["props"]:
                                for field_id in sc.board:
                                    if sc.board[field_id].group == sc.board[field_id_0].group:
                                        houses = getattr(sc.board[field_id], "houses")
                                        for i in range(houses):
                                            if 0 < field_id < 10:
                                                money_available_user += 500
                                            elif 10 < field_id < 20:
                                                money_available_user += 1000
                                            elif 20 < field_id < 30:
                                                money_available_user += 1500
                                            elif 30 < field_id:
                                                money_available_user += 2000
                            if money_needed_user > money_available_user:
                                s.request("str", f"{user.name} doesn't have enough money", to_trade_with)
                                s.request("str", "you dont have enough money", user)
                                break
                            user.money = money_available_user
                            to_trade_with.money = money_available
                            for field_id_0 in requests["props"]:
                                sc.board[field_id_0].owner_id = user.id
                                for field_id in sc.board:
                                    if sc.board[field_id].group == sc.board[field_id_0].group:
                                        sc.board[field_id].houses = 0
                            for field_id_0 in offers["props"]:
                                sc.board[field_id_0].owner_id = to_trade_with.id
                                for field_id in sc.board:
                                    if sc.board[field_id].group == sc.board[field_id_0].group:
                                        sc.board[field_id].houses = 0
                            user.money -= offers["money"]
                            user.money += requests["money"]
                            to_trade_with.money -= requests["money"]
                            to_trade_with.money += offers["money"]
                            break
                        elif dec == "no":
                            s.request("str", "trade would be dead now", user)
                            s.request("str", "trade would be dead now", to_trade_with)
                            break

            else:
                draw = False
                print("WELL THIS ISNT POG")
        except BrokenPipeError:
            pass
