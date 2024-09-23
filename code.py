import machine #type:ignore
import sdcard
import os
import time
from ds3231 import DS3231
from machine import Pin, SoftI2C #type:ignore
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from machine import I2C, Pin #type:ignore
import mcp23017

#Arrays
leds = [0, 1, 2, 3, 4, 5]
cstr_btns = [8, 9, 10, 11, 12, 13]
bombs = [1, 2, 3, 4, 5, 6]
products = []
pump_amounts = []
pump_times = []
liters_content = []

#Pins
prog_btn = 9
buzz_pin = 11
coin_btn = 12
coin = 4
test_btn = 10

#Bools
cstmr_mode = True
prog_mode = True
test_mode = True
bInserted = True
started = True
credits_displayed = False
maintenance = False
btn_pressed = False

#Steps
cstmr_step = 1
prog_step = 1
product_slct = 0
prog_slct = 0
prog_change = 1
config_step = 0

#Counts
tiempoInicio = 0
credits = 0
liters = float(0)
startTime = 0
endTime = 0
elapsedTime = 0

#Functions
def buzzHandle(millis, pulses):
    for i in range(pulses):
        mcp2[buzz_pin].output(1)
        time.sleep_ms(millis/2)
        mcp2[buzz_pin].output(0)

def setLeds(value):
    for i in range(len(leds)):
        mcp1[leds[i]].output(value)

def setLedBM(pinOn):
    for i in range(len(leds)):
        mcp1[leds[i]].output(0)
    mcp1[leds[pinOn]].output(1)
        
def lcdCenterStr(text):
    adjust_center = (20 - len(text)) // 2
    centered_text = ' ' * adjust_center + text
    return centered_text

def coin_interrupt():
    if started and cstmr_step < 2 and not test_mode and not prog_mode:
        credits += 1
        bInserted = True

def change_modeAlert(text1, text2):
    lcd.clear()
    buzzHandle(100,1)
    lcd.move_to(0,1)
    lcd.putstr(lcdCenterStr(text1))
    lcd.move_to(0,2)
    lcd.putstr(lcdCenterStr(text2))
    buzzHandle(300,4)
    lcd.clear()

def modoprueba():
    if test_mode:
        credits = pump_amounts[product_slct]

def readFloatFromFile(file):
    line = file.readline()
    
    line = line.decode('utf-8').strip()
    
    number_str = ''
    for char in reversed(line):
        if char.isdigit() or char == '.':
            number_str = char + number_str
        elif number_str:
            break
    
    try:
        return float(number_str)
    except ValueError:
        return 0.0

def readStringFromEighthChar(file):
    line = file.readline()
    
    line = line.decode('utf-8').strip()
    
    if len(line) >= 19:
        data = line[19:]
        
        adjusted_length = max(0, len(data) - 1)
        
        return data[:adjusted_length]
    else:
        return ''
    
def checkSDCard():
     try:
            os.mount(sd,'/sd')
            files = os.listdir('/sd')
            os.umount('/sd')
            print("Tarjeta SD conectada")
            return True
     except Exception as e:
         print("Error al conectar con la tarjeta:", e)
         return False

def millis():
    int(time.monotonic() * 1000)

def folder_exists(path):
    try:
        contents = os.listdir('/sd')
        if path in contents:
            return True
        else:
            return False
    except Exception as e:
        print("Error al verificar el directorio:", e)
        return False

#Setup
ds = DS3231(sdapin=4, sclpin=5)
i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=10000)

spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0)
cs = machine.Pin(15, machine.Pin.OUT)
sd = sdcard.SDCard(spi, cs)
vfs = os.VfsFat(sd)
mcp1 = mcp23017.MCP23017(SoftI2C, address=0x20)
mcp2 = mcp23017.MCP23017(SoftI2C, address=0x21)

I2C_ADDR = 0x27
totalRows = 4
totalColumns = 20

lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
lcd.display_on

for i in range(len(leds)):
    mcp1.pin(leds[i], mode=0, value=0)

for i in range(len(bombs)):
    mcp2.pin(bombs[i], mode=0, value=0)

for i in range(len(cstr_btns)):
    mcp1.pin(cstr_btns[i], mode=1, pullup=True)

mcp2.pin(buzz_pin, mode=0, value=0)
mcp2.pin(prog_btn, mode=1, pullup=True)
mcp2.pin(coin_btn, mode=1, pullup=True)
coin = Pin(coin, Pin.IN, Pin.PULL_UP) #pendiente
mcp2.pin(test_btn, mode=1, pullup=True)
coin.irq(trigger=Pin.IRQ_RISING, handler=coin_interrupt)

os.mount(vfs, '/sd')
with open('/sd/config.txt', 'r') as f:

    pump_amounts[0] = readFloatFromFile(f)
    pump_times[0] = readFloatFromFile(f)
    liters_content[0] = readFloatFromFile(f)
    products[0] = readStringFromEighthChar(f);
    pump_amounts[1] = readFloatFromFile(f);
    pump_times[1] = readFloatFromFile(f);
    liters_content[1] = readFloatFromFile(f);
    products[1] = readStringFromEighthChar(f);
    pump_amounts[2] = readFloatFromFile(f);
    pump_times[2] = readFloatFromFile(f);
    liters_content[2] = readFloatFromFile(f);
    products[2] = readStringFromEighthChar(f);
    pump_amounts[3] = readFloatFromFile(f);
    pump_times[3] = readFloatFromFile(f);
    liters_content[3] = readFloatFromFile(f);
    products[3] = readStringFromEighthChar(f);
    pump_amounts[4] = readFloatFromFile(f);
    pump_times[4] = readFloatFromFile(f);
    liters_content[4] = readFloatFromFile(f);
    products[4] = readStringFromEighthChar(f);
    pump_amounts[5] = readFloatFromFile(f);
    pump_times[5] = readFloatFromFile(f);
    liters_content[5] = readFloatFromFile(f);
    products[5] = readStringFromEighthChar(f);

os.umount('/sd')

lcd.move_to(0, 0)
lcd.putstr(lcdCenterStr("-CONFIGURACION-"));
lcd.move_to(0, 1)
lcd.putstr(lcdCenterStr("P1 $" + str(pump_amounts[0]) + "|" + str(pump_times[0] / 1000) + "s"))
lcd.move_to(0, 2)
lcd.putstr(lcdCenterStr("P2 $" + str(pump_amounts[1]) + "|" + str(pump_times[1] / 1000) + "s"))
lcd.move_to(0, 3)
lcd.putstr(lcdCenterStr("P3 $" + str(pump_amounts[2]) + "|" + str(pump_times[2] / 1000) + "s"))
time.sleep(3)
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr(lcdCenterStr("-CONFIGURACION-"));
lcd.move_to(0, 1)
lcd.putstr(lcdCenterStr("P4 $" + str(pump_amounts[3]) + "|" + str(pump_times[3] / 1000) + "s"))
lcd.move_to(0, 2)
lcd.putstr(lcdCenterStr("P5 $" + str(pump_amounts[4]) + "|" + str(pump_times[4] / 1000) + "s"))
lcd.move_to(0, 3)
lcd.putstr(lcdCenterStr("P6 $" + str(pump_amounts[5]) + "|" + str(pump_times[5] / 1000) + "s"))
time.sleep(3)
lcd.clear()
buzzHandle(100, 1)

#Loop
while True:
    #           -Test Mode-
    if mcp2.pin(test_btn) == 1 and not test_mode:
        while mcp2.pin(test_btn) == 1:
            time.sleep(0.01)
        credits_displayed = False
        prog_mode = False
        test_mode = True
        credits = 100
        change_modeAlert(" MODO PRUEBA", "ACTIVADO")
    elif mcp2.pin(test_btn) == 1 and test_mode:
        while mcp2.pin(test_btn) == 1:
            time.sleep(0.01)
        test_mode = False
        prog_mode = False
        credits = 0
        change_modeAlert(" MODO PRUEBA", "DESACTIVADO")

    #            -Prog Mode-
    if test_btn.value() == 1 and prog_mode:        
        if checkSDCard:
            os.mount(vfs, '/sd')
            os.remove('/sd/config.txt')
            lcd.clear()
            lcd.move_to(0,1)
            lcd.putstr(lcdCenterStr("GUARDANDO"))
            lcd.move_to(0,2)
            lcd.putstr(lcdCenterStr("CONFIGURACION"))
            buzzHandle(200,3)

            with open('/sd/config.txt', 'w') as f:
                for i in range(6):
                    f.write("PRODUCTO_PRECIO" + str(i + 1) + "=" + str(pump_amounts[i]) + "\n")
                    f.write("PRODUCTO_TIEMPO" + str(i + 1) + "=" + str(pump_times[i]) + "\n")
                    f.write("PRODUCTO_CONTEN" + str(i + 1) + "=" + str(liters_content[i]) + "\n")
                    f.write("PRODUCTO_NOMBRE" + str(i + 1) + "=" + str(products[i]) + "\n")
            time.sleep(1)
            lcd.clear()
            os.unmount('/sd')

        change_modeAlert("MODO PROGRAMADOR", "DESACTIVADO")
        prog_mode = False
        cstmr_mode = True
        cstmr_step = 1
        prog_step = 0
        lcd.clear()

    elif mcp2.pin(prog_btn) == 1 and not prog_mode:
        credits_displayed = False
        prog_mode = True
        cstmr_mode = False
        prog_step = 1
        cstmr_step = 1
        lcd.clear()
        buzzHandle(100,1)

    def cstmr_mode_main():
        if cstmr_mode:
            #init: (pendiente)

            if credits == 0 and not test_mode:
                lcd.move_to(0,1)
                lcd.putstr(lcdCenterStr("BIENVENIDO"))
                lcd.move_to(0,3)
                lcd.putstr(lcdCenterStr("  INGRESE CREDITOS"))

                for i in range(len(leds)):
                    if liters_content[i] < 5:
                        mcp1[leds[i]].output(0)
                    else:
                        mcp1[leds[i]].output(1)
            elif credits >= 0 and test_mode:
                lcd.move_to(0,1)
                lcd.putstr("-PRUEBAS-")
                for i in range(len(leds)):
                    if liters_content[i] < 5:
                        mcp1[leds[i]].output(0)
                    else:
                        mcp1[leds[i]].output(1)
            if cstmr_step == 1:
                if credits > 0:
                    if mcp1.pin(cstr_btns[0]) == 1 and credits >= pump_amounts[0] and liters_content[0] >= 5:
                        while mcp1.pin(cstr_btns[0]) == 1:
                            time.sleep(0.01)
                        product_slct = 0
                        modoprueba()
                        cstmr_step += 1
                        buzzHandle(100,1)
                    elif mcp1.pin(cstr_btns[1]) == 1 and credits >= pump_amounts[1] and liters_content[1] >= 5:
                        while mcp1.pin(cstr_btns[1]) == 1:
                            time.sleep(0.01)
                        product_slct = 1
                        modoprueba()
                        cstmr_step += 1
                        buzzHandle(100,1)
                    elif mcp1.pin(cstr_btns[2]) == 1 and credits >= pump_amounts[2] and liters_content[2] >= 5:
                        while mcp1.pin(cstr_btns[2]) == 1:
                            time.sleep(0.01)
                        product_slct = 2
                        modoprueba()
                        cstmr_step += 1
                        buzzHandle(100,1)
                    elif mcp1.pin(cstr_btns[3]) == 1 and credits >= pump_amounts[3] and liters_content[3] >= 5:
                        while mcp1.pin(cstr_btns[3]) == 1:
                            time.sleep(0.01)
                        product_slct = 3
                        modoprueba()
                        cstmr_step += 1
                        buzzHandle(100,1)
                    elif mcp1.pin(cstr_btns[4]) == 1 and credits >= pump_amounts[4] and liters_content[4] >= 5:
                        while mcp1.pin(cstr_btns[4]) == 1:
                            time.sleep(0.01)
                        product_slct = 4
                        modoprueba()
                        cstmr_step += 1
                        buzzHandle(100,1)
                    elif mcp1.pin(cstr_btns[5]) == 1 and credits >= pump_amounts[5] and liters_content[5] >= 5:
                        while mcp1.pin(cstr_btns[5]) == 1:
                            time.sleep(0.01)
                        product_slct = 5
                        modoprueba()
                        cstmr_step += 1
                        buzzHandle(100,1)
                    elif mcp1.pin(cstr_btns[0]) == 1 and credits < pump_amounts[0] or mcp1.pin(cstr_btns[1]) == 1 and credits < pump_amounts[1] or mcp1.pin(cstr_btns[2]) == 1 and credits < pump_amounts[2] or mcp1.pin(cstr_btns[3]) == 1 and credits < pump_amounts[3] or mcp1.pin(cstr_btns[4]) == 1 and credits < pump_amounts[4] or mcp1.pin(cstr_btns[5]) == 1 and credits < pump_amounts[5]:
                        lcd.clear()
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("CREDITOS"))
                        lcd.move_to(0,2)
                        lcd.putstr(lcdCenterStr("INSUFICIENTES"))
                        buzzHandle(100,4)
                        time.sleep_ms(1500)
                        lcd.clear()
                        lcd.move_to(0,1)
                        lcd.putchar("      CREDITOS")
                        lcd.move_to(0,2)
                        lcd.putstr(lcdCenterStr("$" + str(credits)))
                    elif mcp1.pin(cstr_btns[0]) == 1 and liters_content[0] < 5 or  mcp1.pin(cstr_btns[1]) == 1 and liters_content[1] or mcp1.pin(cstr_btns[2]) == 1 and liters_content[2] or mcp1.pin(cstr_btns[3]) == 1 and liters_content[3] or mcp1.pin(cstr_btns[4]) == 1 and liters_content[4] or mcp1.pin(cstr_btns[5]) == 1 and liters_content[5]:
                        lcd.clear()
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("LITROS"))
                        lcd.move_to(0,2)
                        lcd.putstr(lcdCenterStr("INSUFICIENTES"))
                        buzzHandle(100,4)
                        time.sleep_ms(1500)
                        lcd.clear()

                        if not test_mode:
                            lcd.clear()
                            lcd.move_to(0,1)
                            lcd.putstr("      CREDITOS")
                            lcd.move_to(0,2)
                            lcd.putstr(lcdCenterStr("$" + str(credits)))
                if bInserted  and not test_mode:
                    bInserted = False
                    credits_displayed = True
                    tiempoInicio = millis()
                    lcd.clear()
                    lcd.move_to(0,1)
                    lcd.putstr("      CREDITOS")
                    lcd.move_to(0,2)
                    lcd.putstr(lcdCenterStr("$" + str(credits)))
                elif mcp2.pin(coin_btn) == 1 and not test_mode:
                    credits += 1
                    credits_displayed = True
                    tiempoInicio = millis()
                    lcd.clear()
                    lcd.move_to(0,1)
                    lcd.putstr("      CREDITOS")
                    lcd.move_to(0,2)
                    lcd.putstr(lcdCenterStr("$" + str(credits)))
                elif millis() - tiempoInicio >= 180000 and credits_displayed:
                    credits = 0
                    lcd.clear()
                    credits_displayed = False
                    cstmr_mode_main()
            elif cstmr_step == 2:
                credits_displayed = False
                liters = credits / float(pump_amounts[product_slct])

                if liters <= 5:
                    lcd.clear()
                    lcd.move_to(0,1)
                    lcd.putstr("   COLOQUE ENVASE")
                    lcd.move_to(0,2)
                    lcd.putstr(lcdCenterStr(str(liters) + " L"))
                    buzzHandle(250,10)
                    cstmr_step += 1
                else:
                    lcd.clear()
                    lcd.move_to(0,1)
                    lcd.putstr(lcdCenterStr("5 LITROS"))
                    lcd.move_to(0,2)
                    lcd.putstr(lcdCenterStr("MINIMO"))
                    buzzHandle(400,6)
                    time.sleep_ms(1500)
                    lcd.clear()
                    lcd.move_to(0,1)
                    lcd.putstr("      CREDITOS")
                    lcd.move_to(0,2)
                    lcd.putstr(lcdCenterStr("$" + str(credits)))
                    cstmr_step = 1
                    product_slct = 0
            elif cstmr_step == 3:
                lcd.clear()
                lcd.move_to(0,0)
                lcd.putstr(lcdCenterStr(products[product_slct]))
                lcd.move_to(0,1)
                lcd.putstr(lcdCenterStr("SURTIENDO" + str(liters) + "L"))
                lcd.move_to(0,3)
                lcd.putstr("ESPERE UN MOMENTO...")
                setLedBM(product_slct)
                mcp2[bombs[product_slct]].output(1)
                time.sleep_ms(pump_times[product_slct] * liters)
                mcp2[bombs[product_slct]].output(0)
                cstmr_step += 1
            elif cstmr_step == 4:
                setLeds(1)
                liters_content[product_slct] -= liters
                lcd.clear()
                buzzHandle(100,3)
                lcd.move_to(0,1)
                lcd.putstr("GRACIAS POR COMPRAR!")
                lcd.move_to(0,3)
                lcd.putstr("   VUELVA PRONTO")
                time.sleep_ms(3000)
                if not test_mode:
                    if checkSDCard:
                        os.mount(vfs, '/sd')
                        if not folder_exists("/sd/reports" + str(ds.year()) + "_" + str(ds.month())):
                            os.mkdir('/sd/reports/' + str(ds.year()) + "_" + str(ds.month()))
                        else:
                            os.unmount('/sd')
                        os.mount('/sd/reports')
                        with open('/sd/reports/' + str(ds.year()) + "_" + str(ds.month()) + "/" + str(ds.day()) + ".txt", 'w') as f:
                            if checkSDCard:
                                f.write(str(ds.year()) + "-" + str(ds.month()) + "-" + str(ds.day()) + " P" + str(product_slct) + " " + str(credits) + " " + str(liters))
                                os.unmount('/sd')
                else:
                     if checkSDCard:
                        os.mount(vfs, '/sd')
                        if not folder_exists("/sd/reports" + str(ds.year()) + "_" + str(ds.month())):
                            os.mkdir('/sd/reports/' + str(ds.year()) + "_" + str(ds.month()))
                        else:
                            os.unmount('/sd')
                        os.mount('/sd/reports')
                        with open('/sd/reports/' + str(ds.year()) + "_" + str(ds.month()) + "/TEST_" + str(ds.day()) + ".txt", 'w') as f:
                            if checkSDCard:
                                f.write(str(ds.year()) + "-" + str(ds.month()) + "-" + str(ds.day()) + " P" + str(product_slct) + " " + str(credits) + " " + str(liters))
                                os.unmount('/sd')
                if test_mode:
                    credits = 100
                else:
                    credits = 0
                cstmr_step = 1
                liters = 0
                product_slct = 0
                lcd.clear()
        else:
            if prog_mode:
                setLeds(0)
                if prog_step == 1:
                    change_modeAlert("MODO PROGRAMADOR", "ACTIVADO")
                    credits = 0
                    prog_change = 1
                    lcd.clear()
                    prog_step += 1
                elif prog_step == 2:
                    if mcp1.pin(cstr_btns[0]) == 1:
                        while mcp1.pin(cstr_btns[0]) == 1:
                         time.sleep(0.01)
                        lcd.clear()
                        prog_change += 1
                        time.sleep_ms(100)
                        buzzHandle(100,1)
                    elif prog_change == 6:
                        prog_change = 0
                    if prog_change == 1:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("-CAMBIAR PRECIO-"))
                    elif prog_change == 2:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("-CAMBIAR TIEMPO-"))
                    elif prog_change == 3:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("-RELLENAR-"))
                    elif prog_change == 4:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("-HORARIO-"))
                    elif prog_change == 5:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("-CONFIGURACION-"))
                    elif prog_change == 0:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("-MANTENIMIENTO-"))
                    if mcp1.pin(cstr_btns[1]) == 1:
                        while mcp1.pin(cstr_btns[1]) == 1:
                            time.sleep(0.01)
                        buzzHandle(100,1)
                        lcd.clear()
                        if prog_change == 4 or prog_change == 5 or prog_change == 0:
                            prog_step = 4
                            time.sleep_ms(350)
                        else:
                            prog_step += 1
                            time.sleep_ms(350)
                elif prog_step == 3:
                    if prog_slct == prog_slct:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr(products[prog_slct]))
                    if mcp1.pin(cstr_btns[0]) == 1:
                        while mcp1.pin(cstr_btns[0]) == 1:
                            time.sleep(0.01)
                        lcd.clear()
                        prog_slct += 1
                        buzzHandle(100,1)
                    elif prog_slct == 6:
                        prog_slct = 0
                    elif mcp1.pin(cstr_btns[1]) == 1:
                        while mcp1.pin(cstr_btns[1]) == 1:
                            time.sleep(0.01)
                        buzzHandle(100,1)
                        lcd.clear()
                        prog_step += 1
                    elif mcp1.pin(cstr_btns[2]) == 1:
                        while mcp1.pin(cstr_btns[2]) == 1:
                            time.sleep(0.01)
                        buzzHandle(100,1)
                        prog_slct = 0
                        prog_change = 1
                        prog_step -= 1
                elif prog_step == 4:
                    if prog_change == 1:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("PRECIO / LITRO"))
                        lcd.move_to(0,2)
                        lcd.putstr(lcdCenterStr("$" + str(pump_amounts[prog_slct])))
                        if mcp1.pin(cstr_btns[1]) == 1:
                            while mcp1.pin(cstr_btns[1]) == 1:
                                time.sleep(0.01)
                            pump_amounts[prog_slct] += 1
                            buzzHandle(100,1)
                            time.sleep_ms(150)
                        elif mcp1.pin(cstr_btns[2]) == 1:
                            while mcp1.pin(cstr_btns[2]) == 1:
                                time.sleep(0.01)
                            if pump_amounts[prog_slct] >= 2:
                                pump_amounts[prog_slct] -= 1
                                buzzHandle(100,1)
                                time.sleep_ms(150)
                        elif mcp1.pin(cstr_btns[0]) == 1:
                            while mcp1.pin(cstr_btns[0]) == 1:
                                time.sleep(0.01)
                            buzzHandle(100,1)
                            lcd.clear()
                            prog_slct = 0
                            prog_step = 3
                        elif mcp1.pin(cstr_btns[2]) == 1: #Verificar pin
                            while mcp1.pin(cstr_btns[2]) == 1:
                                time.sleep(0.01)
                            buzzHandle(100,1)
                            prog_step = 2
                    elif prog_change == 2:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("TIEMPO DE BOMBA"))
                        lcd.move_to(0,2)
                        lcd.putstr(lcdCenterStr(str(pump_times[prog_slct]) + " ms"))
                        btn_state = mcp1.pin(cstr_btns[1])
                        if btn_state == 1 and not btn_pressed:
                            startTime = millis()
                            btn_pressed = True
                            lcd.clear()
                            lcd.move_to(0,3)
                            lcd.putstr(lcdCenterStr(" CALIBRANDO..."))
                            mcp2[bombs[prog_slct]].output(1)
                        elif btn_state == 0 and btn_pressed:
                            lcd.clear()
                            mcp2[bombs[prog_slct]].output(0)
                            endTime = millis()
                            btn_pressed = False
                            elapsedTime = endTime - startTime
                            pump_times[prog_slct] = elapsedTime
                        elif mcp1.pin(cstr_btns[0]) == 1:
                            while mcp1.pin(cstr_btns[0]) == 1:
                                time.sleep(0.01)
                            buzzHandle(100,1)
                            lcd.clear()
                            prog_change = 2
                            prog_slct = 0
                            prog_step = 3
                    elif prog_change == 3:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("CANTIDAD PRODUCTO"))
                        lcd.move_to(0,2)
                        lcd.putstr(lcdCenterStr(str(liters_content[prog_slct]) + "L"))
                        if mcp1.pin(cstr_btns[1]) == 1:
                            while mcp1.pin(cstr_btns[1]) == 1:
                                time.sleep(0.01)
                            liters_content[product_slct] = round(liters_content[prog_slct])
                            buzzHandle(100,1)
                            liters_content[prog_slct] += 1
                            time.sleep_ms(150)
                        elif mcp1.pin(cstr_btns[2]) == 1:
                            while mcp1.pin(cstr_btns[2]) == 1:
                                time.sleep(0.01)
                            if liters_content[prog_slct] >= 2:
                                buzzHandle(100,1)
                                liters_content[product_slct] = round(liters_content[product_slct])
                                liters_content[prog_slct] -= 1
                                time.sleep_ms(150)
                        elif mcp1.pin(cstr_btns[3]) == 1:
                            while mcp1.pin(cstr_btns[3]) == 1:
                                time.sleep(0.01)
                            buzzHandle(100,1)
                            liters_content[product_slct] = 20
                            time.sleep_ms(150)
                        elif mcp1.pin(cstr_btns[0]) == 1:
                            while mcp1.pin(cstr_btns[0]) == 1:
                                time.sleep(0.01)
                            buzzHandle(100,1)
                            lcd.clear()
                            prog_step = 3
                            prog_change = 3
                            prog_slct = 0
                        elif mcp1.pin(cstr_btns[2]) == 1:
                            while mcp1.pin(cstr_btns[2]) == 1:
                                time.sleep(0.01)
                            buzzHandle(100,1)
                            prog_step = 2
                            prog_change = 1
                    elif prog_change == 4:
                        lcd.move_to(0,0)
                        lcd.putstr(lcdCenterStr("HORARIO"))
                        lcd.move_to(0,2)
                        lcd.putstr(lcdCenterStr(str(ds.hour()) + ":" + str(ds.min())))
                        lcd.move_to(0,3)
                        lcd.putstr(lcdCenterStr(str(ds.day()) + "/" + str(ds.month()) + "/" + str(ds.year())))
                        if mcp1.pin(cstr_btns[0]) == 1:
                            while mcp1.pin(cstr_btns[0]) == 1:
                                time.sleep(0.01)
                            buzzHandle(100,1)
                            lcd.clear()
                            prog_step = 2
                            prog_change = 1
                            prog_slct = 0
                    elif prog_change == 5:
                        if mcp1.pin(cstr_btns[0]) == 1:
                            while mcp1.pin(cstr_btns[0]) == 1:
                                time.sleep(0.01)
                            config_step += 1
                        elif config_step == 2:
                            config_step = 0
                        if config_step == 0:
                            lcd.move_to(0, 0);
                            lcd.putstr(lcdCenterStr("-CONFIGURACION-"));
                            lcd.move_to(0, 1);
                            lcd.putstr(lcdCenterStr("P1 $" + str(pump_amounts[0]) + "|" + str(pump_times[0] / 1000) + "s"))
                            lcd.move_to(0, 2);
                            lcd.putstr(lcdCenterStr("P2 $" + str(pump_amounts[1]) + "|" + str(pump_times[1] / 1000) + "s"))
                            lcd.move_to(0, 3);
                            lcd.putstr(lcdCenterStr("P3 $" + str(pump_amounts[2]) + "|" + str(pump_times[2] / 1000) + "s"))
                        else:
                            lcd.move_to(0, 0);
                            lcd.putstr(lcdCenterStr("-CONFIGURACION-"));
                            lcd.move_to(0, 1);
                            lcd.putstr(lcdCenterStr("P4 $" + str(pump_amounts[3]) + "|" + str(pump_times[3] / 1000) + "s"))
                            lcd.move_to(0, 2);
                            lcd.putstr(lcdCenterStr("P5 $" + str(pump_amounts[4]) + "|" + str(pump_times[4] / 1000) + "s"))
                            lcd.move_to(0, 3);
                            lcd.putstr(lcdCenterStr("P6 $" + str(pump_amounts[5]) + "|" + str(pump_times[5] / 1000) + "s"))
                        if mcp1.pin(cstr_btns[0]) == 1:
                            while mcp1.pin(cstr_btns[0]) == 1:
                                time.sleep(0.01)
                            buzzHandle(100,1)
                            lcd.clear()
                            prog_step = 2
                            prog_change = 1
                            prog_slct = 0
                    elif prog_change == 0:
                        lcd.move_to(0,1)
                        lcd.putstr(lcdCenterStr("MANTENIMIENTO"))
                        lcd.move_to(0,2)
                        lcd.putstr(lcdCenterStr("DESACTIVADO"))
                        if mcp1.pin(cstr_btns[1]) == 1:
                            while mcp1.pin(cstr_btns[1]) == 1:
                                time.sleep(0.01)
                            change_modeAlert("INICIANDO", "MANTENIMIENTO")
                            time.sleep_ms(2000)
                            lcd.clear()
                            lcd.move_to(0,1)
                            lcd.putstr(lcdCenterStr(" MANTENIMIENTO"))
                            lcd.move_to(0,2)
                            lcd.putstr(lcdCenterStr("EN CURSO"))
                            buzzHandle(100,4)
                            for i in range (len(bombs)):
                                mcp2(bombs[i]).output(1)
                            time.sleep_ms(45000)
                            for i in range (len(bombs)):
                                mcp2(bombs[i]).output(0)
                            lcd.clear()
                            lcd.move_to(0,1)
                            lcd.putstr(lcdCenterStr("MANTENIMIENTO"))
                            lcd.move_to(0,2)
                            lcd.putstr(lcdCenterStr("COMPLETADO"))
                            lcd.move_to(0,3)
                            lcd.putstr(lcdCenterStr("REGRESE MANGUERAS"))
                            buzzHandle(300,4)
                            time.sleep_ms(4000)
                            lcd.clear()
                            prog_step = 2
                            prog_change = 1
                            prog_slct = 0