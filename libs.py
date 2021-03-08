import random
import sys

__author__ = "Johann"

class Screendrawer:
    def draw_board(self, board, users):
        for i in range(int(len(board)/2)):
            temp_price = str(board[i].price)
            while len(temp_price) < 5:
                temp_price = " " + temp_price
            name = board[i].owner_id
            if name == "00000000":
                name = "no one"
            elif name == "SYSTEM":
                name = "SYSTEM"
            else:
                temp = get_name_by_id(name, users)
                name = [" ", " ", " ", " ", " ", " "]
                for x in range(6):
                    try:
                        name[x] = temp[x]
                    except IndexError:
                        pass
                name = "".join(name)

            counter = str(i)
            if len(counter) < 2:
                counter = "0" + counter
            output = f"{counter} : {board[i].name}:{temp_price}$, Owner : {name} Houses : [ "
            output += str("#"*board[i].houses)+str(" "*(5-board[i].houses))
            output += " ]"
            output += " Players : [ "
            counter = 0
            for user in users:
                if user.position == i:
                    counter += 1
                    output += user.name[0:6] + " "*(6-len(user.name)) + " "
            while counter < len(users):
                output += "       "
                counter += 1

            name = board[i+20].owner_id
            if name == "00000000":
                name = "No one"
            elif name == "SYSTEM":
                name = "SYSTEM"
            else:
                temp = get_name_by_id(name, users)
                name = [" ", " ", " ", " ", " ", " "]
                for x in range(6):
                    try:
                        name[x] = temp[x]
                    except IndexError:
                        pass
                    except TypeError:
                        name = ["N", "o", " ", "o", "n", "e"]
                name = "".join(name)
            output += " ]       "
            output += f"{i+20} : {board[i+20].name}:{temp_price}$, Owner : {name} Houses : [ "
            output += str("#"*board[i+20].houses)+str(" "*(5-board[i+20].houses))
            output += " ]"
            output += " Players : [ "
            for user in users:
                if user.position == i+20:
                    output += user.name + " "
            output += " ]"
            print(output)


class Player():
    def __init__(self):
        self.block = False
        self.money = 30000
        self.position = 0
        self.name = ""
        self.id = False
        self.walked = False
        self.sprops = 0
        self.s2props = 0
        self.in_prison = False
        self.prison_counter = 0
        self.debt = []
        self.prison_card_e = False
        self.prison_card_c = False
        self.event_block = False
        self.last_message = ""
        self.conn = ""
        self.message_to_send = ""
        self.thread = ""
        self.response = ""



class Field():
    group = str()
    name = str()
    price = str()
    owned = bool()
    owner_id = "00000000"
    houses = 0
    type = str()
    rents = [0]
    morg = False

    def change_owner(self, id):
        owner_id = str(id)


def read_file(file, length, use_length=True, insert_before=False):
    print("here2")
    try:
        print(f"file name = /monopoly/{file}")
        print(sys.stdout.encoding)
        list = open("/monopoly/"+str(file), "r", encoding="utf-8").readlines()
    except Exception as e:
        print(e)
    print("file cor")
    for i in range(len(list)):
        list[i] = list[i].replace("\n", "")
        if use_length:
            if insert_before:
                while len(list[i]) < length:
                    list[i] = " " + list[i]
            else:
                while len(list[i]) < length:
                    list[i] += " "
    return list


def buy(player, field,server_controller, counter=0):
    sc = server_controller
    if counter == 10:
        sc.request("str", "You didnt buy the Field", player)
        return
    if field.price > player.money:
        sc.request("str", f"You dont have enough money, {field.price} to buy {field.name}", player)
        return
    decision = sc.request("str", f"Do you want to buy {field.name}, for {field.price}?", player).lower()
    if decision == "yes" or decision == "no":
        if decision == "yes":
            field.owned = True
            field.owner_id = player.id
            player.money -= field.price
            if field.type == "SPECIAL-PROPERTY":
                player.sprops += 1
            elif field.type == "SPECIAL-PROPERTY-2":
                player.s2props += 1
        if decision == "no":
            pass
            # auction shit yk yk
    else:
        buy(player, field, sc, counter=counter+1)

def draw_event_card(user, board, users, server_controller, custom_card=0, use_custom_card=False):
    sc = server_controller
    if use_custom_card:
        card = custom_card
    else:
        card = random.randint(0, 15)
    if card == 0:
        sc.request("str", f"onto {board[0].name}", user)
        user.position = 0
        user.money += 4000
    elif card == 1:
        sc.request("str", f"Back to {board[1].name}", user)
        user.position = 1
        land(user, board, users, sc)
    elif card == 2:
        sc.request("str", f"onto {board[5].name}", user)
        if 5 < user.position > 0:
            user.money += 4000
        user.position = 5
        land(user, board, users, sc)
    elif card == 3:
        sc.request("str", "onto the next trainstation", user)
        scam = list(str(user.position))
        while len(scam) < 2:
            scam = ["0"] + scam
        scam[1] = "5"
        scam = "".join(scam)
        user.position = int(scam)
        land(user, board=board, users=users, server_controller=sc)
    elif card == 4:
        sc.request("str", f"onto {board[39].name}", user)
        user.position = 39
        land(user, board=board, users=users, server_controller=sc)
    elif card == 5:
        flag = False
        for i in users:
            if i.prison_card_e:
                flag = True
        if flag:
            draw_event_card(user, board, users, sc)
        else:
            sc.request("str", "You've got a get out of prison free card", user)
            user.prison_card_e = True
    elif card == 6:
        sc.request("str", "You are now in prison", user)
        user.in_prison = True
        user.prison_counter = 0
        user.position = 10
    elif card == 7:
        sc.request("str", f"onto {board[11].name}", user)
        while user.position != 11:
            user.position += 1
            if user.position == 40:
                user.position = 0
            if user.position == 0:
                user.money += 4000
        land(user, board, users, sc)
    elif card == 8:
        sc.request("str", "PAY EVERYONE 1000", user)
        for i in users:
            if i != user:
                user.debt.append([i.id, 1000])
    elif card == 9:
        sc.request("str", "The Bank be like MONETEN +3000$", user)
        user.money += 3000
    elif card == 10:
        sc.request("str", "3 Steps back", user)
        for i in range(3):
            user.position -= 1
            if user.position == -1:
                user.position = 39
        land(user, board, users, sc)
    elif card == 11:
        sc.request("str", f"Onto {board[24].name}", user)
        while user.position != 24:
            user.position += 1
            if user.position == 40:
                user.position = 0
                user.money += 4000
        land(user, board, users, sc)
    elif card == 12:
        sc.request("str", "Bank be like MONETEN +1000$", user)
        user.money += 1000
    elif card == 13:
        p = ""
        while True:
            p = sc.request("str", "1. -200$, 2.Take community card ?", user).lower()
            if p == "1" or p == "2":
                break
        if p == "1":
            user.debt.append(["SYSTEM", 200])
        else:
            draw_community_card(user, board, users, sc)
    elif card == 14:
        sc.request("str", "YOU FOOL THIS IS A SPEED RESTRICTED ZONE -300$", user)
        user.debt.append(["SYSTEM", 300])
    else:
        sc.request("str", "YOU GOTTA PAY UP FOOL, 500$ for every house, capped at 2000$ per street", user)
        owned = []
        amount = 0
        for w_field in range(len((board))):
            if board[w_field].owner_id == user.id:
                owned.append(board[w_field])

        for i in owned:
            if i.houses > 4:
                amount += 2000
            else:
                amount += (i.houses*500)

        user.debt.append(["SYSTEM", amount])

def draw_community_card(user, board, users, server_controller, custom_card=0, use_custom_card=False):
    sc = server_controller
    if use_custom_card:
        card = custom_card
    else:
        card = random.randint(0, 15)
    if card == 0:
        sc.request("str", f"onto {board[0].name}", user)
        user.position = 0
        user.money += 4000
    elif card == 1:
        sc.request("str","Bank be like MONETEN +900$", user)
        user.money += 900
    elif card == 2:
        sc.request("str", "The bank says you pay 800$ per House per field or if you have 5 2300$ on that field", user)
        owned = []
        amount = 0
        for w_field in range(len(board)):
            if board[w_field].owner_id == user.id:
                owned.append(board[w_field])
        for i in owned:
            if i.houses > 4:
                amount += 2300
            else:
                amount += (800*i.houses)
        user.debt.append(["SYSTEM", amount])
    elif card == 3:
        sc.request("str", "bank be like MONETEN +2000$", user)
        user.money += 2000
    elif card == 4:
        sc.request("str", "You sold your old hentai +500$", user)
        user.money += 500
    elif card == 5:
        sc.request("str", "You were in a beauty-contest someone had pity with you and gave you 200$", user)
        user.money += 200
    elif card == 6:
        sc.request("str", "You broke your arm -2000$ doctor costs", user)
        user.debt.append(["SYSTEM", 2000])
    elif card == 7:
        sc.request("str", "You robbed a bank +4000$", user)
        user.money += 4000
    elif card == 8:
        sc.request("str", "It's your Cakeday +1000$ from everyone", user)
        for w_user in range(len(users)):
            if int(users[w_user].id) == int(user.id):
                pass
            else:
                users[w_user].debt.append([user.id, 1000])
    elif card == 9:
        sc.request("str", "You found a dead person in the streets +400$", user)
        user.money += 400
    elif card == 10:
        sc.request("str", "You caught a police officer commit arson +2000$", user)
        user.money += 2000
    elif card == 11:
        sc.request("str", "You killed your grandparent +2000$ inheritance", user)
        user.money += 2000
    elif card == 12:
        sc.request("str", "The police caught you slashing tires of the president -3000$", user)
        user.debt.append(["SYSTEM", 3000])
    elif card == 13:
        sc.request("str", "You didn't eat your apple today, the doctor came and charged you 1000$", user)
        user.debt.append(["SYSTEM", 1000])
    elif card == 14:
        sc.request("str", "You committed the naughties with the first lady thus you are in prison", user)
        user.in_prison = True
        user.prison_counter = 0
        user.position = 10
    else:
        flag = False
        for i in users:
            if i.prison_card_c:
                flag = True
        if flag:
            draw_community_card(user, board, users, sc)
        else:
            sc.request("str", "PRISON CARD", user)
            user.prison_card_c = True


def get_name_by_id(id, users):
    for user in users:
        if id == user.id:
            return user.name

def get_user_by_id(id, users):
    for user in users:
        if id == user.id:
            return user

def land(user, board, users, server_controller, system_id="SYSTEM", total=0):
    sc = server_controller

    position = user.position
    sc.request("str", f"You landed on {board[position].name}. Hit enter to proceed", user)
    type = board[position].type
    if type == "PROPERTY" or type == "SPECIAL-PROPERTY" or type == "SPECIAL-PROPERTY-2":
        if not board[position].owned:
            buy(user, board[position], sc)
        else:
            owner = get_user_by_id(board[position].owner_id, users)
            if owner:
                pass
            else:
                owner = Player()
                owner.id = "E"
            if user.id != owner.id:
                if not board[position].morg:
                    amount  = 0
                    if type == "PROPERTY":
                        amount = board[position].rents[board[position].houses]
                    elif type == "SPECIAL-PROPERTY":
                        if owner.sprops > 1:
                            if owner.sprops > 2:
                                if owner.sprops > 3:
                                    amount = 4000
                                else:
                                    amount = 2000
                            else:
                                amount = 1000
                        else:
                            amount = 500
                    elif type == "SPECIAL-PROPERTY-2":
                        if owner.s2props > 1:
                            amount = 200*total
                        else:
                            amount = 80*total
                    try:
                        user.debt.append([owner.id, amount])
                    except AttributeError:
                        user.debt.append([system_id, amount])
                    owe = amount
                    sc.send("str", f"You need to pay {get_name_by_id(board[position].owner_id, users)} {owe}$ ", user)
                    user.block = True
                else:
                    input("This property is \"HYPOTHEKIERT\"")

    if board[position].type == "PRISON":
        pass
    if board[position].type == "EVENT":
        draw_event_card(user, board, users, sc)
    if board[position].type == "COMMUNITY":
        draw_community_card(user, board, users, sc)
    if board[position].type == "PRISON-WARP":
        sc.send("str", "YOU WENT TO PRISON MY GUY", user)
        user.position = 10
        user.in_prison = True
        user.prison_counter = 0


def make_board():
    system_id = "SYSTEM"
    print("here")
    names = read_file("names.txt", 10, insert_before=False)
    print("read names")
    prices = read_file("prices.txt", 5)
    print("read prices")
    types = read_file("types.txt", 0, use_length=False)
    print("read types")
    rents = read_file("rents.txt", 0, use_length=False)
    print("read rents")
    group = read_file("groups.txt", 0, use_length=False)
    print("read groups")
    print("read all files")
    temp = []
    for i in rents:
        single = i.split(":")
        for x in range(len(single)):
            single[x] = int(single[x])
        temp.append(i.split(":"))
    rents = temp

    board = {}
    for i in range(40):
        board[i] = Field()
        board[i].name = names[i]
        board[i].price = int(prices[i])
        board[i].type = types[i]
        if board[i].type == "TAX":
            board[i].owner_id = system_id
            board[i].owned = True
            board[i].type = "PROPERTY"
        if board[i].type == "PROPERTY":
            board[i].rents = rents[i]
        if board[i].type != "PROPERTY" and board[i].type != "SPECIAL-PROPERTY" and board[
            i].type != "SPECIAL-PROPERTY-2":
            board[i].owned = True
            board[i].houses = 1
            board[i].owner_id = system_id
        board[i].group = group[i]

    return board

