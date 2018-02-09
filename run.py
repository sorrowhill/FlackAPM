import newrelic.agent
newrelic.agent.initialize('./newrelic.ini')

from flask import Flask
app = Flask(__name__)
app = newrelic.agent.wsgi_application()(app)

from time import sleep
import logging
import random

from threading import Timer


@newrelic.agent.background_task()
def background_task():
    while True:
        value = random.randrange(1, 100000)
        if value <= 50:
            break

    Timer(1, background_task).start()


@app.route('/test1')
def run_test1():
    newrelic.agent.set_transaction_name("test1")
    sleep(1)
    return "done\n"


@app.route('/test2')
def run_test2():
    newrelic.agent.set_transaction_name("test2")
    sleep(2)
    return "done\n"


@app.route('/test3')
def run_test3():
    newrelic.agent.set_transaction_name("test3")
    sleep(3)
    return "done\n"


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    Timer(1, background_task).start()

    app.run()
