#!/usr/bin/fish

for user in (ls /home/)
    cd /home/$user/Documents/
    git clone https://github.com/s2n-cnit/104779-internet_programming.git 
end
