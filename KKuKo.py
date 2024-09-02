import requests
import os
import random

def get_last_char(word):
    return word[-1]

def map_initial_consonant(char):
    consonant_map = {
        '뇰':'욜',
        '류': '뉴',
        '녀': '여',
        '뇨': '요',
        '뉴': '유',
        '니': '이',
        '랴': '야',
        '려': '여',
        '례': '예',
        '료': '요',
        '리': '이',
        '랏': '낫',
        '력': '역',
        '뉵': '육',
        '렁': '넝',
        '랄': '날',
        '륵': '늑',
        '년': '연',
        '름':'늠',
        '렬': '열',
        '률': '율',
        '릇': '늣',
        '림': '임',
        '롭': '놉',
        '렁': '넝',
        '롄': '옌',
        '뢰': '뇌',
        '뇽': '용',
        '녁': '역',
        '릿': '잇',
        '룰': '눌'
    }
    return consonant_map.get(char, char)

def check_dueum_and_match(last_char, word):
    first_char = word[0]
    
    if first_char == last_char:
        return True
    
    mapped_char = map_initial_consonant(last_char)
    return mapped_char == first_char

def send_request(start_word, used_words):
    base_link = "https://kkutudic.pythonanywhere.com/"

    payload = {
        'start': start_word,
        'end': '',
        'wordlen': '',
        'file': '',
        'sort_order': 'desc',
        'apply_dueum': 'true',
        'sort_by_next_words': 'false'
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Accept': "*/*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Accept-Language': "ko-KR,ko;q=0.9,en-US;q=0.8,en-US;q=0.7",
        'Connection': "keep-alive",
        'Host': "kkutudic.pythonanywhere.com",
        'Origin': "https://kkutudic.pythonanywhere.com",
        'Referer': "https://kkutudic.pythonanywhere.com/",
        'Sec-Ch-Ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'Sec-Ch-Ua-Mobile': "?0",
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'X-Requested-With': "XMLHttpRequest"
    }

    try:
        print(f"요청 중: '{start_word}'로 시작하는 단어를 찾고 있습니다...")
        response = requests.post(base_link, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            word_list = data.get('missionword', [])
            available_words = [word_info[0] for word_info in word_list if word_info[0] not in used_words]

            if available_words:
                chosen_word = random.choice(available_words)
                used_words.add(chosen_word)
                print(f"컴퓨터가 선택한 단어: {chosen_word}")
                return chosen_word
            else:
                print("컴퓨터가 적합한 단어를 찾지 못했습니다. 컴퓨터 패배.")
                return None
        else:
            print("컴퓨터가 적합한 단어를 찾지 못했습니다. 컴퓨터 패배.")
            return None
    except (requests.exceptions.RequestException, ValueError):
        print("단어 검색 중 오류가 발생했습니다. 컴퓨터 패배.")
        return None

def check_word_existence(word):
    base_link = "https://kkutudic.pythonanywhere.com/"

    payload = {
        'start': word,
        'end': '',
        'wordlen': len(word),
        'file': '',
        'sort_order': 'desc',
        'apply_dueum': 'true',
        'sort_by_next_words': 'false'
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Accept': "*/*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Accept-Language': "ko-KR,ko;q=0.9,en-US;q=0.8,en-US;q=0.7",
        'Connection': "keep-alive",
        'Host': "kkutudic.pythonanywhere.com",
        'Origin': "https://kkutudic.pythonanywhere.com",
        'Referer': "https://kkutudic.pythonanywhere.com/",
        'Sec-Ch-Ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'Sec-Ch-Ua-Mobile': "?0",
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'X-Requested-With': "XMLHttpRequest"
    }

    try:
        response = requests.post(base_link, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return isinstance(data, dict) and 'missionword' in data and len(data['missionword']) > 0
    except (requests.exceptions.RequestException, ValueError):
        print("단어 존재 여부 확인 중 오류가 발생했습니다. 다시 시도하세요.")
        return False

def main():
    os.system('title KKutu.KR AI')
    os.system('cls')

    used_words = set()
    last_computer_word = None

    while True:
        word = input("단어를 입력하세요: ").strip()

        if last_computer_word:
            last_char = get_last_char(last_computer_word)

            if not check_dueum_and_match(last_char, word):
                print(f"'{last_char}'로 시작하는 단어가 아닙니다. 게임 종료.")
                break

        if word in used_words:
            print("이미 사용된 단어입니다. 다른 단어를 입력하세요.")
            continue

        if not check_word_existence(word):
            print("해당 단어는 존재하지 않습니다. 다시 시도하세요.")
            continue

        used_words.add(word)

        end_char = get_last_char(word)
        next_word = send_request(end_char, used_words)
        
        if not next_word:
            print("컴퓨터가 단어를 찾지 못했습니다. 당신의 승리입니다!")
            break
        
        used_words.add(next_word)
        last_computer_word = next_word

if __name__ == "__main__":
    main()
