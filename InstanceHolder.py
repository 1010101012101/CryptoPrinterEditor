
__instances = []

def add_instance(instance, name):
    newinstance = {'name': name, 'instance': instance}
    __instances.append(newinstance)

def get_instance(name):
    for instance in __instances:
        if instance['name'] is name:
            return instance['instance']