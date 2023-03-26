from otree.api import settings

def get_subsession_config():
    config_file = settings.BASE_DIR/fractional_searching/config/config.csv 
    with open(config_file, 'r') as f:
        reader =csv.DictReader(f)
        config = next(reader)
    return congfig

subsession_config = get_subsession_config()
round_number = subsession_config['round']
utility_h = subsession_config['utility_h']
utility_l = subsession_config['utility_l']
utility_m = subsession_config['utility_m']
cost = subsession_config['cost']
cost_i = subsession_config['cost_i']
cost_e = subsession_config['cost_e']
search = subsession_config['search'] 
treat  = subsession['treat']