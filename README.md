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
    - 'immo.vlan.be'
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

  types:
    house: False
    apartment: True
    new_real_estate: False
    
  filters:
    general:
      building_condition: 
        - None
      exclude_building_condition:
        - None
      construction_year_minimum: 1950
      covered_parking_spaces_minimum: 0
      outdoor_parking_spaces_minimum: 0
      facades_minimum: 0

    interior:
      kitchen_type:
        - None
      exclude_kitchen_type:
        - None
      bedrooms_minimum: 2
      bathrooms_minimum: 1
      toilets_minimum: 1
      has_basement: False
      has_attic: False
      is_furnished: False

    exterior:
      surface_of_the_plot_minimum: 100
      is_connected_to_the_sewer_network: True
      has_terrace: False
      has_gas_water_electricity: True

    energy:
      energy_class_maximum: F
      epc_maximum: 700
      has_double_glazing: True
      has_heat_pump: None
      has_pv_cells: None

    townplanning:
      is_flood_zone: False
      Latest_land_use_designation: 'living area'
      has_planning_permission_obtained: True

pushover:
  API_token: 'abcdefghijklmnopqrstuvwxyz0123'
  user_key: 'abcdefghijklmnopqrstuvwxyz0123'
```


