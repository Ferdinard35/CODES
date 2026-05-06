print("Sentence Vowel Counter")
sentence = input("Enter a sentence: ")
vowels = "aeiou"
sentence = sentence.lower()
count = 0

for char in sentence:
    if char in vowels:
        count += 1

print(f"Number of vowels in the sentence: {count}")
