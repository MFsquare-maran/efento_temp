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

        def detection_callback(device, advertisement_data):
            try:
                if device.address.lower() == self.bluetooth_address:
                    self.rssi = advertisement_data.rssi
                    self.name = device.name or "Unknown"
                    manufacturer_data = advertisement_data.manufacturer_data
                    for key, value in manufacturer_data.items():
                        if key == 620 and len(value) >= 1 and value[0] == 0x04:
                            data_collected['scan_response'] = value
            except Exception as e:
                print(f"Error in detection_callback: {e}")

        try:
            scanner = BleakScanner(detection_callback, scanning_mode="active")
            await scanner.start()
            await asyncio.sleep(15.0)
            await scanner.stop()

            if data_collected['scan_response']:
                self._parse_scan_response_frame(data_collected['scan_response'])
        except Exception as e:
            print(f"Error during Bluetooth scan: {e}")
