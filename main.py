from lxml import html
import requests
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.utils.encoding import smart_str, smart_unicode
from subprocess import Popen, PIPE



def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)


def getHouses(link,website):
    page = requests.get(link)
    tree = html.fromstring(page.text)
    finalList=[]

    if 'olx' in website:
        prices = tree.xpath('/html/body/div[1]/div[2]/section/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[1]/td[3]/div/p/strong/text()')
        names = tree.xpath('/html/body/div[1]/div[2]/section/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/div/h3/a/strong/text()')
        area = tree.xpath('/html/body/div[1]/div[2]/section/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td[1]/div/p[2]/text()')
        href = tree.xpath('/html/body/div[1]/div[2]/section/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/div/h3/a/@href')
        for i in range(len(prices)):
            finalList.append([names[i],prices[i],area[i].strip(),href[i]])
	
        return finalList

    elif 'sapo' in website:
        names = tree.xpath('//*[@id]/p[1]/span/text()')
        description = tree.xpath('//*[@id]/p[2]/text()')
        price = tree.xpath('//*[@id]/div[2]/div/p[2]/span/text()')
        href = tree.xpath('//*[@id]/@href')
        href.pop(0)
        href.pop(0)
        for i in range(len(names)):
            finalList.append([names[i],description[i].strip(),price[i],href[i]])
        return finalList

    else:
        return ('nothing')

finalmsg = getHouses('https://www.olx.pt/imoveis/apartamento-casa-a-venda/apartamentos-arrenda/caparica/?search%5Bdescription%5D=1','olx')
finalmsg += getHouses('https://www.olx.pt/imoveis/casas-moradias-para-arrendar-vender/moradias-arrenda/caparica/?search%5Bdescription%5D=1','olx')
finalmsg += getHouses('https://www.olx.pt/imoveis/quartos-para-aluguer/caparica/?search%5Bdescription%5D=1','olx')
finalmsg += getHouses('http://casa.sapo.pt/Alugar/Apartamentos/T0-ate-T2/Almada/Costa-da-Caparica/?sa=15','sapo')

finalstr=''
for i in finalmsg:
	try:
		print (re.sub(r'[\x80-\xFF]+', convert, i[0]))
		finalstr+='<h1>'+re.sub(r'[\x80-\xFF]+', convert,i[0])+'</h1>'
		finalstr+='<h2>'+re.sub(r'[\x80-\xFF]+', convert,i[1])+'</h2>'
		for j in range(2,4):
			print (re.sub(r'[\x80-\xFF]+', convert,i[j])) 
	        	finalstr+="<p>"+re.sub(r'[\x80-\xFF]+', convert,i[j])+"</p>"
	except UnicodeEncodeError:
		print ("did exceptionnnnnnnnnnnnnnn")
		finalstr+='<h1>Casa com encoding Malefico</h1>'
                for j in range(1,4):
                        print (re.sub(r'[\x80-\xFF]+', convert,i[j]))
                        finalstr+="<p>"+re.sub(r'[\x80-\xFF]+', convert,i[j])+"</p>"


finalstr = finalstr.encode('utf8')  
me = "my.real.state.agent@myownserver.com"
you = "p.simoes@campus.fct.unl.pt"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Today's House List"
msg['From'] = me
msg['To'] = you

html = """\
<html>
  <head></head>
  <body>
        """+finalstr+""" </body>
</html>
"""

part2 = MIMEText(html, 'html')
msg.attach(part2)

p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
p.communicate(msg.as_string())

