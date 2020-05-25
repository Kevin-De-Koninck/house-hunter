![Build and tests](https://github.com/Kevin-De-Koninck/house-hunter/workflows/Build%20and%20tests/badge.svg)
![Push Docker container](https://github.com/Kevin-De-Koninck/house-hunter/workflows/Push%20Docker%20container/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Kevin-De-Koninck_house-hunter&metric=alert_status)](https://sonarcloud.io/dashboard?id=Kevin-De-Koninck_house-hunter)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Kevin-De-Koninck_house-hunter&metric=coverage)](https://sonarcloud.io/dashboard?id=Kevin-De-Koninck_house-hunter)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Kevin-De-Koninck_house-hunter&metric=security_rating)](https://sonarcloud.io/dashboard?id=Kevin-De-Koninck_house-hunter)

# house-hunter

## How to build and run

### Dev container

``` bash
./build.sh -p dev
./run.sh
```

### Prod container

``` bash
./build.sh -p prod -v 'v0.0.1'
./run.sh -v 'v0.0.1'
```

## Config file

An example config file:

``` yaml
househunter:
  enabled_sites:
    - 'immoweb.be'
    - 'zimmo.be'
    - immo.vlan.be'
    - 'realo.be'
    - 'immoscoop.be'
  postal_codes:
    - 2200  # Herentals
    - 2000  # Antwerp
  price:
    old_real_estate:
      minimum: 170000
      maximum: 250000
    new_real_estate:
      minimum: 150000
      maximum: 230000
  property:
    type:
      - house
      - apartment
      - new-real-estate-project-houses
      - new-real-estate-project-apartments
    filters:
      required:
        bedrooms_min: 2
        connected_to_the_sewer_network: True
        flood_zone: False
        gas_water_electricity: True
        double_glazing: True
        planning_permission_obtained: True
        Latest_land_use_designation: 'Living area'
        epc_max: 700
        build_year_max: 1990
      preferred:
        building:
          - 'as new'
          - 'good'
        kitchen_type: 'installed' 
        facades: 4
        mobi_score_min: 7
        garage: True
        garden: True

pushover:
  API_token: 'abcdefghijklmnopqrstuvwxyz0123'
  user_key: 'abcdefghijklmnopqrstuvwxyz0123'
```


