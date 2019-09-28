import requests
import bs4

r = requests.get('http://ejudge.cfuv.ru/2019/III_semestr/standings/standings38.html')
r.encoding = 'utf-8'
b = bs4.BeautifulSoup(r.text, features='lxml')
table = b.find_all('table')[1]

data = {

}

tasks = table.find_all('tr')

for row in tasks[1:len(tasks) - 3]:
    res = []
    row = row.find_all('td')
    #print(row)
    for cell in row[2:len(row) - 2]:
        #print('chk')
        c = cell.get_text()
        if (c[0] == '+'):
            res.append(c)
        else:
            if ('cell_attr_pr' in cell['class']):
                res.append('?' + c[1:])
            elif c[0] == '-':
                res.append(c)
            else:
                res.append('.')
    data[row[1].get_text()] = res
for i in data:
    print(i, end = " ")
    print(" ".join(data[i]))