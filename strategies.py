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
    # Check Enter time Condition
    if currentcandle.name.time() == generalconfig["EnterTime"] and not placed:
      (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, "open")
      placed = True
    if placed:
      # Check time based re-entry. If true, re-enter every "ReEnterEvery" number of minutes.
      if (generalconfig["Timerenter"] == defs.YES):
        if (MinCounter % generalconfig["ReEnterEvery"] == 0):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, "open")
      # Check Stop Loss Condition
      (postoExitSL, posConfigtoExitSL) = atom.CheckStopLoss(positions, currentcandle)

      # We enter the loop below if re-entry is true and stop loss was triggered the previous minute.
      if (generalconfig["ReEntrySL"] == defs.YES) and (ReEnterCounterSL <= generalconfig["MaxReEnterCounterSL"]) and (ReEnterNextSL):
        ReEnterNextSL = False
        ReEnterCounterSL += 1
        if (generalconfig["SquareOffSL"] == defs.ONELEG):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, posConfigtoExitSLNext, masterdf, positions,
                                                               currentcandle, "open")
        elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, "open")
      # We enter this loop if there is any position where stop-loss is triggered.
      if (len(postoExitSL) > 0):
        ReEnterNextSL = True
        posConfigtoExitSLNext = posConfigtoExitSL
        atom.ExitPosition(postoExitSL, currentcandle, defs.SL)
        if (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)

      # Check Target Profit Condition
      (postoExitTarget, posConfigtoExitTG) = atom.CheckTargetCondition(positions, currentcandle)

      # We enter the loop below if re-entry is true and target profit condition was triggered the previous minute.
      if (generalconfig["ReEntryTG"] == defs.YES) and (ReEnterCounterTG <= generalconfig["MaxReEnterCounterTG"]) and (ReEnterNextTG):
        ReEnterCounterTG += 1
        if (generalconfig["SquareOffSL"] == defs.ONELEG):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, posConfigtoExitTGNext, masterdf, positions,
                                                               currentcandle, "open")
        elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, "open")

      # We enter this loop if there is any position where target profit condition is satisfied.
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
  return trades

def MultiDayStrategy(masterdf, positions, generalconfig, positionconfig):
  spotdata = atom.GetSpotData(masterdf,generalconfig["symbol"])
  trades = []
  MinCounter = 0
  ReEnterCounterSL = 0
  ReEnterCounterTG = 0
  ReEnterNextSL = False
  ReEnterNextTG = False
  # Check if there is any position where there is a "SL" or "Target" Condition. If not, there is no need to
  # loop and check stop loss/target conditions.
  loop = False
  for posc in positionconfig:
    if (posc["SL"] == defs.YES) or (posc["Target"] == defs.YES):
      loop = True

  # Update the opdata in the positions for the active positions still open!
  atom.UpdatePosition(masterdf, positions)
  for s in range(len(spotdata)):
    MinCounter += 1
    currentcandle = spotdata.iloc[s]
    # Check Enter time and Enter Day Condition
    if currentcandle.name.time() == generalconfig["EnterTime"] and currentcandle.name.weekday() in generalconfig['EnterDay']:
      (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, "open")

    if loop:
      # Check Stop Loss Condition
      (postoExitSL, posConfigtoExitSL) = atom.CheckStopLoss(positions, currentcandle)

      # We enter the loop below if re-entry is true and stop loss was triggered the previous minute.
      if (generalconfig["ReEntrySL"] == defs.YES) and (ReEnterCounterSL <= generalconfig["MaxReEnterCounterSL"]) and (ReEnterNextSL):
        ReEnterNextSL = False
        ReEnterCounterSL += 1
        if (generalconfig["SquareOffSL"] == defs.ONELEG):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, posConfigtoExitSLNext, masterdf, positions,
                                                               currentcandle, "open")
        elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, "open")
      # We enter this loop if there is any position where stop-loss is triggered.
      if (len(postoExitSL) > 0):
        print("SL Hit, Entering the exit and reentry loop")
        ReEnterNextSL = True
        posConfigtoExitSLNext = posConfigtoExitSL
        atom.ExitPosition(postoExitSL, currentcandle, defs.SL)
        if (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)

      # Check Target Profit Condition
      (postoExitTarget, posConfigtoExitTG) = atom.CheckTargetCondition(positions, currentcandle)

      # We enter the loop below if re-entry is true and target profit condition was triggered the previous minute.
      if (generalconfig["ReEntryTG"] == defs.YES) and (ReEnterCounterTG <= generalconfig["MaxReEnterCounterTG"]) and (ReEnterNextTG):
        ReEnterCounterTG += 1
        if (generalconfig["SquareOffSL"] == defs.ONELEG):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, posConfigtoExitTGNext, masterdf, positions,
                                                               currentcandle, "open")
        elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, "open")

      # We enter this loop if there is any position where target profit condition is satisfied.
      if (len(postoExitTarget) > 0):
        ReEnterNextTG = True
        posConfigtoExitTGNext = posConfigtoExitTG
        atom.ExitPosition(postoExitTarget, currentcandle, defs.TARGET)
        if (generalconfig["SquareOffTG"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF)

    # Square off Remaining Legs EOD
    if (currentcandle.name.time() == generalconfig['ExitTime']) and (currentcandle.name.weekday() in generalconfig["ExitDay"]):
      print("Entered exit day!")
      atom.ExitPosition(positions, currentcandle, defs.SQUAREOFFEOD)
      trades = atom.GetFinalTrades(positions)
      positions = []
      print(trades)
  return (trades, positions)


  
