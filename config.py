# -*- coding: utf-8 -*-
import configparser
import os

class Config:
    def __init__(self, config_file="config.ini"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(base_dir, config_file)
        self.mac_address = None
        self.tb_address = None
        self.tb_port = 1883
        self.tb_token = None
        self.load_config()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)

        # Sensor configuration
        self.mac_address = config.get("Sensor", "MACAddress", fallback=None)

        # ThingsBoard configuration
        self.tb_address = config.get("ThingsBoard", "Address", fallback=None)
        self.tb_port = config.getint("ThingsBoard", "Port", fallback=1883)
        self.tb_token = config.get("ThingsBoard", "Token", fallback=None)

    def validate_config(self):
        if not self.mac_address:
            raise ValueError("MAC address is missing in the configuration file.")
        if not self.tb_address or not self.tb_token:
            raise ValueError("ThingsBoard address or token is missing in the configuration file.")

    def get_mac_address(self):
        return self.mac_address

    def get_tb_details(self):
        return self.tb_address, self.tb_port, self.tb_token
