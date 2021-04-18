import pika
import json
import threading
from threading import Thread
from queue import Queue, Empty

from .singleton import Singleton


DECL_QUEUES = ('kusari', 'transactions', 'wealth')

class MessageSender(object, metaclass=Singleton):
    def __init__(self, host, queues):
        credentials = pika.PlainCredentials('user', 'password')
        self.msgs = Queue()
        self.thread = Thread(target=self.run, args=(credentials, host, queues))
        self.thread.start()
        
    def run(self, credentials, host, queues):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, credentials=credentials)
        )
        self.channel = self.connection.channel()
        for queue in queues:
            self.channel.queue_declare(queue=queue)
        self.channel.confirm_delivery()

        while True:
            try:
                data = self.msgs.get(False)
                if data is None:
                    self.connection.close()
                    break
                else:
                    queue, msg = data
                    self.channel.basic_publish(exchange='', routing_key=queue, body=msg)
            except Empty:
                pass

            try:
                self.connection.sleep(0.1)
            except:
                break
    
    def send(self, queue, data):
        self.msgs.put((queue, json.dumps(data)))
