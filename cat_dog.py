import dash
import numpy as np
import requests

from dash import dcc, html
from dash.dependencies import Input, Output, State
from io import BytesIO
from keras.models import load_model
from PIL import Image

# Initializing model.
model = load_model('cd_model.h5')
model.make_predict_function()

app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.Div([
        html.H3(children="Hello :D! I'd like to try and guess if you show me a dog or a cat..."),  
        html.Div([
            html.Div([
                dcc.Input(
                    id='input-url',
                    placeholder='Enter the direct url to the image...',
                    value='https://img00.deviantart.net/b207/i/2008/354/8/2/the_50_50_cat_hd_pic_by_deakablackdragon.jpg',
                    style={'width': '600px'}
                ),
            ]),
            html.Br(),
            html.Div([            
                html.Button(id='submit-button', n_clicks=0, children='Press me and let me guess',
                            style={'font-size': '14px', 'marginLeft': 10}),
                html.A(
                    children=html.Button(children='Source in GitHub', style={'font-size': '14px', 'marginLeft': 10}),
                    href='https://github.com/diabeticowl/Cat-Dog',
                    target='_blank'
                )
            ], style={'display': 'inline-block'})   
        ]),
    ]),
    html.Br(),
    html.Div([
        html.H4(children='Image preview:'),
        html.Img(id='image-preview', src='', style={'width': '400px', 'height': '400px'}, alt='No Image Found'),
        html.H4(id='prediction', children='I think this is a... ')
    ])
],  className='six.columns')


@app.callback(Output('image-preview', 'src'), [Input('input-url', 'value')])
def show_preview(url):
    return url


@app.callback(Output('prediction', 'children'), [Input('submit-button', 'n_clicks')], [State('input-url', 'value')])
def predict_image(_, url):
    img_width, img_height = 64, 64

    try:
        response = requests.get(url)
        im = Image.open(BytesIO(response.content))
        im = im.resize((img_width, img_height))

        im = np.expand_dims(np.array(im), axis=0)

        prediction = model.predict([im])[0][0] >= 0.5

        if prediction:
            return "I think that this image is of a Dog!"
        return "I think that this image is of a Cat!"
    except OSError:
        return "Check the URL passed. It doesn't look like a photo."


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server()
