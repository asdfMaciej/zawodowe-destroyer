import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup


class PlociennikFetcher:
	def __init__(self):
		self.url = 'http://plociennik.info/index.php/informatyka/egzamin-zawodowy/losowane-pytania-z-bazy'
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
			'Accept-Language': 'en-US,en;q=0.8,pl;q=0.6',
			'Referer': 'http://plociennik.info/index.php/informatyka/egzamin-zawodowy/losowane-pytania-z-bazy',
			'Origin': 'http://plociennik.info',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept-Encoding': 'gzip, deflate',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
		}
		self.cookies = {
			'info_test': '1',
			'info_cookie': '1',
			'5cdd60449ffc722bb02339a9718ea7e9': 'a1seuqkrfbud3lhruar8fehfk4'
		}
		self.limit = 600

	def post_params_create(self, egzamin, n):
		if int(n) > self.limit:
			return 0
		if str(egzamin).upper() not in ('E12', 'E13', 'E14'):
			return 0	
		return {
			'liczba_pytan': str(n),
			'kwalifikacja': str(egzamin).upper(),
			'option': 'com_egzamin',
			'view': 'losowanie',
			'task': 'zapisz'
		}

	def fetch_egzamin(self, egzamin):
		if str(egzamin).upper() not in ('E12', 'E13', 'E14'):
			return 0

		n = 500
		if egzamin == 'E12':
			n = 600
		if egzamin == 'E14':
			n = 400
		params = self.post_params_create(egzamin, n)
		print(params)
		r = requests.post(self.url, data=params, headers=self.headers, cookies=self.cookies)
		r.encoding = 'UTF-8'
		return (n, r.text)

	def fetch_egzamin_questions(self, egzamin):
		if str(egzamin).upper() not in ('E12', 'E13', 'E14'):
			return 0
		n, txt = self.fetch_egzamin(egzamin)
		ids = txt.split('<input type="hidden" name="cid" value="')[1:]
		for n, _id in enumerate(ids):
			ids[n] = _id.split('"')[0]

		params = {
			'option': 'com_egzamin',
			'view': 'losowanie',
			'boxchecked': '0',
			'task': 'zapisz-test',
			'liczba_pytan': str(n),
			'kwalifikacja': str(egzamin).upper(),
			'zakoncz': 'Zakończ test',
			'cid': ids,
			'zadania': ','.join(ids)
		}

		r = requests.post(self.url, data=params, headers=self.headers, cookies=self.cookies)
		r.encoding = 'UTF-8'

		pytania = []
		letters_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
		pytki = str(r.text).split('<div class="pyt">')[1:]
		for n_p, p in enumerate(pytki):
			question = p.split('<p>')[1].split('</p>')[0]
			answers = []
			correct = -1
			an = p.split('<div class="odp')[1:]
			for n, a in enumerate(an):
				if a[0] == 'p':  # odpp instead of odp
					correct = n
				answers.append(a.split("'>")[2].split('</p>')[0])
			pytania.append([ids[n_p], question, answers, letters_map[correct], correct])

		return pytania

pf = PlociennikFetcher()
questions = []
questions_ids = []
json_out = {'E12':{}, 'E13':{}, 'E14':{}}
for egzam in ('E12', 'E13', 'E14'):
	for a_n in range(3):
		a = pf.fetch_egzamin_questions(egzam)
		for __q in a:
			if __q[0] not in questions_ids:
				questions_ids.append(__q[0])
				questions.append(__q)
	out_txt = ""

	for nq, q in enumerate(questions):
		soup = BeautifulSoup(q[1])
		txt = str(nq) + '.' + '.'.join(soup.get_text().split('.')[1:])
		out_txt += txt + "\n"
		for n, _q in enumerate(q[2]):
			if q[4] == n:
				out_txt += "DOBRZE - "
			out_txt += _q + "\n"
		out_txt += "\n"
		json_out[egzam][q[0]] = [txt, q[2][0], q[2][1], q[2][2], q[2][3], q[3], q[4]]

print(out_txt)
#with open('pytania.txt', 'w', encoding='utf-8') as f:
#	f.write(out_txt)
with open('pytania.json', 'w', encoding='utf-8') as j:
	json.dump(json_out, j, ensure_ascii=False)
#pf.fetch_egzamin_questions('E12')