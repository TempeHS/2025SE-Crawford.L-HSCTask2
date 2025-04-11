# 2025SE-Crawford.L-HSCTask2

This will be used to predict the weather at Sydney Airport ([YSSY](https://en.wikipedia.org/wiki/Sydney_Airport)).

## Description

An in-depth paragraph about your project and overview of use.

## MLOps

### Design Stage

#### Business Problem:

Pilots don't exactly know what weather to expect in the future, instead they just get past weather (within 30 mins – 1 hour or quicker if the weather is changing rapidly).

#### Success Metrics:

Be able to predict the weather within the next 10-30 mins to above 50% accuracy.

#### Data Columns:

```
time,wmo,name,history_product,air_temp,apparent_t,dewpt,rel_hum,delta_t,wind_dir_deg,wind_spd_kmh,gust_kmh,rain_trace,rain_ten,rain_hour,duration_from_9am,press,lat,lon,location
```

| Column          | Description                                                                |
| --------------- | -------------------------------------------------------------------------- |
| time            | The date and time of the observation.                                      |
| wmo             | The ID of the weather station.                                             |
| name            | The human-friendly name of the weather station.                            |
| history_product | The ID for BOM identification.                                             |
| air_temp        | The air temperature (°C) recorded at the time of observation.              |
| dewpt           | The temperature (°C) at which air becomes saturated and dew forms.         |
| rel_hum         | The percentage of moisture in the air relative to the maximum it can hold. |
| wind_dir_deg    | The direction from which the wind is blowing, in degrees.                  |
| wind_spd_kmh    | The speed of the wind (km/h) at the time of observation.                   |
| gust_kmh        | The maximum wind speed (km/h) recorded during a short period.              |
| press           | Atmospheric pressure (hPa) at the observation site.                        |
| rain_trace      | The amount of precipitation (mm) recorded over a specific period.          |
| lat             | The latitude of the observation site.                                      |
| lon             | The longitude of the observation site.                                     |
| location        | The specific location of the weather station.                              |

## Getting Started

### Dependencies

-   Python requirements:

```
numpy
matplotlib
pandas
scikit-learn
keras
tensorflow
pydot
graphviz
pydot-ng
pillow
pydotplus
ipykernel
metpy
seaborn
Flask
flask_wtf
flask-csp
jsonschema
requests
flask_cors
flask_limiter
flask-talisman
pylint
python-dotenv
```

### Executing program

-   How to run the program

```bash
cd 2./Model-Deployment
python main.py
```

Then access at `https://127.0.0.1:5000/`.

## Help

Any advise for common problems or issues.

```
command to run if program contains helper info
```

## Authors

-   [@DefNotCrawf](https://github.com/DefNotCrawf)

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](./LICENSE) file for details.

## Acknowledgments

Inspiration, code snippets, etc.

-   [Github Markdown Syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
-   [TempeHS Jupyter Notebook Template](https://github.com/TempeHS/TempeHS_Jupyter-Notebook_DevContainer)
-   [TempeHS MLOps](https://github.com/TempeHS/Practical-Application-of-NESA-Software-Engineering-MLOps)
