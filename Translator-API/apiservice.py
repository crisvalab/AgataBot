import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from translator import Translator

app = Starlette(debug=False)

translator = Translator()

response_header = { 'Access-Control-Allow-Origin': '*' }

@app.route('/', methods=['GET', 'POST', 'HEAD'])
async def home_route(request):
    return JSONResponse(content={
        'message': 'Welcome to Translator EN-ES/ES-EN API.',
        'info': 'This API only will run from 0.0.0.0 and is for local use only.',
        'developer': 'Cristian Valero Abundio'
    }, headers=response_header)

@app.route('/translator/es/', methods=['POST'])
async def translate_to_es(request):
    if request.method == 'POST':
        try:
            request_data = await request.json() #{'sentence': 'Hy! My name is Cristian.'}
            sentence = str(request_data['sentence'])
            translation = translator.translate_to_spanish(sentence)
            return JSONResponse(content={
                'sentence': sentence,
                'translation': str(translation)
            }, headers=response_header)
        except:
            return JSONResponse(content={'error:': 'Request not valid.'}, headers=response_header)

@app.route('/translator/en/', methods=['POST'])
async def translate_to_en(request):
    if request.method == 'POST':
        try:
            request_data = await request.json() #{'sentence': 'Hola, me llamo Paco.'}
            sentence = str(request_data['sentence'])
            translation = translator.translate_to_english(sentence)
            return JSONResponse(content={
                'sentence': sentence,
                'translation': translation
            }, headers=response_header)
        except:
            return JSONResponse(content={'error:': 'Request not valid.'}, headers=response_header)

@app.exception_handler(404)
def route_not_found(request, exc):
    return JSONResponse(content={
        'code': 404,
        'message': 'The route you requested not found. Please, try again or contact with an administrator.'
    }, status_code=exc.status_code)

if __name__ == '__main__':
    uvicorn.run(app, port=3002, host='0.0.0.0')