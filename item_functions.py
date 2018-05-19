import libtcodpy as libtcod

from game_messages import Message

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')
    results = []
    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health.')})
    else:
        results.append(entity.fighter.heal(amount))
        results.append({'consumed': True, 'message': Message('Your wounds stitch themselves closed!', libtcod.green)})
    return results