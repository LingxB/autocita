from time import sleep, time
from random import uniform, randint


def wait_between(a,b):
	rand=uniform(a, b)
	sleep(rand)