#!/bin/bash

# Set the URL
URL="https://www.investing.com/currencies/usd-chf"

# Get the current date and time
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Scrape the price
PRICE=$(curl -s "$URL" | grep -oP '"last":\K[\d.]+' | head -n 1)

# Combine the date, time, and price, and append it to price.txt
echo "$DATE - USD/CHF Price: $PRICE" >> price.txt

# Output the date, time, and price
cat price.txt

