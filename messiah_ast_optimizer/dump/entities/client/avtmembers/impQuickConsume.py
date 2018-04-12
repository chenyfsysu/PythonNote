MILITARY_PRICE = frozenset([5113, ])
REFINE_ITEM_MAP = {
	5111: 22904,
	5112: 22905,
	5113: 22906,
}


class AvatarMember(object):
	'''
	快捷元宝操作，只在客户端进行即可，避免直接调用服务端接口出现漏洞
	在客户端集成一些操作，目的只是为了简化大R操作，可以认为是帮他手点，这样较为安全
	'''
	def __init_component__(self, bdict):
		self.quickConsumeCallback = None
		self.quickConsumeIndex = 1
		self.inquirePriceMoneyCb = {}
		self._isQuickConsuming = False
		self.setQuickConsumingTimer = None
		self.moneyItemPriceExpired = {}

	@property
	def isQuickConsuming(self):
		return self._isQuickConsuming

	@isQuickConsuming.setter
	def isQuickConsuming(self, v):
		if self.setQuickConsumingTimer:
			self.cancel_timer(self.setQuickConsumingTimer)
			self.setQuickConsumingTimer = None

		self._isQuickConsuming = v
		if v:
			# 增加定时器，防止出现该变量一直是True，导致快捷元宝功能无法使用
			self.setQuickConsumingTimer = self.add_timer(2, self.resetQuickConsuming)

	def resetQuickConsuming(self):
		self.setQuickConsumingTimer = None
		self.isQuickConsuming = False

	def queryQuickConsumeGold(self, cost, callback):
		if not self.isQuickConsuming:
			self.tryQueryGoldPrice(0, cost, callback)

	@limit_call(0.5)
	def goldConsumeCheck(self, cost, checkCallback=None, costCallback=None, callback=None, msg=''):
		def okCallback():
			checkCallback()
			self.tryQuickConsume(cost, costCallback, callback)

		if not self.canQuickConsume(cost):
			MessageBox().show(
				msg,
				{'name': '取消', 'countdown': 20},
				{'name': '确定', 'callback': lambda: okCallback()}
			)
			return False

		return True

	@limit_call(0.5)
	def tryQuickConsume(self, cost, costGoldCallback=None, consumeCallback=None):
		if self.canQuickConsume(cost):
			consumeCallback and consumeCallback()
			return

		if self.isQuickConsuming:
			return

		self.quickConsumeIndex += 1
		self.quickConsumeCallback = consumeCallback
		self.tryQueryGoldPrice(self.quickConsumeIndex, cost, costGoldCallback)
		# self.canBuyGoldMallItem(itemId, count)

	def tryQueryGoldPrice(self, index, cost, costGoldCallback):
		lack = dict()
		if self.money < cost.get('money', 0):
			lack['money'] = int(math.ceil(float(cost.get('money', 0) - self.money) / const.EXCHANGE_GOLD_MONEY))

		if self.military < cost.get('military', 0):
			lack['military'] = int(math.ceil(float(cost.get('military', 0) - self.money) / const.EXCHANGE_GOLD_MILITARY))

		# 金币商城价格浮动、元宝商城
		items = cost.get('items', {})
		if items:
			lack['items'] = {}
		moneyItems = {}
		for itemId, count in items.iteritems():
			if self.gameItems.getItemCountByItemId(itemId) >= count:
				continue
			n = count - self.gameItems.getItemCountByItemId(itemId)
			ways = map(lambda w: w[0], WTOID.data.get(itemId, {}).get("ways", ()))
			ways = filter(lambda w: w in (WayType.MONEY_MALL, WayType.GOLD_MALL), ways)
			# assert len(ways), "没有商城购买方式 %d" % itemId
			if not ways:
				print itemId, ways
				return costGoldCallback({})

			# 优先元宝商城
			if WayType.GOLD_MALL in ways:
				info = GoldMallCommon.getItemInfoByItemId(itemId)
				if info is None:
					return costGoldCallback({})
				lack['items'][itemId] = info['price'] * n
			else:
				moneyItems[itemId] = n

		if moneyItems:
			self.inquirePrice(MALL_ITEM_CONST.MALL_TYPE_MONEY, moneyItems.keys())
			self.inquirePriceMoneyCb[self.inquirePriceMoney] = (index, cost, lack, moneyItems, costGoldCallback)
		else:
			self.inquirePriceMoney(index, cost, lack, {}, costGoldCallback)

	def inquirePriceMoney(self, index, cost, lack, moneyItems, costGoldCallback=None):
		for itemId, count in moneyItems.iteritems():
			# 这是军资价格，比较特殊
			if itemId in MILITARY_PRICE:
				lack['items'][itemId] = int(math.ceil(float(count * self.tradeInfoMoney.getTradeItem(itemId).price) / const.EXCHANGE_GOLD_MILITARY))
			else:
				lack['items'][itemId] = int(math.ceil(float(count * self.tradeInfoMoney.getTradeItem(itemId).price) / const.EXCHANGE_GOLD_MONEY))

		if not lack.get('items', {}):
			lack.pop('items', None)
		totalGold = sum(map(lambda s: isinstance(s, dict) and sum(s.values()) or s, lack.itervalues()))

		# 查询价格回调
		costGoldCallback and costGoldCallback(lack)

		if self.gameItems.getContainerById(GAMEITEM_CONST.TEMP_BAG_ID):
			PopmsgPool().AddMsg("您的包裹已满，请将临时包裹中物品取出后再试")
			return

		if index != self.quickConsumeIndex:
			return

		# 如果没有消费回调，那仅仅是查询价格
		if not self.quickConsumeCallback:
			return

		if not self.isEnoughGold(totalGold, showRecharge=True):
			return

		self.setQuickConsumeStatus(False)

		moneyGold = lack.get('money', 0) + sum([lack['items'][itemId] for itemId in moneyItems if itemId not in MILITARY_PRICE])
		if moneyGold:
			self.exchangeGoldMoney(moneyGold)
		militaryGold = lack.get('military', 0) + sum([lack['items'][itemId] for itemId in moneyItems if itemId in MILITARY_PRICE])
		if militaryGold:
			self.exchangeGoldMilitary(militaryGold)

		items = cost.get('items', {})
		goldItems = {}
		moneyItems = {}
		for itemId, count in items.iteritems():
			if self.gameItems.getItemCountByItemId(itemId) >= count:
				continue
			n = count - self.gameItems.getItemCountByItemId(itemId)
			ways = map(lambda w: w[0], WTOID.data.get(itemId, {}).get("ways", ()))
			ways = filter(lambda w: w in (WayType.MONEY_MALL, WayType.GOLD_MALL), ways)

			# 优先元宝商城
			if WayType.GOLD_MALL in ways:
				info = GoldMallCommon.getItemInfoByItemId(itemId)
				goldItems[info['itemno']] = n
			else:
				moneyItems[itemId] = n

		goldItems and self.server.quickBuyGoldMallItem(goldItems)
		moneyItems and self.server.quickPlayerBuy(MALL_ITEM_CONST.MALL_TYPE_MONEY, moneyItems)

		self.add_timer(0, functools.partial(self.tickQuickConsume, index, cost))

	def tickQuickConsume(self, index, cost):
		if index != self.quickConsumeIndex:
			return
		if not hasattr(self, 'startQuickConsume'):
			self.startQuickConsume = time.time()

		if self.canQuickConsume(cost):
			del self.startQuickConsume
			self.setQuickConsumeStatus(True)
			self.quickConsumeCallback and self.quickConsumeCallback()
			self.quickConsumeCallback = None
			return

		if time.time() - self.startQuickConsume > 1:
			del self.startQuickConsume
			self.setQuickConsumeStatus(True)
			lacks = {REFINE_ITEM_MAP.get(itemId, itemId): count - self.gameItems.getItemCountByItemId(itemId) for itemId, count in cost.get('items', {}).iteritems() if self.gameItems.getItemCountByItemId(itemId) < count}
			if lacks:
				itemId = lacks.keys()[0]
				ways = map(lambda w: w[0], WTOID.data.get(itemId, {}).get("ways", ()))
				ways = filter(lambda w: w in (WayType.MONEY_MALL, WayType.GOLD_MALL), ways)
				if WayType.GOLD_MALL in ways:
					info = GoldMallCommon.getItemInfoByItemId(itemId)
					canbuy, reason = self.canBuyGoldMallItem(info['itemno'], lacks[itemId])
					if not canbuy:
						PopmsgPool().AddMsg("购买#G%s#W失败, %s" % (item_data.data.get(itemId, {}).get('Name', ''), reason))
				else:
					if self.getMaxBuycount(itemId) < lacks[itemId]:
						PopmsgPool().AddMsg("操作失败, #G%s#W剩余可购数量不足" % item_data.data.get(itemId, {}).get('Name', ''))
					else:
						PopmsgPool().AddMsg("操作失败")

			return

		self.add_timer(0, functools.partial(self.tickQuickConsume, index, cost))

	def canQuickConsume(self, cost):
		if self.money < cost.get('money', 0):
			return False

		if self.military < cost.get('military', 0):
			return False

		for itemId, count in cost.get('items', {}).iteritems():
			if self.gameItems.getItemCountByItemId(itemId) < count:
				return False
		return True

	def setQuickConsumeStatus(self, v):
		PopmsgPool().setEnable(v)
		ItemMeteor.setEnable(v)
		self.isQuickConsuming = not v

	def checkCostMilitaryMall(self, items=None, callback=None):
		if not items:
			callback and callback()
			return

		lack = {}
		for itemId, count in items.iteritems():
			if self.gameItems.getItemCountByItemId(itemId) >= count:
				continue
			n = count - self.gameItems.getItemCountByItemId(itemId)
			ways = [w[0] for w in WTOID.data.get(itemId, {}).get("ways", ()) if w[0] == WayType.MILITARY_MALL]
			if ways:
				lack[itemId] = n

		if lack:
			itemNo = lack.keys()[0]
			MessageBox().show(
				"您缺少#G%s#W，是否前往购买？" % item_data.data.get(itemNo, {}).get('Name', ''),
				{'name': '取消', 'countdown': 10, },
				{'name': '确定', 'callback': lambda: MallMain().showMilitary().buyItem(itemNo, -1)},
			)
			return

		callback and callback()

	# 快捷金币炼化
	@limit_call(0.1)
	def quickRfineUseMoney(self, cost, queryCallback=None, consumeCallback=None):
		print cost, queryCallback, consumeCallback, self.isQuickConsuming
		if consumeCallback and self.canQuickConsume(cost):
			consumeCallback()
			return
		moneyItems = {}
		for itemId, count in cost['items'].iteritems():
			if self.gameItems.getItemCountByItemId(itemId) >= count:
				continue
			n = count - self.gameItems.getItemCountByItemId(itemId)
			ways = map(lambda w: w[0], WTOID.data.get(REFINE_ITEM_MAP.get(itemId, itemId), {}).get("ways", ()))
			ways = filter(lambda w: w in (WayType.MONEY_MALL, ), ways)
			if not ways:
				queryCallback and queryCallback()
				consumeCallback and consumeCallback()
				return

			moneyItems[REFINE_ITEM_MAP.get(itemId, itemId)] = n

		if self.isQuickConsuming:
			return
		self.quickConsumeIndex += 1
		self.quickConsumeCallback = consumeCallback
		querys = [itemId for itemId in moneyItems.keys() if time.time() > self.moneyItemPriceExpired.get(itemId, 0)]
		if querys:
			self.inquirePrice(MALL_ITEM_CONST.MALL_TYPE_MONEY, querys)
			self.inquirePriceMoneyCb[self.inquireRefineMoney] = (self.quickConsumeIndex, cost, moneyItems, queryCallback, querys)
		else:
			self.inquireRefineMoney(self.quickConsumeIndex, cost, moneyItems, queryCallback, querys)

	def inquireRefineMoney(self, index, cost, moneyItems, queryCallback, querys):
		for itemId in querys:
			self.moneyItemPriceExpired[itemId] = time.time() + 5
		total = 0
		for itemId, count in moneyItems.iteritems():
			total += count * self.tradeInfoMoney.getTradeItem(itemId).price
		if queryCallback:
			queryCallback(total + cost.get('money'))

		if index != self.quickConsumeIndex:
			return
		if self.quickConsumeCallback:
			def doQuickBuy():
				moneyItems and self.server.quickPlayerBuy(MALL_ITEM_CONST.MALL_TYPE_MONEY, moneyItems)
				self.add_timer(0, functools.partial(self.tickQuickConsume, index, cost))
			if self.money < total + cost.get('money'):
				ExchangeMain().showMoneyConfirmPlane(total + cost.get('money') - self.money, doQuickBuy)
				return
			doQuickBuy()
