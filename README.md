# DRF 1일차 숙제


## 1. args, kwargs를 사용하는 예제 코드 짜보기
원래 함수를 정의하고 난 후 함수의 파라미터의 개수는 변하지 않는다.   
예를 들어,   

def print_numbers(a,b,c):   
    print(a)   
    print(b)   
    print(c)   


와 같이 정의했을 때, 3개의 파라미터 a, b, c에 3개의 인자값이 들어가야 한다.   
그렇지 않으면 인자의 개수가 많거나 적다는 오류가 발생한다.   
하지만,      

def print_numbers(*args):   
    for arg in args:   
        print(arg)   


>>> print_numbers(1,2,3,4,5)   
1   
2   
3   
4   
5   


와 같이 파라미터에 *(애스터리스크)를 붙여주면 몇 개의 이자를 넣든 상관이 없다.   
이때 args라고 작성한 이유가 궁금할 수 있다.   
하지만 관례적으로 arguments의 줄임말인 args를 사용하는 것일 뿐, 만약 a나 b, x 등 다른 것을 넣어도 크게 상관이 없다!    


*args  --> 튜플 형태로    
여기서 조금 더 *을 이해하기 위해 arhs 자체는 어떻게 출력되는지 한 번 확인해보려고 한다.    
def print_numbers(*args):    
    return args       


a = print_numbers(1,2,3,4)     
a       
(1,2,3,4)     # 결과 -> 튜플 형태로!!       


*args에 여러 개의 인자를 집어넣고 args 자체는 함수에서 어떻게 처리하는지 확인해보면, (1,2,3,4)와 같이 튜플 형태로 출력이 된다.    
즉 *가 여러 개의 인자를 받을 수 있도록 튜플형태로 문을 열어주는(?) 느낌, 튜플로 받아들이는 통로같은... 느낌이라고 생각하자.....     

리스트, 튜플, 문자열과 같이 시퀀스 자료형은 for 문을 통해 각 요소들을 차례대로 출력할 수 있다.    

즉, 여러 개의 인자를 받아 *로 한 덩어리의 튜플로 만들어 준다고 생각하면 된다.     


**kwargs(키워드 인수)    
우리는 함수를 사용할 때 보통 인수의 위치를 기억해야 합니다. 그렇지 않으면 잘못된 값이 들어갈 수 있기 때문입니다.      
위치 인수 활용 예)     
def my_info(name, age, address):      
    print("성명:", name)     
    print("나이:", age)     
    print("주소:", address)     

### 원하는 값을 제대로 넣었을 때     
my_info("김희정", 11, "서울")      
성명: 김희정      
나이: 11      
주소: 서울      

###잘못된 값을 넣었을 때      
my_info(11, "김희정", "서울")       
성명: 11      
나이: 김희정       
주소: 서울        

만약 1000줄이 넘는 코드를 작성했다고 가정했을 때, 일일이 함수의 인수 위치를 기억하기 어려울 수 있습니다. 그래서 우리가 사용할 수 있는 방법이 바로 키워드 인수입니다!     
키워드 인수 활용 예)    
my_info(address="서울", age=11, name="김희정")        
성명: 김희정      
나이: 11      
주소: 서울       

위의 예시에서는 함수를 호출할 때 키워드 인수로 직접 값을 넣었습니다.     


이제는 딕셔너리를 사용해서 키워드 인수를 값으로 넣어보겠습니다.      
이제 본격적으로 **를 붙여서 함수에 넣어주면 됩니다.      

def my_info(name, age, address):     
    print("성명:", name)    
    print("나이:", age)     
    print("주소:", address)      

a = {'name': '김희정', 'age': 11, 'address': '서울'}       
my_info(**a)      

성명: 김희정     
나이: 11     
주소: 서울     

딕셔너리a를 my_info 함수의 인수에 넣었습니다.      
이때 **를 작성해주면 딕셔너리 a의 키 값 ('name', 'age', 'address')이 정의된 함수 my_info의 인수와 이름이 일치하는 것과 연결하여 출력됩니다.      



지금까지는 이미 인수가 정해진 함수를 만들고 난 후 딕셔너리를 인자로 넣었습니다.     
이번에는 함수를 만들 때부터 **를 파라미터로 넣어 사용해보겠습니다.      

def my_info(**kwargs):     
    for kw, arg in kwargs.items():     
        print(kw,":", arg, sep='')     

### 키워드 인수를 직접 넣는 경우     
my_info(name="김희정")     
name:김희정     

my_info(name="김희정", age=11)     
name:김희정      
age:11      

my_info(name="김희정", age=11, address="서울")      
name:김희정      
age:11      
address:서울      


### 딕셔너리 형태로 넣는 경우      
a = {'name': '김희정'}     
my_info(**a)     
name:김희정     

a = {'name': '김희정', 'age':11}      
my_info(**a)      
name:김희정      
age:11      

a = {'name': '김희정', 'age':11, 'address':'서울'}     
my_info(**a)     
name:김희정     
age:11      
address:서울      

함수를 처음 정의할 때 **kwargs를 매개변수로 넣으면, 위와 같이 개수와 상관없이 키와 값이 있는 형태일 때, 오류가 생기지 않고 제대로 출력이 됩니다.      
kwargs는 관례적으로 사용하는 단어일 뿐 다른 단어를 사용해도 문제없이 출력됩니다. 단, kwargs로 쓰는 것을 권장합니다.      
즉, **kwargs는 키와 값의 형태인 인수를 개수에 상관없이 받을 수 있는 것을 의미합니다.       

## 2. mutable과 immutable은 어떤 특성이 있고, 어떤 자료형이 어디에 해당하는지 서술하기     
Mutable : 변경가능한 자료형 / 리스트(list), 딕셔너리(dictionary), 세트(Set), Numpy의 배열(ndarray)      
>>> x = [1,2,3]     
>>> y = x     
>>> y += [4,]     
>>> x     
[1,2,3,4]     
>>> y     
[1,2,3,4]     

Immutable : 변경불가능한 자료형 / 숫자형(Int, Float), 참/거짓(Bool), 문자열(string), 튜플(tuple)      
>>> x = (1,2,3)      
>>> y = x     
>>> y += (4,)     
>>> x     
(1,2,3)     
>>> y     
(1,2,3,4)     

Python에서 immutable 자료형(숫자, 문자열, 튜플)은 직접 값이 변경되는 deep copy로 이해할 수 있다.      
반면에 mutable 자료형(즉, 쓰기가 가능한 컨테이너)는 shallow copy(내부적으로 포인터만 복사)를 적용된다.     

## 3. DB Field에서 사용되는 Key 종류와 특징 서술하기      
키(Key)는 데이터베이스에서 조건에 만족하는 튜플을 찾거나 순서대로 정렬할 때 다른 튜플들과 구별할 수 있는 유일한 기준이 되는 Attribute(속성). ( 튜플: 릴레이션을 구성하는 각각의 행, 속성의 모임)      
기본키(Primary Key) : 후보키 중에서 선택한 하나의 주 키(Main Key) / 한 릴레이션에서 특정 튜플을 유일하게 구별할 수 있는 속성 / 기본키로 정의된 속성에는 동일한 값이 중복되어 저장될 수 없음 / Null값을 절대 가질 수 없음       
Unique Key : 테이블 내 항상 유일해야 하는 값 / 해당 컬럼에 입력되는 데이터가 각각 유일하다는 것을 보장하기 위한 제약조건 / 중복을 허용하지 않음 / Null값을 가질 수 있음( Unique Key에 PK도 포함이 되어있음 )      
외래키(Foreign Key) : 관계를 맺고 있는 릴레이션 R1, R2. 릴레이션R1이 참조하고 있는 릴레이션R2의 기본키와 같은 R1릴레이션의 속성 / 외래키로 지정되면 참조 테이블의 기본키에 없는 값은 입력할 수 없음      

## 4. django에서 queryset과 object는 어떻게 다른지 서술하기       
쿼리셋(QuerySet): 데이터베이스에서 전달받은 모델의 객체 목록(object들의 집합) / 리스트와 구조가 같지만, 파이썬 기본 자료구조가 아니기 때문에 파이썬에서 읽고 쓰기 위해서는 자료형으로 변환을 해줘야 한다.      
 예) <QuerySet [<Post: my post title>, <Post: another post title>]>      
 
오브젝트(Object): 테이블에 입력된 특정 레코드      


# 2일차 과제

1. Django 프로젝트를 생성하고, user 라는 앱을 만들어서 settings.py 에 등록해보세요.

2. user/models.py에 `Custom user model`을 생성한 후 django에서 user table을 생성 한 모델로 사용할 수 있도록 설정해주세요

3. user/models.py에 사용자의 상세 정보를 저장할 수 있는 `UserProfile` 이라는 모델을 생성해주세요

4. blog라는 앱을 만든 후 settings.py에 등록해주세요

5. blog/models.py에 <카테고리 이름, 설명>이 들어갈 수 있는 `Category`라는 모델을 만들어보세요.

6. blog/models.py에 <글 작성자, 글 제목, 카테고리, 글 내용>이 들어갈 수 있는 `Article` 이라는 모델을 만들어보세요.(카테고리는 2개 이상 선택할 수 있어야 해요)

7. Article 모델에서 외래 키를 활용해서 작성자와 카테고리의 관계를 맺어주세요

8. admin.py에 만들었던 모델들을 추가해 사용자와 게시글을 자유롭게 생성, 수정 할 수 있도록 설정해주세요

9. CBV 기반으로 로그인 / 로구아웃 기능을 구현해주세요

10. CBV 기반으로 로그인 한 사용자의 게시글의 제목을 리턴해주는 기능을 구현해주세요

---

# 3일차 과제

1. blog 앱에 <게시글, 사용자, 내용>이 포함된 comment 테이블을 작성해주세요

2. 외래 키를 사용해서 Article, User 테이블과 관계를 맺어주세요

3. admin.py에 comment를 추가해 자유롭게 생성, 수정 할 수 있도록 해주세요

4. serializer를 활용해 로그인 한 사용자의 기본 정보와 상세 정보를 리턴해 주는 기능을 만들어주세요

5. 4번의 serializer에 추가로 로그인 한 사용자의 게시글, 댓글을 리턴해주는 기능을 구현해주세요

6.  blog 앱에 title / category / contents를 입력받아서 게시글을 작성하는 기능을 구현해주세요

- 만약 title이 5자 이하라면 게시글을 작성할 수 없다고 리턴해주세요

- 만약 contents가 20자 이하라면 게시글을 작성할 수 없다고 리턴해주세요

- 만약 카테고리가 지정되지 않았다면 카테고리를 지정해야 한다고 리턴해주세요

6. custom permission class를 활용해 가입 후 3일 이상 지난 사용자만 게시글을 쓸 수 있도록 해주세요

- 테스트 할 때에는 가입 후 3분 이상 지난 사용자가 게시글을 쓸 수 있게 해주세요

- join_date는 datetime field로 만들어주세요

---

# 4일차 과제

1. admin 페이지에 user admin을 등록하고, userprofile 테이블을 user admin 페이지에서 같이 보고 설정 할 수 있도록 해주세요

2. article 테이블에 <노출 시작 일자, 노출 종료 일자>를 추가해주세요

3. article view에 게시글 조회 기능을 만들되, 현재 일자를 기준으로 노출 시작 일자와 노출 종료 일자 사이에 있는 항목들만 리턴해주도록 필터를 설정해주세요

- 리턴 데이터는 게시글 작성일 기준으로 정렬하여 최근 쓴 글이 가장 먼저 올라오도록 해주세요

4. 기존 article 생성 기능을 유지하되, article은 admin user 혹은 가입 후 7일이 지난 사용자만 생성 가능하도록 해주세요

- 조회는 로그인 한 사용자에 대해서만 가능하도록 설정해주세요

# 5일차 과제

1. product라는 앱을 새로 생성해주세요

2. product 앱에서 <작성자, 제목, 썸네일, 설명, 등록일자, 노출 시작 일, 노출 종료일>가 포함된 product 테이블을 생성해주세요

3. django serializer에서 기본적으로 제공하는 validate / create / update 기능을 사용해 event 테이블의 생성/수정 기능을 구현해주세요

- postman으로 파일을 업로드 할 때는 raw 대신 form-data를 사용하고, Key type을 File로 설정해주세요

4. 등록된 이벤트 중 현재 시간이 노출 시작 일과 노출 종료 일의 사이에 있거나, 로그인 한 사용자가 작성한 product 쿼리셋을 직렬화 해서 리턴해주는 serializer를 만들어주세요

5. product field를 admin에서 관리할 수 있도록 등록해주세요

# 6일차 과제

1. product 앱의 product 테이블 구성을 <작성자, 썸네일, 상품 설명, 등록일자, 노출 종료 일자, 가격, 수정 일자, 활성화 여부>로 변경해주세요
2. django serializer를 사용해 validate / create / update 하는 기능을 구현해주세요
   1. custom validation 기능을 사용해 노출 종료 일자가 현재보다 더 이전 시점이라면 상품을 등록할 수 없도록 해주세요
   2. custom creator 기능을 사용해 상품 설명의 마지막에 "<등록 일자>에 등록된 상품입니다." 라는 문구를 추가해주세요
   3. custom update 기능을 사용해 상품이 update 됐을 때 상품 설명의 가장 첫줄에 "<수정 일자>에 수정되었습니다." 라는 문구를 추가해주세요
3. product 앱에서 <작성자, 상품, 내용, 평점, 작성일>을 담고 있는 review 테이블을 만들어주세요
4. review 테이블을 관리자 페이지에서 자유롭게 추가/수정 할 수 있도록 설정해주세요
5. 현재 날짜를 기준으로, 노출 종료 날짜가 지나지 않았고 활성화 여부가 True이거나 로그인 한 사용자가 등록 한 상품들의 정보를 serializer를 사용해 리턴해주세요
6. 5번 상품 정보를 리턴 할 때 상품에 달린 review와 평균 점수를 함께 리턴해주세요
   1. 평균 점수는 (리뷰 평점의 합/리뷰 갯수)로 구해주세요
   2. 작성 된 리뷰는 모두 return하는 것이 아닌, 가장 최근 리뷰 1개만 리턴해주세요
7. 로그인 하지 않은 사용자는 상품 조회만 가능하고, 회원가입 이후 3일 이상 지난 사용자만 상품을 등록 할 수 있도록 권한을 설정해주세요
