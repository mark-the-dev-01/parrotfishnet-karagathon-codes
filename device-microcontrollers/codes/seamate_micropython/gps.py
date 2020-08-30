from machine import UART, Pin, SPI,PWM
# from micropyGPS import MicropyGPS
import utime
# import lcd_gfx
# from bmp import bmp
# import ST7735
import nmea
import ili_9225_3
from semate import data_mv

lat_ch=8.559266
long_ch=124.525643
lat_org=8.559266
long_org=124.525643
#samp_lat=8.545178
#samp_long=124.566116

# d=nmea.get_distance(lat_ch,long_ch,samp_lat,samp_long)
# while True:
    	# pass

# def display(my_nmea, margin, d):
# 	d.p_string(margin,5,my_nmea.time)
# 	d.p_string(margin,15,my_nmea.date)
# 	d.p_string(margin,25,'{:10.4f}'.format(my_nmea.latitude))
# 	d.p_string(margin,35,'{:10.4f}'.format(my_nmea.longitude))
# 	d.p_string(margin,45,'{:02d}'.format(my_nmea.satcount))

# margin = 72

# spi = SPI(-1, baudrate=80000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

# d = ST7735.ST7735(spi, offset=3, c_mode='BGR')
# d.reset()
# d.begin()

# d._bground = 0x0000
# d.fill_screen(d._bground)

# utime.sleep(1)

# d._bground = 0x001f
# d.fill_screen(d._bground)

# d._color = 0xffff

# d.set_rotation(1)

# d.p_string(2,5, '      Time: ')
# d.p_string(2,15,'      Date: ')
# d.p_string(2,25,'  Latitude: ')
# d.p_string(2,35,' Longitude: ')
# d.p_string(2,45,'Satellites: ')
SW1=Pin(17,Pin.IN)
SW2=Pin(16,Pin.IN)
buz=PWM(Pin(21))
buz.freq(1000)
buz.duty(0)
def beep():
    buz.duty(512)
    utime.sleep(0.1)
    buz.duty(0)

    	 

# my_gps = MicropyGPS(location_formatting='dd')
spi=SPI(1,baudrate=40000000, mosi=Pin(13), miso=Pin(12), sck=Pin(14))
uart = UART(1, 9600,tx=23,rx=22)
now = utime.ticks_ms()
sentence = ''
state = ''
my_nmea = nmea.nmea(debug=0)
lcd=ili_9225_3.TFT_22_ILI9225(spi)
lcd.init()
#lcd.setEntryMode(0)
lcd.clear()
lcd.fillRectangle(0,0,lcd.width,lcd.height,0xFFFF)
lcd.DrawImage(40,60,88,60,data_mv)
beep()
utime.sleep(2)
while SW2.value()==1:
    pass
beep()
lcd.StatDisplay()
beep()

while 1:
	while uart.any():
		b = uart.read()
		my_nmea.parse(b)
	if SW2.value()==0:
		lat_org=my_nmea.latitude
		long_org=my_nmea.longitude
		beep()
	
	
	if utime.ticks_diff(utime.ticks_ms(), now) > 1000:
		now = utime.ticks_ms()
		d_ch=nmea.get_distance(my_nmea.latitude,my_nmea.longitude,lat_ch,long_ch)
		d_o=nmea.get_distance(my_nmea.latitude,my_nmea.longitude,lat_org,long_org)
		lcd.LocUpdate(my_nmea.latitude,my_nmea.longitude,my_nmea.time,my_nmea.satcount,d_ch,d_o)
		print('{} {} {} {} num of sat:{}'.format(my_nmea.time, my_nmea.date, my_nmea.latitude, my_nmea.longitude,my_nmea.satcount))
		#display(my_nmea, margin, d)
