from microbit import *
import utime
import microbit

unsigned = Image("90009:90009:90009:90009:09990")
signed = Image("99999:00900:00900:00900:99999")
floating = Image("09990:09000:09900:09000:09000")
character = Image("09999:90000:90000:90000:09999")

screen = 0
bit_on_intensity = 5
bit_off_intensity = 0
led_value = 0
bit_pattern = []
i = len(bit_pattern)
j = i - 24

blink_half_period = 500  # half a second
blink_value = 0
blink_ms = utime.ticks_ms()
current_led_value = 0  # off
hold_ms = 500  # hold threshold

while True:
    if screen == 0:
        check_ms = utime.ticks_ms()
        if utime.ticks_diff(check_ms, blink_ms) >= blink_half_period:
            blink_ms = check_ms
            blink_value = (blink_value + 1) % 2
            if blink_value:
                if i < 25:
                    display.set_pixel(i % 5, i // 5, 9)
                else:
                    display.set_pixel(j % 5, j // 5, 9)
            elif current_led_value:
                if i < 25:
                    display.set_pixel(i % 5, i // 5, bit_on_intensity)
                else:
                    display.set_pixel(j % 5, j // 5, bit_on_intensity)
            else:
                if i < 25:
                    display.set_pixel(i % 5, i // 5, 0)
                else:
                    display.set_pixel(j % 5, j // 5, 0)

            if button_a.was_pressed():
                led_value = (current_led_value + 1) % 2  # alternating: if 1, then 0; if 0, then 1
                current_led_value = led_value
                if led_value > 0:
                    if i < 25:
                        display.set_pixel(i % 5, i // 5, bit_on_intensity)
                    else:
                        display.set_pixel(j % 5, j // 5, bit_on_intensity)
                if led_value == 0:
                    if i < 25:
                        display.set_pixel(i % 5, i // 5, 0)
                    else:
                        display.set_pixel(j % 5, j // 5, 0)

            if button_b.was_pressed():
                start_ms = utime.ticks_ms()
                while button_b.is_pressed():
                    pass
                if utime.ticks_ms() - start_ms >= hold_ms:
                    screen = (screen + 1) % 2
                elif led_value == 1:
                    if i < 25:
                        display.set_pixel(i % 5, i // 5, bit_on_intensity)
                    else:
                        display.set_pixel(j % 5, j // 5, bit_on_intensity)
                    bit_pattern.append('1')
                    i = len(bit_pattern)
                    current_led_value = 0
                    led_value = 0
                    j = i - 25
                    if j == 0:
                        microbit.display.clear()
                elif led_value != 1:
                    if i < 25:
                        display.set_pixel(i % 5, i // 5, 0)
                    else:
                        display.set_pixel(j % 5, j // 5, 0)
                    bit_pattern.append('0')
                    i = len(bit_pattern)
                    j = i - 25
                    if j == 0:
                        microbit.display.clear()
                if i == 32:
                    screen = (screen + 1) % 2

    if screen == 1:
        microbit.display.clear()
        display.show(unsigned)
        d = 0
        while True:
            if button_a.was_pressed():
                d = (d + 1) % 4
                if d == 0:
                    display.show(unsigned)
                if d == 1:
                    display.show(signed)
                if d == 2:
                    display.show(floating)
                if d == 3:
                    display.show(character)
            elif button_b.was_pressed():
                start_ms = utime.ticks_ms()
                while button_b.is_pressed():
                    pass
                if utime.ticks_ms() - start_ms > hold_ms:
                    # hold
                    microbit.display.clear()
                    bit_pattern.clear()
                    i = 0
                    led_value = 0
                    current_led_value = 0
                    screen = 0
                    break
                if d == 0:
                    if len(bit_pattern) > 0:
                        display.scroll(int(''.join(str(i) for i in bit_pattern), 2))
                    else:
                        display.scroll("No Value")
                    display.show(unsigned)
                if d == 1:
                    flipped_list = ['0' if b == '1' else '1' for b in bit_pattern]
                    flipped_pattern = ''.join(flipped_list)
                    value = sum([int(flipped_pattern[i])*(2**(len(flipped_pattern)-i-1)) for i in range(len(flipped_pattern))])
                    if int(''.join(str(i) for i in bit_pattern[0:1])) == 1:
                        value = -value
                        value = value - 1
                        display.scroll(value)
                    else:
                        value = value - 1
                        display.scroll(value)
                    display.show(signed)
                if d == 2:
                    sign = (int(''.join(str(i) for i in bit_pattern[0:1]), 2))
                    if sign == 1:
                        sign = "-"
                    if sign == 0:
                        sign = ""
                    exponent = (int(''.join(str(i) for i in bit_pattern[1:9]), 2)-127)
                    mantissa = bit_pattern[9:32]
                    for i in range(0, len(mantissa)-1):
                        mantissa[i] = int(mantissa[i])*2**(-(i+1))
                    mantissa = sum(float(i) for i in mantissa)
                    display.scroll(sign)
                    display.scroll((1+mantissa)*2**exponent)
                    display.show(floating)
                if d == 3:
                    display.scroll(chr(int(''.join(str(i) for i in bit_pattern[0:8]), 2)) \
                        + chr(int(''.join(str(i) for i in bit_pattern[8:16]), 2)) \
                        + chr(int(''.join(str(i) for i in bit_pattern[16:24]), 2)) \
                        + chr(int(''.join(str(i) for i in bit_pattern[24:32]), 2)))
                    display.show(character)
