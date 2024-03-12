import serial 
import requests
import re

serial_port = 'COM3' 
baud_rate = 9600

thingspeak_channel_id = '2465340' 
thingspeak_api_key = '3U933WRMAOG9E1BP' 
thingspeak_api_url = f'https://api.thingspeak.com/update?api_key={thingspeak_api_key}'

ser = serial.Serial(serial_port, baud_rate)
while True: 
    data = ser.readline().decode('utf-8').strip() 
    print("Received data:", data)
    
    # Check if the line contains expected substrings
    if 'Soil Moisture' in data or 'Humidity' in data or 'Temperature' in data:
        try:
            numerical_values = re.findall(r'\d+\.\d+|\d+', data)

            soilMoisture = float(numerical_values[0])

            humidity = float(numerical_values[1])

            temp = float(numerical_values[2])

            #Send data to ThingSpeak
            params = {'field1': soilMoisture,
                      'field2': temp,
                      'field3': humidity
                      }
            response = requests.post(thingspeak_api_url, params=params)

            print("ThingSpeak Response:", response.text)
        except (ValueError, IndexError) as e:
            print(f"Error processing data: {e}. Skipping.")
    else:
        print("Invalid data format. Skipping.")
