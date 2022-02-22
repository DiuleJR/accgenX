password = "23051401@"  # <---Mude a senha

import requests, random, string, secmail, pyshorteners, amino, names
from bs4 import BeautifulSoup
from time import sleep
from amino.lib.util.exceptions import ActionNotAllowed, IncorrectVerificationCode, ServiceUnderMaintenance
from pyfiglet import figlet_format
from flask import Flask


abertura = figlet_format("a c c g e n  X\n       p t - b r")
print(abertura)


# ===============Funções==================
def nome_aleatorio():
    nome = ''
    for i in names.get_first_name():
        nome += i
    return nome


def api(url):
    return requests.post("https://api-xmega11.herokuapp.com/", data={"text": url}).json()['captcha']


def deviceId():
    return requests.get("https://device-xmega.herokuapp.com/").text


def gerar_aleatorio(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def gerar_email():
    email = "xmega-" + gerar_aleatorio() + "@wwjmp.com"
    return email


def link_codigo(email):
    try:
        mail = secmail.SecMail()
        sleep(2)
        inbox = mail.get_messages(email)
        for Id in inbox.id:
            msg = mail.read_message(email=email, id=Id).htmlBody
            bs = BeautifulSoup(msg, 'html.parser')
            images = bs.find_all('a')[0]
            url = (images['href'])
            if url is not None:
                return url
    except:
        pass


def encurtar_link(link):
    ps = pyshorteners.Shortener()
    return ps.tinyurl.short(fr"{link}")

app = Flask(__name__)


@app.route('/')
def home():
    return " ~~8:> \n\t\t~~8:>"


def main():
    app.run(host='0.0.0.0', port=random.randint(2000, 9000))


def rodando():
    # ==================Gerador=============================
    print("\033[34mGitHub: https://github.com/DiuleJR\033[m\n")
    print("\033[1;30;44mBy Xmega11\033[m \033[34mVersion____REPLIT_\033[m\n\n")
    print("[\033[1;31mAtenção\033[m] \033[1;33mVocê pode criar somente 5 contas por replit\033[m")
    contador = 0

    while True:

        try:
            with open("device.json", "w") as f:
                f.close()

            if contador == 5:
                print("\n[\033[1;31mAtenção\033[m] \033[1;33mVocê criou 5 contas, dê um FORK para continuar criando contas!")
                contador = 0
                break

            client = amino.Client()
            email = gerar_email()
            nickname = nome_aleatorio() + '⁹⁹⁹'
            print(f"\n[\033[1;31mGerando email\033[m][\033[1;35m{email}\033[m][\033[1;32m{contador + 1}\033[m]")
            client.request_verify_code(email=email)
            link = encurtar_link(link_codigo(email))
            print(f"[ \033[1;33mLink\033[m ] \033[1;32m{link}\033[m")
            codigo = api(link)

            print(f"[\033[1;37mCódigo\033[m]: {codigo}")
            # codigo = input("[\033[1;37mCódigo\033[m]: ")
            # slk = api(link)
            if codigo == '':
                print("\n[\033[1;31mAtenção\033[m] \033[1;33mVocê não digitou o código, reinicie o script!")
                break

            device = deviceId()
            client.register(nickname, email, password, codigo, device)
            client.login(email=email, password=password)
            client.join_community("39276113")  # <----- Sua cid da comunidade
            print("[\033[1;32mConta salva!\033[m]")
            contador += 1

        except ActionNotAllowed:
            print("\n[\033[1;31mAtenção\033[m] \033[1;33mLimite de contas criadas atingido, dê um FORK para continuar criando contas\033[m")
            break

        except IncorrectVerificationCode:
            print("\n[\033[1;31mAtenção\033[m] \033[1;33mVocê digitou o código errado, reinicie o script!\033[m")
            break

        except ServiceUnderMaintenance:
            print("\n[\033[1;31mAtenção\033[m] \033[1;33mParece que o serviço está em manutenção, tente mais tarde!")
            break

        except:
            print("\n[\033[1;31mAtenção\033[m] \033[1;33mErro desconhecido, tente reiniciar o script!")
            break

        with open("accounts.json", "a+") as x:
            acc = f'\n{{\n"email": "{email}",\n"password": "{password}",\n"device": "{device}"\n}},'
            # acc = f'\n{{\n"email": "{email}",\n"password": "{password}",\n"device": "{device}"\n}},'
            x.write(acc)

        with open("emails.txt", "a+") as c:
            acc = f"{email}\n"
            c.write(acc)


if __name__ == "__main__":
    rodando()
