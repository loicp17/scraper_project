#!/bin/bash

# Set the URL
URL="https://www.investing.com/currencies/usd-chf"

# Get the current date and time
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Scrape the price
PRICE=$(curl -s "$URL" | grep -oP '"last":\K[\d.]+' | head -n 1)

# Check if PRICE is non-empty and numeric
if [[ -n "$PRICE" && "$PRICE" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    echo "$DATE - USD/CHF Price: $PRICE" >> price.txt
else
    echo "$DATE - ERROR: Price not found or invalid" >> price.txt
fi

# Output the last few lines of price.txt
tail -n 10 price.txt
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
