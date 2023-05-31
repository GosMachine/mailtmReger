from mailtm.email import Email
import threading


def worker():
    proxypath = r'C:\Users\Sadas\Desktop\reger\mailtmReger\Webshare 10 proxies (1).txt' #путь к прокси
    test = Email(proxypath)
    test.register()
    print(f"\nEmail Adress: {test.address}:{test.password}")
    with threading.Lock():
        with open("result.txt", "a") as file:
            file.write(f"{test.address}:{test.password}\n")


threads = []
count = 0
need_accounts = 500 #сколько нужно аккаунтов
count_threads = 5 #сколько потоков
while count < need_accounts:
    for _ in range(count_threads):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    count += count_threads
