<h1 align="center">
  WVTool
</h1>

<h4 align="center">
  WVTool - Weather Visualization Tool
</h4>

<p align="center">
  <a href="#about">About</a> •
  <a href="#features">Features</a> •
  <a href="#install">Install</a> •
  <a href="#workflow">Workflow</a> •
  <a href="#architecture-diagram">Architecture Diagram</a> •
  <a href="#project-requirements">Project Requirements</a> •
  <a href="#schedule">Schedule</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

![cefet](https://i.imgur.com/K0E5iFC.jpg)

## About

WVTool stands for Weather Visualization Tool. WVtool is a project that its main goal
is to visualize GOES-16 weather data for Rio de Janeiro region. This project is done
by CEFET/RJ CC course students.

## Features

* Interactive Weather Map
  * Zoom in
  * Zoom out
  * Translation
* Multilayer
  * Select different map layers
  * Select different weather features layers

## Install

For running this project locally you will need to install:

1. [Git](https://github.com/git/git)
2. [Docker](https://www.docker.com/)

```bash
# Clone the repository
git clone https://github.com/dennis-10/weather-visualization-tool

# Go into project directory
cd weather-visualization-tool

# Go into backend directory
cd backend

# Create a .env file inside backend directory
SOURCE="DATA_PATH"

- DATA_PATH must be a path with data.  C:/Users/user_name/Desktop/WVT e.g. 
- Inside DATA_PATH root folder must contain 2 subfolders: 
   "dados_pluviometros" : pluviometric stations data
   "satelite_data" : unziped satelite's data with subfolders YEAR>>DAY_OF_YEAR>>HOUR_OF_DAY

# Build the Dockerfile for generating an image
docker-compose build

# Run the Docker container
docker-compose up

```
- Drop data in local folder
- Select meteorological variable
- Set Initial Date and Hour and End Date and Hour (minutes must be 00, 15, 30 or 45)
- Choose grid cell number
- Press Play button

## Workflow

![workflow](https://i.imgur.com/dQhte2C.png)

## Class Diagram
[Class Diagram](https://github.com/dennis-10/weather-visualization-tool/blob/dev/docs/assets/Diagrama%20de%20Classe.pdf)

## Architecture and technologies

WVTool was developed under the Client-Server architecture, using the Flask web micro-framework. Both the frontend and the backend were developed using Flask. The application was containerized with Docker. The main tool for displaying the map was the Folium library, based on the Leaflet library.

[Architecture Diagram](https://github.com/dennis-10/weather-visualization-tool/blob/dev/docs/assets/Diagrama%20de%20Arquitetura.pdf)

## Project Requirements

The original requirement document can be found in this [link](https://github.com/cassiofb-dev/weather-visualization-tool/tree/master/docs/assets/PCS2022.1-Projeto1-wvtool_compressed.pdf).

### Functional Requirements

1. As a background resource, the app must allow users to configurate the local data repository. * THIS FR IS SET VIA COMMAND LINE
   1. The data must not be alterated in comparison to its font.
2. The app must consume the weather data in local repository.
3. The user can choose the weather variable.
4. The app main view must have 3 layers:
   1. Layer 1: Rio de Janeiro map.
   2. Layer 2: Weather geospatial  data in timelapse animation.
   3. Layer 3: 7x7 Grid over Rio de Janeiro area.
5. The app must allow user controls like: zoom in, zoom out and translation.
6. The app main view must be a timelapse wather geospatial data animation. It must show the evolution of the choosed weather variable:
   1. The animation must show data grouped by a time interval of 15 minutes.
   2. The animation must be controlled by a control bar.
   3. The control bar must allow users to define the inital and final datetime.
   4. The control bar must allow users to pause visualization.
   5. The control bar must allow users to skip to the previos or next period.
7. The app must have, as auxiliary views, plot of the geospatial data provided by weather stations:
   1. Each plot must be linked to a dropdown that allows users to choose one of the 49 grid cells.
   2. The plot must show the data linked to weather station observations in the selected grid area.
   3. Each plot must show the precipitation data as a line plot in which the x axis contains the time dimension and y axis contains the observation value.
   4. The plot must evolve as an animation that is linked to the main view time and the current time in the main view must be the central time in the auxiliary view.
   5. In each animated interation, the auxiliary view plot must show the observations of the 12 previous and next periods.
8. The app must allow users to download the animation as a animated gif or a png image of the current interation.

### Non-functional Requirements

1. Beside the app source code, the items bellow must also be included as tasks:
   1. <a href="#install">Installation and configuration documentation</a>.
   2. <a href="#architecture-diagram">Architecture diagram</a>.
   3. Class diagram.
2. The app development must be evolutive and versioned on github.
3. The github repository must be shared to show the app evolution.
4. The first task must be done as a read me markdown file on github.
5. The tasks 1.2, 1.3 and 1.4 must be in docs directiory.


## License

MIT

---

> Raphael do Val [@raphadvl](https://github.com/raphadvl) &nbsp;&middot;&nbsp;
> Dennis Rodrigues [@dennis-10](https://github.com/dennis-10) &nbsp;&middot;&nbsp;
