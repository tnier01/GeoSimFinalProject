from pcraster import *
from pcraster.framework import *

class Fire(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone(200, 200,  1, 0, 0)

  def initial(self):
      prey = uniform(1) < 0.1
      predator = uniform(1) < 0.05
      infected = uniform(1) < 0.05

      self.prey = ifthenelse(prey, scalar(1.0), 0.0)
      self.predator = ifthenelse(predator, scalar(1.0), ifthenelse(infected, scalar(2.0), 0.0))

      self.report(self.prey, 'plot/prey_1')
      self.report(self.predator, 'plot/predator_1')

  def dynamic(self):
      prey = pcreq(self.prey, 1)

      predator = pcreq(self.predator, 1)

      infected = pcreq(self.predator, 2)

      hunted = pcrand(prey, pcror(predator, infected))

      neighbours = window4total(scalar(pcrand(prey, pcrnot(hunted))))

      alive_neighbour = pcror(neighbours > 0, pcrand(prey, pcrnot(hunted)))

      hunted_neighbour = window4total(scalar(hunted))

      infected_neighbour = window4total(scalar(infected))

      sound_hunt_predator = pcrand(hunted, pcrnot(pcror(infected_neighbour > 0, infected)))
      sound_hunt_neighbour = window4total(scalar(sound_hunt_predator)) > 0

      new_sound_predator = pcror(sound_hunt_predator, sound_hunt_neighbour)
          # = pcror(pcrand(hunted_neighbour > 0, pcrnot(infected_neighbour > 0)), pcrand(hunted, pcrnot(infected_neighbour > 0)))

      new_infected_predator = pcrand(hunted, pcror(infected, infected_neighbour > 0))
      
      self.prey = alive_neighbour
      
      self.predator = ifthenelse(new_infected_predator, scalar(2.0), ifthenelse(new_sound_predator, scalar(1.0), 0.0))
      
      self.report(self.prey, 'plot/pred_dis/prey')
      self.report(self.predator, 'plot/pred_dis/predator')

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


nrOfTimeSteps = 250
myModel = Fire()
dynamicModel = DynamicFramework(myModel, nrOfTimeSteps)
dynamicModel.run()

