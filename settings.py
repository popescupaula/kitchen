import queue

global TIME_UNIT
TIME_UNIT = 1

global FOOD_ITEMS_Q
FOOD_ITEMS_Q = queue.PriorityQueue()

global ORDER_LIST
ORDER_LIST = []

global COOKS
COOKS = [{
    "id": 1,
    "rank": 3,
    "proficiency": 3,
    "name": "Gordon Ramsay",
    "catch-phrase": "Hey, panini head, are you listening to me?"
}, {
    "id": 2,
    "rank": 1,
    "proficiency": 3,
    "name": "Guy Fieri",
    "catch-phrase": "Holy moly, Stromboli!"
}, {
    "id": 3,
    "rank": 2,
    "proficiency": 3,
    "name": "Rachael Ray",
    "catch-phrase": "Yum-O"
}]

global STOVES_Q
STOVES_Q = queue.Queue()
STOVES_Q.put(0)
STOVES_Q.put(1)
STOVES_Q.put(2)
STOVES_Q.put(3)

global OVENS_Q
OVENS_Q = queue.Queue()
OVENS_Q.put_nowait(0)
OVENS_Q.put_nowait(1)
OVENS_Q.put_nowait(2)
OVENS_Q.put_nowait(3)

global FOODS
FOODS = [{
    "id": 1,
    "name": "pizza",
    "preparation-time": 20,
    "complexity": 2,
    "cooking-apparatus": "oven"
}, {
    "id": 2,
    "name": "salad",
    "preparation-time": 10,
    "complexity": 1,
    "cooking-apparatus": None
}, {
	"id": 3,
	"name": "zeama",
	"preparation-time": 7 ,
	"complexity": 1 ,
	"cooking-apparatus": "stove"
}, {
    "id": 4,
    "name": "Scallop Sashimi with Meyer Lemon Confit",
    "preparation-time": 32,
    "complexity": 3,
    "cooking-apparatus": None
}, {
    "id": 5,
    "name": "Island Duck with Mulberry Mustard",
    "preparation-time": 35,
    "complexity": 3,
    "cooking-apparatus": "oven"
}, {
    "id": 6,
    "name": "Waffles",
    "preparation-time": 10,
    "complexity": 1,
    "cooking-apparatus": "stove"
}, {
    "id": 7,
    "name": "Aubergine",
    "preparation-time": 20,
    "complexity": 2,
    "cooking-apparatus": None
}, {
    "id": 8,
    "name": "Lasagna",
    "preparation-time": 30,
    "complexity": 2,
    "cooking-apparatus": "oven"
}, {
    "id": 9,
    "name": "Burger",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": "oven"
}, {
    "id": 10,
    "name": "Gyros",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": None
}]