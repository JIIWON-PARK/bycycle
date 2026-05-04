CREATE TABLE 대여소 (
대여소번호 TEXT not null, --'0없음'
보관소명 TEXT,
자치구 text,
상세주소 TEXT,
위도 REAL,
경도 REAL,
설치시기 TEXT,
LCD INTEGER,
QR INTEGER,
운영방식 TEXT,
PRIMARY KEY(대여소번호)
);

CREATE TABLE 이용정보 (
id INTEGER PRIMARY KEY,
대여일자 TEXT NOT NULL,
대여소번호 text  NOT NULL,
대여소명 TEXT,
대여구분코드 TEXT,
성별 TEXT,
연령대 TEXT,
이용건수 INTEGER,
운동량 REAL,
탄소량 REAL,
이동거리 REAL,
이용시간 INTEGER,
FOREIGN KEY(대여소번호) REFERENCES 대여소(대여소번호)
);

CREATE TABLE 기온 (
년월 TEXT NOT NULL,
지점 TEXT NOT NULL,
평균기온 REAL,
평균최저기온 REAL,
평균최고기온 REAL,
PRIMARY KEY (년월, 지점)
);

CREATE TABLE 강수량(
년월 TEXT NOT NULL,
지점 TEXT NOT NULL,
강수량 REAL,
PRIMARY KEY(년월, 지점)
);

DROP TABLE IF EXISTS 이용정보;
DROP TABLE IF EXISTS 대여소;
DROP TABLE IF EXISTS 기온;
DROP TABLE IF EXISTS 강수량;

CREATE TABLE 대여소 (
대여소번호 TEXT not null, --'0없음'
보관소명 TEXT,
자치구 text,
상세주소 TEXT,
위도 REAL,
경도 REAL,
설치시기 TEXT,
LCD INTEGER,
QR INTEGER,
운영방식 TEXT,
PRIMARY KEY(대여소번호)
);
CREATE TABLE 이용정보 (
id INTEGER PRIMARY KEY,
대여일자 TEXT NOT NULL,
대여소번호 text  NOT NULL,
대여소명 TEXT,
대여구분코드 TEXT,
성별 TEXT,
연령대 TEXT,
이용건수 INTEGER,
운동량 REAL,
탄소량 REAL,
이동거리 REAL,
이용시간 INTEGER,
FOREIGN KEY(대여소번호) REFERENCES 대여소(대여소번호)
);
CREATE TABLE 기온 (
년월 TEXT NOT NULL,
지점 TEXT NOT NULL,
평균기온 REAL,
평균최저기온 REAL,
평균최고기온 REAL,
PRIMARY KEY (년월, 지점)
);
CREATE TABLE 강수량(
년월 TEXT NOT NULL,
지점 TEXT NOT NULL,
강수량 REAL,
PRIMARY KEY(년월, 지점)
);

DROP TABLE IF EXISTS ta;
DROP TABLE IF EXISTS rn;
DROP TABLE IF EXISTS 이용정보;

SELECT 
    A.대여소번호, 
    A.보관소명, 
    A.위도, 
    A.경도,
    SUM(B.이용건수) AS 총이용건수
FROM 대여소 A
JOIN 이용정보 B ON A.대여소번호 = B.대여소번호
WHERE B.대여일자 BETWEEN '202507' AND '202512'
GROUP BY 
    A.대여소번호, 
    A.보관소명, 
    A.위도, 
    A.경도;