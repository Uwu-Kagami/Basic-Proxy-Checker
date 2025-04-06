import requests
import concurrent.futures
import time

PROXY_FILE = "PROXY_FILE"
VALID_PROXY_FILE = "VALID_PROXY_FILE"

def read_prox(file):
    try:
        with open(file, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Le fichier {file} est introuvable.")
        return []

def try_prox(proxy, test_url="https://www.google.com"):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"https://{proxy}"
    }
    
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"✅ Proxy valide : {proxy}")
            return proxy
    except requests.exceptions.RequestException:
        print(f"❌ Proxy invalide : {proxy}")
    
    return None

def checkprox():
    print("Chargement des proxys...")
    proxies = read_prox(PROXY_FILE)
    
    if not proxies:
        print("Aucune adresse proxy trouvée.")
        return

    print(f"🔹 {len(proxies)} proxys trouvés. Test en cours...")

    valid_proxies_tahlesfou = []
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(try_prox, proxies))

    valid_proxies_tahlesfou = [proxy for proxy in results if proxy]

    with open(VALID_PROXY_FILE, "w") as f:
        f.write("\n".join(valid_proxies_tahlesfou))

    print(f"\n✅ {len(valid_proxies_tahlesfou)} proxys fonctionnels trouvés et enregistrés dans {VALID_PROXY_FILE}")
    print(f"Total time : {round(time.time() - start_time, 2)} secondes.")

if __name__ == "__main__":
    checkprox()
