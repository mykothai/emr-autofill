import time


def send_delayed_keys(element, text, delay=0.2):
    for character in text:
        end_time = time.time() + delay
        element.send_keys(character)
        time.sleep(end_time - time.time())
