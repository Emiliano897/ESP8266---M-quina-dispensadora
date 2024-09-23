def prog_mode_stps():            
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