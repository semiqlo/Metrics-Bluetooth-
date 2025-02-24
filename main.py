from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListItemButton
import bluetooth
import math

class BluetoothScanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.list_view = ListView()
        self.add_widget(self.list_view)
        self.scan_devices()

    def scan_devices(self):
        self.list_view.adapter.data.clear()
        nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True)
        for addr, name in nearby_devices:
            rssi = self.get_signal_strength(addr)
            distance = self.estimate_distance(rssi) if rssi is not None else "Desconocida"
            self.list_view.adapter.data.append(f"{name} ({addr}) - Distancia: {distance}m")

    def get_signal_strength(self, target_address):
        # Aquí se necesitaría un método real para obtener el RSSI en Android
        return -50  # Valor simulado de RSSI

    def estimate_distance(self, rssi):
        tx_power = -59  # Ajustar según calibración
        ratio = rssi / tx_power
        if ratio < 1.0:
            return round(math.pow(ratio, 10), 1)
        return round((0.89976) * math.pow(ratio, 7.7095) + 0.111, 1)

class BluetoothApp(App):
    def build(self):
        return BluetoothScanner()

if __name__ == "__main__":
    BluetoothApp().run()