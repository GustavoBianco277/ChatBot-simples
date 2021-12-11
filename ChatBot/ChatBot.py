import pygame
pygame.init()
cont = 0
Janela = pygame.display.set_mode((1024, 600))
pygame.display.set_caption('Project_X')
CorAtiva = (0, 0, 255)
CorInativa = color = (255, 0, 0)
CorTexto = (255, 255, 255)
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial black', 20)
text = ''
texto = font.render(' ', True, (255, 255, 255))
PosTexto = texto.get_rect()
rect = pygame.Rect(100, 530, 800, 50)
Texto = font.render(text, True, CorTexto)
active = False
contador = 0
tst = 300
conversa = [' ']


def Horario():
    from datetime import datetime
    hora = datetime.today().hour
    minuto = datetime.today().minute
    if hora < 10:
        hora = '0' + str(hora)
    if minuto < 10:
        minuto = '0' + str(minuto)
    horario = str(f'{hora}:{minuto}')
    return horario


def Data():
    from datetime import datetime
    dia = datetime.today().day
    mes = datetime.today().month
    ano = datetime.today().year
    if dia < 10:
        dia = '0' + str(dia)
    if mes < 10:
        mes = '0' + str(mes)
    data = str(f'{dia}/{mes}/{ano}')
    return data


def RemoveLetras(Interracao):
    Pergunta = ''
    cont = 1
    Interracao = str(Interracao).lower()
    for letra in Interracao:
        try:
            if Interracao[cont] != letra:
                Pergunta += letra
            cont += 1
        except IndexError:
            Pergunta += letra
            break
    return str(Pergunta).title().strip()


def RemovePalavras(Lista, Sinais, Pergunta):
    for c in range(0, 2):
        for palavra in Lista:
            palavra = str(palavra).title()
            if palavra in Pergunta:
                Pergunta = Pergunta.replace(palavra + str(' '), '')
            if palavra in Pergunta:
                Pergunta = Pergunta.replace(str(' ') + palavra, '')
            if "  " in Pergunta:
                Pergunta = Pergunta.replace('  ', ' ')
        for sinal in Sinais:
            if sinal in Pergunta:
                Pergunta = Pergunta.replace(sinal, '')
    return str(Pergunta).title().strip()


def AnalizeCritica(Lista, NomeLista, Pergunta):
    for palavra in Lista:
        if palavra in Pergunta:
            Pergunta = Pergunta.replace(str(f'{palavra}'), NomeLista)
            break
    return str(Pergunta).title().strip()


def CopiarAprendizado(NomeLista):
    Lista = []
    cont = 1
    ListaT = []
    NomeLista = NomeLista.upper()
    with open('lib/memory/memoria.txt', 'r') as arquivo:
        for linha in arquivo:
            ListaT.append(linha.replace('\n', ''))
        while ListaT[cont] != NomeLista:
            cont += 1
            continue
        for c in range(cont, len(ListaT)):
            if ListaT[c] == NomeLista:
                continue
            if ListaT[c] != '':
                Lista.append(ListaT[c].replace('\n', ''))
            else:
                break
    return Lista


palavrasDesnecessarias = CopiarAprendizado('palavrasdesnecessarias')
despedida = CopiarAprendizado('despedida')
comprimento = CopiarAprendizado('comprimento')
acenar = CopiarAprendizado('acenar')
elogio = CopiarAprendizado('elogio')
desrespeito = CopiarAprendizado('desrespeito')
sinais = CopiarAprendizado('sinais')
aberto = True
while aberto:
    clock.tick(500)
    interracao = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            aberto = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = CorAtiva if active else CorInativa
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    interracao = text
                    if interracao != '':
                        Space = True
                    else:
                        Space = False
                    if Space:
                        tst -= 70
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                Texto = font.render(text, True, CorTexto)
    Janela.fill((30, 30, 30))
    Janela.blit(Texto, (rect.x + 5, rect.y + 5))
    pygame.draw.rect(Janela, color, rect, 2)
    b = pygame.draw.rect(Janela, (0, 0, 255), (0, 450, 1025, 10))
    # Mostra na tela
    Janela.blit(texto, PosTexto)
    altura = tst
    contador = 0
    for linha in conversa:
        linha = str(linha).capitalize()
        if contador % 2 == 1:
            Txtconv = font.render(linha, True, (0, 255, 0))
            tamanho = Txtconv.get_rect().width
            a = pygame.draw.rect(Janela, (30, 30, 30), (900-tamanho, altura+7, tamanho, 20))
            Janela.blit(Txtconv, (900-tamanho, altura))
        else:
            Txtconv = font.render(linha, True, (255, 255, 255))
            tamanho = Txtconv.get_rect().width
            a = pygame.draw.rect(Janela, (30, 30, 30), (100, altura + 7, tamanho, 20))
            Janela.blit(Txtconv, (100, altura))
        altura += 30
        contador += 1
        if a.colliderect(b):
            colidiuC = True
        else:
            colidiuC = False
    if not colidiuC:
        tst += 2
    pygame.display.flip()
    despedidaBool = perguntaMem = comprimentoBool = porqueBool = perguntaBool = Aprende = False
    # Transfere a memoria para uma lista
    lista = CopiarAprendizado('aprendizado')
    if interracao == "":
        continue
    else:
        conversa.append(interracao)
        # Salva novos dados
        if 'NAO APRENDI ISSO AINDA, O QUE DEVO RESPONDER ?' in lista[cont]:
            pergunta = str(interracao).upper()
            arquivo = open('lib/memory/memoria.txt', 'a')
            arquivo.write(pergunta + '\n')
            arquivo.close()
            PosTexto.center = (370, 490)
            texto = font.render('Jac Aprendeu isso !', True, (0, 255, 0))
            Janela.blit(texto, PosTexto)
            cont = 0
            comprimentoBool = True
            Space = False
        with open('lib/memory/memoria.txt', 'r') as arq:
            ListaGlobal = arq.readlines()
        if ListaGlobal[-1].istitle():
            ListaGlobal.remove(ListaGlobal[-1])
        with open('lib/memory/memoria.txt', 'w') as rebot:
            for plv in ListaGlobal:
                rebot.write(plv)
        # Remove as letras desnecessarias
        pergunta = RemoveLetras(interracao)
        # Remove as palavras desnecessarias
        pergunta = RemovePalavras(palavrasDesnecessarias, sinais, pergunta)
        # Responde o comprimento
        if pergunta in comprimento:
            if 'TUDO CERTO, E COM VOCE ?' in lista[cont]:
                cont = 0
                comprimentoBool = True
                conversa.append('Que Bom !')
        if pergunta in 'Legal':
            conversa.append('Uhum')
            comprimentoBool = True
        # responde o porque
        if pergunta in "Porque Por Que Como Asim Porque Nao Por Que Nao Iso Erado Iso Nao Certo":
            try:
                if 'ISSO SERIA IMPOSSIVEL !' in lista[cont]:
                    porqueBool = True
                    conversa.append('Porque eu sou um sistema virtual, e voces humanos são "Reais" !')
                elif 'NAO NE' in lista[cont]:
                    print(f'Jac: \033[1;33mPorque eu nao tenho como andar !')
                    porqueBool = True
                elif 'NAO TENHO SEXO DEFINIDO !' in lista[cont]:
                    print(f'Jac: \033[1;33mEu sou um sistema virtual, nao tem porque eu ter sexo !')
                    porqueBool = True
                else:
                    print(f'Jac: \033[1;33mQue ?')
                    porqueBool = True
            except IndexError:
                print('\033[1;31mNão faça frases sem sentido !')
                porqueBool = True
        # Analiza critica
        pergunta = AnalizeCritica(elogio, '(elogio)', pergunta)
        pergunta = AnalizeCritica(desrespeito, '(desrespeito)', pergunta)
        pergunta = AnalizeCritica(comprimento, ' (comprimento)', pergunta)
        # Analiza se é um aceno
        if pergunta in acenar:
            comprimentoBool = True
            conversa.append(str(pergunta).capitalize())
            PosTexto.center = (370, 475)
            texto = font.render('', True, (0, 255, 0))
            Janela.blit(texto, PosTexto)
        # Analiza se é uma despedida
        for palavra in despedida:
            if palavra in pergunta:
                despedidaBool = True
                conversa.append('Tchau')
                PosTexto.center = (370, 475)
                texto = font.render('', True, (0, 255, 0))
                Janela.blit(texto, PosTexto)
                break
        # Analiza essas perguntas antes de usar a memoria
        if pergunta in 'E Que Horas Sao Agora E Que Horas Que Sao Que Horas Sao As Horas':
            perguntaBool = True
            conversa.append(f'São {Horario()}')
            PosTexto.center = (370, 475)
            texto = font.render('', True, (0, 255, 0))
            Janela.blit(texto, PosTexto)
        elif pergunta in 'E Que Dia E Hoje Em Que Dia Nos Estamos Hoje E Que Dia O Dia De Hoje':
            perguntaBool = True
            conversa.append(f'Hoje é {Data()}')
            PosTexto.center = (370, 475)
            texto = font.render('', True, (0, 255, 0))
            Janela.blit(texto, PosTexto)
        elif pergunta in 'E Qual E Seu Nome E Qual E O Seu Nome E Qual O Seu Nome':
            perguntaBool = True
            conversa.append('Meu nome e Jac')
            PosTexto.center = (370, 475)
            texto = font.render('', True, (0, 255, 0))
            Janela.blit(texto, PosTexto)
        if comprimentoBool or despedidaBool or porqueBool or perguntaBool:
            continue
        # Procura a pergunta no banco de memoria
        else:
            cont = 0
            for linha in lista:
                cont += 1
                if pergunta in linha:
                    perguntaMem = True
                    break
            # Da resposta para o usuário
            if perguntaMem:
                frase = lista[cont].replace('\n', '')
                conversa.append(f'{frase.capitalize()}')
                PosTexto.center = (370, 475)
                texto = font.render('', True, (0, 255, 0))
                Janela.blit(texto, PosTexto)
            # Diz que nao sabe responder e tenta aprender
            else:
                Resposta = pergunta
                pergunta = '(ErrorNotInMemory)'
                cont = 0
                for linha in lista:
                    cont += 1
                    if pergunta in linha:
                        Aprende = True
                        break
                if Aprende:
                    frase = lista[cont].replace('\n', '')
                    arquivo = open('lib/memory/memoria.txt', 'a')
                    arquivo.write(str(Resposta).strip().title() + '\n')
                    texto = font.render(f'{frase.capitalize()}', True, (255, 0, 0))
                    PosTexto.center = (220, 490)
                    Janela.blit(texto, PosTexto)
                    Space = False
                    arquivo.close()
pygame.quit()
