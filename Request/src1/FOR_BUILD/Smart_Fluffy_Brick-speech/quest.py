#!/usr/bin/python3
import requests, os
from bs4 import BeautifulSoup as beso
#################################################################################
def GetThingQuest(request):
	try:#Тут короче делаем реквест, получаем данные json, и расшифровываем
		for i in range(len(requests.post('https://ru.wikipedia.org/w/api.php', data={'action':'opensearch', 'search':request, 'format':'json'}).json())):
			ans = (requests.post('https://ru.wikipedia.org/w/api.php', data={'action':'opensearch', 'search':request, 'format':'json'}).json())[2][i]
			if len(ans) > 21:#тут интересная схема поиска
				qi = i
				break

		bb = 0
		eb = 0
		todel = ""
		xy = {'(':')','[':']','{':'}'}
		for x in xy:#А тут мы убираем всё, что в любых скобках(масс. "xy")
			y = xy[x]
			for i in ans:
				if i == x:
					bb += 1
				elif i == y:
					eb += 1
				if bb > 0:
					todel += i
				if (bb == eb) and (bb > 0):
					ans = ans.replace(todel, "")
					todel = ""
					bb = 0
					eb = 0

		ans = ans.lower()
		ban = {' i ':' певрый ',' ii ':' второй ',' iii ':' третий ',' iv ':' четвёртый ',' v ':' пятый ',' vi ':' шестой ', ' vii ':' седьмой ',  'viii ':' восьмой ',' iix ':' восьмой ',' ix ':' девятый ',' x ':' десятый ',' xi ':'  одиннадцатый ', ' xii ':' двенадцатый ', ' xiii ':' тринадцатый', ' xiiv ':' тринадцатый ', ' xiv ':' четырнадцатый ',' xv ':' пятнадцатый ',' xvi ':' шестнадцатый ',' xvii ':' семнадцатый ',' xviii ':' восемнадцатый ',' xiix ':' восемнадцатый ',' xix ':' девятнадцатый ',' xx ':' двадцатый ',' xxi ':' двадцать первый ',' xxii ':' двадцать второй ',' xxiii ':' двадцать третий ',' xxiiv':' двадцать третий ',' xxiv ':' двадцать четвёртый ',' xxv ':' двадцать пятый ',' xxvi ':' двадцать шестой ',' xxvii ':' двадцать седьмой','(':'',')':'','[':'',']':'','{':'','}':'','англ.':'','франц.':'','фран.':''}
		for key in list(ban.keys()):#А здесь заменяем римскую нумерацию нормальной(не идеально по родам) и подчищаем скобки и некоторые сокращения.
			ans = ans.replace(key, ban[key])
		if qi > 0:#qi -- номер ответа от Вики. если он > 0 -- значит ответ сожет быть неточным. Это мы указываем в ответе:
			ans = "Возможно, вы имели ввиду "+ans+". Wikipedia... точка org..."
		return ans
	except:
		ans = "Я вас не понял, перефразируйте запрос"
		return ans
#################################################################################
def WhatIs(text, text_arr):
	url = ""
	try:# Тут длинная цепочка поиска и определения типа запроса...
		mi = text_arr.index('такая') + 1
	except:
		try:
			mi = text_arr.index('такой') + 1
		except:
			try:
				mi = text_arr.index('такое') + 1
			except:
				try:
					mi = text_arr.index('такие') + 1
				except:
					mi = text_arr.index('значит') + 1
	mi1 = mi
	while mi1 < len(text_arr):#Тут мы составляем валидный запрос
		if mi1 > mi:
			url += " "
		url += str(text_arr[mi1])
		mi1 += 1
	ans = GetThingQuest(url)
	return ans
#################################################################################
def Trans(text, lang):
	langs = {'русский':'ru','английский':'en'}
	try:#Тут пытаемся перевести через Яндекс фразу....
		mi = text.find("переведи на ")
		a = list(langs.keys()).index(lang)
		mi = mi + len(list(langs.keys())[a]) + 12
		text = text[mi:]
		lang = langs.get(lang)
		ans = requests.post('https://translate.yandex.net/api/v1.5/tr.json/translate', data={'key':'trnsl.1.1.20160723T075443Z.3071860cf4a85efc.3fef18c09d8253d502944581b4360833ed8749f2','lang':lang,'text':text}).json()
		ans = "Ответ: "+ans['text'][0]+". Переведено Yandex... точка ru..."
	except:#...Но если у нас не получается:
		ans = "Данный язык недоступен. Доступные языки: "+str(list(langs.keys()))
	return ans
def Weather(text, text_arr):
	#Это условные названия городов для realmeteo.ru
	adds = ['великий','нижний','минеральные','санкт']#так начинаются города, состоящий из двух слов
	cities = {'абакан':'abakan','анапа':'anapa','архангельск':'arkhangelsk','астрахань':'astrakhan','барнаул':'barnaul','брянск':'bryansk','великий новгород':'vnovgorod','владивосток':'vladivostok','волгоград':'volgograd','вологда':'vologda','воронеж':'voronezh','екатеринбург':'ekaterinburg','иваново':'ivanovo','ижевск':'izhevsk','казань':'kazan','калининград':'kaliningrad','киров':'kirov','краснодар':'krasnodar','красноярск':'krasnoyarsk','магадан':'magadan','магнитогорск':'magnitogorsk','майкоп':'maykop','махачкала':'mahachkala','москва':'moscow','мурманск':'murmansk','набережные челны':'nab_chelnu','новокузнецк':'novokuznetsk','омск':'omsk','оренбург':'orenburg','пенза':'penza','пермь':'perm','псков':'pskov','санкт-петербург':'spb','саратов':'saratov','симферополь':'simferopol','смоленск':'smolensk','сочи':'sochi','сыктывкар':'syktyvkar','таганрог':'taganrog','тверь':'tver','тула':'tula','тюмень':'tumen','уфа':'ufa','хабаровск':'habarovsk','чебоксары':'cheboksary','челябинск':'chelyabinsk','ярослваль':'yaroslavl'}
	citycodes = {0:3, 1:4, 2:3, 3:4, 4:3}#это данные для поиска значений
	finlist = []#будущий лист значений
	#try:#Пробуем...
	for i in range(1):
		mi = text_arr.index("городе") + 1
		city = text_arr[mi]#город
		if adds.count(city) != 0:#Нас лучай, если название города состоит из двух слов:
			city += " "+text_arr[mi+1]
		city1=  city
		city = cities[city]#а теперь условное название города
		ans = requests.get('http://www.realmeteo.ru/'+city+'/1/current').text
		soup = beso(ans, "lxml")
		meteo = soup.findAll('td', {'class':'meteodata'})#Ищем все теги td
		for i in range(5):#перебираем по пяти параметрам(нас интересуют только перве пять в "meteo")
			meteodata = str(meteo[i])
			howtoread = citycodes[i]#какие данные читать

			meteodata = meteodata.replace("<", "|")######
			meteodata = meteodata.replace(">", "|")##тут мы подготавливаем...
			meteodata = meteodata.replace("\n", "|")#####

			meteodata = meteodata.split("|")#...И создаём массив данных...
			finlist.append(meteodata[howtoread])#...Чтобы записать его в общий лист =)

		real_temp = finlist[0]#######
		thin_temp = finlist[1]####
		baro_metr = finlist[2]#Вот тут мы вытаскиваем данные по переменным
		aqua_metr = finlist[3]####
		wind_metr = finlist[4]#######
		ans = "Погода в городе "+city1+". Температура воздуха "+real_temp+" градусов. Ощущается "+thin_temp+". Атмосферное давление "+baro_metr+" миллиметров ртутного столба. Влажность воздуха "+aqua_metr+" процентов. Скорость ветра "+wind_metr+" метров в секунду. RealMeteo... точка ru..."
	#except:#...А если не получается:
	#	ans = "Я не знаю такого города"
	return ans	

def main(text):
	l_text = text.lower()
	arr_l_text = l_text.split()
#################################################################################
	#Тут всё очевидно:
	if (arr_l_text[0] == "погода") or (arr_l_text[1] == "погода"):
		ans = Weather(text, arr_l_text)
	elif (arr_l_text[0] == "переведи") or (arr_l_text[1] == "переведи"):
		lang = arr_l_text[2]
		ans = Trans(l_text, lang)
	elif (arr_l_text[0] == "вопрос") or (arr_l_text[1] == "вопрос"):
		if (l_text.find('кто такой') != -1) or (l_text.find('кто такая') != -1) or (l_text.find('кто такое') != -1) or (l_text.find('что такое') != -1) or (l_text.find('кто такие') != -1) or ((l_text.find('что значит')) != 1):
			ans = WhatIs(l_text, arr_l_text)
	else:
		ans = "Странные вещи говорите вы. Не понимаю вас я."
	#try:
	#	os.system('clear')
	#except:
	#	os.system('cls')
	return ans

###MAIN###
#print(main(input()))