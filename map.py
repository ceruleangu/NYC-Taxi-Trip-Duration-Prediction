import bronx
import brooklyn
import manhattan
import island
import queens
import json

cx = {}
cy = {}
x, y = bronx.Bronx()
cx.update(x)
cy.update(y)
x, y = brooklyn.brooklyn()
cx.update(x)
cy.update(y)
x, y = manhattan.manhattan()
cx.update(x)
cy.update(y)
x, y = queens.queens()
cx.update(x)
cy.update(y)
x, y = island.island()
cx.update(x)
cy.update(y)

json_str = json.dumps(cx)
with open('cx.json', 'w') as json_file:
    json_file.write(json_str)

json_str = json.dumps(cy)
with open('cy.json', 'w') as json_file:
    json_file.write(json_str)