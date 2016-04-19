# creates new db schema
if cat ../sql/create.sql | mysql; then
    echo -e "\e[32mDatabase is created.\033[0m"
else
    echo -e "\e[31mDatabase is NOT created.\033[0m"
fi

# imports data from cald db
if python ../catcher/importCaldData.py; then
    echo -e "\e[32mData from cald db are imported.\033[0m"
else
    echo -e "\e[31mData from cald db are NOT imported.\033[0m"
fi

# import first data
if cat ../catcher/init/dataset.sql | mysql; then
    echo -e "\e[32mDataset is imported.\033[0m"
else
    echo -e "\e[31mDataset is NOT imported.\033[0m"
fi

# creates init data
if python ../catcher/init/createInitData.py; then
    echo -e "\e[32mInit data are created.\033[0m"
else
    echo -e "\e[31mInit data are NOT created.\033[0m"
fi