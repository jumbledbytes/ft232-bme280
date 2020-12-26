from bme280logger import log, LogLevel
from ft232h import FT232Pins


class BME280Config:

    def __init__(self, data=None):
        self.deviceURI: str = "ftdi://ftdi:232h/1"
        self.chipSelect: FT232Pins = FT232Pins.D3
        self.busFrequency: int = 100000  # Hz
        self.logLevel: LogLevel = LogLevel.INFO
        self.valid = True

        if data != None:
            self.load(data)

    def load(self, data: dict) -> bool:
        if data == None:
            return False
        chipSelect = data.get("chipSelect", None)
        if(chipSelect != None):
            chipSelect = FT232Pins[chipSelect]
        else:
            chipSelect = self.chipSelect

        self.deviceURI = data.get("deviceURI", self.deviceURI)
        self.chipSelect = chipSelect
        self.busFrequency = int(data.get("busFrequency", self.busFrequency))

        self.valid = self.validate()
        return self.valid

    def validate(self) -> bool:
        valid = True
        if self.chipSelect not in FT232Pins:
            log(LogLevel.WARNING, "Invalid chipSelect value %s" % self.chipSelect)
            valid = False
        if self.busFrequency < 92 or self.busFrequency > 30000000:
            log(LogLevel.WARNING,
                "Invalid bus frequency. Valid values: 92 < frequency < 30000000")
            valid = False

        return valid
