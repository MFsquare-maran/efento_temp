# -*- coding: utf-8 -*-
import socket
import uuid
import platform
import netifaces

class HostInfo:
    @staticmethod
    def get_info():
        # IP Address from eth0
        ip_address = "Unknown"
        try:
            ifaddrs = netifaces.ifaddresses('eth0')
            if netifaces.AF_INET in ifaddrs:
                ip_address = ifaddrs[netifaces.AF_INET][0]['addr']
        except Exception:
            pass

        # MAC Address
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])

        # Hostname
        hostname = socket.gethostname()

        # OS Details
        os_name = platform.system()
        os_version = platform.version()
        os_release = platform.release()

        # Uptime
        uptime = "Unknown"
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime = f"{int(uptime_seconds // 3600)} hours, {int((uptime_seconds % 3600) // 60)} minutes"
        except Exception:
            pass  # For systems without /proc/uptime

        return {
            "ip_address": ip_address,
            "mac_address": mac_address,
            "hostname": hostname,
            "os_name": os_name,
            "os_version": os_version,
            "os_release": os_release,
            "uptime": uptime
        }
