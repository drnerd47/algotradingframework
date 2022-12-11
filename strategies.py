import atomic as atom
import definitions as defs
import directional as direc
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
        #print("SL Hit, Entering the exit and reentry loop")
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
      atom.ExitPosition(positions, currentcandle, defs.SQUAREOFFEOD)
      trades = atom.GetFinalTrades(positions)
      positions = []
  return (trades, positions)


def DirectionalStrategy(data, masterdf, generalconfig, positionconfig, TIconfig, start_date):
  spotdata = data[data.index.date == start_date]
  placedBull = False
  placedBear = False
  positions = []
  trades = []
  for s in range(len(spotdata)): 
    currentcandle = spotdata.iloc[s]
    (bullentry, bearentry) = direc.CheckEntryCondition(currentcandle, TIconfig)
    # Check Enter Condition
    if bullentry and not placedBull:
      (positions, positionsNotPlaced) = direc.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, "close", defs.BULL)
      placedBull = True
    if bearentry and not placedBear:
      (positions, positionsNotPlaced) = direc.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, "close", defs.BEAR)
      placedBear = True
    if placedBull or placedBear:
      # Check Stop Loss Condition
      if (generalconfig["StopLoss"]):
        if (generalconfig["StopLossCond"] == "TIBased"):
          postoExitSL = direc.CheckStopLossTI(positions, currentcandle, TIconfig)
        elif (generalconfig["StopLossCond"] == "PremiumBased"):
          (postoExitSL, posConfigtoExitSL) = atom.CheckStopLoss(positions, currentcandle)
        # We enter this loop if there is any position where stop-loss is triggered.
        if (len(postoExitSL) > 0):
          direc.ExitPosition(postoExitSL, currentcandle, defs.SL)

      # Check Target Profit Condition
      if (generalconfig["Target"]):
        if (generalconfig["TargetCond"] == "TIBased"):
          postoExitTarget = direc.CheckTargetConditionTI(positions, currentcandle, TIconfig)
        elif (generalconfig["TargetCond"] == "PremiumBased"):
          (postoExitTarget, posConfigtoExitTG) = atom.CheckTargetCondition(positions, currentcandle)
        # We enter this loop if there is any position where target profit condition is satisfied.
        if (len(postoExitTarget) > 0):
          direc.ExitPosition(postoExitTarget, currentcandle, defs.TARGET)

      # Square off Remaining Legs EOD
      if (currentcandle.name.time() == generalconfig["ExitTime"]):
        atom.ExitPosition(positions, currentcandle, defs.SQUAREOFFEOD)
        trades = atom.GetFinalTrades(positions)
  return trades