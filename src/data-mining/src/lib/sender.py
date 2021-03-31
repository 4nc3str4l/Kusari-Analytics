import pika
import json
import threading
from threading import Thread
from queue import Queue, Empty

from .singleton import Singleton


class MessageSender(object, metaclass=Singleton):
    def __init__(self, host, queue):
        credentials = pika.PlainCredentials('user', 'password')
        self.queue = queue
        self.msgs = Queue()
        self.thread = Thread(target=self.run, args=(credentials, host, queue))
        self.thread.start()
        
    def run(self, credentials, host, queue):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, credentials=credentials)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.confirm_delivery()

        while True:
            try:
                msg = self.msgs.get(False)
                if msg is None:
                    self.connection.close()
                    break
                else:
                    self.channel.basic_publish(exchange='', routing_key=self.queue, body=msg)
            except Empty:
                pass

            try:
                self.connection.sleep(0.1)
            except:
                break
    
    def send(self, data):
        self.msgs.put(json.dumps(data))
