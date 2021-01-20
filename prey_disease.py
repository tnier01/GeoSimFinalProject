from pcraster import *
from pcraster.framework import *

class Fire(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone(200, 200,  1, 0, 0)

  def initial(self):
      prey = uniform(1) < 0.05
      predator = uniform(1) < 0.1
      infected = uniform(1) < 0.05

      self.predator = ifthenelse(predator, scalar(1.0), 0.0)
      self.prey = ifthenelse(prey, scalar(1.0), ifthenelse(infected, scalar(2.0), 0.0))

      self.report(self.prey, 'plot/prey_2')
      self.report(self.predator, 'plot/predator_2')

  def dynamic(self):
      prey = pcreq(self.prey, 1)

      predator = pcreq(self.predator, 1)

      infected = pcreq(self.prey, 2)

      infected_neighbour = window4total(scalar(infected)) > 0

      hunted = pcrand(pcror(infected, prey), predator)




      infected_not_hunted = pcror(pcrand(prey, infected_neighbour), pcrand(infected, pcrnot(hunted)))

      neighbours = window4total(scalar(pcrand(pcrnot(infected_neighbour), pcrand(prey, pcrnot(hunted)))))

      alive_neighbour = pcror(neighbours > 0, pcrand(prey, pcrnot(hunted)))



      hunted_neighbour = window4total(scalar(hunted))

      hunted_new = pcror(hunted_neighbour > 0, hunted)



      self.prey = ifthenelse(infected_not_hunted, scalar(2.0), ifthenelse(alive_neighbour, scalar(1.0), 0.0))
      
      self.predator = hunted_new
      
      self.report(self.prey, 'plot/prey_2')
      self.report(self.predator, 'plot/pred_2')

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


nrOfTimeSteps = 181
myModel = Fire()
dynamicModel = DynamicFramework(myModel, nrOfTimeSteps)
dynamicModel.run()

