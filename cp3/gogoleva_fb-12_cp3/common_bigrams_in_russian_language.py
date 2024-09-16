import re

file_path = r"C:\Users\Polya\Desktop\KPI\crypto\crypto-23-24\cp1\gogoleva_fb-12_cp1\bible.txt"

with open(file_path, "r", encoding="windows-1251") as file:
    cleaned_text = ''
    for line in file:
        line = re.sub(r'[^а-яА-ЯёЁ]', '', line)  # Вилучення всіх символів окрім літер
        cleaned_text += line.lower()

# Підрахунок частоти біграм
bigram_with_overlap_counts = {}
bigram_without_overlap_counts = {}

for i in range(len(cleaned_text) - 1):
    # Підрахунок частоти біграм з перетином
    bigram_with_overlap = cleaned_text[i:i + 2]
    if bigram_with_overlap in bigram_with_overlap_counts:
        bigram_with_overlap_counts[bigram_with_overlap] += 1
    else:
        bigram_with_overlap_counts[bigram_with_overlap] = 1

    if i % 2 == 0:
        # Підрахунок частоти біграм без перетину
        bigram_without_overlap = cleaned_text[i:i + 2]
        if bigram_without_overlap in bigram_without_overlap_counts:
            bigram_without_overlap_counts[bigram_without_overlap] += 1
        else:
            bigram_without_overlap_counts[bigram_without_overlap] = 1

# Сортування біграм за частотою
sorted_bigram_with_overlap = sorted(bigram_with_overlap_counts.items(), key=lambda x: x[1], reverse=True)
sorted_bigram_without_overlap = sorted(bigram_without_overlap_counts.items(), key=lambda x: x[1], reverse=True)

# Виведення п'ятьох найчастіших біграм
print("П'ять найчастіших біграм з перетином в російській мові:")
for i in range(5):
    print(f"{sorted_bigram_with_overlap[i][0]}: {sorted_bigram_with_overlap[i][1]} разів")

print("\nП'ять найчастіших біграм без перетину в російській мові:")
for i in range(5):
    print(f"{sorted_bigram_without_overlap[i][0]}: {sorted_bigram_without_overlap[i][1]} разів")
