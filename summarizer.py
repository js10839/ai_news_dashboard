import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

def NewsSummarizer(original_news):
    client = OpenAI(api_key=API_KEY)

    try:
        response = client.chat.completions.create(
            model = 'gpt-5-mini',
            messages = [
                {
                'role': 'system',
                'content': '너는 뉴스 기사를 읽고 핵심 내용을 3줄로 요약해주는 유능한 어시스턴트야. 원문 언어로 요약해줘.'
                },
                {
                    'role': 'user',
                    'content': original_news
                }
            ]
        )

        summary = response.choices[0].message.content
        return summary
    
    except Exception as e:
        print(f'에러 발생: {e}')
        return None
    
# if __name__ == "__main__":

#     test_text = """
#     (테스트용 긴 글)
#     애플이 새로운 아이폰 16을 공개했다. 이번 모델은 AI 기능이 대폭 강화되었으며, 
#     카메라 성능 또한 비약적으로 상승했다. 전문가들은 이번 출시가 스마트폰 시장의 
#     새로운 전환점이 될 것이라고 분석하고 있다. 배터리 수명 또한 전작 대비 20% 증가했다.
#     """
    
#     print("AI에게 요약을 요청하는 중...")
#     result = summarize_news(test_text)
#     print("\n[요약 결과]")
#     print(result)

