echo -e "You want to create database as root."

# creates new db schema
if cat /home/dstlmrk/catcher/sql/createDb.sql | mysql -u root -p; then
    echo -e "\e[32mDatabase is created.\033[0m"
else
    echo -e "\e[31mDatabase is NOT created.\033[0m"
fi

# imports data from cald db
if python /home/dstlmrk/catcher/catcher/importCaldData.py; then
    echo -e "\e[32mData from cald db are imported.\033[0m"
else
    echo -e "\e[31mData from cald db are NOT imported.\033[0m"
fi

# creates init data
if python /home/dstlmrk/catcher/catcher/createInitData.py; then
    echo -e "\e[32mInit data are created.\033[0m"
else
    echo -e "\e[31mInit data are NOT created.\033[0m"
fi