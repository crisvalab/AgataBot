import requests
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette(debug=False)

response_header = {
    'Access-Control-Allow-Origin': '*'
}

API_TRANSLATE_TO_ES = 'http://0.0.0.0:3002/translator/es/'
API_TRANSLATE_TO_EN = 'http://0.0.0.0:3002/translator/en/'
API_OBTAIN_ANSWER = 'http://0.0.0.0:3001/agata/answer/'

def throw_request_error(req):
    return JSONResponse(content={
        'message': 'The intern request not be valid.',
        'reason': str(req.reason)
    }, headers=response_header)

@app.route('/', methods=['GET', 'POST'])
def home_route(request):
    return JSONResponse(content={
        'message': 'Welcome to the Bridge API.',
        'info': 'This API intercommunicates all the rest of the microservices in the network to balance and distribute all the incoming requests.',
        'developer': 'Cristian Valero Abundio'
    }, headers=response_header)

@app.route('/agata/conversate/en/', methods=['POST'])
async def generate_english_answer(request):
    if request.method == 'POST':
        request_data = await request.json() #{'id': 3, 'question': ''}
        id, question = str(request_data['id']), str(request_data['question']) 
        req = requests.post(url=API_OBTAIN_ANSWER, json={'id': id, 'question': question})
        if req.status_code == 200:
            answer = req.json()['answer']
            return JSONResponse(content={
                'question': str(question),
                'answer': str(answer)
            }, headers=response_header)
        else:
            throw_request_error(req=req)

@app.route('/agata/conversate/es/', methods=['POST'])
async def generate_spanish_answer(request):
    if request.method == 'POST':
        request_data = await request.json() #{'id': 3, 'question': ''}
        id, question = str(request_data['id']), str(request_data['question'])
        req = requests.post(url=API_TRANSLATE_TO_EN, json={'sentence': question})
        if req.status_code == 200:
            sentence_to_en = req.json()
            sentence_to_en = sentence_to_en['translation'] #This is the translated sentence.
            req = requests.post(url=API_OBTAIN_ANSWER, json={'id': id, 'question': sentence_to_en})
            if req.status_code == 200:
                answer = req.json()
                answer = answer['answer'] #This is the retrived answer.
                req = requests.post(url=API_TRANSLATE_TO_ES, json={'sentence': answer})
                if req.status_code == 200:
                    sentence_to_es = req.json()
                    sentence_to_es = sentence_to_es['translation']
                    return JSONResponse(content={
                        'question': str(question),
                        'question_to_en': str(sentence_to_en),
                        'answer': str(answer),
                        'answer_to_es': str(sentence_to_es)
                    }, headers=response_header)
                else:
                    throw_request_error(req=req)
            else:
                throw_request_error(req=req)
        else:
            throw_request_error(req=req)

@app.exception_handler(404)
def route_not_found(request, exc):
    return JSONResponse(content={
        'code': 404,
        'message': 'The route you requested not found. Please, try again or contact with an administrator.'
    }, status_code=exc.status_code)

if __name__ == '__main__':
    uvicorn.run(app, port=3000, host='0.0.0.0')