from drawzero import *

if __name__ == '__main__':
    copy_examples()

    grid()
    rect('red', (50, 150), 900, 700)
    line('orange', (100, 500), (900, 500))
    text('green', 'Hello world!', (500, 250), fontsize=72)
    text('blue', 'Привет, мир!', (500, 750), fontsize=72)
