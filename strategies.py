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

  OHLCEnter = 'open'
  exitSLOHLC = 'close'
  exitTGOHLC = 'close'
  exitSQOHLC = 'close'
  exitSQEODOHLC = 'open'

  for s in range(len(spotdata)):
    MinCounter += 1
    currentcandle = spotdata.iloc[s]
    # Check Enter time Condition
    if currentcandle.name.time() == generalconfig["EnterTime"] and not placed:
      (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, OHLCEnter)
      placed = True
    if placed:
      # Check time based re-entry. If true, re-enter every "ReEnterEvery" number of minutes.
      if (generalconfig["Timerenter"] == defs.YES):
        if (MinCounter % generalconfig["ReEnterEvery"] == 0):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, OHLCEnter)
      # Check Stop Loss Condition
      (postoExitSL, posConfigtoExitSL) = atom.CheckStopLoss(positions, currentcandle)

      # We enter the loop below if re-entry is true and stop loss was triggered the previous minute.
      if (generalconfig["ReEntrySL"] == defs.YES) and (ReEnterCounterSL <= generalconfig["MaxReEnterCounterSL"]) and (ReEnterNextSL):
        ReEnterNextSL = False
        ReEnterCounterSL += 1
        if (generalconfig["SquareOffSL"] == defs.ONELEG):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, posConfigtoExitSLNext, masterdf, positions,
                                                               currentcandle, OHLCEnter)
        elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, OHLCEnter)
      # We enter this loop if there is any position where stop-loss is triggered.
      if (len(postoExitSL) > 0):
        ReEnterNextSL = True
        posConfigtoExitSLNext = posConfigtoExitSL
        atom.ExitPosition(postoExitSL, currentcandle, defs.SL, exitSLOHLC)
        if (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF, exitSQOHLC)

      # Check Target Profit Condition
      (postoExitTarget, posConfigtoExitTG) = atom.CheckTargetCondition(positions, currentcandle)

      # We enter the loop below if re-entry is true and target profit condition was triggered the previous minute.
      if (generalconfig["ReEntryTG"] == defs.YES) and (ReEnterCounterTG <= generalconfig["MaxReEnterCounterTG"]) and (ReEnterNextTG):
        ReEnterCounterTG += 1
        if (generalconfig["SquareOffSL"] == defs.ONELEG):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, posConfigtoExitTGNext, masterdf, positions,
                                                               currentcandle, OHLCEnter)
        elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, OHLCEnter)

      # We enter this loop if there is any position where target profit condition is satisfied.
      if (len(postoExitTarget) > 0):
        ReEnterNextTG = True
        posConfigtoExitTGNext = posConfigtoExitTG
        atom.ExitPosition(postoExitTarget, currentcandle, defs.TARGET, exitTGOHLC)
        if (generalconfig["SquareOffTG"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF, exitSQOHLC)

      # Square off Remaining Legs EOD
      if (currentcandle.name.time() == generalconfig["ExitTime"]):
        atom.ExitPosition(positions, currentcandle, defs.SQUAREOFFEOD, exitSQEODOHLC)
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

  OHLCEnter = 'open'
  exitSLOHLC = 'close'
  exitTGOHLC = 'close'
  exitSQOHLC = 'close'
  exitSQEODOHLC = 'open'

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
      (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, OHLCEnter)

    if loop:
      # Check Stop Loss Condition
      (postoExitSL, posConfigtoExitSL) = atom.CheckStopLoss(positions, currentcandle)

      # We enter the loop below if re-entry is true and stop loss was triggered the previous minute.
      if (generalconfig["ReEntrySL"] == defs.YES) and (ReEnterCounterSL <= generalconfig["MaxReEnterCounterSL"]) and (ReEnterNextSL):
        ReEnterNextSL = False
        ReEnterCounterSL += 1
        if (generalconfig["SquareOffSL"] == defs.ONELEG):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, posConfigtoExitSLNext, masterdf, positions,
                                                               currentcandle, OHLCEnter)
        elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, OHLCEnter)
      # We enter this loop if there is any position where stop-loss is triggered.
      if (len(postoExitSL) > 0):
        #print("SL Hit, Entering the exit and reentry loop")
        ReEnterNextSL = True
        posConfigtoExitSLNext = posConfigtoExitSL
        atom.ExitPosition(postoExitSL, currentcandle, defs.SL, exitSLOHLC)
        if (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF, exitSQOHLC)

      # Check Target Profit Condition
      (postoExitTarget, posConfigtoExitTG) = atom.CheckTargetCondition(positions, currentcandle)

      # We enter the loop below if re-entry is true and target profit condition was triggered the previous minute.
      if (generalconfig["ReEntryTG"] == defs.YES) and (ReEnterCounterTG <= generalconfig["MaxReEnterCounterTG"]) and (ReEnterNextTG):
        ReEnterCounterTG += 1
        if (generalconfig["SquareOffSL"] == defs.ONELEG):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, posConfigtoExitTGNext, masterdf, positions,
                                                               currentcandle, OHLCEnter)
        elif (generalconfig["SquareOffSL"] == defs.ALLLEGS):
          (positions, positionsNotPlaced) = atom.EnterPosition(generalconfig, positionconfig, masterdf, positions,
                                                               currentcandle, OHLCEnter)

      # We enter this loop if there is any position where target profit condition is satisfied.
      if (len(postoExitTarget) > 0):
        ReEnterNextTG = True
        posConfigtoExitTGNext = posConfigtoExitTG
        atom.ExitPosition(postoExitTarget, currentcandle, defs.TARGET, exitTGOHLC)
        if (generalconfig["SquareOffTG"] == defs.ALLLEGS):
          atom.ExitPosition(positions, currentcandle, defs.SQUAREOFF, exitSQOHLC)

    # Square off Remaining Legs EOD
    if (currentcandle.name.time() == generalconfig['ExitTime']) and (currentcandle.name.weekday() in generalconfig["ExitDay"]):
      atom.ExitPosition(positions, currentcandle, defs.SQUAREOFFEOD, exitSQEODOHLC)
      trades = atom.GetFinalTrades(positions)
      positions = []
  return (trades, positions)


def DirectionalStrategy(data, masterdf, generalconfig, positionconfig, TIconfig, start_date):
  spotdata = data[data.index.date == start_date]
  spotdatafull = atom.GetSpotData(masterdf, generalconfig["symbol"])
  placedBull = False
  placedBear = False
  exitDone = False
  positions = []
  trades = []
  OHLCEnter = 'open'
  exitSLOHLC = 'open'
  exitTGOHLC = 'open'
  exitSQEODOHLC = 'open'
  for s in range(len(spotdata)): 
    currentcandle = spotdata.iloc[s]
#<<<<<<< Updated upstream
#    if (currentcandle.name in spotdatafull.index):
#      sfull = spotdatafull.index.get_loc(currentcandle.name)
      
#      if (sfull < len(spotdatafull)-1):
#        nextcandle = spotdatafull.iloc[sfull+1]
#      else:
#        nextcandle = currentcandle
#    else:
#      nextcandle = currentcandle

#=======
    if (s < len(spotdata)-1):
      nextcandle = spotdata.iloc[s+1]
    else:
      nextcandle = currentcandle
    #if (currentcandle.name in spotdatafull.index):
    #  sfull = spotdatafull.index.get_loc(currentcandle.name)
    #  if (sfull < len(spotdatafull)-1):
    #    currentcandlenext = spotdatafull.iloc[sfull+1]
    #  else:
    #    currentcandlenext = currentcandle
    #else:
    #  currentcandlenext = currentcandle

    (bullentry, bearentry) = direc.CheckEntryCondition(currentcandle, TIconfig)
  # Check Enter Condition
    if bullentry and not placedBull:
      (positions, positionsNotPlaced) = direc.EnterPosition(generalconfig, positionconfig, masterdf, positions, nextcandle, OHLCEnter, defs.BULL)
      data.loc[currentcandle.name]['Signal'] = defs.ENTERBULLPOSITION
      placedBull = True
    if bearentry and not placedBear:
      (positions, positionsNotPlaced) = direc.EnterPosition(generalconfig, positionconfig, masterdf, positions, nextcandle, OHLCEnter, defs.BEAR)
      data.loc[currentcandle.name]['Signal'] = defs.ENTERBEARPOSITION
      placedBear = True
    if placedBull or placedBear:
      # Check Stop Loss Condition
      if (generalconfig["StopLoss"]):
        if (generalconfig["StopLossCond"] == "TIBased"):
          postoExitSL = direc.CheckStopLossTI(positions, currentcandle, nextcandle, TIconfig)
          if (len(postoExitSL) > 0):
            direc.ExitPosition(postoExitSL, nextcandle, defs.SL, exitSLOHLC)
            data.loc[currentcandle.name]['Signal'] = defs.STOPLOSSHIT
        elif (generalconfig["StopLossCond"] == "PremiumBased"):
          (postoExitSL, posConfigtoExitSL) = atom.CheckStopLoss(positions, nextcandle)
        # We enter this loop if there is any position where stop-loss is triggered.
          if (len(postoExitSL) > 0):
            atom.ExitPosition(postoExitSL, nextcandle, defs.SL, exitSLOHLC)
            data.loc[currentcandle.name]['Signal'] = defs.STOPLOSSHIT

      # Check Target Profit Condition
      if (generalconfig["Target"]):
        if (generalconfig["TargetCond"] == "TIBased"):
          postoExitTarget = direc.CheckTargetConditionTI(positions, currentcandle, TIconfig)
          if (len(postoExitTarget) > 0):
            direc.ExitPosition(postoExitSL, nextcandle, defs.SL, exitTGOHLC)
            data.loc[currentcandle.name]['Signal'] = defs.TARGETREACHED
        elif (generalconfig["TargetCond"] == "PremiumBased"):
          (postoExitTarget, posConfigtoExitTG) = atom.CheckTargetCondition(positions, nextcandle)
        # We enter this loop if there is any position where target profit condition is satisfied.
          if (len(postoExitTarget) > 0):
            direc.ExitPosition(postoExitTarget, nextcandle, defs.TARGET, exitTGOHLC)
            data.loc[currentcandle.name]['Signal'] = defs.TARGETREACHED

      # Square off Remaining Legs EOD
      if (currentcandle.name.time() >= generalconfig["ExitTime"]) and not exitDone:
        direc.ExitPosition(positions, currentcandle, defs.SQUAREOFFEOD, exitSQEODOHLC)
        data.loc[currentcandle.name]['Signal'] = defs.EXITTIME
        trades = atom.GetFinalTrades(positions)
        exitDone = True

  return trades