import combatpokemonmembers



@with_tag('IsPokemon')
@Components(*combatpokemonmembers.importall())
class CombatPokemon(ClientAreaEntity):
	""" 召唤兽的战斗单位形态，是召唤兽在其他客户端的表现
	"""
	Property('pokeid')
	Property('pid')
	Property("no")
	Property('star')
	Property("ownerid")
	Property("ownerName")

	@property
	def owner(self):
		return EntityManager.getentity(self.ownerid)