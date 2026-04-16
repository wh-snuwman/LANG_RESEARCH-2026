
from colorString import colorString


'''
# 코드를 토큰으로 쪼개는법
# 알아야할 규칙:
# 변수할당: 변수는 = 로 구분할수 있다. 등호를 기준으로 좌항,우항으로 나누고
#           우항을 토큰화 한다. 좌항은 리스트나 객체내부 데이터 참조가 아니라면, 그냥 이름 자체로 저자아하면된다.

알아야할점 : 토큰화는 재귀적으로 실행된다. 따라서 예약어를 감지하면 그냥 토큰화 시킨다음 바로 다음 함수로 넘기면 된다!


# < 데이터저장 >
# 괄호와 예약어를 기준으로 공백없는 코드라인을 분해
# 등호를 기준으로 우항의 토큰을 저장
# 우항토큰을 괄호와 사칙연산을 풀어서 최종적으로 값하나를 우항으로 지정(return)
# 좌항의 지정에 따라 데이터를 저장 

# < 함수실행 >
# 사실 함수도 비슷하다. 전체 코드를 저장해서호출할떄마다 바꾸면 된다.
# 함수정의를 하면 함수이름과 내부 코드를 같이 저장한다
# 정의후, 함수가 호출되면 input값을 함수에 전달후, 코드를 해석한다.(재귀함수 쓰면 좋을듯?)
# 이떄 : 파라미터에 들어오는 값을 최종적으로 하나의 값만 있는 상태여야 한다. (2개이상의 토큰이면 안됨)

'''
'''
1. 입력값 받기
2. 입력된 문자열을 하나씩 돌면서 예약어 감지
    이때. 예약어는 현재 저장된 딕셔너리나 배열에서 뺴온다.
    <예약어 감지방법>
    - 한글자인 예약어는 if 하나로 감지가 가능하다
    -두글자 이상인예약어도 똑같다. if문으로 글자를 감지후, 만약에 글자가
        특정 예약어의 첫번째 글자와 같다면 if문으로 다음글자를 추가로 감지한다.
        (이때 사용자가 설정할수 있는 예약어의 길이를 설정해두어 for문을 너무 많이 순회하는것을 방지한다. ex) 16글자 )
        예약어가 아니면 오류로 반환한다
        예약어이면 문자열을 자른후 다음단계로 넘긴다

3. 위 단계로 거치면 최종적으로 (토큰 - 나머지글자) 꼴로 토큰이 생성된다
4. 만들어진 토큰은 저장후 나머지문자열을 재귀함수를 통해 넘긴다.
=========================== 재귀 =============================

1. 파라미터로 입력받은값의 길이나 토큰검사를 한다.
    - 토큰이 있으면 위의 과정을 다시 진행한다
    - 토큰이 없거나 (토큰 + 토큰) 꼴로 나누어질수 있다면 이 값을 리스트로 리턴한다
        리턴하면 그 위에 있던 함수들도 모두 리턴되고 최종적으로 리스트 하나가 리턴된다


==> 최종적으로 토큰이 저장된 리스트 하나가 나온다!
ex) (타입은 리스트)  
    name = 10               =>      ['name','=','10']
    name = (10+20)          =>      ['name','=','(','10','+','20',')']

'''
REVERSED_WORD = {
    "bracket_s" : "(",
    "bracket_e" : ")",
    "equal" : "=",
    "for" : "for",
    "null" : "null",
    "true" : "true",
    "false" : "false",
}

# age = (30+20)
CODE = """

true null false null
"""


# 최적화를 위해 상요하는 예약어의 첫번쨰 글자 모음
REVERSED_WORD_SPLIT = {}
REVERSED_WORD_F  = [i[0] for i in list(REVERSED_WORD.values())]

for k,v in REVERSED_WORD.items():
    REVERSED_WORD_SPLIT[v] = []
    for c in v:
        REVERSED_WORD_SPLIT[v].append(c)

CODE = CODE.strip() # 모든코드 모음
LINES = CODE.split('\n') # 코드를 라인단위로 나누어서 저장한 데이터


def isIn(s = str,c = str)-> (0 | 1):
    for i in s:
        if i == c:
            return 1
    return 0



def SPACE_REMOVE(str_ = str) -> str: # 문자열내의 모든 공백제거
    lineNospace = ''
    for i in str_:
        if (i != ' '):
            lineNospace += i
    return lineNospace

# 문자열을 토큰화 시켜쥼(토큰은 예약어,변수명,괄호등으로 나누어진 코드의 기본단위)
def TOKENIZATION(LINE_ = str) -> list:
    command_type = 'none'
    if isIn(REVERSED_WORD['equal'],'='): # 등호가 포함되어 있는지 확인(커맨드 타입 구별)
        command_type = 'allocation'
    else:
        command_type = 'function'
    LINE = SPACE_REMOVE(LINE_) # 모든공백제거
    is_wordSense = False # 현재 예약어를 감지중인지
    words_sense = [] # 예약어의 n번째 글자가 같을수 있으니 여러개의 예약어를 동시에 감지
    wordSense_count = {} # 감지중일때 반복문을 실행하며 n번째글자가 예약어의 n번째 자리와 동일한지 확인할떄 쓰는 카운터
    count = 0
    token = []
    for char in LINE:
        if char in list(REVERSED_WORD.values()): # 한글자 예약어는 바로 감지 가능!
            # print(f'한글자 예약어 감지됨:{char}') 
            continue
            # 바로 토큰화 시키고 다음으로

        elif char in  REVERSED_WORD_F: # 예약어의 첫글자가 감지됨 == 뒤의 글자에 따라 예약어 일수도 아닐수도 있음
            for k,v in REVERSED_WORD_SPLIT.items():
                is_wordSense  = True # 예약어 감지를 시작함
                if v[0] == char:
                    words_sense.append(k) # 현재 감지중인 예약어의 타입형 이름( = (x) equal (o))
                    wordSense_count[k] = 0

        if is_wordSense:
            delType_ = []
            for wordType in words_sense:
                # 조건1 : 감지하고 있는 단어의 길이가 감지 범위보다 작으면 안됨.
                # 조건2 : 현재 감지중인 n번째 글자가 예약어의 n번째 글자와 같아야함.
                if (len(REVERSED_WORD_SPLIT[wordType]) > wordSense_count[wordType]) and (REVERSED_WORD_SPLIT[wordType][wordSense_count[wordType]] == char):
                    # 예약어가 최종적으로 맞는지 감지
                    # 아직 감지가 최종적으로 끝나지 않았으면 계속해서 진행
                    if len(REVERSED_WORD_SPLIT[wordType]) == wordSense_count[wordType]+1: # 감지했던 모든 문자가 예약어의 글자와 동일함 -> 토큰화
                        token.append(LINE[0:count+1])
                        other = LINE[count+1:]
                        print(colorString(other,(255,255,0)))
                        
                        if not len(other) <= 1:
                            result = TOKENIZATION(other) # 재귀함수를 사용하여 결과 도출.(타입은 리스트)
                            for i in result: # 그냥 바로 append하면 리스트 중첩상태로 저장됨. 따라서 풀어서 저장해줘야함
                                token.append(i)
                        return token
                    

                    wordSense_count[wordType] += 1
                else:
                    # print(colorString(wordType,(0,0,255)))
                    delType_.append(wordType) # 반복문 실행중에 항목제거 시, 순서제어에 오류발생(심지어 에러도 안뜸..!) -> 반복문 분리해서 지우기 
            for i in delType_: 
                words_sense.remove(i)

        count += 1 # 감지하는 자리수(공통) 하나씩 올리기



for LINE in LINES:
    line_nospace = SPACE_REMOVE(LINE)
    token = TOKENIZATION(line_nospace)


    print(token)