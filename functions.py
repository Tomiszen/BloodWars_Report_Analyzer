def list_to_dict(list_to_convert, split_string=' poz. '):
    return {item.split(split_string)[0]: int(item.split(split_string)[1])
            for item in list_to_convert if split_string in item}


def translate_parameter(parameter, language):
    vocabulary = {'pl': {'strength': 'siła',
                         'agility': 'zwinność',
                         'toughness': 'odporność',
                         'appearance': 'wygląd',
                         'charisma': 'charyzma',
                         'reputation': 'wpływy',
                         'perception': 'spostrzegawczość',
                         'intelligence': 'inteligencja',
                         'knowledge': 'wiedza',
                         'initiative': 'inicjatywa',
                         'hp': 'punkty życia',
                         'defence': 'obrona',
                         'luck': 'szczęście'
                         },
                  'en': {'strength': 'strength',
                         'agility': 'agility',
                         'toughness': 'toughness',
                         'appearance': 'appearance',
                         'charisma': 'charisma',
                         'reputation': 'reputation',
                         'perception': 'perception',
                         'intelligence': 'intelligence',
                         'knowledge': 'knowledge',
                         'initiative': 'inicjatywa',
                         'hp': 'punkty życia',
                         'defence': 'obrona',
                         'luck': 'szczęście'
                         }
                  }
    return vocabulary[language][parameter]
