import machine,time
from micropython import const
import framebuf
import ustruct
import courrier16 #font file

# register definitions
ILI9225_DRIVER_OUTPUT_CTRL      =const(0x01)  # Driver Output Control
ILI9225_LCD_AC_DRIVING_CTRL     =const(0x02)  # LCD AC Driving Control
ILI9225_ENTRY_MODE              =const(0x03)  # Entry Mode
ILI9225_DISP_CTRL1              =const(0x07)   # Display Control 1
ILI9225_BLANK_PERIOD_CTRL1      =const(0x08)  # Blank Period Control
ILI9225_FRAME_CYCLE_CTRL        =const(0x0B)  # Frame Cycle Control
ILI9225_INTERFACE_CTRL          =const(0x0C)  # Interface Control
ILI9225_OSC_CTRL                =const(0x0F) #Osc Control
ILI9225_POWER_CTRL1             =const(0x10)  # Power Control 1
ILI9225_POWER_CTRL2             =const(0x11)  # Power Control 2
ILI9225_POWER_CTRL3             =const(0x12)  # Power Control 3
ILI9225_POWER_CTRL4             =const(0x13)  # Power Control 4
ILI9225_POWER_CTRL5             =const(0x14)  # Power Control 5
ILI9225_VCI_RECYCLING           =const(0x15)  # VCI Recycling
ILI9225_RAM_ADDR_SET1           =const(0x20)  # Horizontal GRAM Address Set
ILI9225_RAM_ADDR_SET2           =const(0x21)  # Vertical GRAM Address Set
ILI9225_GRAM_DATA_REG           =const(0x22)  # GRAM Data Register
ILI9225_GATE_SCAN_CTRL          =const(0x30)  # Gate Scan Control Register
ILI9225_VERTICAL_SCROLL_CTRL1   =const(0x31)  #// Vertical Scroll Control 1 Register
ILI9225_VERTICAL_SCROLL_CTRL2   =const(0x32)  #// Vertical Scroll Control 2 Register
ILI9225_VERTICAL_SCROLL_CTRL3   =const(0x33)  #// Vertical Scroll Control 3 Register
ILI9225_PARTIAL_DRIVING_POS1    =const(0x34)  #// Partial Driving Position 1 Register
ILI9225_PARTIAL_DRIVING_POS2    =const(0x35)  #// Partial Driving Position 2 Register
ILI9225_HORIZONTAL_WINDOW_ADDR1 =const(0x36)  #// Horizontal Address Start Position
ILI9225_HORIZONTAL_WINDOW_ADDR2 =const(0x37)  #// Horizontal Address End Position
ILI9225_VERTICAL_WINDOW_ADDR1   =const(0x38)  #// Vertical Address Start Position
ILI9225_VERTICAL_WINDOW_ADDR2   =const(0x39)  #// Vertical Address End Position
ILI9225_GAMMA_CTRL1             =const(0x50)  #// Gamma Control 1
ILI9225_GAMMA_CTRL2             =const(0x51)  #// Gamma Control 2
ILI9225_GAMMA_CTRL3             =const(0x52)  #// Gamma Control 3
ILI9225_GAMMA_CTRL4             =const(0x53)  #// Gamma Control 4
ILI9225_GAMMA_CTRL5             =const(0x54)  #// Gamma Control 5
ILI9225_GAMMA_CTRL6             =const(0x55)  #// Gamma Control 6
ILI9225_GAMMA_CTRL7             =const(0x56)  #// Gamma Control 7
ILI9225_GAMMA_CTRL8             =const(0x57)  #// Gamma Control 8
ILI9225_GAMMA_CTRL9             =const(0x58)  #// Gamma Control 9
ILI9225_GAMMA_CTRL10            =const(0x59)  #// Gamma Control 10

ILI9225C_INVOFF                 =const(0x20)
ILI9225C_INVON                  =const(0x21)

# tft_rst = machine.Pin(22, machine.Pin.OUT, 0)
# tft_bckl = machine.Pin(5, machine.Pin.OUT, 0)
# tft_rs = machine.Pin(21, machine.Pin.OUT, 0)
# tft_clk = machine.Pin(18, machine.Pin.OUT, 0)
# tft_sdi = machine.Pin(19, machine.Pin.OUT, 0)
# tft_cs = machine.Pin(23, machine.Pin.OUT, 0)
# tft_sdo = machine.Pin(17, machine.Pin.OUT, 0)
#spi=machine.SPI(1,baudrate=1000000, mosi=tft_sdi, miso=tft_sdo, sck=tft_clk)
spi=machine.SPI(1,baudrate=40000000, mosi=machine.Pin(13), miso=machine.Pin(12), sck=machine.Pin(14))
#spi.init(baudrate=40000000, mosi=tft_sdi, sck=tft_clk)
  
class TFT_22_ILI9225:
  def __init__(self,spi,width=176, height=220, rs=25, rst=26, led=33 ,cs=27,brightness=200):
    self.spi=spi
    self.width=width
    self.height=height
    self.maxX=width
    self.maxY=height
    self.orientation=0
    self.bgColor=0x0000
    self.entryMode=0b011 #AM,ID1,ID0 
    self.rst  = machine.Pin(rst, machine.Pin.OUT)
    self.rs   = machine.Pin(rs, machine.Pin.OUT)
    self.cs   = machine.Pin(cs, machine.Pin.OUT)
    self.led  = machine.Pin(led, machine.Pin.OUT)
    self.brightness = brightness
  def init(self):
    self.rst.value(0)
    self.led.value(1) # momentary flash backlight
    time.sleep(0.2)
    self.led.value(0)
    self.rs.value(0)
    #start of initialization
    self.cs.value(1) #pul, out of reset
    self.rst.value(1)
    time.sleep_ms(1) 
    self.rst.value(0)#reset the lcd by pulling reset low
    time.sleep_ms(10)
    self.rst.value(1) #pull reset line hight to exit reset
    time.sleep_ms(50)
    #initialize lcd
    self.writeRegister(ILI9225_POWER_CTRL1,b'\x00\x00')
    self.writeRegister(ILI9225_POWER_CTRL2,b'\x00\x00')
    self.writeRegister(ILI9225_POWER_CTRL3,b'\x00\x00')
    self.writeRegister(ILI9225_POWER_CTRL4,b'\x00\x00')
    self.writeRegister(ILI9225_POWER_CTRL5,b'\x00\x00')
    time.sleep_ms(40)
    self.writeRegister(ILI9225_POWER_CTRL2,b'\x00\x18')
    self.writeRegister(ILI9225_POWER_CTRL3,b'\x61\x21')
    self.writeRegister(ILI9225_POWER_CTRL4,b'\x00\x6F')
    self.writeRegister(ILI9225_POWER_CTRL5,b'\x49\x5F')
    self.writeRegister(ILI9225_POWER_CTRL1,b'\x08\x00')
    time.sleep_ms(10)
    self.writeRegister(ILI9225_POWER_CTRL2,b'\x10\x3B')
    time.sleep_ms(50)
    #self.writeRegister(ILI9225_DRIVER_OUTPUT_CTRL,b'\x01\x1C')
    self.writeRegister(ILI9225_DRIVER_OUTPUT_CTRL,b'\x02\x1C') #reverse orientation
    self.writeRegister(ILI9225_LCD_AC_DRIVING_CTRL,b'\x01\x00')
    #self.writeRegister(ILI9225_ENTRY_MODE,b'\x10\x30') #harizontal scan(left-right,up-down)
    self.writeRegister(ILI9225_ENTRY_MODE,b'\x10\x30') #reverse 
    self.writeRegister(ILI9225_DISP_CTRL1,b'\x00\x00')  #panel is off
    self.writeRegister(ILI9225_BLANK_PERIOD_CTRL1,b'\x08\x08')
    self.writeRegister(ILI9225_FRAME_CYCLE_CTRL,b'\x11\x00')
    self.writeRegister(ILI9225_INTERFACE_CTRL,b'\x00\x00')
    self.writeRegister(ILI9225_OSC_CTRL,b'\x0D\x01')
    self.writeRegister(ILI9225_VCI_RECYCLING,b'\x00\x20')
#     self.writeRegister(ILI9225_RAM_ADDR_SET1,b'\x00\x00')
#     self.writeRegister(ILI9225_RAM_ADDR_SET2,b'\x00\x00')
    self.writeRegister(ILI9225_RAM_ADDR_SET1,b'\x00\x00')
    self.writeRegister(ILI9225_RAM_ADDR_SET2,b'\x00\x00')
    #SET GRAM AREA
    self.writeRegister(ILI9225_GATE_SCAN_CTRL,b'\x00\x00')
    self.writeRegister(ILI9225_VERTICAL_SCROLL_CTRL1,b'\x00\xDB')
    self.writeRegister(ILI9225_VERTICAL_SCROLL_CTRL2,b'\x00\x00')
    self.writeRegister(ILI9225_VERTICAL_SCROLL_CTRL3,b'\x00\x00')
    self.writeRegister(ILI9225_PARTIAL_DRIVING_POS1,b'\x00\xDB')
    self.writeRegister(ILI9225_PARTIAL_DRIVING_POS2,b'\x00\x00')
    self.writeRegister(ILI9225_HORIZONTAL_WINDOW_ADDR1,b'\x00\xAF')
    self.writeRegister(ILI9225_HORIZONTAL_WINDOW_ADDR2,b'\x00\x00')
    self.writeRegister(ILI9225_VERTICAL_WINDOW_ADDR1,b'\x00\xDB')
    self.writeRegister(ILI9225_VERTICAL_WINDOW_ADDR2,b'\x00\x00')
    #set gamma Curve
    self.writeRegister(ILI9225_GAMMA_CTRL1,b'\x00\x00')
    self.writeRegister(ILI9225_GAMMA_CTRL2,b'\x08\x08')
    self.writeRegister(ILI9225_GAMMA_CTRL3,b'\x08\x0A')
    self.writeRegister(ILI9225_GAMMA_CTRL4,b'\x00\x0A')
    self.writeRegister(ILI9225_GAMMA_CTRL5,b'\x0A\x08')
    self.writeRegister(ILI9225_GAMMA_CTRL6,b'\x08\x08')
    self.writeRegister(ILI9225_GAMMA_CTRL7,b'\x00\x00')
    self.writeRegister(ILI9225_GAMMA_CTRL8,b'\x0A\x00')
    self.writeRegister(ILI9225_GAMMA_CTRL9,b'\x07\x10')
    self.writeRegister(ILI9225_GAMMA_CTRL10,b'\x07\x10')
    self.writeRegister(ILI9225_DISP_CTRL1,b'\x00\x12') #partiall on
   
    time.sleep_ms(50)
    self.writeRegister(ILI9225_DISP_CTRL1,b'\x10\x17') #full on
    self.led.value(1)
    self.setOrientation(0)
    self.bgColor=0x0000



  def write_cmd(self, cmd):
    """"slow write"""    
    self.rs.value(0)
    self.cs.value(0)
    self.spi.write(bytes([0,cmd]))
    self.cs.value(1)
  def write_data(self, data):
    """slow write"""
    self.rs.value(1)
    self.cs.value(0)
    self.spi.write(data) 
    self.cs.value(1)

  def writeRegister(self,reg,data):
    self.rs(0)
    self.cs(0)
    self.spi.write(bytes([0,reg]))   
    self.rs(1)
    self.spi.write(data) 
    self.cs(1)

  def setOrientation(self,orientation):
    if orientation==0:
          self.maxX=self.width
          self.maxY=self.height
          self.orientation=orientation
          return
    if orientation==1:
          self.maxX=self.height
          self.maxY=self.width
          self.orientation=orientation
          return     
    if orientation==2:
          self.maxX=self.width
          self.maxY=self.height
          self.orientation=orientation
          return
    if orientation==3:
          self.maxX=self.height
          self.maxY=self.width
          self.orientation=orientation
          return

  def clear(self):
        old=self.orientation
        self.setOrientation(0)
        self.fillRectangle(0,0,self.maxX-1,self.maxY-1,0x0000)
        self.setOrientation(old)

  def fillRectangle(self,x1,y1,x2,y2,color):
      """color is an 16 bit RGB integer value"""
      self.setWindow(x1,y1,x2,y2)
      self.write_cmd(ILI9225_GRAM_DATA_REG)
      color=color.to_bytes(2,'big')
      data_length=(y2-y1+1)*(x2-x1+1)
      chunks,rest=divmod(data_length,1024) #devide data into smaller chunk so delay is bearable in rendering
      data=color*1024
      self.rs.value(1)
      self.cs.value(0)
      if chunks:
          for t in range(chunks):
            self.spi.write(data)
      if rest:
            self.spi.write(color*rest)
      self.cs.value(0)

  

  def setEntryMode(self,Emode):
        self.entryMode=Emode
        self.writeRegister(ILI9225_ENTRY_MODE,bytes((0x10,self.entryMode<<3)))

  def setWindow(self,x0,y0,x1,y1):
    # clip to TFT-Dimensions
    x0=min((x0,self.maxX-1))
    x1=min((x1,self.maxX-1))
    y0=min((y0,self.maxY-1))
    y1=min((y1,self.maxY-1))
    #set window
    self.writeRegister(ILI9225_HORIZONTAL_WINDOW_ADDR1,bytes((0x00,x1)))
    self.writeRegister(ILI9225_HORIZONTAL_WINDOW_ADDR2,bytes((0x00,x0)))
    self.writeRegister(ILI9225_VERTICAL_WINDOW_ADDR1,bytes((0x00,y1)))
    self.writeRegister(ILI9225_VERTICAL_WINDOW_ADDR2,bytes((0x00,y0)))
    #set starting address of GRAM 
    self.writeRegister(ILI9225_RAM_ADDR_SET1,bytes((0x00,x0)))
    self.writeRegister(ILI9225_RAM_ADDR_SET2,bytes((0x00,y0)))

  def writeDisplay(self,data):
      """method to write transfer display data to the LCD
          data is a series of bytes"""
      self.writeRegister(ILI9225_GRAM_DATA_REG,data)
  def char(self, char, x, y, color=0xffff, background=0x0000):
      """20x13 chargracter glyph generation, courier font"""
      self.setWindow(x,y,x+courrier16.width-1,y+courrier16.height)
      buffer = courrier16.getChar(char)
      #buffer=bytearray(courrier.font[26:26+26])
      #print(buffer)
      # color = ustruct.pack(">H", color)
      # background = ustruct.pack(">H", background)
      data = bytearray([])  #12 is the bit width
      data_index=0
      for c, byte in enumerate(buffer):
            if c%2==0:
                  data=data+self.byteto16bit(byte,8,color,background)
            else:
                  data=data+self.byteto16bit(byte,courrier16.width-8,color,background)
                  
            #print(c)
            #print(data)

      #   self.write_cmd(ILI9225_GRAM_DATA_REG)
        #print(data)
      self.writeDisplay(data)

  def byteto16bit(self,byt,width,color=0xffff, background=0x0000):
        buffer_16=bytearray(2*width)
        color = ustruct.pack(">H", color)
        background = ustruct.pack(">H", background)
        for i in range(width):
              data= (byt>>7-i) & 0x01
              if data:
                    buffer_16[i*2]=color[0]
                    buffer_16[i*2+1]=color[1]
              else:
                    buffer_16[i*2]=background[0]
                    buffer_16[i*2+1]=background[1]
                         

        return buffer_16 

  def text(self, text, x, y, color=0xffff, background=0x0000):
         tx = x
         ty = y

         
         for char in text:
            self.char(char, tx, ty, color, background)
            tx += courrier16.width
# bitmaps routine
  def DrawImage(self,x1,y1,width,height,imageArray):
      """color is an 16 bit RGB integer value"""
      self.setWindow(x1,y1,x1+width-1,y1+height-1)
      data_length=len(imageArray)
      self.write_cmd(ILI9225_GRAM_DATA_REG)
      #color=color.to_bytes(2,'big')
      #data_length=(y2-y1+1)*(x2-x1+1)
      chunks,rest=divmod(data_length,1024) #devide data into smaller chunk so delay is bearable in rendering
      #data=color*1024
      self.rs.value(1)
      self.cs.value(0)
      if chunks:
          for t in range(chunks):
            self.spi.write(imageArray[t*1024:t*1024+1024])
      if rest:
            self.spi.write(imageArray[-rest:])
      self.cs.value(0)

         
  def StatDisplay(self):
        self.clear()
        self.text('Location',2,5,0x07E0)
        self.text('Info',115,5,0x07E0)
        self.text('Lat:',5,30)
        self.text('Lon:',5,52)
        #self.text('123.5',75,30,0xFFE0) #lat update
        #self.text('123.12',75,52,0x895C) #long update
        self.text('FMA:',5,82)   
        self.text('LGU:',5,102)  
        self.text('9',70,82,0xFFE0)  #FMA update
        self.text('El Salv',70,102,0x895C) #LGU update
        self.text('DistOrg:',5,122)
        self.text('DistLGU:',5,142)
        self.text('2.0',110,122,0xFFE0)  #distOrg update
        self.text('8.5',110,142,0x895C) #distLGU update
        self.text('Waters:',5,162)
        self.text('Time:',5,182)
        self.text('Mun',120,162,0xFFE0)  #water update
        #self.text('15:23',80,182,0x895C) #time update
        self.text('NumSat:',5,200)
        #self.text('10',100,200,0xFD20)  #no of sat update
       #self.text('15:23',80,182,0x895C)
  def LocUpdate(self,lat,long,time,num_sat,d,d0):
        self.text("{:7.4f}".format(lat),60,30)
        self.text("{:7.4f}".format(long),60,52)
        self.text(str(time),65,182,0x895C)
        self.text(str(num_sat),100,200,0x895C)
        self.text("{:7.4f}".format(d),110,142,0x895C) #distLGU update
        self.text("{:7.4f}".format(d0),110,122,0xFFE0) #distLGU update
      #self.resetWindow()
   





      
#lcd=TFT_22_ILI9225(spi)
#lcd.init()
#lcd.clear()
#lcd.StatDisplay()
# def rect(col):
#       colors=[0x8000,0x9772]
#       lcd.fillRectangle(0,0,lcd.width,lcd.height,colors[col])











  
        


