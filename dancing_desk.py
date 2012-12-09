import pygame
# from collections import deque
pygame.display.init()
pygame.joystick.init()
stick = pygame.joystick.Joystick(pygame.joystick.get_count()-1)
stick.init()

numaxes = stick.get_numaxes()
numbuttons = stick.get_numbuttons()
numhats = stick.get_numhats()
# print "numaxes:", numaxes

pygame.event.set_allowed([pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYAXISMOTION])

P1_EVENT_SEQUENCE = []
P2_EVENT_SEQUENCE = []

def read_p1(evt):
	# print evt
	if evt.type == pygame.JOYAXISMOTION:
		value = round(evt.value)
		# print "joy axis motion", evt.type, value
		if evt.axis == 6:
			if value == -1:
				return "left"
			elif value == 1:
				return "right"
		elif evt.axis == 7:
			if value == -1:
				return "up"
			elif value == 1:
				return "down"
	elif evt.type == pygame.JOYBUTTONDOWN:
		if evt.button == 12:
			return "triangle"
		elif evt.button == 13:
			return "o"
		elif evt.button == 14:
			return "x"
		elif evt.button == 15:
			return "square"
		elif evt.button == 20:
			return "select"
		elif evt.button == 21:
			return "start"
	elif evt.type == pygame.JOYBUTTONUP:
		# do we actually need to track the up events?
		pass
	return False # if nothing matched return false

def read_p2(evt):
	# print evt
	if evt.type == pygame.JOYAXISMOTION:
		value = round(evt.value)
		if evt.axis == 3:
			if value == -1:
				return "up"
			elif value == 1:
				return "down"
		elif evt.axis == 2:
			if value == -1:
				return "left"
			elif value == 1:
				return "right"
	elif evt.type == pygame.JOYBUTTONDOWN:
		if evt.button == 0:
			return "triangle"
		elif evt.button == 1:
			return "o"
		elif evt.button == 2:
			return "x"
		elif evt.button == 3:
			return "square"
		elif evt.button == 8:
			return "select"
		elif evt.button == 9:
			return "start"
	elif evt.type == pygame.JOYBUTTONUP:
		# do we actually need to track the up events?
		pass
	return False # if nothing matched return false

def read_event(evt):
	# left side (player 1)
	# up: 		get_axis(8) == -1
	# down:		get_axis(8) == 1
	# left:		get_axis(7) == -1
	# right:	get_axis(7) == 1
	# get_axis(7) and get_axis(8)
	# triangle:		get_button(12)
	# o:			get_button(13)
	# x:			get_button(14)
	# square:		get_button(15)
	# select: 		get_button(20)
	# start:		get_button(21)

	# right side (player 2)
	# up: 		get_axis(4) == -1
	# down:		get_axis(4) == 1
	# left:		get_axis(3) == -1
	# right:	get_axis(3) == 1
	# get_axis(3) and get_axis(4)
	# triangle:		get_button(0)
	# o:			get_button(1)
	# x:			get_button(2)
	# square:		get_button(3)
	# select: 		get_button(8)
	# start:		get_button(9)
	# print pygame.event.event_name(evt.type)
	# print evt

	p1 = read_p1(evt)
	# print evt, p1
	if p1 != False:
		print "p1:", p1
		P1_EVENT_SEQUENCE.append(p1)
		parse_event_sequence(P1_EVENT_SEQUENCE)
		return True
	else:
		p2 = read_p2(evt)
		if p2 != False:
			print "p2:",p2
			P2_EVENT_SEQUENCE.append(p2)
			parse_event_sequence(P2_EVENT_SEQUENCE)
			return True
	return False

import shlex, subprocess
from subprocess import call,check_output
def staging_deploy():
	call(["open","http://inewsdeploy.prvt.nytimes.com/projects/145/stages/331/deployments/new?task=deploy"])
def nice_moves():
	call(["osascript", "-e", '"set Volume 10"'])
	call(["say", "-v", 'agnes', "-r", "270", '"nice moves"'])
def git_commit():
	subprocess.Popen(shlex.split("git commit -am 'dancing desk commit'"), cwd="/Users/204377/Desktop/dancing_desk/")

def git_push():
	subprocess.Popen(shlex.split("git push origin master"), cwd="/Users/204377/Desktop/dancing_desk/")

COMMANDS = {
	"staging_deploy": staging_deploy,
	"nice_moves": nice_moves,
	"git_commit": git_commit,
	"git_push": git_push
}
KEYWORDS = ["up","down","left","right","triangle","o","x","square","select","start"]
PATTERNS = [
	[["up", "right", "down", "left"], "squiggle"],
	[["up"], "up"],
	[["square","square","square"], "git_commit"],
	[["o","o","o"], "git_push"],
	[["select","start"], "staging_deploy"],
	[["up","up","down","down","left","right","left","right","o","x","start"], "nice_moves"]
]

def parse_event_sequence(seq):
	# print seq
	for pat,out in PATTERNS:
		if len(seq) >= len(pat) and seq[len(seq)-len(pat):] == pat:
			if COMMANDS.has_key(out): COMMANDS[out]()
			print out + "!"


while True:
	# pygame.event.pump()
	# print [round(stick.get_axis(i)) for i in range(numaxes)]
	# buttons = [(i,stick.get_button(i)) for i in range(numbuttons)]
	# print buttons	
	# print [stick.get_hat(i) for i in range(numhats)]
	# print [stick.get_axis(i) for i in range(numaxes)] + [stick.get_button(i) for i in range(numbuttons)]

	# block execution until another event comes
	read_event(pygame.event.wait())
		
