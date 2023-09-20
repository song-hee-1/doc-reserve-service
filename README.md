
## Doctor Reserve Service

진료 예약을 위한 의사 검색 및 진료요청을 할 수 있는  REST API 

</br>

## 목차

- [Doctor Reserve Service](#doctor-reserve-service)
- [사용 기술](#사용-기술)
- [설계사항](#설계사항)
  - [데이터베이스 모델링](#데이터베이스-모델링)
      - [전체(시스템 포함)](#전체시스템-포함)
      - [앱(시스템 제외)](#앱시스템-제외)
  - [구조 및 아키텍쳐](#구조-및-아키텍쳐)
  - [API 엔드포인트](#api-엔드포인트)
  - [Pytest를 이용한 테스트 코드](#pytest를-이용한-테스트-코드)
- [프로젝트 실행 방법](#프로젝트-실행-방법)
- [데이터 추가](#데이터-추가)


</br>

## 사용 기술

-   **Back-End**  : Python, Django, Django REST Framework, Crontab
-   **Database**  : SQLite
-   **ETC**  : Git, Github,

</br>

## 설계사항

### 데이터베이스 모델링
##### 전체(시스템 포함) 

![erd](https://github.com/song-hee-1/doc-reserve-service/assets/83492367/d01b162b-6d9e-422d-8c39-24f8b73df067)



##### 앱(시스템 제외)
![my_project_model](https://github.com/song-hee-1/doc-reserve-service/assets/83492367/74ed99fb-f392-41a2-a666-feea506e791c)


- 데이터의 추적성 및 관리를 위하여 `created_at`, `updated_at` 을 가지고 있는 `core` 앱에 TimeStampModel을 모듈화
- 무결성을 위해 모델의 필드는 str 형식의 chocie로 처리
- 요구사항을 토대로 `User` , `Speciality`, `Doctor`  , `DoctorSchedule`, `Clinic` , `NonInsuredMedicalCategory`, `ClinicAppointment` 모델 설계

- 각 모델의 관계

	- **`Doctor` 모델과 `Speciality` 모델 간의 다대다 (Many-to-Many) 관계:**

		- 의사(`Doctor`)는 여러 진료 과목(`Speciality`)에 속할 수 있고, 진료 과목 역시 여러 의사와 연관될 수 있습니다.
		- 이 관계는 `specialities` 필드를 통해 정의되어 있습니다.

	- **`Doctor` 모델과 `Clinic` 모델 간의 일대다 (Many-to-One) 관계:**

		- 여러 의사(`Doctor`)는 하나의 병원(`Clinic`)에 근무할 수 있으며, 하나의 병원은 여러 의사를 포함할 수 있습니다.
		- 이 관계는 `clinic` 필드를 통해 정의되어 있습니다.

	- **`Doctor` 모델과 `DoctorSchedule` 모델 간의 일대다 (One-to-Many) 관계:**

		- 각 의사(`Doctor`)는 여러 개의 진료 스케줄(`DoctorSchedule`)을 가질 수 있습니다.
		- 이	 관계는 `schedules` 필드를 통해 정의되어 있으며, `doctor` 필드를 통해 의사와 진료 스케줄이 연결됩니다.

	- **`Clinic` 모델과 `Doctor` 모델 간의 역참조 (Reverse Relationship):**

	- `	Doctor` 모델에서 `clinic` 필드를 통해 병원에 접근할 수 있고, `Clinic` 모델에서는 `doctors` 역참조를 통해 해당 병원에 속한 의사들에 접근할 수 있습니다.

	- **`Doctor` 모델과 `ClinicAppointment` 모델 간의 일대다 (One-to-Many) 관계:**

		- 각 의사(`Doctor`)는 여러 개의 진료 요청(`ClinicAppointment`)을 받을 수 있습니다.
		- 이 관계는 `clinic_appointments` 역참조를 통해 의사와 진료 요청이 연결됩니다.

	- **`accounts.User` 모델과 `ClinicAppointment` 모델 간의 일대다 (One-to-Many) 관계:**

		- 각 환자(`User`)는 여러 개의 진료 요청(`ClinicAppointment`)을 생성할 수 있습니다.
		- 이 관계는 `clinic_appointments` 역참조를 통해 환자와 진료 요청이 연결됩니다.

</br>

### 구조 및 아키텍쳐
 *앱 이름 :복수, 폴더명 : 복수, 파일명 : 단수*


- ResponseFormatter를 추가하여 api response의 구조 통일
- custom exception handler를 이용하여 error response에 http status code 추가
-  core.utils.exception에 APIException 유틸화하여 관리

</br>

**service_layer**
- 유지보수 및 비즈니스 로직 관리를 위하여 view에 service_layer 추가
- 모든 service_layer는 base_service를 상속받아 관리
- service를 기준으로 serializer, views 분리

</br>

**Serializer**
- **효율성 및 확장성의 용이성**을 위하여 basic_serializer를 통하여 외래키를 제외한 필드 관리
	- 해당 모델을 사용하는 serializer는 basic_serializer를 상속받아 필드 관리 (`Meta.fields 이용`)
	- 모델에 새로운 필드가 추가될 경우 basic_serializer에 필드 추가하면 해당 모델의 다른 serializer에도 **자동 적용**

- *명명규칙* :
	- *Input* : *{service_name}{base_name}Qs{model_name}Serializer*
	- *Output* : *{service_name}{base_name]{http_method_name}Serializer


</br>


### API 엔드포인트


| 엔드포인트                              | 설명                                          | HTTP 메서드 |
| --------------------------------------- | -------------------------------------------- | ----------- |
| `/api/accounts/user/`                   | 사용자 정보를 조회합니다.                     | GET         |
| `/api/accounts/user/login/`             | 사용자 인증 정보를 전송하여 로그인을 시도합니다. | POST        |
| `/api/accounts/user/logout/`            | 로그아웃을 수행합니다.                        | POST        |
| `/api/accounts/user/signup/`            | 새로운 사용자를 등록합니다.                   | POST        |
| `/api/clinics/appointment/`             | 진료 요청 목록을 조회합니다.                 | GET         |
| `/api/clinics/approve_appointment/`     | 진료 요청을 수락합니다.                     | POST        |
| `/api/clinics/request_appointment/`     | 진료 요청을 생성합니다.                     | POST        |
| `/api/clinics/search/`                  | 진료 정보를 검색합니다.                     | GET         |
| `/api/schema/`                         | API 스키마를 조회합니다.                     | GET         |
| `/api/schema/swagger-ui/`               | Swagger UI를 통해 API 문서를 확인합니다.     | GET         |


- drf-spectacular를 이용한 문서화
- local에서 `api/schema/swagger-ui` 로 접속하면 API별 schema 및 Test 가능
</br>


### Pytest를 이용한 테스트 코드 
| Name                                       | Stmts | Miss | Cover |
|--------------------------------------------|---------|----------|-------|
| tests/conftest.py                          | 97      | 11       | 89%   |
| tests/test_accounts/test_user_view.py      | 21      | 0        | 100%  |
| tests/test_clinics/test_clinic_view.py     | 143     | 0        | 100%  |
| **TOTAL**                                  | **652** | **36**   | **94%**|

- 요구사항에 대한 test case 작성
	- `freezegun` 라이브러리를 이용하여 특정 시점(`2022년 1월 15일`)의 상황에서 테스트
- conftes.py에 자주 사용되는 함수들 fixture를 통해 유틸화
- 94%의 test-coverage

</br>

</br>



## 프로젝트 실행 방법
sqlite(DB)도 같이 올려뒀습니다.
하단의 정보를 토대로 로그인하시면 됩니다.

admin ID / PW : admin@offical.net ,  0000

1. 가상환경 설정
	`python3 -m venv {가상환경이름} `
2. 의존성 설치
	`pip install -r requirements/local.txt`
3. 서버 실행
	`python manage.py runserver` 

**`api/schema/swagger-ui` 에 접속하시면 UI와 함께 API별로 테스트할 수 있습니다.**

</br>

## 데이터 추가
- `create_data_scripty.py`를 이용하여 데이터를 추가하는 것이 가능합니다
- `python manage.py shell < create_data_script.py` 을 입력해주시면 데이터가 생성됩니다.
