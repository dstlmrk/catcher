echo -e "You want to drop database as root."

if cat /home/dstlmrk/catcher/sql/dropDb.sql | mysql -u root -p; then
    echo -e "\e[32mDatabase is dropped.\033[0m"
else
    echo -e "\e[31mDatabase is NOT dropped.\033[0m"
fi