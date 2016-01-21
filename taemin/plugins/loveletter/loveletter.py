#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Mon super LoveLetter """

import random

class Card(object):
    def __init__(self, name):
        self.name = name
        self.description = None
        self.value = 0
        self.need_player = False
        self.need_card = False
        self.normalize()

    def __repr__(self):
        return "<Card %s>" % self.name

    def __str__(self):
        return "<Card %s>" % self.name

    def normalize(self):
        if self.name == "guard":
            self.description = "Name a non-Guard card and choose another player. If that player has that card, he or she is out of the round"
            self.value = 1
            self.need_player = True
            self.need_card = True
        elif self.name == "priest":
            self.description = "Look at another player's hand"
            self.value = 2
            self.need_player = True
        elif self.name == "baron":
            self.description = "You and another player secretly compare hands. The player with the lower value is out of the round."
            self.value = 3
            self.need_player = True
        elif self.name == "handmaid":
            self.description = "Until your next turn, ignore all effects from other player's cards."
            self.value = 4
        elif self.name == "prince":
            self.description = "Choose any player (including youserlf) to discard his or her hand and draw a new card"
            self.value = 5
            self.need_player = True
        elif self.name == "king":
            self.description = "Trade hands with another player of your choice."
            self.value = 6
            self.need_player = True
        elif self.name == "countess":
            self.description = "If you have this card and the King or Prince in your hand, you must discard this card."
            self.value = 7
        elif self.name == "princess":
            self.description = "If you discard this card, you are out of the round"
            self.value = 8

class Player(object):
    def __init__(self, loveletter, name):
        self.game = loveletter
        self.cards = []
        self.name = name
        self.shield = False

    def __repr__(self):
        return "<Player %s>" % self.name

    def __str__(self):
        return "<Player %s>" % self.name

    def draw_card(self):
        if len(self.cards) > 2:
            raise NameError("Pas plus de deux cartes par joueur !")

        card = self.game.cards.pop()

        if not card:
            if not self.cards:
                self.game.kill_player(self)

            self.game.find_winner()
        else:
            self.cards.append(card)

    def active_card(self):
        if self.cards:
            return self.cards[0]
        else:
            return None

    def play(self, card, player=None, target_card=None):
        if not self.game.started:
            raise NameError("Partie pas encore commencée")
        if self != self.game.next_player():
            raise NameError("Ce n'est pas ton tour de jouer, c'est à %s" % self.game.next_player())

        return self.play_card(card, player, target_card)

    def trash_card(self):
        card = self.cards.pop()
        if card and card.value == 8:
            self.game.kill_player(self)
        return card

    def play_card(self, card, player=None, target_card=None):
        if player:
            player = player.lower()

        if card not in self.cards:
            raise ValueError("Euh tu as pas cette carte mon bonhomme")

        if (not player or player not in self.game.players) and card.need_player:
            raise ValueError("Besoin de spécifier la cible")

        if not target_card and card.need_card:
            raise ValueError("Besoin de spécifier une carte")

        if self.active_card().value == 7 and card.value in (5, 6):
            raise ValueError("Tu dois jouer ta comptesse :p")

        if player:
            player = self.game.players[player]
        if target_card:
            target_card = Card(target_card)
            if target_card.value == 1:
                raise ValueError("On ne peut pas cibler un garde :p")

        self.shield = False
        self.cards.remove(card)
        self.game.last_played = self

        msg = ""

        if player and player.shield:
            msg = "Protect by handmaid"
        else:
            if card.value == 1:
                if target_card.value == player.active_card().value:
                    self.game.kill_player(player)
                    msg = "%s a tué le %s de %s" % (self.name, target_card.name, player.name)
                else:
                    msg = "Le garde a frappé dans le vide..."

            elif card.value == 2:
                msg = "PRIV %s" % player.active_card().name

            elif card.value == 3:
                if self.active_card().value > player.active_card().value:
                    self.game.kill_player(player)
                    msg = "%s a tué le %s de %s" % (self.name, player.active_card(), player.name)

                elif self.active_card().value < player.active_card().value:
                    self.game.kill_player(self)
                    msg = "%s a tué le %s de %s" % (player.name, target_card.name, self.name)

            elif card.value == 4:
                self.shield = True
                msg = "%s est maintenant protégé" % (self.name)
            elif card.value == 5:
                trash_card = player.trash_card()
                player.draw_card()
                msg = "%s a jeté son %s" % (player.name, trash_card.name)
            elif card.value == 6:
                cards = player.cards
                player.cards = self.cards
                self.cards = cards
                msg = "%s est %s ont échangé leur cartes" % (player.name, self.name)
            elif card.value == 7:
                msg = "%s a jeté sa comptesse" % self.name
            elif card.value == 8:
                self.game.kill_player(self)
                msg = "%s est mort en jetant sa princesse" % self.name

        if not self.game.cards:
            self.game.find_winner()

        self.game.next_player().draw_card()

        return msg

class LoveLetter(object):
    def __init__(self):
        self.cards = []
        for card in ["guard", "guard", "guard", "guard", "guard",
                     "priest", "priest",
                     "baron", "baron",
                     "handmaid", "handmaid",
                     "prince", "prince",
                     "king", "countess", "princess"]:
            self.cards.append(Card(card))
        random.shuffle(self.cards)

        self.players = {}
        self.turn = []
        self.last_played = None
        self.started = False
        self.winner = None

    def add_player(self, name):
        name = name.lower()
        if name in self.players:
            raise NameError("Cette personne joue déjà !!!")
        if self.started:
            raise NameError("La partie a déjà commencé, attendez la suivante !")

        self.players[name] = Player(self, name)
        self.turn.append(self.players[name])

    def kill_player(self, player):
        self.players.pop(player.name, None)
        if len(self.players.keys()) <= 1:
            self.find_winner()
        return player

    def next_player(self):
        if self.last_played:
            idx = self.turn.index(self.last_played)
            if idx >= len(self.turn) - 1:
                idx = 0
            else:
                idx += 1
        else:
            idx = 0
        if self.turn[idx].name not in self.players:
            self.last_played = self.turn[idx]
            return self.next_player()

        return self.turn[idx]

    def restart(self):
        self.__init__()

    def start(self):
        if len(self.turn) < 2:
            raise ValueError("Il faut au moins 2 joueurs")
        if self.started:
            raise ValueError("La partie a déjà commencé, attendez la suivante !")

        for player in self.turn:
            player.draw_card()

        random.shuffle(self.turn)
        self.next_player().draw_card()
        self.started = True

    def play(self, player_name, card_name, target_player=None, target_card=None):
        player = self.players.get(player_name.lower())
        if not player:
            raise NameError("Tu n'es pas dans la partie")

        for p_card in player.cards:
            if p_card.name.lower() == card_name.lower():
                card = p_card

        if not card:
            raise NameError("Euh tu n'as pas cette carte mon bonhomme")

        return player.play(card, target_player, target_card)

    def next_play(self, card, player=None, target_card=None):
        return self.next_player().play(card, player, target_card)

    def find_winner(self):
        plyr = None
        mx = 0
        if not self.started:
            return plyr
        elif len(self.players.keys()) == 1:
            plyr = self.players.values()[0]
        elif not self.cards:
            for player in self.players.itervalues():
                if player.active_card() and player.active_card().value > mx:
                    mx = player.active_card().value
                    plyr = player
        return plyr

    def print_state(self):
        msg = "Partie avec : %s\n" % str(self.turn)
        if not self.started:
            msg += "Partie pas encore commencé"
        elif self.winner:
            msg += "Partie gagné par %s" % self.winner.name
        else:
            msg += "Il reste %d cartes, c'est à %s de jouer" % (len(self.cards), self.next_player().name)

        return msg


if __name__ == "__main__":
    game = LoveLetter()
    game.add_player("taemin")
    game.add_player("miku")
    game.start()

