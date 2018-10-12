#coding: utf-8
import numpy as np
import math


#La clase medida aún está en proceso, puede tener errores en las incertidumbres o en 
#algún otro resultado. Si encuentras algún bug comentalo.

class Medida(object):
	
	'''
	La clase Medida permite crear y operar objetos con valor, unidades e incertidumbre,
	automatizando los cálculos. Se pueden usar sobre estos objetos los siguientes
	operadores: +, -, *, /, +=, -=, *=, /=, **, ==, !=, <, >, >=, <= 
	La representación con print tiene la forma: valor ± incertidumbre unidades
	'''

	def __init__(self, value, s, units):
	
		self.value = float(value)
		self.s = float(s)
		self.units = units	
	
	#implementar __repr__
		
	def __str__(self):
		#representación con print
		
		#falta que ajuste las cifras significativas
		return "%f ± %f %s" %(self.value, self.s, self.units)
		
		
	def __neg__(self):
		return Medida(-self.value, self.s, self.units)
		
	def __mul__(self,multiplier):
		#operador *
		
		if isinstance(multiplier, Medida):
			
			#fórmulas para los valores e incertidumbres al multiplicar dos Medidas
			if multiplier.value/self.value == multiplier.s/self.s:
				value = self.value*multiplier.value
				s = abs(2*multiplier.value)
				units = self.units + '^2'
				
			else:	 
				value = self.value*multiplier.value
				s = math.sqrt((self.s*multiplier.value)**2 +\
				 (self.value*multiplier.s)**2)
				units = self.units + '·' + multiplier.units
			
			#u = multiplier.value**2*self.u + self.value**2*multiplier.u
			return Medida(value, s, units)
		
		elif type(multiplier) == int or type(multiplier) == float:
			#si la Medida se multiplica por un número estos son los cálculos
			value = multiplier*self.value
			s = abs(multiplier*self.s)
			units = self.units
			
			return Medida(value, s, units)
		
		else:
			#para cualquier otro tipo se lanza un error
			raise ValueError('Tipo no válido para multiplicar una Medida: %s'\
			 %type(multiplier))
			 
 	def __rmul__(self, multiplier):
	 	#multiplicación por la derecha, sólo se ejecutará si se intenta
	 	#multiplicar por un tipo no válido; es decir x * y donde x no es Medida,
	 	#ya que la función se invoca sobre el primer objeto, x.__mul__(y)
	 	
	 	if type(multiplier) == int or type(multiplier) == float:
	 	
	 		value = multiplier*self.value
			s = abs(multiplier*self.s)
			units = self.units
			
			return Medida(value, s, units)
			
		else:
			#si no se multiplica por un número se lanza un error
			raise ValueError('Tipo no válido para multiplicar una Medida: %s'\
			 %type(multiplier))
			 
	def __imul__(self, multiplier):
	 	#operador *=
	 	return self*multiplier
	 		
   			
	def __add__(self, adder):
		#fórmulas para valores e incertidumbres al sumar dos Medidas
		if isinstance(adder, Medida):
			
			#comprueba que ambas medidas tengan las mismas unidades para poder sumarlas
			if adder.units != self.units:
				raise ValueError('Las unidades deben coincidir para sumar medidas')
				
			if adder.value/self.value == adder.s/self.s:
				s = self.s*math.sqrt(1+ adder.value/self.value)
			else:
				s = math.sqrt(self.s**2 + adder.s**2)
			value = self.value + adder.value
			units = self.units
			#u = self.u + adder.u
			
			return Medida(value, s, units)
		
		else: 
			raise ValueError('Tipo no válido para sumar una Medida: %s'\
			 %type(adder))
			 
	def __iadd__(self, adder):
 		#operador +=
	 	return self + adder
	 	
 	def __sub__(self, substractor):
 		#resta, operador -
 		return self + -substractor
 		
	def __isub__(self, substractor):
		#operador -=
		return self - subtractor
			 
	def __div__(self, divider):
	 	#cálculos del valor y la incertidumbre al dividir una medida por otra
	 	#o por un número, operador / , no usar '//' en ningún caso, no está 
	 	#implementado
	 	if isinstance(divider, Medida):
	 		
	 		if divider.value == 0:
	 			raise ValueError('No se puede dividir por una medida de valor 0')
 			
 			
 			if self.value/divider.value == self.s/divider.s:
 				return self.value/divider.value
 			else:
 				value = self.value/divider.value
 				s = math.sqrt((self.s/divider.value)**2 + \
 				(self.value*divider.s/divider.value**2)**2)
 				units = self.units + '/' + divider.units
 			
 			#u = self.u/divider.value**2 + self.value**2*divider.u/divider.value**2
 			
 			return Medida(value, s, units)
 			
 			
		elif type(divider) == int or type(divider) == float:
			
			value = self.value/divider
			s = self.s/divider
			units = self.units
			
			return Medida(value, s, units)
		
		else: 
			raise ValueError('Tipo no válido para dividir una Medida: %s'\
			 %type(divider))	
			 
	def __rdiv__(self,divider):
	 	
	 	#como __rmul__ pero con división, sirve para dividir un número entre una
	 	#medida
	 	if type(divider) == int or type(divider) == float:
	 		try:
		 		value = divider/self.value
		 		s = divider*self.s/self.value**2
		 		units = '1/' + self.units
		 		
		 		return Medida(value, s, units)
			except ZeroDivisionError:
				pass
				#implementar situación de error
		
		else:
			raise ValueError('Tipo no válido para la operación: %s' %type(divider))
			
	def __idiv__(self, divider):
		#operador /=
		return self/divider
		
	def __pow__(self, power):
		#cálculos para elevar una medida a una potencia, operador **
		if type(power) == int or type(power) == float:
			
			value = self.value**power
			s = abs(power*self.value**(power-1)*self.s)
			units = self.units + '^' + str(power)
			
			return Medida(value, s, units)
	
	#los operadores de orden e igualdad sólo tienen en cuenta el valor de la Medida,
	#no su incertidumbre ni sus unidades
			
	def __eq__(self, other):
		#operador ==
		return self.value == other.value
	
	def __ne__(self, other):
		#operador !=
		return not self == other
		
	def __lt__(self, other):
		#operador <
		return self.value < other.value
		
	def __gt__(self, other):
		#operador >
		return self.value > other.value
		
	def __le__(self, other):
		#operador <=
		return self == other or self < other
	
	def __ge__(self, other):
		#operador >=
		return self == other or self > other
				
	
class Constant(Medida):
	'''
	Inicialización rápida de Medidas de incertidumbre 0
	'''
	def __init__(self, value, units):
		self.value = value
		self.s = 0
		self.untis = units



#--------------------------------
#Por hacer:
#>Implementar representación en cifras significativas
#>Crear sistema de unidades que se puedan operar entre ellas
#>Crear funciones que actuen sobre las medidas, ej.: exponencial, coseno, seno...
#>Implementar calculo vectorial: crear vectores de medidas y hacerlos compatibles 
#con numpy	
