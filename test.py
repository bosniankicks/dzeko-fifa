import requests
from bs4 import BeautifulSoup
import subprocess

url = 'https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/register-interest'

headers = {
    'Host': 'www.fifa.com',
    'If-None-Match': 'W/"f8f-oQ4dWrWN+US6oYuM/02Fu4xfARM"',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'If-Modified-Since': 'Sat, 10 Aug 2024 15:07:48 GMT',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

response = requests.get(url, headers=headers)
if response.status_code == 202:
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')
    modified_script = ""
    for script in scripts:
        if script.string and 'function challenge() {' in script.string:
            start_index = script.string.find('function challenge() {')
            end_index = script.string.find('var answerCookie = "__eccha="+val+";path=/";') + len('var answerCookie = "__eccha="+val+";path=/";')
            challenge_function = script.string[start_index:end_index]
            modified_script = f"""
{challenge_function}
console.log("Val: " + val);
console.log("Token Cookie: " + tokenCookie);
console.log("Answer Cookie: " + answerCookie);
}}  // Closing brace for the challenge function
challenge();
"""
            break

    if modified_script:
        with open('data.js', 'w', encoding='utf-8') as file:
            file.write(modified_script)
        print('wrote data to data.js')
        subprocess.run(["node", "data.js"], check=True)
    else:
        print('shit not there brother')
else:
    print('fail:', response.status_code)
