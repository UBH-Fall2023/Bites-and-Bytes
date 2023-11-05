from flask import Flask, request, jsonify
import csv
import random


def checkInput(input):
  input=input.split(",")
  flag=False
  errorString=""
  newList=[]
  for i in input:
    newList.append(i.lower())
    if (not isFood(i)):
      errorString=errorString+" "+i
      flag=True
  if (flag):
    return "invalid food:"+errorString
  return newList

def throwRamen():
  return random.randint(0,10)==10


#returns dict of all valid foods
def defFood():
  validFoods={}
  with open('myfood.csv') as file:
    reader = csv.reader(file)
    for row in reader:
      if (not validFoods.keys().__contains__(row[0])):
        validFoods[row[0].lower()]=row[0].lower()
        
    
        
  return validFoods

#checks if food is valid
def isFood(food):
  food=food.lower()
  return food in foodDict

#generates a dict where the keys are recipes and the values are lists of ingredients
def genRecipies(file):
  with open(file) as file:
    reader = csv.reader(file)
    ingredientsDict={}
    instructionsDict={}
    for row in reader:
      ingredientsDict[row[0]]=row[1].split(",")
      instructionsDict[row[0]]=row[2].split(",")
    return [ingredientsDict,instructionsDict]

#checks if all ingredients in a recipe are present in the input list
def compareLists(L1,L2):
  for i in L1:
    if (not L2.__contains__(i)):
      return False
  return True

#RecipieDict will store a dict of {dishName:[ingredients]}}
def findRecipe(input):
  ValidRecipies=[]
  for i in ingredientsDict:
    ingredientsDict[i].sort()
    input.sort()
    flag=True
    for j in ingredientsDict[i]:

      if(not input.__contains__(j)):
        flag=False

    if (flag):
      ValidRecipies.append(i)

  return ValidRecipies

def returnRecipe(ValidRecipes):
  if len(ValidRecipes)==0:
    return "dig the instant ramen out of your pantry"
  randindex=random.randint(0,len(ValidRecipes))
  recipe=ValidRecipes[randindex]
  instructions = instructionsList[0][recipe][0]
  return "Recipe: "+recipe+" - "+instructions

foodDict=defFood()
recipeList=genRecipies('recipe.csv')
ingredientsDict=recipeList[0]
instructionsDict=recipeList[1]
instructionsList=[]
newDict={}
for i in instructionsDict:
  newDict[i]=instructionsDict[i]
  instructionsList.append(newDict)


def main(input):
  c1=checkInput(input)
  if isinstance(c1, str):
    return c1
  c2=findRecipe(c1)
  c3=returnRecipe(c2)
  return c3






app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html', 'r').read()


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user_input = data['userInput']
  
    # Process the user input (you can replace this with your own logic)
    processed_result = main(user_input)

    return jsonify({'message': processed_result})

if __name__ == '__main__':
    app.run(host = '0.0.0.0')