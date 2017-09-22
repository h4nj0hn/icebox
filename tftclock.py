import pygame
import os
import subprocess
import RPi.GPIO as GPIO
import time

#Note #21 changed to #27 for rev2 Pi
button_map = {23:(255,0,0), 22:(0,255,0), 27:(0,0,255), 18:(0,0,0)}

#Setup the GPIOs as inputs with Pull Ups since the buttons are connected to GND
GPIO.setmode(GPIO.BCM)
for k in button_map.keys():
    GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Colours
WHITE = (255,255,255)
AMBER = (247,135,53)
LAZER = (82,247,53)
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((320, 240))
lcd.fill((0,0,0))
pygame.display.update()

font_big = pygame.font.Font(None, 24)
title_font = pygame.font.Font( None , 50)

while True:
   	# Draw a black filled box to clear the image.
    
    lcd.fill((0,0,0))
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I "#| cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    Time = time.strftime("%H:%M:%S %Z", time.localtime())

    # Write bottom title
    titl = font_big.render("h4nj0hn-blkbx", True, LAZER)
    titrect = titl.get_rect(center=(160,210))

    # Write IP
    IPR = font_big.render("IP: " + str(IP)[:-1], True, WHITE)
    rect = IPR.get_rect(center=(160,120))

    # Write time
    TM = title_font.render(str(Time), True, AMBER)
    recttm = TM.get_rect(center=(160,50))

    # Write CPU
    CPUr = font_big.render(str(CPU), True, WHITE)
    rectcpu = CPUr.get_rect(center=(160,140))

    # Write RAM
    Memr = font_big.render(str(MemUsage), True, WHITE)
    rectmem = Memr.get_rect(center=(160,160))

    # blit to screen
    lcd.blit(titl, titrect)
    lcd.blit(IPR, rect)
    lcd.blit(TM, recttm)
    lcd.blit(CPUr, rectcpu)
    lcd.blit(Memr, rectmem)

    pygame.display.update()
    time.sleep(0.1)
