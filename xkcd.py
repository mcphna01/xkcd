from flask import Flask, request, render_template
import random

app=Flask(__name__)

@app.route('/')
def base():
	return render_template('index.html')


def easyscore(word):
	score=0.0
	left="asdfgqwertzxvcb"
	right="yuiophjklnm"
	for i in range(len(word)-1):
		if word[i] in left and word[i+1] in right:
			score+=1
		elif word[i] in right and word[i+1] in left:
			score+=1
		elif word[i]==word[i+1]:
			score+=1
	return score/(len(word)-1)

@app.route('/genpass')
def genpass():
	words = open("words.txt",'r')
	wordlist = [word.strip() for word in words]
	min_length=int(request.args.get('min_length'))
	max_length=int(request.args.get('max_length'))
	min_word_length=int(request.args.get('min_word_length'))
	max_word_length=int(request.args.get('max_word_length'))

	numletters={'e':3,'s':5,'o':0,'l':1,'z':2}

	numsub=False
	if request.args.get('num_sub'):
		numsub=True

	easytyping=False
	if request.args.get('easy'):
		easytyping=True

	param_list=[]
	for word in wordlist:
		if len(word)>=min_word_length and len(word)<=max_word_length:
			param_list.append(word)
	listlen=len(param_list)

	pass_list=[]
	while len(pass_list)<4:
		index1=random.randint(0,listlen-1)
		index2=random.randint(0,listlen-1)
		index3=random.randint(0,listlen-1)
		index4=random.randint(0,listlen-1)
		password="{}{}{}{}{}{}{}".format(param_list[index1]," ",param_list[index2]," ",param_list[index3]," ",param_list[index4])
		if len(password)>=min_length+3 and len(password)<=max_length+3:
			if numsub==True:
				newpassword=""
				for letter in password:
					if letter in numletters:
						newpassword+=str(numletters[letter])
					else:
						newpassword+=letter
				if easytyping==True:	
					if easyscore(password)>=0.7:
						pass_list.append(newpassword)
				else:
					pass_list.append(newpassword)
			else:
				if easytyping==True:	
					if easyscore(password)>=0.7:
						pass_list.append(password)
				else:
					pass_list.append(password)

	return render_template('pass.html',pass_list=pass_list)

if __name__=='__main__':
	app.run(debug=True)