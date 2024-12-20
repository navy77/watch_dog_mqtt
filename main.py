import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import json
load_dotenv()

mqtt_broker = '192.168.0.160'
mqtt_port = 1883
mqtt_topic = 'data/test'
number_rows = 2

client = mqtt.Client()

# Function to connect to the broker with a retry mechanism
def connect_broker():
    while True:
        try:
            client.connect(mqtt_broker, mqtt_port, 60)
            print("Connected to MQTT broker")
            break
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Call the function to connect to the broker
connect_broker()

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f'File {event.src_path} has been created')
        name = str(event.src_path)
        name_split = name.split("#")
        die = name_split[1]
        bash = name_split[2]
        lot = name_split[3]
        cav_full = name_split[4]
        cav_split = cav_full.split(".")
        cav = cav_split[0]
        time.sleep(1)
        data = pd.read_csv(name, header=None, nrows=number_rows)
        df = pd.DataFrame(data)
        df_split = df[0].str.split("=", expand=True)
        df_split[0] = df_split[0].str.strip()
        df_split[1] = df_split[1].str.strip()
        data_dict = dict(zip(df_split[0], df_split[1]))

        data_dict["die"] = str(die)
        data_dict["bash"] = str(bash)
        data_dict["lot"] = str(lot)
        data_dict["cav"] = str(cav)

        json_data = json.dumps(data_dict, indent=4)
        client.publish(mqtt_topic, json_data)

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='D:\\watch_dog_mqtt\\data', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
