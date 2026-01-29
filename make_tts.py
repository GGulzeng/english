import os
import re
from gtts import gTTS

# 1. 파일 읽기
try:
    with open('quizzes.js', 'r', encoding='utf-8') as f:
        content = f.read()
except:
    print("파일을 읽을 수 없습니다. quizzes.js 파일이 같은 폴더에 있는지 확인하세요.")
    exit()

# 2. 정규식을 사용하여 데이터 강제 추출
# (JSON 변환 대신 텍스트에서 직접 단어와 레벨을 뽑아냅니다)
base_dir = "sounds"

# 레벨별 섹션 나누기
sections = re.split(r'"(elementary|middle|high)"\s*:\s*\[', content)

current_level = None
for i in range(1, len(sections), 2):
    level_name = sections[i]  # elementary, middle, high
    data_block = sections[i+1] # 해당 레벨의 데이터 덩어리
    
    # 해당 레벨 폴더 생성
    level_dir = os.path.join(base_dir, level_name)
    if not os.path.exists(level_dir):
        os.makedirs(level_dir)
    
    # 덩어리 안에서 단어('word') 추출
    # 패턴: "question": "단어의 뜻은? '단어'"
    words = re.findall(r"단어의 뜻은\?\s*'(.*?)'", data_block)
    words = list(dict.fromkeys(words)) # 중복 제거
    
    print(f"--- {level_name} 단계 시작 (발견된 단어: {len(words)}개) ---")
    
    for word in words:
        word = word.strip()
        if not word: continue
        
        # 파일명 금지 문자 제거
        safe_name = re.sub(r'[\\/:*?"<>|]', '_', word).replace(" ", "_")
        file_path = os.path.join(level_dir, f"{safe_name}.mp3")
        
        if not os.path.exists(file_path):
            try:
                tts = gTTS(text=word, lang='en')
                tts.save(file_path)
                print(f"저장 성공: {word}")
            except Exception as e:
                print(f"저장 실패: {word} ({e})")
        else:
            # 이미 있으면 패스
            pass

print("\n 모든 TTS 생성이 완료되었습니다! 'sounds' 폴더를 확인하세요.")