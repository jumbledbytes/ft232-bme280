from datetime import datetime
import json
from pyftdi.spi import SpiController
from bme280spi import BME280spi

from ft232h import FT232Pins
from bme280config import BME280Config

from bme280logger import log, LogLevel


class BME280DataRecord:
    def __init__(self, time, pressure, temperature, humidity):
        self.time = time
        self.pressure = pressure
        self.temperature = temperature
        self.humidity = humidity

    def json(self) -> str:
        jsonObject: dict = {}
        jsonObject['pressure'] = self.pressure
        jsonObject['temperature'] = self.temperature
        jsonObject['humidity'] = self.humidity
        return json.dumps(jsonObject)

    def string(self) -> str:
        return f"temperature: {self.temperature}, pressure: {self.pressure}, humidity: {self.humidity}"


class BME280Reader:
    def __init__(self, config: BME280Config = BME280Config()):
        self.config: BME280Config = config
        self.bme280: BME280spi = None

    def connect(self) -> bool:
        if self.bme280 != None:
            return True

        log(LogLevel.INFO, "Connecting to FT232H via SPI")
        spiController = SpiController()
        spiController.configure(self.config.deviceURI)
        spi = spiController.get_port(self.config.chipSelect.value)
        spi.set_frequency(self.config.busFrequency)

        try:
            self.bme280 = BME280spi(spi)
        except RuntimeError as err:
            log(LogLevel.ERROR, "Failed to connect to BME280: %s" % err)
            return False
        return True

    def connected(self) -> bool:
        return self.bme280 != None

    def read(self) -> BME280DataRecord:
        if self.bme280 == None:
            log(LogLevel.ERROR, "Attempt to read from disconnected BME280 sensor")
            return None

        now = datetime.utcnow().strftime('%FT%TZ')
        temperature, pressure, humidity = self.bme280.read()
        return BME280DataRecord(now, pressure, temperature, humidity)
