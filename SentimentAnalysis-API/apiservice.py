from analysis.analysis import SentimentAnalysis
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

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

if __name__ == '__main__':
    an = SentimentAnalysis()
    uvicorn.run(app, host='0.0.0.0', port=3003)
    #print(an.analize("I don't like pizza."))