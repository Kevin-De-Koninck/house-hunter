![Build and tests](https://github.com/Kevin-De-Koninck/house-hunter/workflows/Build%20and%20tests/badge.svg)
![Push Docker container](https://github.com/Kevin-De-Koninck/house-hunter/workflows/Push%20Docker%20container/badge.svg)

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

## Pushover keys

This project requires the PushOver keys to be present in a YAML file that is volume mounted inside the container. An example config file:




``` yaml
househunter:
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
    bedrooms_min: 2
    connected_to_the_sewer_network: True
    flood_zone: False
    gas_water_electricity: True
    double_glazing: True
    planning_permission_obtained: True
    Latest_land_use_designation: 'Living area'
    preffered_filters:
      building_conditions:
        - 'as new'
        - 'good'
      kitchen_type: 'installed' 
      facades: 4

pushover:
  API_token: 'abcdefghijklmnopqrstuvwxyz0123'
  user_key: 'abcdefghijklmnopqrstuvwxyz0123'
```


