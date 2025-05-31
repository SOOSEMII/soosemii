# major list
liberalArt = ("국어국문학과", "국제학부", "역사학과", "교육학과", "글로벌인재학부")
socialScience = ("행정학과", "미디어커뮤니케이션학과", "법학과")
business = ("경제학과", "경영학부")
hospitality = ("호텔관광외식경역학부", "호텔외식관광프랜차이즈경영학과", "호텔외식비즈니스학과", "글로벌조리학과")
naturalScience = ("수학통계학과", "물리천문학과", "화학과")
lifeScience = ("생명시스템학부", "스마트생명산업융합학과")
convergence = ("전자정보통신공학과", "반도체시스템공학과", "컴퓨터공학과", "소프트웨어학과", "정보보호학과", "AI로봇학과", "인공지능데이터사이언스학과", "창의소프트학부", "지능정보융합학과")
engineering = ("건축공학과", "건축학과", "건설환경공학과", "환경에너지공간융합학과", "지구자원시스템공학과", "기계공학과", "나노신소재공학과", "양자원자력공학과", "국방시스템공학과", "우주항공드론학부")
arts = ("회화과", "패션디자인학과", "음악과", "체육학과", "무용과", "영화예술학과")

def major_selection(dept):
        match dept:
            case "인문과학대":
                return liberalArt
            case "사회과학대":
                return socialScience
            case "경영경제대":
                return business
            case "호텔관광대":
                return hospitality
            case "자연과학대":
                return naturalScience
            case "생명과학대":
                return lifeScience
            case "인공지능융합대":
                return convergence
            case "공과대":
                return engineering
            case "예체능대":
                return arts