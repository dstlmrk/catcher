if cat ../sql/createDb.sql | mysql; then
    echo -e "\e[32mDatabase is created.\033[0m"
else
    echo -e "\e[31mDatabase is NOT created.\033[0m"
fi
