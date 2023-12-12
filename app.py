import os
from flask import Flask, render_template, request
import openai
import pandas as pd

app = Flask(__name__)

# OpenAI API 키를 환경 변수에서 가져오기
openai.api_key = os.environ.get('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')

class OpenAITravelPlanner:
    def __init__(self):
        self.destinations = {
            'Seoul': {'activities': ['Palace Visit', 'Shopping', 'Korean BBQ']},
            'Busan': {'activities': ['Beach Visit', 'Seafood Tasting', 'Hiking']},
            'Jeju': {'activities': ['Waterfalls Tour', 'Hiking', 'Cave Exploration']}
        }

    def generate_itinerary(self, destination, duration, transportation):
        prompt = f"Plan a {duration}-day trip to {destination}. Suggest activities, transportation mode: {transportation}."
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.7,
            max_tokens=150
        )
        suggested_activities = response['choices'][0]['text'].strip()

        return {
            'destination': destination,
            'duration': duration,
            'transportation': transportation,
            'suggested_activities': suggested_activities
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_destination = request.form['destination']
        user_duration = int(request.form['duration'])
        user_transportation = request.form['transportation']

        planner = OpenAITravelPlanner()
        recommended_itinerary = planner.generate_itinerary(user_destination, user_duration, user_transportation)

        if recommended_itinerary:
            df = pd.DataFrame([recommended_itinerary])
            df.to_excel("Recommended_Itinerary_OpenAI.xlsx", index=False)
            return render_template('result.html', result=recommended_itinerary)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
