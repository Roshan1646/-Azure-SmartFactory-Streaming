import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json
import random
import datetime

# --- CONFIGURATION ---
# 1. Paste your Connection String between the quotes below
EVENT_HUB_CONN_STR = "PRIMARY_CONNNECTION_STRING"
# 2. Ensure this matches the name you gave your Event Hub
EVENT_HUB_NAME = "EVENT_HUB_NAME"

async def send_events():
    # This client is our "Messenger" to Azure
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONN_STR,
        eventhub_name=EVENT_HUB_NAME
    )
    async with producer:
        print(f"--- Factory Simulation Started: Sending data to {EVENT_HUB_NAME} ---")
        while True:
            events_to_send = []
            for i in range(1, 11): # Simulating 10 Machines
                sensor_id = f"Machine_{i:02d}"
                
                # Generate random sensor data
                temp = round(random.uniform(60, 95), 2)
                energy = round(random.uniform(0.5, 2.5), 2)
                status = "Operational"
                
                # Randomly create an "Overheating" anomaly
                if random.random() < 0.05:
                    temp = round(random.uniform(100, 120), 2)
                    status = "Critical"

                data = {
                    "sensorId": sensor_id,
                    "temperature": temp,
                    "energyConsumption": energy,
                    "status": status,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
                }
                
                # Convert the dictionary to a JSON string
                json_data = json.dumps(data)
                events_to_send.append(EventData(json_data))
            
            # Send the batch of 10 readings to Azure
            await producer.send_batch(events_to_send)
            print(f"Sent 10 readings at {datetime.datetime.now().strftime('%H:%M:%S')}")
            await asyncio.sleep(1) # Wait 1 second before next reading

if __name__ == "__main__":
    try:
        asyncio.run(send_events())
    except KeyboardInterrupt:
        print("Simulation stopped.")
