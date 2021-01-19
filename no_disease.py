from pcraster import *
from pcraster.framework import *

class Fire(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone(200, 200,  1, 0, 0)

  def initial(self):
      prey = uniform(1) < 0.1
      predator = uniform(1) < 0.1

      self.prey = ifthenelse(prey, scalar(1.0), 0.0)
      self.predator = ifthenelse(predator, scalar(1.0), 0.0)

      self.report(self.prey, 'plot/prey')
      self.report(self.predator, 'plot/predator')

  def dynamic(self):
      prey = pcreq(self.prey, 1)

      predator = pcreq(self.predator, 1)

      hunted = pcrand(prey, predator)

      neighbours = window4total(scalar(pcrand(prey, pcrnot(hunted))))

      alive_neighbour = pcror(neighbours > 0, pcrand(prey, pcrnot(hunted)))

      hunted_neighbour = window4total(scalar(hunted))

      hunted_new = pcror(hunted_neighbour > 0, pcrand(predator, hunted))
      
      self.prey = alive_neighbour
      
      self.predator = hunted_new
      
      self.report(self.prey, 'plot/prey')
      self.report(self.predator, 'plot/predator')

      # burningNeighbours = window4total(scalar(self.fire))
      # neighbourBurns = burningNeighbours > 0
      # self.report(neighbourBurns, 'ngbBrns')
      # 
      # potentialNewFire = pcrand(neighbourBurns, pcrnot(self.fire))
      # self.report(potentialNewFire, 'pnf')
      # 
      # realization = uniform(1) < 0.1
      # 
      # newFire = pcrand(realization, potentialNewFire)
      # self.report(newFire, 'newFire')
      # 
      # self.fire = pcror(self.fire, newFire)
      # self.report(self.fire, 'fire')


nrOfTimeSteps = 100
myModel = Fire()
dynamicModel = DynamicFramework(myModel, nrOfTimeSteps)
dynamicModel.run()

