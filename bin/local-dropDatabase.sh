if cat ../sql/dropDb.sql | mysql; then
    echo -e "\e[32mDatabase is dropped.\033[0m"
else
    echo -e "\e[31mDatabase is NOT dropped.\033[0m"
fi
