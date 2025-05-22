from flask import Flask, request
import time
import random

app = Flask(__name__)

##FOR DEBUGGING
app.logger.setLevel("INFO") #Lowering the log level to show INFO messages

@app.route("/")
def hello():
    # Simulate a normal request processing time (e.g., 50-150 ms)
    proc_time = random.randint(50, 150)
    time.sleep(proc_time / 1000.0)  # sleep for that many milliseconds
    app.logger.info(f"Handled / in {proc_time}ms\n")
    return f"Hello, world! Success - {proc_time}\n", 200

@app.route("/chaos")
def chaos():
    # Simulate an anomalously slow request or error
    proc_time = random.randint(1000, 2500)  # 1 to 2 seconds delay (anomaly)
    time.sleep(proc_time / 1000.0)
    # 50% of the time, return error to simulate chaos
    if random.random() < 0.5:
        app.logger.error(f"Chaos endpoint error! Took {proc_time}ms\n")
        return f"Something went wrong! Took {proc_time}ms\n", 500
    else:
        app.logger.info(f"Chaos endpoint slow response: {proc_time}ms\n")
        return f"Chaos handled slowly. Took {proc_time}ms\n", 200

if __name__ == "__main__":
    # Bind to port 5000 on all interfaces
    app.run(host="0.0.0.0", port=5000)
