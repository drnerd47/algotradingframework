import atomic as atom
import definitions as defs
import time

def IntraDayStrategy(masterdf, generalconfig, positionconfig):
  spotdata = atom.GetSpotData(masterdf,generalconfig["symbol"])
  placed = False
  needsExit = False
  positions = []
  trades = []
  MinCounter = 0
  ReEnterCounterSL = 0
  ReEnterCounterTG = 0
  for s in range(len(spotdata)):
    MinCounter += 1
    currentcandle = spotdata.iloc[s]
    if currentcandle.name.time() == generalconfig["EnterTime"] and not placed:
      (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)
      placed = True
    if placed:
      if (generalconfig["Timerenter"] == defs.YES):
        if (MinCounter % generalconfig["ReEnterEvery"] == 0):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle)
      postoExitSL = atom.CheckStopLoss(positions, currentcandle)
      if (len(postoExitSL) > 0):
        atom.ExitPosition(postoExitSL, currentcandle, defs.SL)
        if (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)
        if (generalconfig["ReEntrySL"] == defs.YES) and (ReEnterCounterSL <= generalconfig["MaxReEnterCounterSL"]):
          ReEnterCounterSL += 1
          if (generalconfig["SquareOffSL"] == defs.ONELEG):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, postoExitSL, currentcandle)
          elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)

      postoExitTarget = atom.CheckTargetCondition(positions, currentcandle)
      if (len(postoExitTarget) > 0):
        atom.ExitPosition(postoExitTarget, currentcandle, defs.TARGET)
        if (generalconfig["SquareOffTG"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)
        if (generalconfig["ReEntryTG"] == defs.YES) and (ReEnterCounterTG <= generalconfig["MaxReEnterCounterTG"]):
          ReEnterCounterTG += 1
          if (generalconfig["SquareOffSL"] == defs.ONELEG):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, postoExitTarget, currentcandle)
          elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)

      # Square off Remaining Legs EOD
      if (currentcandle.name.time() == generalconfig["ExitTime"]):
        atom.ExitPosition(positions, currentcandle, defs.SQUAREOFFEOD)
        trades = atom.GetFinalTrades(positions)
        print(trades)
  return trades

def MultidayStrategy(masterdf, generalconfig, positionconfig):
  spotdata = atom.GetSpotData(masterdf,generalconfig["symbol"])
  placed = False
  needsExit = False
  positions = []
  trades = []
  for s in range(len(spotdata)):
    currentcandle = spotdata.iloc[s]
  
    if (currentcandle.name.weekday() == generalconfig['EnterDay'] and currentcandle.name.time() == generalconfig["EnterTime"]) and not placed:
      if generalconfig["debug"] == defs.DEBUGTIME:
        tic = time.perf_counter()
        (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)
      if generalconfig["debug"] == defs.DEBUGTIME:
        toc = time.perf_counter()
        print(f"Time taken by EnterPosition is {toc - tic:0.4f} seconds")
      placed = True
    if placed:
      postoExitSL = atom.CheckStopLoss(positions, currentcandle)
      if (len(postoExitSL) > 0):
        atom.ExitPosition(postoExitSL, currentcandle, defs.SL)
        if (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)
        if (generalconfig["ReEntrySL"] == defs.YES):
          if (generalconfig["SquareOffSL"] == defs.ONELEG):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, postoExitSL, currentcandle)
          elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)

      postoExitTarget = atom.CheckTargetCondition(positions, currentcandle)
      if (len(postoExitTarget) > 0):
        atom.ExitPosition(postoExitTarget, currentcandle, defs.TARGET)
        if (generalconfig["SquareOffTG"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)
        if (generalconfig["ReEntrySL"] == defs.YES):
          if (generalconfig["SquareOffSL"] == defs.ONELEG):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, postoExitTarget, currentcandle)
          elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)

      # Square off Remaining Legs at Exit day
            
      if (currentcandle.name.weekday() == generalconfig['ExitDay'] and currentcandle.name.time() == generalconfig["ExitTime"]):
        atom.ExitPosition(positions, currentcandle, defs.SQUAREOFFEOD)
        trades = atom.GetFinalTrades(positions)
        print(trades)
  return trades


# def MultidayStrategy(masterdf, generalconfig, positionconfig):
#   spotdata = atom.GetSpotData(masterdf,generalconfig["symbol"])
#   placed = False
#   positions = []
#   trades = []
#   for s in range(len(spotdata)):
#     currentcandle = spotdata.iloc[s]
#     #currentcandle.name.weekday() == generalconfig['EnterDay']:
#     if currentcandle.name.weekday() == generalconfig['EnterDay'] and currentcandle.name.time() == generalconfig["EnterTime"] and not placed:
#       (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)
#       placed = True
#     if placed:
#       if (generalconfig["SL"] == defs.YES):
#         postoExitSL = atom.CheckStopLoss(positions, currentcandle)
#         if (len(postoExitSL) > 0):
#           atom.ExitPosition(postoExitSL, currentcandle, defs.SL)
#           if (generalconfig["SquareOffSL"] == defs.ALLLEGS):
#             atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)
#           if (generalconfig["ReEntrySL"] == defs.YES):
#             if (generalconfig["SquareOffSL"] == defs.ONELEG):
#               atom.EnterPosition(generalconfig, positionconfig, masterdf, postoExitSL, currentcandle)
#             elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
#               atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)

#       if (generalconfig["Target"] == defs.YES):
#         postoExitTarget = atom.CheckTargetCondition(positions, currentcandle)
#         if (len(postoExitTarget) > 0):
#           atom.ExitPosition(postoExitTarget, currentcandle, defs.TARGET)
#           if (generalconfig["SquareOffTG"] == defs.ALLLEGS):
#             atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)
#           if (generalconfig["ReEntrySL"] == defs.YES):
#             if (generalconfig["SquareOffSL"] == defs.ONELEG):
#               atom.EnterPosition(generalconfig, positionconfig, masterdf, postoExitTarget, currentcandle)
#             elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
#               atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)

#       # Square off Remaining Legs EOD
#       if currentcandle.name.weekday() == generalconfig['ExitDay']:
#         if currentcandle.name.time() == generalconfig["ExitTime"]:
#             atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)
#             trades = atom.GetFinalTrades(positions)
#   return trades



  
