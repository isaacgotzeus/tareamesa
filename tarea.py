import mesa
import random



class Wally(mesa.Agent):

  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.wealth = 1

  def move(self):
    possible_steps = self.model.grid.get_neighborhood(self.pos,
                                                      moore=True,
                                                      include_center=False)
    new_pos = self.random.choice(possible_steps)
    self.model.grid.move_agent(self, new_pos)

  def step(self):
    self.move()

    cell = self.model.grid.get_cell_list_contents([self.pos])
    for i in cell:
      if type(i) == Trash and i.cantidad == True:
        self.model.grid.remove_agent(i)
        self.wealth += 1

class Trash(mesa.Agent):

  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.cantidad = True
    self.wealth = 1

  def step(self):
    contador = 0
    contador += 1

class Modelo(mesa.Model):

  def __init__(self, N, T):
    self.num = N
    self.num2 = T
    self.grid = mesa.space.MultiGrid(10, 10, False)
    self.schedule = mesa.time.RandomActivation(self)
    self.running = True

    
    for i in range(self.num):
      wally2 = Wally(i, self)
      self.schedule.add(wally2)
      self.grid.place_agent(wally2, (1, 1))

    for i in range(self.num2):
      basura = Trash(self.num + i, self)
      self.schedule.add(basura)
      x = random.randint(0, 9)
      y = random.randint(0, 9)
      self.grid.place_agent(basura, (x, y))

    self.datacollector = mesa.DataCollector(
      model_reporters={"Gini": compute_gini},
      agent_reporters={"Wealth": "wealth"})

  def step(self):
    self.datacollector.collect(self)
    self.schedule.step()


def compute_gini(model):
  agent_wealths = [agent.wealth for agent in model.schedule.agents]
  a = sorted(agent_wealths)
  b = model.num
  c = sum(xi * (b - i) for i, xi in enumerate(a)) / (b * sum(a))
  return 1 + (1 / b) - 2 * c


def agent_port(agent):

  portrayal = {
    "Shape": "circle",
    "Filled": "true",
    "Layer": "Act Aspiradora",
    "Color": "red",
    "r": 0.5,
  }

  if type(agent) == Trash:

    portrayal["Color"] = "green"

  return portrayal


grid = mesa.visualization.CanvasGrid(agent_port, 10, 10, 500, 500)
chart = mesa.visualization.ChartModule([{
  "Label": "Gini",
  "Color": "Black"
}],
                                       data_collector_name='datacollector')
server = mesa.visualization.ModularServer(Modelo, [grid, chart], "Act Aspiradora",
                                          {
                                            "N": 7,
                                            "T": 58
                                          })

server.port = 8522

server.launch()
