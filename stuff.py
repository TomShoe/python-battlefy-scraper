from datetime import datetime,timedelta
from pytz import timezone
import requests,json,sys
from teams import teams

team1, team2, score1, score2, winner, date = ([] for y in range(6))
hour, minute, month, day, year = ([] for y in range(5))
timex = []

def jloader():
	
	link = "https://dtmwra1jsgyb0.cloudfront.net/stages/5e223506edae743046ecdaa1/groups/round/1"
	response = json.loads(requests.get(link).text)
	x = len(response)
	
	if "match" in link:
		matchFillSingle(x, response)
	
	if "group" in link:
		count = 0
		inner = []
		for i in range(x):
			inner.append(len(response[i]['matches']))
			count = count+1	
		matchFill(x, response, inner, count)

	winnerFill()
	rename()
	printer()
		
def matchFillSingle(con, response):

	def nameFill(x):
		for i in range(x):
			try:
				team1.append(response[i]['top']['name'])
			except KeyError:
				team1.append('')	
				continue

		for i in range(x):	
			try:
				team2.append(response[i]['bottom']['name'])
			except KeyError:
				team2.append('')	
				continue
		

	def scoreFill(x):
		for m in range(x):	
			try:
				score1.append(response[m]['top']['score'])
			except KeyError:
				score1.append('')	
				continue

		for n in range(x):	
			try:
				score2.append(response[n]['bottom']['score'])
			except KeyError:
				score2.append('')	
				continue
	
	def getTime(x):
		b = 0
		for b in range(x):
			try:
				timex.append(datetime.strptime(response[b]['schedule']['startTime'], '%Y-%m-%dT%H:%M:%S.%fZ'))
			except KeyError:
				timex.append(datetime.strptime(response[b]['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ'))
			except ValueError:
				timex.append(datetime.strptime(response[b]['schedule']['startTime'], '%Y-%m-%dT%H:%M:%SZ'))
				
		for y in range(len(timex)):
			timex[y] = (timex[y] - timedelta(hours=8))
						
		for a in range(x):
			date.append(timex[a].strftime("%Y-%m-%d"))
			hour.append(timex[a].strftime("%H"))
			minute.append(timex[a].strftime("%M"))

	
	nameFill(con)
	scoreFill(con)
	getTime(con)
	return
	
	
def matchFill(con, response, inner, count):


	def nameFill(x, inner):
		j = 0
		k = 0
		for i in range(x):
			m = inner[i]
			for j in range(m):
				try:
					team1.append(response[i]['matches'][j]['top']['team']['name'])
				except KeyError:
					team1.append('')	
					continue

		for i in range(x):
			m = inner[i]
			for k in range(m):
				try:
					team2.append(response[i]['matches'][k]['bottom']['team']['name'])
				except KeyError:
					team2.append('')	
					continue
		

	def scoreFill(x, inner):
		n = 0
		p = 0
		for m in range(x):	
			k = inner[m]
			for n in range(k):
				try:
					score1.append(response[m]['matches'][n]['top']['score'])
				except KeyError:
					score1.append('')	
					continue

		for m in range(x):	
			k = inner[m]
			for p in range(k):
				try:
					score2.append(response[m]['matches'][p]['bottom']['score'])
				except KeyError:
					score2.append('')	
					continue
	
	def getTime(x, inner):
		for b in range(x):
			k = inner[b]
			for g in range(k):
				try:
					timex.append(datetime.strptime(response[b]['matches'][g]['schedule']['startTime'], '%Y-%m-%dT%H:%M:%S.%fZ'))
				except KeyError:
					timex.append(datetime.strptime(response[b]['matches'][g]['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ'))
					continue
				except ValueError:
					timex.append(datetime.strptime(response[b]['matches'][g]['schedule']['startTime'], '%Y-%m-%dT%H:%M:%SZ'))
		
		for y in range(len(timex)):
			timex[y] = (timex[y] - timedelta(hours=8))
			
		for a in range(len(timex)):
			date.append(timex[a].strftime("%Y-%m-%d"))
			hour.append(timex[a].strftime("%H"))
			minute.append(timex[a].strftime("%M"))

	
	nameFill(con, inner)
	scoreFill(con, inner)
	getTime(con, inner)
	return	
	
			
					
def winnerFill():		
	for j in range(len(team1)):
			if (score1[j] > score2[j]):
					winner.append('1')
			elif (score2[j] > score1[j]):
					winner.append('2')
			else:
					winner.append('')
					
def rename():		
	for g in range(len(team1)):
		team1[g] = teams.get(str(team1[g]), team1[g])
		team2[g] = teams.get(str(team2[g]), team2[g])	

def printer():
	for y in range(len(team1)):
		print("{{MatchSchedule" + "|team1=" + str(team1[y]) + "|team2=" + str(team2[y]) + "|team1score=" + str(score1[y]) + "|team2score=" + str(score2[y]) + "|winner=" + str(winner[y]) + "|date=" + str(date[y]) + "|time=" + str(hour[y]) + ":" + str(minute[y]) + "|timezone=PST|dst=no|vod1=|stream=}}")
	
if __name__ == "__main__":
	jloader()
