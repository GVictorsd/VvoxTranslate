import requests
import urllib
import os, sys
import json

def voicetypes(url, outfilename):
    base_url = url
    r = requests.get(f'{base_url}/speakers')
    print('getting speaker list...')
    with open(outfilename, 'w', encoding='utf-8') as outfile:
        json.dump(r.json(), outfile, indent=4, ensure_ascii=False )

def speak(sentence, base_url, speaker_id=1, speech_filename = 'out.wav'):
    # base_url = 'https://9682-34-142-209-28.ap.ngrok.io'

    params_encoded = urllib.parse.urlencode({'text': sentence, 'speaker': speaker_id})
    r = requests.post(f'{base_url}/audio_query?{params_encoded}')
    voicevox_query = r.json()
    voicevox_query['volumeScale'] = 4.0
    # voicevox_query['intonationScale'] = 1.5
    # voicevox_query['prePhonemeLength'] = 1.0
    # voicevox_query['postPhonemeLength'] = 1.0

    params_encoded = urllib.parse.urlencode({'speaker': speaker_id})
    r = requests.post(f'{base_url}/synthesis?{params_encoded}', json=voicevox_query)

    with open(speech_filename, 'wb') as outfile:
        outfile.write(r.content)

    print('playing...\n')
    os.system(f'play {speech_filename} > /dev/null 2>&1')

def translate(text, source_lang = 'auto', target_lang = 'ja'):
    base_url = 'https://translate.googleapis.com/translate_a/single'
    params_encoded = urllib.parse.urlencode({
        'client': 'gtx',
        'sl': source_lang,
        'tl': target_lang, 
        'dt':'t', 
        'q': text
    })
    r = requests.post(f'{base_url}?{params_encoded}')
    r = r.json()
    return r[0][0][0]

def getspeaker(index):
    index = index-1
    with open('speakers.json', 'r', encoding='utf-8') as infile:
        json_obj = json.load(infile)
        print(json_obj[index]['name'])
        for i in json_obj[index]['styles']:
            print(f"{i['name']}: {i['id']}")


def main():

    if(len(sys.argv) != 2):
        print('Usage: python3 getaudio.py "text"')
        exit()

    base_url = sys.argv[1]
    print(base_url)
    speaker_id = 1
    speakerjson_filename = 'speakers.json'

    if(not os.path.exists(speakerjson_filename)):
        voicetypes(base_url, speakerjson_filename)

    while(1):
        input_text = input('text: ')

        if(input_text == '.exit'):
            exit()

        elif(input_text == '.list'):
            getspeaker(int(input('enter speaker index: ')))
            num = int(input('Change speaker id: '))
            if(num != 0):
                speaker_id = num
                print(f'speaker id set to {speaker_id}')

        elif(input_text == '.setid'):
            speaker_id = int(input('enter speaker id: '))
            print(f'speaker id set to {speaker_id}')

        elif (input_text == '.help'):
            print('list: list speakers')
            print('setid: set speaker id')
            print('exit: exit')

        else:
            transText = translate(input_text, target_lang='ja')
            print(transText)
            speak(transText, base_url, speaker_id)

        print()

    # speak('こんにちは、音声合成の世界へようこそ')
    # base_url = 'https://3ff0-34-87-184-184.ap.ngrok.io'
    # while(1):
    #     text = input('text: ')
    #     transText = translate(text, target_lang='ja')
    #     print(transText)
    #     speak(transText, base_url, speaker_id)

    # voicetypes()

    # getspeaker(int(input()))


    # text = 'こんにちは'
    # for i in range(51,61):
    #     speak(text, base_url, speaker_id=f'{i}', speech_filename=f'out{i}.wav')


if __name__ == '__main__':
    main()