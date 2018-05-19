import libtcodpy as libtcod
from game_messages import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results=[]
        alreadyin = False
        for initems in self.items:
            if initems.name == item.name and initems.stack == True and item.stack == True:
                alreadyin = True
                initems.stack_amount += item.stack_amount
                break
        if alreadyin:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}'.format(item.name))
            })
        else:
            if len(self.items) >= self.capacity:
                results.append({
                    'item_added': None,
                    'message': Message('You can\'t pick that up, your inventory is full!')
                })
            else:
                results.append({
                    'item_added': item,
                    'message': Message('You pick up the {0}'.format(item.name))
                })
                self.items.append(item)
        return results

    def use(self, item_entity, **kwargs):
        results = []
        item_component = item_entity.item
        if item_component.use_function is None:
            results.append({'message': Message('The {0} cannot be used'.format(item_entity.name))})
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity, 1, False)
            results.extend(item_use_results)
        return results

    def remove_item(self, item, amount, all):
        if item.stack == True and item.stack_amount > 0+amount and all == False:
            item.stack_amount -= amount
        else:
            self.items.remove(item)


    def drop_item(self, item):
        results = []
        item.x = self.owner.x
        item.y = self.owner.y
        self.remove_item(item, 0, True)
        results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name))})
        return results