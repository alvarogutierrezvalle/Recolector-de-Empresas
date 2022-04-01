import requests
from bs4 import BeautifulSoup
import pandas as pd


#Pegamos el link de la web con el filtro que querramos buscar
web_metal = 'https://www.expansion.com/empresas-de/fabricacion-de-metal-excepto-maquinaria-y-equipos-de-transporte/madrid/'
web_equipotransportes = "https://www.expansion.com/empresas-de/equipos-de-transportes/madrid/"
lista_empresas = []

page_web = web_metal
PAGINAS = 2

for i in range(1,PAGINAS+1):
    print("pagina:", i)
    try:
        r = requests.get(page_web)
        soup = BeautifulSoup(r.text, 'lxml')

        tabla_empresas = soup.find('div', id='simulacion_tabla')
        empresas = tabla_empresas.find_all('li', class_=None)

        for n in empresas:

            link= n.find('a')['href']
            poblacion= n.find('li', class_="col2")
        
            #A continuación hacemos un beautifulsoup de cada página de empresa, para sacar los datos

            r = requests.get(link)
            soup = BeautifulSoup(r.text, 'lxml')

            nombre_empresa = soup.find("td", id="nombre_empresa_dato")
            empleados = soup.find("td", id="numero_empleados_dato")
            facturacion = soup.find("td", id="facturacion_dato")
            sector = soup.find("td", id="sector_empresa")
            direccion = soup.find("td", id="direccion_empresa")
            telefono = soup.find("td", id="telefono_empresa")

            data_empresa = {"nombre": nombre_empresa.get_text(),
                            "web": link,
                            "empleados":empleados.get_text(),
                            "facturacion":facturacion.get_text(),
                            "sector":sector.get_text(),
                            "dirección":direccion.get_text(),
                            "poblacion":poblacion.get_text(),
                            "telefono":telefono.get_text()
                            }
            lista_empresas.append(data_empresa)
        i+=1
        page_web = web_metal+str(i)+".html"
    except:
        pass

df = pd.DataFrame(list(lista_empresas))

order = ["nombre","web","empleados","facturacion","sector","dirección","poblacion","telefono"]
df = df[order]

df.to_excel('empresas_data.xlsx', index = False)

