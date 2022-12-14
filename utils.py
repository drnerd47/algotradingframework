import definitions as defs


def BuyMarginCalculator(trades, symbol):
  if symbol == defs.BN :
    margin = trades.EnterPrice * defs.BNLOTSIZE
  elif symbol == defs.N :
    margin = trades.EnterPrice * defs.NLOTSIZE
  return (margin.max(), margin.mean(), margin.min())