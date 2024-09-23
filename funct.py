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