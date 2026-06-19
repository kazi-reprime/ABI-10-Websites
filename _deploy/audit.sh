#!/usr/bin/env bash
set -e
RESULT=()
for n in 1 2 3 4 5 6 7 8 9 10; do
  url="https://abi-app-$n.vercel.app"
  # Fetch homepage and check various properties
  body=$(curl -s "$url/" --max-time 12)
  has_title=$(echo "$body" | grep -c '<title>American Barber')
  has_viewport=$(echo "$body" | grep -c 'name="viewport"')
  has_desc=$(echo "$body" | grep -c 'name="description"')
  has_og=$(echo "$body" | grep -c 'property="og:title"')
  has_jsonld=$(echo "$body" | grep -c 'application/ld+json')
  has_canonical=$(echo "$body" | grep -c 'rel="canonical"')
  has_cdn=$(echo "$body" | grep -c 'abi-assets.vercel.app')
  has_burger=$(echo "$body" | grep -c '\.burger')
  has_faq_link=$(echo "$body" | grep -c 'href="/faq')
  size_kb=$(echo -n "$body" | wc -c | awk '{print int($1/1024)}')
  # Subpage statuses (follow redirects)
  pg=$(curl -sL -o /dev/null -w '%{http_code}' "$url/programs.html" --max-time 10)
  gl=$(curl -sL -o /dev/null -w '%{http_code}' "$url/gallery.html" --max-time 10)
  fq=$(curl -sL -o /dev/null -w '%{http_code}' "$url/faq.html" --max-time 10)
  ct=$(curl -sL -o /dev/null -w '%{http_code}' "$url/contact.html" --max-time 10)
  sm=$(curl -s -o /dev/null -w '%{http_code}' "$url/sitemap.xml" --max-time 10)
  rb=$(curl -s -o /dev/null -w '%{http_code}' "$url/robots.txt" --max-time 10)
  echo "abi-app-$n | title=$has_title viewport=$has_viewport desc=$has_desc og=$has_og jsonld=$has_jsonld canonical=$has_canonical cdn=$has_cdn burger=$has_burger | pages: P=$pg G=$gl F=$fq C=$ct sm=$sm rb=$rb | ${size_kb}KB"
done
