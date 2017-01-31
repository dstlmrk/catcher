#!/usr/bin/env bash

# create new database
if cat ../db/model/schema.sql | mysql -u root -p; then
    echo -e "\e[32mDatabase is created.\033[0m"
else
    echo -e "\e[31mDatabase is NOT created.\033[0m"
fi

# import init data
# TODO: casem presunout do Python scriptu
if cat ../db/scripts/dataset.sql | mysql -u root -p; then
    echo -e "\e[32mDataset is imported.\033[0m"
else
    echo -e "\e[31mDataset is NOT imported.\033[0m"
fi

# create init data
if python ../db/scripts/init_data.py; then
    echo -e "\e[32mInit data are created.\033[0m"
else
    echo -e "\e[31mInit data are NOT created.\033[0m"
fi
