# -*- coding: utf-8 -*-
import asyncio
from config import Config
from sensor import Sensor
from tb_mfsquare import TBMFSquare
from host_info import HostInfo

async def get_sensor_data(config):
    mac_address = config.get_mac_address()
    tb_address, tb_port, tb_token = config.get_tb_details()

    sensor = Sensor(bluetooth_address=mac_address)
    await sensor.get_data()

    tb_client = TBMFSquare(tb_address, tb_port, tb_token)
    tb_client.connect()

    # Publish attributes
    host_info = HostInfo.get_info()
    tb_client.publish("v1/devices/me/attributes", host_info)
    
    Sensor_attributes = {"Sensor Firmware": sensor.fwversion, "Sensor Macadresse": sensor.MACAdresse}
    
    tb_client.publish("v1/devices/me/attributes", Sensor_attributes)

    # Publish telemetry data
    if sensor.temperature is not None:
        telemetry_data = {
            "temperature": sensor.temperature,
            "rssi": sensor.rssi,
            "battery": sensor.battery
        }
        tb_client.publish("v1/devices/me/telemetry", telemetry_data)

    tb_client.disconnect()
    return sensor

if __name__ == "__main__":
    async def main():
        try:
            config = Config()
            config.validate_config()

            sensor = await get_sensor_data(config)
            if sensor.temperature is not None:
                print(f"Sensor Name: {sensor.MACAdresse}")
                print(f"RSSI: {sensor.rssi} dBm")
                print(f"Temperature: {sensor.temperature} {sensor.unit}")

                print("\nHost Information:")
                host_info = HostInfo.get_info()
                for key, value in host_info.items():
                    print(f"{key}: {value}")
            else:
                print("Failed to retrieve sensor data.")
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())
