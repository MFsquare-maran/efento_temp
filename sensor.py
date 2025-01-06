# -*- coding: utf-8 -*-
import asyncio
from bleak import BleakScanner

class Sensor:
    def __init__(self, bluetooth_address):
        self.bluetooth_address = bluetooth_address.lower()
        self.temperature = None
        self.unit = None
        self.rssi = None
        self.name = None
        self.fwversion = None
        self.battery = None
        self.MACAdresse = None


    def parse_advertisement_frame(self,data):
      try:

          idx = 1   
          

          Macadresse_roh = data[idx:idx+6]
          
          self.MACAdresse = ':'.join(f'{byte:02X}' for byte in Macadresse_roh)

          
          
          idx = 7  # Skip Manufacturing Data Version
        
          # Firmware Version
          firmware_version_bytes = data[idx:idx+2]
          idx += 2
          firmware_version_int = int.from_bytes(firmware_version_bytes, byteorder='big')
        
          lts_version = firmware_version_int & 0x1F
          minor_version = (firmware_version_int >> 5) & 0x3F
          major_version = (firmware_version_int >> 11) & 0x1F
          self.fwversion = f"{major_version}.{minor_version}.{lts_version}"
    
          # Battery Level
          idx = 9
          status_byte = data[idx]
          battery_level_bit = status_byte & 0x01
          self.battery = "OK" if battery_level_bit else "Low"

 
      except Exception as e:
          print(f"Error in parse_advertisement_frame: {e}")
  
    
    def _parse_scan_response_frame(self, data):
        try:
            idx = 1  # Skip Manufacturing Data Version
            while idx < len(data) - 2:
                measurement_type = data[idx]
                idx += 1
                measurement_value_bytes = data[idx:idx+3]
                idx += 3
                raw_value = int.from_bytes(measurement_value_bytes, byteorder='big')
                zigzag_decoded = (raw_value >> 1) ^ -(raw_value & 1)

                if measurement_type == 0x01:  # Temperature
                    self.temperature = round(zigzag_decoded * 0.1, 1)
                    self.unit = "C"
        except Exception as e:
            print(f"Error parsing scan response frame: {e}")

    async def get_data(self):
        data_collected = {'scan_response': None}
        data_collected2 = {'scan_response2': None}

        def detection_callback(device, advertisement_data):
            try:
                if device.address.lower() == self.bluetooth_address:
                    self.rssi = advertisement_data.rssi
                    self.name = device.name or "Unknown"
                    manufacturer_data = advertisement_data.manufacturer_data
                    for key, value in manufacturer_data.items():
                        if key == 620 and len(value) >= 1 and value[0] == 0x04:
                            data_collected['scan_response'] = value
                        if key == 620 and len(value) >= 11 and value[0] == 0x03:
                            data_collected2['scan_response2'] = value
            except Exception as e:
                print(f"Error in detection_callback: {e}")

        max_attempts = 4
        attempt = 0

        while attempt < max_attempts:
          try:
            scanner = BleakScanner(detection_callback, scanning_mode="active")
            await scanner.start()
            await asyncio.sleep(15.0)
            await scanner.stop()
            print("-----------------------------------------")
            print(data_collected.get('scan_response', b'').hex())
            print(data_collected2.get('scan_response2', b'').hex())
            print("-----------------------------------------")

            if data_collected.get('scan_response'):
              self._parse_scan_response_frame(data_collected['scan_response'])
            if data_collected2.get('scan_response2'):
              self.parse_advertisement_frame(data_collected2['scan_response2'])
              break  # Scan erfolgreich, Schleife beenden

            attempt += 1
            if attempt < max_attempts:
              print(f"Scan unvollständig. Versuche erneut ({attempt}/{max_attempts})...")
            else:
              print("Maximale Anzahl an Versuchen erreicht. Scan abgebrochen.")
          except Exception as e:
            print(f"Fehler während des Scans: {e}")
            attempt += 1

