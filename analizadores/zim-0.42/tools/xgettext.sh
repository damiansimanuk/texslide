echo 'Extracting translatable strings ...'
find zim -name '*.py' | sort | xgettext -f - -o zim.pot
echo 'Extracting comments ...'
./tools/extract_translator_comments.py
