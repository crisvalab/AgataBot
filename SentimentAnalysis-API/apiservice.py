from analysis.analysis import SentimentAnalysis
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

app = Starlette(debug=False)
response_header = { 'Access-Control-Allow-Origin': '*' }

analyzer = SentimentAnalysis()

@app.route('/', methods=['GET', 'POST', 'HEAD'])
async def home_route(request):
    return JSONResponse(content={
        'message': 'Welcome to SentimentAnalysis-API.',
        'info': 'This API only will run from 0.0.0.0 and is for local use only.',
        'developer': 'Cristian Valero Abundio'
    }, headers=response_header)

@app.exception_handler(404)
def route_not_found(request, exc):
    return JSONResponse(content={
        'code': 404,
        'message': 'The route you requested not found. Please, try again or contact with an administrator.'
    }, status_code=exc.status_code)


@app.route('/analyze/', methods=['POST'])
async def generate_answer(request):
    if request.method == 'POST':
        try:
            request_data = await request.json() #{ 'text': 'This is the text to analize' }
            if request_data != None:
                text = str(request_data['text'])
                analysis_result = analyzer.analize(text)
                return JSONResponse(content={
                    'text': str(text),
                    'result': analysis_result,
                }, headers=response_header)
            else:
                return JSONResponse(content={'error:': 'You should send json body.'}, headers=response_header)
        except:
            return JSONResponse(content={'error:': 'Request not valid.'}, headers=response_header)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3003)