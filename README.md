# Overview

The `ft232-bme280` package is a small utility that supports reading data from a BME280 sensor that is connected to a system through a USB connected FT232H breakout board.

This implementation is inspired by the the [ft232h-bme280](https://github.com/rsmith-nl/ft232-bme280) project. This is an extension of that project that intends to create a more modular package structure to facilitate the integration of the ft232h bridge with a weewx extension. The end purpose of this particular package is to integrate a Bosche BEM280 sensor with commodity hardware that lacks an I2c interfave but is running weewx.

The WeeWx extension that uses this package is available [here](https://github.com/jumbledbytes/ft232-bme280-weewx)

# Installation

## Hardware dependencies

### FT232H Breakout Board

This package is tested using an Adafruit FT232H breakout board. At time of writing the board is available from Adafruit directly on their [web store](https://www.adafruit.com/product/2264).

Follow the instructions provided by Adafruit to solder connecting pins onto the breakout board.

### Bosche BME280 Temperature, Pressure, and Humidity Sensor

You will need a Bosche based BME280 sensor. There are many implementations available online. I used a [Waveshare BME280 Environmental Sensor](https://www.amazon.com/gp/product/B07P4CWGGK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

## Wiring the FT232H and BME280 sensor.

The terminology and naming of the pins on the breakout boards vary by manufacturer, but the standards are similar. Once connection pins are soldered onto the FT232H breakout board connect the pins to the BME280 as follows:

- 5V <-> VIN
- GND <-> GND
- D0 <-> SCK
- D1 <-> SDI
- D2 <-> SDO
- D3 <-> CS

## Connecting to the computer

Once the FT232 breakout board and the BME280 sensor are wired up the FT232 breakout board can be connected to the USB port on your computer

## Software Installation

This package is written to support Python3. Python 2 is not supported.

### Dependencies

This package depends on `pyftdi` which can be installed via:

```
pip3 install pyftdi
```

### Python Package

This package can be installed by running the following via sudo or using a privileged account:

```
python setup.py install
```

# Usage

Using the ft232-bme280 package comes with a default configuration that should work with simple setups where there is only one ft232h breakout board connected. Initializing the package and reading data can be peformed as follows:

```python
bme280Reader = BME280Reader()
bme280Reader.connect()

bme280Data = bme280Reader.read()
print(f"temperature: {bme280Data.temperature}, pressure: {bme280Data.pressure}, humidity: {bme280Data.humidity})
```

## Configuration

The default configuration should work for simple installations, however if it does not work or needs to be modified the BME280Reader module can take a configuration object.

### Configuration Options

**chipSelect**: This identifies the how the CS pin on the BME280 is connected to the FT232H breakout board. The default is `D3`

**deviceURI**: This is the ftdti URI used to connect to the FT232H breakout board. The default is ftdi://ftdi:232h/1 is should match the URI when only one FT232H board is connected to the system. If you have more than one FT232 breakout board connected you will need to find the URI for the board you want to connect to.

**busFrequency**: This is the frequency the device bus runs at. The default is 100000Hz. Valid values are between 92Hz and 30MHz (the frequency used depends on the particular FT232 implementation being used)

### Overriding the Configuration

If you pass in a dictionary with overrides the override values will be used.

```python

overrides : dict = {}
overrides['deviceURI']

# This will override only the deviceURI value and leave
# the existing default values unmodified
bme280Config = BME280Config(overrides)

bme280Reader = BME280Reader(bme280Config)
# ...
```

## Testing the package

The package comes with a simple test script `bme280-spi-test.py` that can be run to verify the FT232 -> BME280 connection as well as the package configuration. Assuming all is properly connected and configured you can run:

`python bme280-spi-test.py`

which should output something similar to the following (your values will vary depending on your configuration and environmen):

```
Connecting to BME280 at ftdi://ftdi:232h/1
0: 2020-12-26T18:36:21Z 20.91 100321 41.73
1: 2020-12-26T18:36:26Z 20.91 100321 41.73
2: 2020-12-26T18:36:31Z 20.85 100319 41.71
```
