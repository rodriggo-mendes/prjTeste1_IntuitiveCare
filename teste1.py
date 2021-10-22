from bs4 import BeautifulSoup # Windows / MacOS: pip install beautifulsoup4
                              # Linux: pip3 install beautifulsoup4

from clint.textui import progress # Windows / MacOS: pip install clint
                                  # Linux: pip3 install clint
import requests
import sys
import os


def validacaoHTTP(resposta):
    if resposta.status_code != 200:
        print('Não foi possível acessar a página solicitada')
    if resposta.status_code >= 400 and resposta.status_code <= 499:
        print('Houve um erro de comunicação com o cliente')
    if resposta.status_code >= 500 and resposta.status_code <= 599:
        print('Houve um erro de comunicação com o servidor')
        input('\nPressione qualquer tecla para sair...\n\t')
        sys.exit()


os.system('cls')

print('\n -------------------------------------------------')
print('| BAIXAR COMPONENTE ORGANIZACIONAL DO PADRÃO TISS |')
print(' -------------------------------------------------\n')

resposta = requests.get('https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss/')
validacaoHTTP(resposta)

# Coletando o link para o Padrão TISS mais recente
codigoFonte = BeautifulSoup(resposta.content, 'html.parser')
conteudo = codigoFonte.find('div', attrs={'id' : 'content-core'})
if 'Padrão TISS' and ('Versão' or 'versão') in conteudo.h2.text:
    versaoPadraoTiss = conteudo.h2.text
    redirecaoArquivosTiss = conteudo.h2.find_next().a.get('href')
    resposta = requests.get(redirecaoArquivosTiss)
else:
    print('Não foi possível encontrar o link para o Padrão TISS mais recente')
    input('\nPressione qualquer tecla para sair...\n\t')
    sys.exit()

validacaoHTTP(resposta)

# Coletando o link do PDF do Componente Organizacional
codigoFonte = BeautifulSoup(resposta.content, 'html.parser')
tabelaDocumentos = codigoFonte.find_all('tr')
for tr in tabelaDocumentos[1:]:
    if ('Componente Organizacional' or 'componente organizacional') in tr.td:
        versaoTiss = tr.td.find_next()
        urlDownload = versaoTiss.find_next().a.get('href')
        versaoTiss = tr.td.find_next().text
        break

# Baixando o PDF do Componente Organizacional
print('VERSÃO MAIS RECENTE: ' + versaoPadraoTiss + '\n')
arquivoPdf = requests.get(urlDownload, stream = True)
with open('padrao_tiss_componente_organizacional_' + versaoTiss + '.pdf', 'wb') as pdf:
    tamanho = int(arquivoPdf.headers.get('content-length'))
    for chunk in progress.bar(arquivoPdf.iter_content(chunk_size=1024), expected_size=(tamanho/1024) + 1): 
        if chunk:
            pdf.write(chunk)
            pdf.flush()

if os.path.exists('./padrao_tiss_componente_organizacional_' + versaoTiss + '.pdf'):
    print('\nArquivo referente ao Componente Organizacional do Padrão TISS baixado com sucesso!')
else:
    print('\nNão foi possível baixar o arquivo solicitado')

input('Pressione qualquer tecla para sair...\n')