import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from openai import OpenAI

# .env 파일 가져오기
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

app = Flask(__name__)

def generate_quote():
    prompt = "사용자가 버튼을 3번 누르면, 오늘의 명언을 하나 생성해서 출력해줘"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "오늘의 명언을 생성해주는 역할을 합니다. 명언을 생성할 때마다 다른 명언을 생성합니다. 다른 잡담은 하지 말고 명언만 출력해줍니다."
            },
            {
                "role": "user",
                "content": prompt
            },
        ]
    )

    quote = response.choices[0].message.content.strip()
    return quote

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-quote', methods=['POST'])
def generate_quote_endpoint():
    quote = generate_quote()
    return jsonify({'quote': quote})

if __name__ == '__main__':
    app.run(debug=True)
