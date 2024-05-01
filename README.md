![Passes tests](https://github.com/software-students-spring2024/4-containerized-app-exercise-team-kiwi2/actions/workflows/build.yaml/badge.svg)

# Containerized App Exercise

## Team members

Stanley Moukhametzianov (SM9231) [Github Profile](https://github.com/Stanley-Moukhametzianov)
<br>
Benson Li (BL2995) [Github Profile](https://github.com/bensonnli)
<br>
Nicholas Meng (ndm9914) [Github Profile](https://github.com/Nmeng01)
<br>
Sangeyl Lee (SL6733) [Github Profile](https://github.com/S2ang) 

## Concept

The idea behind this app is to allow users to generate recommendations for things to do while on vacation. The user can choose to search for things to do in their current location or at a searched location. The app takes advantage of HTML5 geolocation, allowing the browser to ask the user if they want their location to be tracked. Giving this permission then allows the user to generate a list of 5 recommendations for the best things to do in the city that they are located in. For searching location, the user can simply get recommendations for things to do at a place, or they can specify their schedule and generate responses based on how long they spend at a location. The app uses OpenAI to generate recommendations, so the list may differ each time you open the web app. 

## Container Imager Links
[Web App Image](https://hub.docker.com/r/nmeng01/webapp-image)

[ML Client Image](https://hub.docker.com/r/nmeng01/ml-image)

## Configuration

- Firstly, you need to add the openAI api key. Our API key will be sent in our class discord channel: team-kiwi2.  
- Once you have the API key, you need to add it to the docker-compose.yml file in the root directory of the project. Under the ml_app section there will be an environment variable:  OPENAI_API_KEY: "{Insert key here}". You just need to replace the string {Insert key here} with the api key. 
- To run the project, in the terminal run the command:  “ docker-compose up ”. This will start the web-app, ml-app and mongodb. 
- Once everything is done loading, the web app will be hosted at the url: http://localhost:5000/ 
- On the url, you will be taken to our home page where you can select different options for getting vacation recommendations. If you choose the 'Locate Me' option, you need to allow your browser to access your location, so you can just click allow. If you are on Safari, the browser's location settings might cause an error. In that case, we suggest using Chrome- the chrome default settings have so far worked each time. After you allow, you will see your longitude and latitude on the screen and a button. For the other options, simply fill in the necessary location inputs. 
