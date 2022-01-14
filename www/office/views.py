import random
import datetime as dt
from django.shortcuts import render

# Create your views here.
context = {
    "GATES": {
        1: {
            "label": "First",
            "waiters": []
        },
        2: {
            "label": "Seccond",
            "waiters": []
        },
        3: {
            "label": "Third",
            "waiters": []
        }
    },
    "Peoples": {},
    "Logs": {
        'Logs_activate': False,
        1: {
            'label': "low",
            'color': 'white',
            'data': []
        },
        2: {
            'label': "mid",
            'color': 'yellow',
            'data': []
        },
        3: {
            'label': "high",
            'color': 'red',
            'data': []
        },
    }
}

print(context)


def index(request):
    global context
    move_gate = request.GET.get('move_gate')
    move_people = request.GET.get('move_people')
    add = request.GET.get('add')
    logs = request.GET.get('logs')
    refresh = request.GET.get('refresh')

    if add:
        add_people(1)

    if move_gate:
        gate = int(move_gate)
        move_from_gate(gate)

    if move_people:
        people_id = int(move_people)
        move_spec_people(people_id)

    if logs:
        context['Logs']["Logs_activate"] = not context['Logs']["Logs_activate"]

    if refresh:
        context['Logs']["Logs_activate"] = False

    if add is None and move_gate is None and logs is None and refresh is None and move_people is None:
        setup_index(1)

    return render(request, 'index.html', context)


def add_people(gate):
    global context
    persons = len(context['Peoples'])
    new_person_id = persons + 1
    position = len(context['GATES'][gate]['waiters'])+1
    context['Peoples'][new_person_id] = {
        "id": new_person_id,
        "gate": gate,
        "positon": position
    }
    context['GATES'][gate]['waiters'].append(new_person_id)
    log(2, f"Spawnut Člověk {new_person_id}, byl přiřazen na přepážku {context['GATES'][gate]['label']} a je na pozici {position}")


def move_from_gate(gate):
    global context
    if len(context['GATES'][gate]['waiters']) != 0:
        people_position = 0
        people_to_move = context['GATES'][gate]['waiters'][people_position]
        context['GATES'][gate]['waiters'].remove(people_to_move)
        gate += 1
        if gate <= len(context['GATES']):
            context['GATES'][gate]['waiters'].append(people_to_move)
            position = len(context['GATES'][gate]['waiters'])
            update_people(people_to_move, gate, position)
            log(2, f"Člověk {people_to_move}, byl přiřazen na přepážku {context['GATES'][gate]['label']} a je na pozici {position}")
        else:
            update_people(people_to_move, "remove", 0)
            log(3, f"Člověk {people_to_move}, byl odstraněn")
            context['Logs']["Logs_activate"] = True


def move_spec_people(id):
    global context
    for people in context['Peoples']:
        if people == id:
            gate = context['Peoples'][id]['gate']
            context['GATES'][gate]['waiters'].remove(id)
            gate += 1
            if gate <= len(context['GATES']):
                context['GATES'][gate]['waiters'].append(id)
                position = len(context['GATES'][gate]['waiters'])
                update_people(id, gate, position)
                log(2, f"Člověk {id}, byl přiřazen na přepážku {context['GATES'][gate]['label']} a je na pozici {position}")
            else:
                update_people(id, "remove", 0)
                log(3, f"Člověk {id}, byl odstraněn")
                context['Logs']["Logs_activate"] = True


def update_people(id, gate, position):
    global context
    context['Peoples'][id]['gate'] = gate
    context['Peoples'][id]['position'] = position
    log(1, f"Člověk id {id}, byl aktualizován")


def setup_index(gate):
    global context
    context = {
        "GATES": {
            1: {
                "label": "First",
                "waiters": []
            },
            2: {
                "label": "Seccond",
                "waiters": []
            },
            3: {
                "label": "Third",
                "waiters": []
            }
        },
        "Peoples": {},
        "Logs": {
            'Logs_activate': False,
            1: {
                'label': "low",
                'color': 'white',
                'data': []
            },
            2: {
                'label': "mid",
                'color': 'yellow',
                'data': []
            },
            3: {
                'label': "high",
                'color': 'red',
                'data': []
            },
        }
    }
    position = 0
    for i in range(1, random.randint(5, 22)):
        position += 1
        context['Peoples'][i] = {
            "id": i,
            "gate": gate,
            "positon": position
        }
        context['GATES'][gate]['waiters'].append(i)
        log(1, f"Člověk {i}, byl přiřazen na přepážku {context['GATES'][gate]['label']} a je na pozici {position}")


def log(level, string):
    string = string + ' |  Time: ' + str(dt.datetime.now())
    context['Logs'][level]['data'].append(string)
