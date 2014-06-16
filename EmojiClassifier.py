"""Straight forward Emoji Classifier:

If (UTF-8) encrypted Emoji code is found within a String,
return the Emoji Type.

Upon Update -- Map numerical values to sentimental values
"""

_emojis = {
	"\xF0\x9F\x98\x83": "Happy",		# \xF0\x9F\x98\x83 - Happy [1500]
	"\xF0\x9F\x98\x8C": "Relaxed",		## \xF0\x9F\x98\x8C - relieved face [315]
	"\xF0\x9F\x98\x84": "Elated",		## \xF0\x9F\x98\x84 - smiling face with open mouth and smiling eyes[1500]
	"\xF0\x9F\x98\x9D": "Excited",		## \xF0\x9F\x98\x9D - face with stuck-out toungue and tightly closing eyes [1211]
	"\xF0\x9F\x98\xB3": "Stressed",		## \xF0\x9F\x98\xB3 - Flushed face [969]
	"\xF0\x9F\x98\xA1": "Upset",		## \xF0\x9F\x98\xA1 - Red pouting face [670]
	"\xF0\x9F\x98\x9E": "Unhappy",		## \xF0\x9F\x98\x9E - disappointed face [635]
	"\xF0\x9F\x98\xA2": "Sad",			## \xF0\x9F\x98\xA2 - crying face [508]
	"\xF0\x9F\x98\x8A": "Pleasant"	# \xF0\x9F\x98\x8A - smiling face with smiling eyes [1460]
}

tweet = "hello, I #like to eat\xF0\x9F\x98\x83\xF0\x9F\x98\x83\xF0\x9F\x98\x83!!!!! \xF0\x9F\x98\xA2\xF0\x9F\x98\x84"

def search(tweet):
	for key in _emojis.keys():
		# print key
		# emojis = _emojis[key]
		# yield emojis
		if key in tweet:
			# print "key: %s, value: %s" % (key, _emojis[key])
			yield (key, _emojis[key])
		# else: return False


# search(tweet)
results =  search(tweet)
for r in results:
	print(r)
