import settings as settings
import time
import logging
import queue
import threading
import itertools
import requests
from flask import Flask, request

logging.basicConfig(filename='kitchen.log', level=logging.DEBUG, format='%(asctime)s:  %(message)s', datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)

app = Flask(__name__)

counter = itertools.count()

@app.route('/order', methods=['POST'])
def order():
    data = request.get_json()
    logger.info(f'NEW ORDER {data["order_id"][0:4]} | priority: {data["priority"]} | items: {data["items"]}\n')
    convert_order_to_food_items(data)
    return {'isSuccess': True}

def convert_order_to_food_items(data):
    priority = -int(data['priority'])
    kitchen_order = {
        'order_id': data['order_id'],
        'table_id': data['table_id'],
        'waiter_id': data['waiter_id'],
        'items': data['items'],
        'priority': priority,
        'max_wait': data['max_wait'],
        'received_time': time.time(),
        'cooking_details': queue.Queue(),
        'is_done_counter': 0,
        'time_start': data['time_start'],
    }
    settings.ORDER_LIST.append(kitchen_order)
    for item_id in data['items']:
        food = next((f for i, f in enumerate(settings.FOODS) if f['id'] == item_id), None)
        if food is not None:
            settings.FOOD_ITEMS_Q.put_nowait((priority, next(counter), {
                'food_id': food['id'],
                'order_id': data['order_id'],
                'priority': priority
            }))


def can_prepare(cook, ovens: queue.Queue, stoves: queue.Queue, food, order):
    if food['complexity'] == cook['rank'] or food['complexity'] - 1 == cook['rank']:
        apparatus = food['cooking-apparatus']
        if apparatus == 'oven':
            try:
                o = ovens.get_nowait()
                logger.info(f'{threading.current_thread().name} COOKING  foodId: {food["id"]} | orderId: {order["order_id"][0:4]} | priority: {order["priority"]} | oven: {o}')
                return True
            except Exception as e:
                return False
        elif apparatus == 'stove':
            try:
                s = stoves.get_nowait()
                logger.info(f'{threading.current_thread().name} COOKING foodId: {food["id"]} | orderId: {order["order_id"][0:4]} | priority: {order["priority"]} | stove: {s}')
                return True
            except Exception as e:
                return False
        elif apparatus is None:
            logger.info(f'{threading.current_thread().name} COOKING foodId: {food["id"]} | orderId: {order["order_id"][0:4]} | priority: {order["priority"]} (hands)')
            return True
        return False
    return False


def cook_hand_work(cook, ovens: queue.Queue, stoves: queue.Queue, food_items: queue.Queue):
    while True:
        try:
            q_item = food_items.get_nowait()
            food_item = q_item[2]
            curr_counter = q_item[1]
            food_details = next((f for f in settings.FOODS if f['id'] == food_item['food_id']), None)
            (order_idx, order_details) = next(((idx, order) for idx, order in enumerate(settings.ORDER_LIST) if order['order_id'] == food_item['order_id']), (None, None))

            if can_prepare(cook, ovens, stoves, food_details, order_details):
                time.sleep(food_details['preparation-time'] * settings.TIME_UNIT)
                settings.ORDER_LIST[order_idx]['is_done_counter'] += 1
                if settings.ORDER_LIST[order_idx]['is_done_counter'] == len(settings.ORDER_LIST[order_idx]['items']):
                    logger.info(f'{threading.current_thread().name} PREPARED orderId: {order_details["order_id"][0:4]} | priority: {order_details["priority"]}')
                    settings.ORDER_LIST[order_idx]['cooking_details'].put({'food_id': food_details['id'], 'cook_id': cook['id']})
                    payload = {
                        **settings.ORDER_LIST[order_idx],
                        'cooking_time': int(time.time() - settings.ORDER_LIST[order_idx]['received_time']),
                        'cooking_details': list(settings.ORDER_LIST[order_idx]['cooking_details'].queue)
                    }
                    requests.post('http://localhost:5000/distribution', json=payload, timeout=0.0000000001)
                apparatus = food_details['cooking-apparatus']
                if apparatus == 'oven':
                    n = ovens.qsize()
                    ovens.put_nowait(n)
                elif apparatus == 'stove':
                    n = stoves.qsize()
                    stoves.put_nowait(n)
            else:
                food_items.put_nowait((food_item['priority'], curr_counter, food_item))

        except Exception as e:
            pass


def cook_work(info, ovens, stoves, food_items):
    for i in range(info['proficiency']):
        hand_thread = threading.Thread(target=cook_hand_work, args=(info, ovens, stoves, food_items,), daemon=True, name=f'#{i}-{info["name"]}-$')
        hand_thread.start()


def start_kitchen():
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False), daemon=True)
    flask_thread.start()

    for _, cook_data in enumerate(settings.COOKS):
        cook_thread = threading.Thread(target=cook_work, args=(cook_data, settings.OVENS_Q, settings.STOVES_Q, settings.FOOD_ITEMS_Q,), daemon=True)
        cook_thread.start()

    while True:
        pass


if __name__ == '__main__':
    start_kitchen()