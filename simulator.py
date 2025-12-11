import requests, time, random, datetime

URL = "http://127.0.0.1:5000/api/events"
rooms = ["Living Room","Kitchen","Bedroom","Garage"]

def simulate():
    last_alert = datetime.datetime.now()
    while True:
        room = random.choice(rooms)
        temp = round(random.uniform(24, 42), 1)
        hum  = round(random.uniform(35, 70), 0)
        event_type = "alert" if temp > 36 else "info"
        message = f"Temperature {temp}°C, Humidity {hum}% in {room}"

        # every 15 minutes force a special alert
        if (datetime.datetime.now() - last_alert).total_seconds() > 900:
            alert = random.choice(["Gas leakage","Fire detected","Motion detected"])
            event_type = "alert"
            message = f"{alert} in {room}!"
            last_alert = datetime.datetime.now()

        data = {
            "device_name": f"{room} Sensor",
            "event_type": event_type,
            "message": message,
            "temperature": temp,
            "humidity": hum
        }
        try:
            requests.post(URL, json=data, timeout=3)
            print("sent", data)
        except Exception as e:
            print("err", e)
        time.sleep(5)

if __name__ == "__main__":
    simulate()
