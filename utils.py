import definitions as defs


def BuyMarginCalculator(trades, symbol):
  if symbol == defs.BN :
    margin = trades.EnterPrice * defs.BNLOTSIZE
  elif symbol == defs.N :
    margin = trades.EnterPrice * defs.NLOTSIZE
  return (margin.max(), margin.mean(), margin.min())

def SellMarginCalculator(positiontype, numcalllegs, numputlegs, symbol):
  if (positiontype == "Naked"):
    if (symbol == defs.BN):
      singlecost = 150000
      doublecost = 180000
    elif (symbol == defs.N):
      singlecost = 125000
      doublecost = 110000
  elif (positiontype == "Hedged"):
    if (symbol == defs.BN):
      singlecost = 45000
      doublecost = 70000
    elif (symbol == defs.N):
      singlecost = 30000
      doublecost = 60000
  return min(numcalllegs, numputlegs)*doublecost + (max(numcalllegs, numputlegs) - min(numcalllegs, numputlegs))*singlecost
