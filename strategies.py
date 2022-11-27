import atomic as atom
import definitions as defs
import time

def IntraDayStrategy(masterdf, generalconfig, positionconfig):
  spotdata = atom.GetSpotData(masterdf,generalconfig["symbol"])
  placed = False
  needsExit = False
  positions = []
  trades = []
  for s in range(len(spotdata)):
    currentcandle = spotdata.iloc[s]
    if currentcandle.name.time() == generalconfig["EnterTime"] and not placed:
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
          if (generalconfig["SquareOffSL"] == defs.EXITLEG):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, postoExitSL, currentcandle)
          elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)

      postoExitTarget = atom.CheckTargetCondition(positions, currentcandle)
      if (len(postoExitTarget) > 0):
        atom.ExitPosition(postoExitTarget, currentcandle, defs.TARGET)
        if (generalconfig["SquareOffTG"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)
        if (generalconfig["ReEntrySL"] == defs.YES):
          if (generalconfig["SquareOffSL"] == defs.EXITLEG):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, postoExitTarget, currentcandle)
          elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
            atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)

      # Square off Remaining Legs EOD
      if (currentcandle.name.time() == generalconfig["ExitTime"]) or (needsExit == True):
          exit = atom.ExitPosition(positions, currentcandle, defs.SQUAREOFFEOD)
          if (exit == False):
            needsExit = True
          else:
            trades = atom.GetFinalTrades(positions)
            print(trades)
  return trades

def MultidayStrategy(masterdf, generalconfig, positionconfig):
  spotdata = atom.GetSpotData(masterdf,generalconfig["symbol"])
  placed = False
  positions = []
  trades = []
  for s in range(len(spotdata)):
    currentcandle = spotdata.iloc[s]
    if currentcandle.name.time() == generalconfig["EnterTime"] and not placed:
      positions = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)
      placed = True
    if placed:
      if (generalconfig["SL"] == defs.YES):
        postoExitSL = atom.CheckStopLoss(masterdf, positions, currentcandle)
        if (len(postoExitSL) > 0):
          atom.ExitPosition(masterdf, postoExitSL, currentcandle, defs.SL)
          if (generalconfig["SquareOffSL"] == defs.ALLLEGS):
            atom.ExitPosition(masterdf, positions, currentcandle, defs.SQUAREOFF)
          if (generalconfig["ReEntrySL"] == defs.YES):
            if (generalconfig["SquareOffSL"] == defs.EXITLEG):
              atom.EnterPosition(generalconfig, positionconfig, masterdf, postoExitSL, currentcandle)
            elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
              atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)

      if (generalconfig["Target"] == defs.YES):
        postoExitTarget = atom.CheckTargetCondition(masterdf, positions, currentcandle)
        if (len(postoExitTarget) > 0):
          atom.ExitPosition(masterdf, postoExitTarget, currentcandle, defs.TARGET)
          if (generalconfig["SquareOffTG"] == defs.ALLLEGS):
            atom.ExitPosition(masterdf, positions, currentcandle, defs.SQUAREOFF)
          if (generalconfig["ReEntrySL"] == defs.YES):
            if (generalconfig["SquareOffSL"] == defs.EXITLEG):
              atom.EnterPosition(generalconfig, positionconfig, masterdf, postoExitTarget, currentcandle)
            elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
              atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle)

      # Square off Remaining Legs EOD
      if currentcandle.name.time() == generalconfig["ExitTime"]:
          atom.ExitPosition(masterdf, positions, currentcandle, defs.SQUAREOFF)
          trades = atom.GetFinalTrades(positions)
  return trades



  
