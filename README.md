# Life

This is a 'pet' prject of mine, an attempt to simulate life. I have implemented the DNA of the creatures, and am now working on the neural network.

## STATS/DNA
	- reproduction age
	- metabolism = speed/2*size
	- size
	- speed
	- energy gain
	- feild of view
	- view range
	- smell range (for reproduction)
	- pheromone range
	- pheromone scent 
	- color RED
	- color GREEN
	- color BLUE
	- lifespan 
	- mutation rate

These stats will be set by the ants DNA, this will be 'nature'. An ant wil get its DNA from its parents and will define its base stats. 
It will also inherit its neural network from its parents, but this should be an untrained, or less trained version. 

The creatures color will be defined by its DNA by splitting all stats into 3 sections and giving a RGB value to each section, in hopes that similar creatures are similar colors.
The color of the creature will decide the pheromone scent (a numeric value) and the attraction will be based on how close this value is to their RGB values. 

This should thoreticly make it so that the ants are attracted to other ants that share genes similar to their own.

## Nerual Network 
### Inputs
	State
	- hungieness
	- maturity
	- health
	- speed

	Vision
	- distance to closest ant
	- postion of closest ant
	- distance to closest food
	- postion of closest food
	- number of ants seen
	- number of food seen
	- closest ants color
	- pheromone level

### Outputs
	Movement
	- up
	- down
	- left
	- right

	Wants
	- eat
	- look for mate
	- produce phomones

