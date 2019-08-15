

def countdown(t):
    "Thanks to: https://www.codespeedy.com/how-to-create-a-countdown-in-python/"

    import time

    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print('Blast Off!!!')


if __name__ == "__main__":
    t = input("Enter the time in seconds: ")
    countdown(int(t))
