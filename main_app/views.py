from django.shortcuts import render

finches = [
  {'name': 'House Finch', 'scientificname': 'Haemorhous mexicanus', 'description': 'The house finch is a bird in the finch family Fringillidae. It is native to western North America and has been introduced to the eastern half of the continent and Hawaii.', 'mass': '0.74 oz', 'diet': 'Eats almost exclusively plant materials, including seeds, buds and fruits. Wild foods include wild mustard seeds, knotweed, thistle, mulberry, poison oak, cactus, and many other species.'},
  {'name': 'Eurasian Bullfinch', 'scientificname': ' Pyrrhula pyrrhula', 'description': 'The Eurasian bullfinch, common bullfinch or bullfinch is a small passerine bird in the finch family, Fringillidae.', 'mass': '0.86 oz', 'diet': 'Feeds mainly on the seeds and buds of fruit trees. Ash and hawthorn are typically favored in autumn and early winter. They also favor kale, quinoa, and millet.'},
]

# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def finches_index(request):
  return render(request, 'finches/index.html', {
    'finches': finches
  })