import atomic as atom
import definitions as defs
import time

def IntraDayStrategy(masterdf, generalconfig, positionconfig):
  spotdata = atom.GetSpotData(masterdf,generalconfig["symbol"])
  placed = False
  positions = []
  trades = []
  MinCounter = 0
  ReEnterCounterSL = 0
  ReEnterCounterTG = 0
  ReEnterNextSL = False
  ReEnterNextTG = False
  for s in range(len(spotdata)):
    MinCounter += 1
    currentcandle = spotdata.iloc[s]
    if currentcandle.name.time() == generalconfig["EnterTime"] and not placed:
      (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, "open")
      placed = True
    if placed:
      if (generalconfig["Timerenter"] == defs.YES):
        if (MinCounter % generalconfig["ReEnterEvery"] == 0):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, "open")
      (postoExitSL, posConfigtoExitSL) = atom.CheckStopLoss(positions, currentcandle)
      if (generalconfig["ReEntrySL"] == defs.YES) and (ReEnterCounterSL <= generalconfig["MaxReEnterCounterSL"]) and (ReEnterNextSL):
        ReEnterNextSL = False
        ReEnterCounterSL += 1
        if (generalconfig["SquareOffSL"] == defs.ONELEG):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, posConfigtoExitSLNext, masterdf, positions,
                                                               currentcandle, "open")
        elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, "open")
      if (len(postoExitSL) > 0):
        print("SL Hit, Entering the exit and reentry loop")
        ReEnterNextSL = True
        posConfigtoExitSLNext = posConfigtoExitSL
        atom.ExitPosition(postoExitSL, currentcandle, defs.SL)
        if (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)

      (postoExitTarget, posConfigtoExitTG) = atom.CheckTargetCondition(positions, currentcandle)
      if (generalconfig["ReEntryTG"] == defs.YES) and (ReEnterCounterTG <= generalconfig["MaxReEnterCounterTG"]) and (ReEnterNextTG):
        ReEnterCounterTG += 1
        if (generalconfig["SquareOffSL"] == defs.ONELEG):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, posConfigtoExitTGNext, masterdf, positions,
                                                               currentcandle, "open")
        elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, "open")
      if (len(postoExitTarget) > 0):
        ReEnterNextTG = True
        posConfigtoExitTGNext = posConfigtoExitTG
        atom.ExitPosition(postoExitTarget, currentcandle, defs.TARGET)
        if (generalconfig["SquareOffTG"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)

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



  
