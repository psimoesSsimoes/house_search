from lxml import html
import requests
from email.mime.text import MIMEText
from subprocess import Popen, PIPE



def getHouses(link,website):
    page = requests.get(link)
    tree = html.fromstring(page.content)
    finalList=[]

    if 'olx' in website:
        prices = tree.xpath('/html/body/div[1]/div[2]/section/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[1]/td[3]/div/p/strong/text()')
        names = tree.xpath('/html/body/div[1]/div[2]/section/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/div/h3/a/strong/text()')
        area = tree.xpath('/html/body/div[1]/div[2]/section/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td[1]/div/p[2]/text()')
        href = tree.xpath('/html/body/div[1]/div[2]/section/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/div/h3/a/@href')
        for i in range(len(prices)):
            finalList.append((names[i],prices[i],area[i].strip(),'https://www.olx.pt'+href[i]))
        return finalList

    elif 'sapo' in website:
        names = tree.xpath('//*[@id]/p[1]/span/text()')
        description = tree.xpath('//*[@id]/p[2]/text()')
        price = tree.xpath('//*[@id]/div[2]/div/p[2]/span/text()')
        href = tree.xpath('//*[@id]/@href')
        href.pop(0)
        href.pop(0)
        for i in range(len(names)):
            finalList.append((names[i],description[i].strip(),price[i],'http://casa.sapo.pt'+href[i]))
        return finalList

    else:
        return ('nothing')

finalmsg = getHouses('https://www.olx.pt/imoveis/apartamento-casa-a-venda/apartamentos-arrenda/caparica/?search%5Bdescription%5D=1','olx')
finalmsg += getHouses('https://www.olx.pt/imoveis/casas-moradias-para-arrendar-vender/moradias-arrenda/caparica/?search%5Bdescription%5D=1','olx')
finalmsg += getHouses('https://www.olx.pt/imoveis/quartos-para-aluguer/caparica/?search%5Bdescription%5D=1','olx')
finalmsg += getHouses('http://casa.sapo.pt/Alugar/Apartamentos/T0-ate-T2/Almada/Costa-da-Caparica/?sa=15','sapo')


msg = MIMEText(finalmsg)
msg["From"] = "my.real.state.agent@fitman.com"
msg["To"] = "p.simoes@campus.fct.unl.pt"
msg["Subject"] = "Houses list for today."
p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
p.communicate(msg.as_string())
