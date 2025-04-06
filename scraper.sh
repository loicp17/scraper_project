#!/bin/bash

# Set the URL
URL="https://www.investing.com/currencies/usd-chf"

# Scrape the price and save to price.txt
curl -s "$URL" | grep -oP '<span class="text-2xl">[\d,]+\.\d+' | grep -oP '[\d,]+\.\d+' > price.txt

# Output the price
cat price.txt
