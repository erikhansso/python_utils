from subprocess import Popen
import sys

filename = "pathtomyfile"
iterations = 1000

while iterations > 0:
    print("Starting ", filename)
    p = Popen("python " + filename, shell=True)
    p.wait()
    iterations -= 1

print("somehow exited the infinite loop??")
