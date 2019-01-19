import ssl, socket, csv
from urllib.request import urlopen
from datetime import datetime


error_domains = []

# Чтение списка доменов


def get_domains():
    with open("domains.txt") as file:
        domains = [row.strip() for row in file]
    return domains


# Проверка домена на ошибки


def check_domain(domain):
    # Игнорируем проверку ssl сертификатаИ
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        resp = urlopen(domain, context=ctx)
        code = resp.getcode()
        if (code not in [200, 301]):
            return False
        else:
            return True
    except socket.error:
        return False

# Логирование ошибок


def log(domain):
    with open('error.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now(), domain, 'error'])

# Проверка доменов на ответы


domains = get_domains()

for domain in domains:
    if not check_domain(domain):
        log(domain)
        error_domains.append(domain)