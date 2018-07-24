## calcs.py
## Yuan Wang

from scipy.stats import norm

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from demo import demoPlot

__MEAN_KIDS_PER_FAMILY__ = 2.4
__STD_DEV_KPF__ = 0.9

__BASE_PARENT_IQ__ = 160
__STANDARD_DEV__ = 15
__POPULATION_MEAN_IQ__ = 105 ## assuption on educational cohort
__MEAN_REGRESSION__ = 0.3

__COLORMAPS__ = [ cm.Purples, cm.Blues, cm.BuGn, cm.Greens, cm.Oranges, cm.Reds, ]

## returns probability of having at least one child with target IQ
def calc(counterpartyIQ, numberOfKids, targetIQ=150, genders=1):
	parentExpected = (counterpartyIQ + __BASE_PARENT_IQ__) / 2.0
	expected = __POPULATION_MEAN_IQ__ * __MEAN_REGRESSION__ + parentExpected * (1 - __MEAN_REGRESSION__)

	prob = norm.cdf(targetIQ, expected, __STANDARD_DEV__)

	## if we're restricting ourselves to male heirs
	if genders == 1:
		prob = 0.5 + 0.5 * prob

	else:
		if genders != 2:
			print("Warning: invalid gender count. Default of 1 used.")
	return (1 - (prob)**numberOfKids)

## include data on population
def popCalc(counterpartyIQ, targetIQ=150, genders=1):
	print("Counterparty Rarity:", 1 - norm.cdf(counterpartyIQ, __POPULATION_MEAN_IQ__, __STANDARD_DEV__))

	for numKids in range(1, 6):
		print("Success Probability,", numKids, 'kid(s):', calc(counterpartyIQ, numKids, targetIQ, genders))

def printCalc(counterpartyIQ, numberOfKids, targetIQ=150, genders=1):
	return str(round(calc(counterpartyIQ, numberOfKids, targetIQ) * 100, 1)) + '%'

def plotCalc():
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	# Make data.
	for numKids in range(1, 6):

		X = np.arange(100, 180, 0.25)
		Y = np.arange(100, 180, 0.25)
		X, Y = np.meshgrid(X, Y)

		def f(x, y):
			return calc(
				counterpartyIQ=x, 
				numberOfKids=numKids, 
				targetIQ=y, 
				genders=2
			)

		g = np.vectorize(f)
		Z = g(X, Y)

		# Plot the surface.
		surf = ax.plot_surface(X, Y, Z, cmap=__COLORMAPS__[numKids - 1],
		                       linewidth=0, antialiased=False)

		# Customize the z axis.
	ax.set_zlim(0, 1.00)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.03f'))

	# Add a color bar which maps values to colors.
	plt.xlabel('Counterparty IQ')
	plt.ylabel('Target IQ')
	plt.title('Attainment probability planes for 1, 2, 3, 4, 5 kids')

	fig.colorbar(surf, shrink=0.5, aspect=5)

	plt.show()

def plotNumKids():
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	# Make data.
	for targetIQ in range(145, 180, 100):

		X = np.arange(100, 180, 0.25)
		Y = np.arange(0, 10, 1 / 32)

		X, Y = np.meshgrid(X, Y)

		def f(x, y):
			return calc(
				counterpartyIQ=x, 
				numberOfKids=y, 
				targetIQ=targetIQ, 
				genders=2
			)

		g = np.vectorize(f)
		Z = g(X, Y)

		# Plot the surface.
		surf = ax.plot_surface(X, Y, Z, cmap=__COLORMAPS__[1],
		                       linewidth=0, antialiased=False)

		# Customize the z axis.
	ax.set_zlim(0, 1.00)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.03f'))

	# Add a color bar which maps values to colors.
	plt.xlabel('Given Counterparty IQ')
	plt.ylabel('Child Count')
	plt.title('Attainment probability plane for IQ 145')

	fig.colorbar(surf, shrink=0.5, aspect=5)

	plt.show()

def plotWithRarity():
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	# Make data.
	for targetIQ in range(145, 180, 100):

		X = np.arange(70, 180, 0.25)
		Y = np.arange(0, 10, 10 / len(X))

		X, Y = np.meshgrid(X, Y)

		
		def f(x, y):
			counterpartyRarity = (1 - norm.cdf(x , __POPULATION_MEAN_IQ__, __STANDARD_DEV__))
			childCountRarity = (1 - norm.cdf(y, __MEAN_KIDS_PER_FAMILY__, __STD_DEV_KPF__))
			rarityModifier = counterpartyRarity * childCountRarity + 0.06

			return rarityModifier * calc(
				counterpartyIQ=x, 
				numberOfKids=y, 
				targetIQ=targetIQ, 
				genders=2
			) 

		g = np.vectorize(f)
		Z = g(X, Y)

		# Plot the surface.
		surf = ax.plot_surface(X, Y, Z, cmap=__COLORMAPS__[1],
		                       linewidth=0, antialiased=False)

		# Customize the z axis.
	# ax.set_zlim(0, 1.00)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.03f'))

	# Add a color bar which maps values to colors.
	plt.xlabel('Targeted Counterparty IQ')
	plt.ylabel('Targeted Child Count')
	plt.title('Attainment probability plane for IQ 145')

	fig.colorbar(surf, shrink=0.5, aspect=5)

	plt.show()



def main():
	# plotCalc()
	# plotNumKids()
	plotWithRarity()

if __name__=="__main__":
	print(main())