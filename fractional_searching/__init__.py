from otree.api import *
import csv
import random
import math

author = 'Yilin Li'

doc = """
Experiment testing the fractional searching algorithm 
"""
 
class C(BaseConstants):
    NAME_IN_URL = 'fractional_searching'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 15

def creating_session(subsession):
    subsession.group_randomly()
    round_number = subsession.round_number
    with open('fractional_searching/config/config.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i + 1 == round_number:
                print(row)
                subsession.round_number = int(row['round'])
                subsession.utility_h = int(row['utility_h'])
                subsession.utility_l = int(row['utility_l'])
                subsession.utility_m = int(row['utility_m'])
                subsession.cost = int(row['cost'])
                subsession.cost_i = int(row['cost_i'])
                subsession.cost_e = int(row['cost_e'])
                subsession.search = int(row['search'])
                subsession.treat = row['treat']

class Subsession(BaseSubsession):
    utility_h = models.IntegerField()
    utility_l = models.IntegerField()
    utility_m = models.IntegerField()
    cost = models.IntegerField()
    cost_i = models.IntegerField()
    cost_e = models.IntegerField()
    search = models.IntegerField()
    treat = models.StringField()


class Group(BaseGroup):
    incumbent_utility1 = models.IntegerField()
    incumbent_demand1 = models.IntegerField()
    incumbent_payoff1 = models.IntegerField()
    entrant_utility1 = models.IntegerField()
    entrant_demand1 = models.IntegerField()
    entrant_payoff1 = models.IntegerField()
    status = models.BooleanField()
    incumbent_utility2 = models.IntegerField()
    incumbent_demand2 = models.IntegerField()
    incumbent_payoff2 = models.IntegerField()
    entrant_utility2 = models.IntegerField()
    entrant_demand2 = models.IntegerField()
    entrant_payoff2 = models.IntegerField()


class Player(BasePlayer):
    quality = models.IntegerField(
        choices=[
            [0, 'X'],
            [1, 'Y'], 
        ],
        widget=widgets.RadioSelect,
        label='Please choose your product type: ',
        blank=False,
    )

    price1 = models.IntegerField(
        label='Please enter the price (integer only) you want to charge for your product in stage 2: ',
        blank=False,
    )

    price2 = models.IntegerField(
        label='Please enter the price (integer only) you want to charge for your product in stage 3: ',
        blank=False,
    )

    def player_role(self):
        if self.id_in_group % 2:
            return 'incumbent'
        else:
            return 'entrant'

    def set_payoffs(self):
        if self.player_role() == 'incumbent':
            self.payoff = self.group.incumbent_payoff1 + self.group.incumbent_payoff2
        else:
            self.payoff = self.group.entrant_payoff1 + self.group.entrant_payoff2

def price1_min(player):
    if player.player_role() == 'incumbent': 
        return player.subsession.cost if player.quality == 0 else player.subsession.cost_i 
    else:
        return player.subsession.cost if player.quality == 0 else player.subsession.cost_e

def price1_max(player):
    if player.player_role() == 'incumbent': 
        return player.subsession.utility_l if player.quality == 0 else player.subsession.utility_h
    else:
        if player.subsession.treat == 'OL':
            return player.subsession.utility_l if player.quality == 0 else player.subsession.utility_h
        else:
            return player.subsession.utility_m 

def price2_min(player):
    if player.player_role() == 'incumbent': 
        return player.subsession.cost if player.quality == 0 else player.subsession.cost_i 
    else:
        return player.subsession.cost if player.quality == 0 else player.subsession.cost_e

def price2_max(player):
    if player.player_role() == 'incumbent' or player.subsession.treat == 'OL': 
        return player.subsession.utility_l if player.quality == 0 else player.subsession.utility_h
    else:
        if player.group.entrant_demand1 > 0: 
            return player.subsession.utility_l if player.quality == 0 else player.subsession.utility_h
        else:
            return player.subsession.utility_m 
    

# PAGES
class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'num_rounds': C.NUM_ROUNDS} 

class Instruction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': C.NUM_ROUNDS,
            'treat': self.subsession.treat, 
            'search': self.subsession.search, 
            'rest': 100 - self.subsession.search, 
        }
class IncumbentQuality(Page):
    def is_displayed(self):
        return self.subsession.treat != 'OL' and self.player_role() == 'incumbent'

    form_model = 'player'
    form_fields = ['quality']

    @staticmethod
    def vars_for_template(self):
        return {
            'round_number': self.subsession.round_number, 
            'utility_h': self.subsession.utility_h, 
            'utility_l': self.subsession.utility_l, 
            'utility_m': self.subsession.utility_m, 
            'cost': self.subsession.cost, 
            'cost_i': self.subsession.cost_i, 
            'cost_e': self.subsession.cost_e, 
            'search': self.subsession.search, 
            'treat': self.subsession.treat, 
            'role': 'Player A' if self.player_role() == 'incumbent' else 'Player B', 
            'rest': 100 - self.subsession.search, 
        }
class SequentialWaitPage(WaitPage):
    pass

class EntrantQuality(Page):
    def is_displayed(self):
        return self.subsession.treat != 'OL' and self.player_role() == 'entrant'

    form_model = 'player'
    form_fields = ['quality']

    @staticmethod
    def vars_for_template(self):
        players = self.group.get_players()
        for p in players:
            if p.id_in_group != self.id_in_group: 
                opponent = p
        return {
            'round_number': self.subsession.round_number, 
            'utility_h': self.subsession.utility_h, 
            'utility_l': self.subsession.utility_l, 
            'utility_m': self.subsession.utility_m, 
            'cost': self.subsession.cost, 
            'cost_i': self.subsession.cost_i, 
            'cost_e': self.subsession.cost_e, 
            'search': self.subsession.search, 
            'treat': self.subsession.treat, 
            'role': 'Player A' if self.player_role() == 'incumbent' else 'Player B', 
            'rest': 100 - self.subsession.search, 
            'opponent_quality': 'Y' if opponent.quality else 'X',
        }

class Stage1Quality(Page):
    def is_displayed(self):
        return self.subsession.treat == 'OL'

    form_model = 'player'
    form_fields = ['quality']

    @staticmethod
    def vars_for_template(self):
        return {
            'round_number': self.subsession.round_number, 
            'utility_h': self.subsession.utility_h, 
            'utility_l': self.subsession.utility_l, 
            'utility_m': self.subsession.utility_m, 
            'cost': self.subsession.cost, 
            'cost_i': self.subsession.cost_i, 
            'cost_e': self.subsession.cost_e, 
            'search': self.subsession.search, 
            'treat': self.subsession.treat, 
            'role': 'Player A' if self.player_role() == 'incumbent' else 'Player B', 
            'rest': 100 - self.subsession.search, 
        }
    

class Stage2Price(Page):
    form_model = 'player'
    form_fields = ['price1']

    @staticmethod
    def vars_for_template(self):
        utility = {0: self.subsession.utility_l, 1: self.subsession.utility_h}
        costs_i = {0: self.subsession.cost, 1: self.subsession.cost_i}
        costs_e = {0: self.subsession.cost, 1: self.subsession.cost_e}
        players = self.group.get_players()
        for p in players:
            if p.id_in_group != self.id_in_group: 
                opponent = p
        for p in players:
            if self.player_role() == p.player_role() == 'incumbent':
                opponent_value = utility[opponent.quality] if self.subsession.treat == 'OL' else self.subsession.utility_m
            elif self.player_role() == p.player_role() == 'entrant':
                opponent_value = utility[opponent.quality]
        return {
            'round_number': self.subsession.round_number, 
            'utility_h': self.subsession.utility_h, 
            'utility_l': self.subsession.utility_l, 
            'utility_m': self.subsession.utility_m, 
            'cost': self.subsession.cost, 
            'cost_i': self.subsession.cost_i, 
            'cost_e': self.subsession.cost_e, 
            'search': self.subsession.search, 
            'treat': self.subsession.treat, 
            'role': 'Player A' if self.player_role() == 'incumbent' else 'Player B', 
            'rest': 100 - self.subsession.search, 
            'type': 'Y' if self.quality else 'X', 
            'utility': self.subsession.utility_h if self.quality else self.subsession.utility_l,
            'opponent_quality': 'Y' if opponent.quality else 'X',  
            'opponent_role': 'Player B' if self.player_role() == 'incumbent' else 'Player A', 
            'opponent_cost': costs_i[opponent.quality] if opponent.player_role() == 'incumbent' else costs_e[opponent.quality], 
            'opponent_value': opponent_value, 
        }

class Calculation(Page):
    def is_displayed(self):
        utility = {0: self.subsession.utility_l, 1: self.subsession.utility_h}
        costs_i = {0: self.subsession.cost, 1: self.subsession.cost_i}
        costs_e = {0: self.subsession.cost, 1: self.subsession.cost_e}
        players = self.group.get_players()
        incumbent_value = entrant_value = 0
        for p in players:
            if p.player_role() == 'incumbent':
                p.group.incumbent_utility1 = utility[p.quality] - p.price1
                incumbent_value = utility[p.quality]
            else:
                if p.subsession.treat == 'OL':
                    p.group.entrant_utility1 = utility[p.quality] - p.price1
                    entrant_value = utility[p.quality]
                else:
                    p.group.entrant_utility1 = p.subsession.utility_m - p.price1
                    entrant_value = p.subsession.utility_m
        if self.subsession.treat != 'FC':
            if self.group.incumbent_utility1 > self.group.entrant_utility1:
                self.group.incumbent_demand1 = 100 
                self.group.entrant_demand1 = 0
            elif self.group.incumbent_utility1 == self.group.entrant_utility1: 
                if incumbent_value > entrant_value:
                    self.group.incumbent_demand1 = 100 
                    self.group.entrant_demand1 = 0
                elif incumbent_value < entrant_value:
                    self.group.incumbent_demand1 = 0
                    self.group.entrant_demand1 = 100
                else: 
                    self.group.incumbent_demand1 = self.group.entrant_demand1 = 50
            else:
                self.group.incumbent_demand1 = 0
                self.group.entrant_demand1 = 100
        else:
            if self.group.incumbent_utility1 >= 0:
                self.group.incumbent_demand1 = 100 - self.subsession.search
            if self.group.entrant_utility1 >= 0:
                self.group.entrant_demand1 = self.subsession.search
        if self.group.entrant_demand1 > 0: 
            self.group.status = 1
        else:
            self.group.status = 0
        for p in players:
            if self.player_role() == p.player_role() == 'incumbent':
                p.group.incumbent_payoff1 = p.group.incumbent_demand1 * (p.price1 - costs_i[p.quality])
            elif self.player_role() == p.player_role() == 'entrant':
                p.group.entrant_payoff1 = p.group.entrant_demand1 * (p.price1 - costs_e[p.quality])
        return False


class Stage3Price(Page):
    form_model = 'player'
    form_fields = ['price2']

    @staticmethod
    def vars_for_template(self):
        utility = {0: self.subsession.utility_l, 1: self.subsession.utility_h}
        costs_i = {0: self.subsession.cost, 1: self.subsession.cost_i}
        costs_e = {0: self.subsession.cost, 1: self.subsession.cost_e}
        players = self.group.get_players()
        for p in players:
            if p.id_in_group != self.id_in_group: 
                opponent = p
        for p in players:
            if self.player_role() == p.player_role() == 'incumbent':
                opponent_value = utility[opponent.quality] if p.group.entrant_demand1 > 0 else self.subsession.utility_m
            elif self.player_role() == p.player_role() == 'entrant':
                opponent_value = utility[opponent.quality]
        return {
            'round_number': self.subsession.round_number, 
            'utility_h': self.subsession.utility_h, 
            'utility_l': self.subsession.utility_l, 
            'utility_m': self.subsession.utility_m, 
            'cost': self.subsession.cost, 
            'cost_i': self.subsession.cost_i, 
            'cost_e': self.subsession.cost_e, 
            'search': self.subsession.search, 
            'treat': self.subsession.treat, 
            'role': 'Player A' if self.player_role() == 'incumbent' else 'Player B', 
            'rest': 100 - self.subsession.search, 
            'entry': self.group.status, 
            'type': 'Y' if self.quality else 'X', 
            'utility': self.subsession.utility_h if self.quality else self.subsession.utility_l,
            'demand1': self.group.incumbent_demand1 if self.player_role() == 'incumbent' else self.group.entrant_demand1, 
            'price1': self.price1,
            'payoff1': self.group.incumbent_payoff1 if self.player_role() == 'incumbent' else self.group.entrant_payoff1, 
            'opponent_quality': 'Y' if opponent.quality else 'X',  
            'opponent_role': 'Player B' if self.player_role() == 'incumbent' else 'Player A', 
            'opponent_price1': opponent.price1, 
            'opponent_cost': costs_i[opponent.quality] if opponent.player_role() == 'incumbent' else costs_e[opponent.quality], 
            'opponent_value': opponent_value, 
        }

class Stage1WaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass 

class Stage2WaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass 

class Stage3WaitPage(WaitPage):
    pass

class Results(Page):
    @staticmethod
    def vars_for_template(self): 
        utility = {0: self.subsession.utility_l, 1: self.subsession.utility_h}
        costs_i = {0: self.subsession.cost, 1: self.subsession.cost_i}
        costs_e = {0: self.subsession.cost, 1: self.subsession.cost_e}
        players = self.group.get_players()
        incumbent_value = entrant_value = 0
        for p in players:
            if p.id_in_group != self.id_in_group: 
                opponent = p
            if p.player_role() == 'incumbent':
                p.group.incumbent_utility2 = utility[p.quality] - p.price2
                incumbent_value = utility[p.quality]
            else:
                if p.subsession.treat == 'OL' or self.group.status:
                    p.group.entrant_utility2 = utility[p.quality] - p.price2
                    entrant_value = utility[p.quality]
                else:
                    p.group.entrant_utility2 = p.subsession.utility_m - p.price2
                    entrant_value = p.subsession.utility_m
        if self.group.incumbent_utility2 > self.group.entrant_utility2:
            self.group.incumbent_demand2 = 100 
            self.group.entrant_demand2 = 0
        elif self.group.incumbent_utility2 == self.group.entrant_utility2: 
            if incumbent_value > entrant_value:
                self.group.incumbent_demand2 = 100 
                self.group.entrant_demand2 = 0
            elif incumbent_value < entrant_value:
                self.group.incumbent_demand2 = 0
                self.group.entrant_demand2 = 100
            else: 
                self.group.incumbent_demand2 = self.group.entrant_demand2 = 50
        else:
            self.group.incumbent_demand2 = 0
            self.group.entrant_demand2 = 100
        
        for p in players:
            if self.player_role() == p.player_role() == 'incumbent':
                p.group.incumbent_payoff2 = p.group.incumbent_demand2 * (p.price2 - costs_i[p.quality])
                opponent_value = utility[opponent.quality] if p.group.entrant_demand2 > 0 else self.subsession.utility_m
            elif self.player_role() == p.player_role() == 'entrant':
                p.group.entrant_payoff2 = p.group.entrant_demand2 * (p.price2 - costs_e[p.quality])
                opponent_value = utility[opponent.quality]
        self.set_payoffs()
        return {
            'round_number': self.subsession.round_number, 
            'utility_h': self.subsession.utility_h, 
            'utility_l': self.subsession.utility_l, 
            'utility_m': self.subsession.utility_m, 
            'cost': self.subsession.cost, 
            'cost_i': self.subsession.cost_i, 
            'cost_e': self.subsession.cost_e, 
            'search': self.subsession.search, 
            'treat': self.subsession.treat, 
            'role': 'Player A' if self.player_role() == 'incumbent' else 'Player B', 
            'rest': 100 - self.subsession.search, 
            'entry': self.group.status,
            'type': 'Y' if self.quality else 'X', 
            'utility': self.subsession.utility_h if self.quality else self.subsession.utility_l,
            'demand1': self.group.incumbent_demand1 if self.player_role() == 'incumbent' else self.group.entrant_demand1, 
            'demand2': self.group.incumbent_demand2 if self.player_role() == 'incumbent' else self.group.entrant_demand2, 
            'price1': self.price1,
            'price2': self.price2,
            'payoff1': self.group.incumbent_payoff1 if self.player_role() == 'incumbent' else self.group.entrant_payoff1, 
            'payoff2': self.group.incumbent_payoff2 if self.player_role() == 'incumbent' else self.group.entrant_payoff2, 
            'opponent_quality': 'Y' if opponent.quality else 'X',  
            'opponent_role': 'Player B' if self.player_role() == 'incumbent' else 'Player A', 
            'opponent_price2': opponent.price2, 
            'opponent_cost': costs_i[opponent.quality] if opponent.player_role() == 'incumbent' else costs_e[opponent.quality], 
            'opponent_value': opponent_value, 
            'cumulative_payoff': sum([p.payoff for p in self.in_all_rounds()]), 
            'round_payoff': self.payoff, 
        }

class FinalResults(Page):
    def is_displayed(self):
        return self.subsession.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(self):
        rounds = self.in_all_rounds()
        payoffs = [p.payoff for p in rounds]
        total_payoff = sum(payoffs)
        return {
            'payoffs': payoffs, 
            'total_payoff': total_payoff, 
        }


page_sequence = [
    Welcome,
    Instruction,
    IncumbentQuality,
    SequentialWaitPage,
    EntrantQuality,
    Stage1Quality,
    Stage1WaitPage,
    Stage2Price, 
    Stage2WaitPage, 
    Calculation, 
    Stage3Price, 
    Stage3WaitPage,
    Results, 
    FinalResults,
]
