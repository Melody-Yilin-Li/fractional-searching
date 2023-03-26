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
    print("group")
    pass
    # incumbent_utility1 = models.IntegerField()
    # incumbent_demand1 = models.IntegerField()
    # incumbent_payoff1 = models.IntegerField()
    # entrant_utility1 = models.IntegerField()
    # entrant_demand1 = models.IntegerField()
    # entrant_payoff1 = models.IntegerField()
    # status = models.BooleanField()
    # incumbent_utility2 = models.IntegerField()
    # incumbent_demand2 = models.IntegerField()
    # incumbent_payoff2 = models.IntegerField()
    # entrant_utility2 = models.IntegerField()
    # entrant_demand2 = models.IntegerField()
    # entrant_payoff2 = models.IntegerField()

    # def set_payoffs(self):
    #     if self.subsession.treat == 'OL':

        
    #     elif self.subsession.treat == 'CC':

    #     elif self.subsession.treat == 'FC':



class Player(BasePlayer):
    print("player")
    pass

    # quality = models.IntegerField(
    #     choices=[
    #         [0, 'X'],
    #         [1, 'Y'], 
    #     ],
    #     widget=widgets.RadioSelect
    # )

    # price1 = models.IntegerField()

    # price2 = models.IntegerField()

    # def player_role(self):
    #     if self.id_in_group % 2:
    #         return 'incumbent'
    #     else:
    #         return 'entrant'

    

# PAGES
class Welcome(Page):
    pass
    # def is_displayed(self):
    #     return self.round_number == 1

    # def vars_for_template(self):
    #     return {'num_rounds': self.num_rounds} 

class Instruction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'num_rounds': C.NUM_ROUNDS}

class Stage1Quality(Page):
    def vars_for_template(self):
        print(self.subsession)

    # pass
    # form_model = 'player'
    # form_fields = ['quality']

class Stage2Price(Page):
    pass
    # form_model = 'player'
    # form_fields = ['price1']

class Stage3Price(Page):
    pass
    # form_model = 'player'
    # form_fields = ['price2']

class WaitPage(WaitPage):
    pass
    # def is_displayed(self):
    #     return self.round_number <= self.subsession.num_rounds

class Results(Page):
    pass
    # def is_displayed(self):
    #     return self.round_number <= self.subsession.num_rounds

    # def vars_for_template(self):
    #     return {
    #         'cumulative_payoff': sum([p.payoff for p in self.in_all_rounds()])
    #     }



page_sequence = [
    Welcome,
    Instruction,
    # Stage1Quality
]
